"""
dg1022/driver.py

Low-level SCPI interface to the Rigol DG1022 function/arbitrary waveform generator.

Handles only instrument communication — no experiment logic, no Qt.

Two modes:
  "hardware"   — connects via pyvisa (USB)
  "simulation" — tracks state in memory for development without hardware

SCPI commands verified against the DG1022 Programming Guide (Aug 2009),
docs/DG1022_ProgrammingGuide_EN.md.

Channel convention:
    channel = 1 -> CH1 (default; SCPI commands without :CH2 suffix)
    channel = 2 -> CH2 (SCPI commands with :CH2 suffix)
"""

import time
import numpy as np

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_VISA = "USB0::0x1AB1::0x0588::DG1D000000000::INSTR"
TIMEOUT_MS   = 10_000
IDN_EXPECTED = "RIGOL TECHNOLOGIES,DG1022"

# Function names (as used by the SCPI FUNCtion command).
FUNCTIONS = ("SIN", "SQU", "RAMP", "PULS", "NOIS", "DC", "USER")

# Voltage units
VOLT_UNITS = ("VPP", "VRMS", "DBM")

# Trigger sources for burst/sweep
TRIG_SOURCES = ("IMM", "EXT", "BUS")

# Output load: 50 ohm or INFinity (high Z)
LOAD_HIGH_Z = "INF"


def _ch_suffix(channel: int) -> str:
    """Return SCPI channel suffix: '' for CH1, ':CH2' for CH2."""
    if channel == 1:
        return ""
    if channel == 2:
        return ":CH2"
    raise ValueError(f"channel must be 1 or 2, got {channel}")


class _LinuxUsbtmcShim:
    """
    Minimal pyvisa-MessageBasedResource-compatible adapter for the Linux
    kernel's `/dev/usbtmc*` character device.

    USBTMC framing is handled in the kernel — each `os.write` is one OUT
    message and each `os.read` returns exactly one IN message — so the
    write_termination / read_termination attributes are accepted but not
    appended.  This avoids having to unbind the kernel driver so libusb
    (pyvisa-py) can claim the device.

    Permissions: `/dev/usbtmc*` defaults to root-only.  Add a udev rule
    such as `KERNEL=="usbtmc*", MODE="0660", GROUP="plugdev"` to grant
    user-level access.
    """

    # Minimum delay between an OUT (write) and the following IN (read).
    # The kernel /dev/usbtmc layer does not retry the IN request, so if the
    # IN poll arrives before the device has queued its response the kernel
    # will return ETIMEDOUT.  ~50 ms is plenty for the DG1022.
    _QUERY_DELAY_S = 0.05

    def __init__(self, path: str, timeout_ms: int = 10_000):
        import os
        self._fd = os.open(path, os.O_RDWR)
        self.timeout            = timeout_ms
        # DG1022 firmware needs a '\n' at the end of each command. The kernel
        # USBTMC layer handles message framing on the wire, but the device's
        # SCPI parser still looks for '\n' to mark end-of-command.
        self.write_termination  = "\n"
        self.read_termination   = ""

    def write(self, cmd: str) -> None:
        import os
        if self.write_termination and not cmd.endswith(self.write_termination):
            cmd = cmd + self.write_termination
        os.write(self._fd, cmd.encode("ascii"))

    def read(self) -> str:
        import os
        chunk = os.read(self._fd, 4096)
        return chunk.decode("ascii", errors="replace").rstrip()

    def query(self, cmd: str, delay: float = 0.0) -> str:
        self.write(cmd)
        time.sleep(max(delay, self._QUERY_DELAY_S))
        return self.read()

    def write_binary_values(self, cmd: str, values, datatype: str = "B",
                            is_big_endian: bool = False,
                            header_fmt: str = "ieee") -> None:
        """SCPI definite-length-block binary write (IEEE 488.2 #<n><len><data>)."""
        import os, struct
        # Pack values according to datatype
        fmt = (">" if is_big_endian else "<") + datatype * len(values)
        data = struct.pack(fmt, *values)
        n = len(data)
        n_digits = len(str(n))
        header = f"{cmd} #{n_digits}{n}".encode("ascii")
        os.write(self._fd, header + data)

    def close(self) -> None:
        import os
        try:
            os.close(self._fd)
        except Exception:
            pass


class DG1022Driver:
    """
    Low-level SCPI driver for the Rigol DG1022.

    Parameters
    ----------
    visa : str
        VISA resource string (USB).
    mode : str
        "hardware" or "simulation".
    """

    def __init__(self, visa: str = DEFAULT_VISA, mode: str = "simulation"):
        if mode not in ("hardware", "simulation"):
            raise ValueError(f"mode must be 'hardware' or 'simulation', got {mode!r}")
        self._visa_str  = visa
        self._mode      = mode
        self._inst      = None
        self._rm        = None
        self._connected = False

        # Per-channel simulated state. Indexed by channel id (1, 2).
        self._sim_state: dict[int, dict] = {
            ch: {
                "function":   "SIN",
                "frequency":  1000.0,
                "amplitude":  5.0,
                "offset":     0.0,
                "phase":      0.0,
                "unit":       "VPP",
                "output":     False,
                "load":       50.0,        # ohm or float('inf')
                "polarity":   "NORM",
                "duty_cycle": 50.0,        # % (square)
                "symmetry":   50.0,        # % (ramp)
                "pulse_period": 1e-3,
                "pulse_width":  5e-4,
                "pulse_dcyc":   50.0,
                "user_wave":  "EXP_RISE",  # selected arb name
            } for ch in (1, 2)
        }

        # Volatile arbitrary waveform memory (one buffer; selectable per channel)
        self._sim_volatile: np.ndarray | None = None

        # Burst/sweep state (CH1 only)
        self._sim_burst = {
            "state":   False,
            "mode":    "TRIG",
            "ncyc":    1,
            "period":  0.01,
            "phase":   0.0,
        }
        self._sim_sweep = {
            "state":   False,
            "spacing": "LIN",
            "time":    1.0,
            "start":   100.0,
            "stop":    1000.0,
        }
        self._sim_trigger_source = "IMM"

    # ------------------------------------------------------------------
    # Connection
    # ------------------------------------------------------------------

    def connect(self):
        if self._connected:
            return
        if self._mode == "hardware":
            self._connect_hardware()
        self._connected = True

    def disconnect(self):
        if not self._connected:
            return
        if self._mode == "hardware":
            self._disconnect_hardware()
        self._connected = False

    @property
    def is_connected(self) -> bool:
        return self._connected

    @property
    def mode(self) -> str:
        return self._mode

    @property
    def visa_resource(self) -> str:
        return self._visa_str

    def identify(self) -> str:
        if self._mode == "hardware":
            return self._inst.query("*IDN?").strip()
        return f"RIGOL TECHNOLOGIES,DG1022,DG[sim]00000001,00.01.00.00.00"

    def reset(self):
        """Restore default state (*RST)."""
        if self._mode == "hardware":
            self._inst.write("*RST")
            self._inst.query("*OPC?")
        else:
            self.__init__(visa=self._visa_str, mode=self._mode)
            self._connected = True

    # ------------------------------------------------------------------
    # APPLy — combined function/freq/amp/offset in one command
    # ------------------------------------------------------------------

    def apply(self,
              function:  str,
              frequency: float = 1000.0,
              amplitude: float = 5.0,
              offset:    float = 0.0,
              channel:   int   = 1):
        """
        Issue an APPLy:<FUNC> command — sets function and all three parameters.

        Parameters
        ----------
        function : str
            One of: 'SIN', 'SQU', 'RAMP', 'PULS', 'NOIS', 'DC', 'USER'.
        frequency : float
            Hz. Ignored for NOIS and DC (pass any value).
        amplitude : float
            In current voltage unit (default Vpp). Ignored for DC.
        offset : float
            VDC.
        channel : int
            1 or 2.
        """
        fn = function.upper()
        if fn not in FUNCTIONS:
            raise ValueError(f"function must be one of {FUNCTIONS}, got {function!r}")

        # APPLy spelling: SIN -> SINusoid, SQU -> SQUare, RAMP -> RAMP,
        # PULS -> PULSe, NOIS -> NOISe, DC -> DC, USER -> USER
        scpi_name = {
            "SIN":  "SIN",  "SQU":  "SQU", "RAMP": "RAMP",
            "PULS": "PULS", "NOIS": "NOIS", "DC":   "DC",
            "USER": "USER",
        }[fn]
        suffix = _ch_suffix(channel)
        cmd = f"APPL:{scpi_name}{suffix} {frequency:.6f},{amplitude:.6f},{offset:.6f}"

        if self._mode == "hardware":
            self._inst.write(cmd)
        st = self._sim_state[channel]
        st["function"]  = fn
        st["frequency"] = float(frequency)
        st["amplitude"] = float(amplitude)
        st["offset"]    = float(offset)
        if fn == "SQU":
            st["duty_cycle"] = 50.0
        elif fn == "RAMP":
            st["symmetry"] = 50.0

    def query_apply(self, channel: int = 1) -> str:
        """Return the APPL? string, e.g. 'CH1:"SIN,1.000000e+03,5.000000e+00,0.000000e+00"'."""
        suffix = _ch_suffix(channel)
        cmd = f"APPL{suffix}?"
        if self._mode == "hardware":
            return self._inst.query(cmd).strip()
        st = self._sim_state[channel]
        return (f'CH{channel}:"{st["function"]},'
                f'{st["frequency"]:.6e},{st["amplitude"]:.6e},{st["offset"]:.6e}"')

    # ------------------------------------------------------------------
    # FUNCtion — set function only
    # ------------------------------------------------------------------

    def set_function(self, function: str, channel: int = 1):
        fn = function.upper()
        if fn not in FUNCTIONS:
            raise ValueError(f"function must be one of {FUNCTIONS}, got {function!r}")
        suffix = _ch_suffix(channel)
        if self._mode == "hardware":
            self._inst.write(f"FUNC{suffix} {fn}")
        self._sim_state[channel]["function"] = fn

    def get_function(self, channel: int = 1) -> str:
        suffix = _ch_suffix(channel)
        if self._mode == "hardware":
            return self._inst.query(f"FUNC{suffix}?").strip()
        st = self._sim_state[channel]
        return f"CH{channel}:{st['function']}"

    def set_user_wave(self, name: str, channel: int = 1):
        """Select a built-in or user arbitrary waveform on channel."""
        suffix = _ch_suffix(channel)
        if self._mode == "hardware":
            self._inst.write(f"FUNC:USER{suffix} {name}")
        self._sim_state[channel]["user_wave"] = name

    def set_square_duty_cycle(self, percent: float, channel: int = 1):
        suffix = _ch_suffix(channel)
        if self._mode == "hardware":
            self._inst.write(f"FUNC:SQU:DCYC{suffix} {percent:.4f}")
        self._sim_state[channel]["duty_cycle"] = float(percent)

    def set_ramp_symmetry(self, percent: float, channel: int = 1):
        suffix = _ch_suffix(channel)
        if self._mode == "hardware":
            self._inst.write(f"FUNC:RAMP:SYMM{suffix} {percent:.4f}")
        self._sim_state[channel]["symmetry"] = float(percent)

    # ------------------------------------------------------------------
    # FREQuency / VOLTage
    # ------------------------------------------------------------------

    def set_frequency(self, frequency: float, channel: int = 1):
        suffix = _ch_suffix(channel)
        if self._mode == "hardware":
            self._inst.write(f"FREQ{suffix} {frequency:.6f}")
        self._sim_state[channel]["frequency"] = float(frequency)

    def get_frequency(self, channel: int = 1) -> float:
        suffix = _ch_suffix(channel)
        if self._mode == "hardware":
            return float(self._inst.query(f"FREQ{suffix}?").split(":")[-1])
        return self._sim_state[channel]["frequency"]

    def set_amplitude(self, amplitude: float, channel: int = 1):
        suffix = _ch_suffix(channel)
        if self._mode == "hardware":
            self._inst.write(f"VOLT{suffix} {amplitude:.6f}")
        self._sim_state[channel]["amplitude"] = float(amplitude)

    def get_amplitude(self, channel: int = 1) -> float:
        suffix = _ch_suffix(channel)
        if self._mode == "hardware":
            return float(self._inst.query(f"VOLT{suffix}?").split(":")[-1])
        return self._sim_state[channel]["amplitude"]

    def set_offset(self, offset: float, channel: int = 1):
        suffix = _ch_suffix(channel)
        if self._mode == "hardware":
            self._inst.write(f"VOLT:OFFS{suffix} {offset:.6f}")
        self._sim_state[channel]["offset"] = float(offset)

    def get_offset(self, channel: int = 1) -> float:
        suffix = _ch_suffix(channel)
        if self._mode == "hardware":
            return float(self._inst.query(f"VOLT:OFFS{suffix}?").split(":")[-1])
        return self._sim_state[channel]["offset"]

    def set_high_level(self, high_v: float, channel: int = 1):
        suffix = _ch_suffix(channel)
        if self._mode == "hardware":
            self._inst.write(f"VOLT:HIGH{suffix} {high_v:.6f}")
        # Update simulated amp/offset to be consistent
        low = self._sim_state[channel]["offset"] - self._sim_state[channel]["amplitude"] / 2
        self._sim_state[channel]["amplitude"] = high_v - low
        self._sim_state[channel]["offset"]    = (high_v + low) / 2

    def set_low_level(self, low_v: float, channel: int = 1):
        suffix = _ch_suffix(channel)
        if self._mode == "hardware":
            self._inst.write(f"VOLT:LOW{suffix} {low_v:.6f}")
        high = self._sim_state[channel]["offset"] + self._sim_state[channel]["amplitude"] / 2
        self._sim_state[channel]["amplitude"] = high - low_v
        self._sim_state[channel]["offset"]    = (high + low_v) / 2

    def set_voltage_unit(self, unit: str, channel: int = 1):
        u = unit.upper()
        if u not in VOLT_UNITS:
            raise ValueError(f"unit must be one of {VOLT_UNITS}, got {unit!r}")
        suffix = _ch_suffix(channel)
        if self._mode == "hardware":
            self._inst.write(f"VOLT:UNIT{suffix} {u}")
        self._sim_state[channel]["unit"] = u

    # ------------------------------------------------------------------
    # OUTPut
    # ------------------------------------------------------------------

    def output_on(self, channel: int = 1):
        suffix = _ch_suffix(channel)
        if self._mode == "hardware":
            self._inst.write(f"OUTP{suffix} ON")
        self._sim_state[channel]["output"] = True

    def output_off(self, channel: int = 1):
        suffix = _ch_suffix(channel)
        if self._mode == "hardware":
            self._inst.write(f"OUTP{suffix} OFF")
        self._sim_state[channel]["output"] = False

    def get_output_state(self, channel: int = 1) -> bool:
        suffix = _ch_suffix(channel)
        if self._mode == "hardware":
            resp = self._inst.query(f"OUTP{suffix}?").strip().upper()
            return resp.endswith("ON")
        return self._sim_state[channel]["output"]

    def set_load(self, load_ohms: float | str, channel: int = 1):
        """Set output load. Use 'INF' or float('inf') for high-Z."""
        suffix = _ch_suffix(channel)
        if isinstance(load_ohms, str) and load_ohms.upper().startswith("INF"):
            arg = "INF"
            sim_val = float("inf")
        elif np.isinf(load_ohms):
            arg = "INF"
            sim_val = float("inf")
        else:
            arg = f"{float(load_ohms):.2f}"
            sim_val = float(load_ohms)
        if self._mode == "hardware":
            self._inst.write(f"OUTP:LOAD{suffix} {arg}")
        self._sim_state[channel]["load"] = sim_val

    def set_polarity(self, polarity: str, channel: int = 1):
        p = polarity.upper()
        if p not in ("NORM", "NORMAL", "INV", "INVERTED"):
            raise ValueError(f"polarity must be NORM or INV, got {polarity!r}")
        p = "NORM" if p.startswith("NORM") else "INV"
        suffix = _ch_suffix(channel)
        if self._mode == "hardware":
            self._inst.write(f"OUTP:POL{suffix} {p}")
        self._sim_state[channel]["polarity"] = p

    def set_sync_output(self, enable: bool):
        """Enable/disable rear-panel sync output (CH1 only)."""
        state = "ON" if enable else "OFF"
        if self._mode == "hardware":
            self._inst.write(f"OUTP:SYNC {state}")

    # ------------------------------------------------------------------
    # PULSe
    # ------------------------------------------------------------------

    def set_pulse_period(self, period_s: float, channel: int = 1):
        suffix = _ch_suffix(channel)
        if self._mode == "hardware":
            self._inst.write(f"PULS:PER{suffix} {period_s:.9f}")
        self._sim_state[channel]["pulse_period"] = float(period_s)

    def set_pulse_width(self, width_s: float, channel: int = 1):
        suffix = _ch_suffix(channel)
        if self._mode == "hardware":
            self._inst.write(f"PULS:WIDT{suffix} {width_s:.9f}")
        self._sim_state[channel]["pulse_width"] = float(width_s)

    def set_pulse_duty_cycle(self, percent: float, channel: int = 1):
        suffix = _ch_suffix(channel)
        if self._mode == "hardware":
            self._inst.write(f"PULS:DCYC{suffix} {percent:.4f}")
        self._sim_state[channel]["pulse_dcyc"] = float(percent)

    # ------------------------------------------------------------------
    # PHASe
    # ------------------------------------------------------------------

    def set_phase(self, degrees: float, channel: int = 1):
        suffix = _ch_suffix(channel)
        if self._mode == "hardware":
            self._inst.write(f"PHAS{suffix} {degrees:.4f}")
        self._sim_state[channel]["phase"] = float(degrees)

    def align_phase(self):
        """Realign CH1/CH2 phase output."""
        if self._mode == "hardware":
            self._inst.write("PHAS:ALIGN")

    # ------------------------------------------------------------------
    # BURSt (CH1)
    # ------------------------------------------------------------------

    def burst_enable(self, enable: bool):
        state = "ON" if enable else "OFF"
        if self._mode == "hardware":
            self._inst.write(f"BURS:STAT {state}")
        self._sim_burst["state"] = bool(enable)

    def set_burst_mode(self, mode: str):
        m = mode.upper()
        if m not in ("TRIG", "TRIGGERED", "GAT", "GATED"):
            raise ValueError(f"burst mode must be TRIG or GAT, got {mode!r}")
        m = "TRIG" if m.startswith("TRIG") else "GAT"
        if self._mode == "hardware":
            self._inst.write(f"BURS:MODE {m}")
        self._sim_burst["mode"] = m

    def set_burst_ncycles(self, ncycles: int | str):
        """Cycles 1..50,000, or 'INF' for infinite."""
        if isinstance(ncycles, str) and ncycles.upper().startswith("INF"):
            arg = "INF"; sim_val = "INF"
        else:
            arg = f"{int(ncycles)}"; sim_val = int(ncycles)
        if self._mode == "hardware":
            self._inst.write(f"BURS:NCYC {arg}")
        self._sim_burst["ncyc"] = sim_val

    def set_burst_internal_period(self, period_s: float):
        if self._mode == "hardware":
            self._inst.write(f"BURS:INT:PER {period_s:.9f}")
        self._sim_burst["period"] = float(period_s)

    def set_burst_phase(self, degrees: float):
        if self._mode == "hardware":
            self._inst.write(f"BURS:PHAS {degrees:.4f}")
        self._sim_burst["phase"] = float(degrees)

    # ------------------------------------------------------------------
    # SWEep (CH1)
    # ------------------------------------------------------------------

    def sweep_enable(self, enable: bool):
        state = "ON" if enable else "OFF"
        if self._mode == "hardware":
            self._inst.write(f"SWE:STAT {state}")
        self._sim_sweep["state"] = bool(enable)

    def set_sweep_spacing(self, spacing: str):
        s = spacing.upper()
        if s not in ("LIN", "LINEAR", "LOG", "LOGARITHMIC"):
            raise ValueError(f"spacing must be LIN or LOG, got {spacing!r}")
        s = "LIN" if s.startswith("LIN") else "LOG"
        if self._mode == "hardware":
            self._inst.write(f"SWE:SPAC {s}")
        self._sim_sweep["spacing"] = s

    def set_sweep_time(self, seconds: float):
        if self._mode == "hardware":
            self._inst.write(f"SWE:TIME {seconds:.6f}")
        self._sim_sweep["time"] = float(seconds)

    def set_frequency_start(self, frequency: float):
        if self._mode == "hardware":
            self._inst.write(f"FREQ:STAR {frequency:.6f}")
        self._sim_sweep["start"] = float(frequency)

    def set_frequency_stop(self, frequency: float):
        if self._mode == "hardware":
            self._inst.write(f"FREQ:STOP {frequency:.6f}")
        self._sim_sweep["stop"] = float(frequency)

    # ------------------------------------------------------------------
    # TRIGger
    # ------------------------------------------------------------------

    def set_trigger_source(self, source: str):
        s = source.upper()
        if s not in TRIG_SOURCES + ("IMMEDIATE", "EXTERNAL"):
            raise ValueError(f"trigger source must be IMM/EXT/BUS, got {source!r}")
        s = {"IMMEDIATE": "IMM", "EXTERNAL": "EXT"}.get(s, s)
        if self._mode == "hardware":
            self._inst.write(f"TRIG:SOUR {s}")
        self._sim_trigger_source = s

    def trigger(self):
        """Issue a software (BUS) trigger."""
        if self._mode == "hardware":
            self._inst.write("*TRG")

    # ------------------------------------------------------------------
    # DATA — arbitrary waveform download (CH1 volatile memory)
    # ------------------------------------------------------------------

    def download_arbitrary(self, samples: np.ndarray, normalized: bool = True):
        """
        Download a user arbitrary waveform to volatile memory.

        Parameters
        ----------
        samples : np.ndarray
            1-D array. If normalized=True, values are floats in [-1, 1]
            and the DATA VOLATILE,<value>,... command is used.
            If normalized=False, values are DAC integers in [0, 16383]
            and the DATA:DAC VOLATILE,<int>,... command is used.
        normalized : bool
            Selects between DATA (float) and DATA:DAC (integer) downloads.

        Notes
        -----
        Per the programming guide, each waveform may contain 1 to 524,288
        points. To then output this wave, call set_user_wave("VOLATILE",ch)
        and apply()/set_function() with USER.
        """
        arr = np.asarray(samples).flatten()
        n = arr.size
        if n < 1 or n > 524_288:
            raise ValueError(f"length must be 1..524288, got {n}")

        if normalized:
            if np.any(np.abs(arr) > 1.0):
                raise ValueError("normalized samples must be in [-1, 1]")
            payload = ",".join(f"{v:.6f}" for v in arr.astype(np.float64))
            cmd = "DATA VOLATILE," + payload
        else:
            ints = arr.astype(np.int64)
            if np.any(ints < 0) or np.any(ints > 16_383):
                raise ValueError("DAC samples must be integers in [0, 16383]")
            payload = ",".join(str(int(v)) for v in ints)
            cmd = "DATA:DAC VOLATILE," + payload

        if self._mode == "hardware":
            self._inst.write(cmd)
        # Store normalized in sim for visualization
        if normalized:
            self._sim_volatile = arr.astype(np.float64).copy()
        else:
            self._sim_volatile = (ints.astype(np.float64) / 16_383.0) * 2 - 1

    def copy_to_nonvolatile(self, name: str):
        """Copy volatile memory to a non-volatile slot under <name>."""
        if self._mode == "hardware":
            self._inst.write(f"DATA:COPY {name},VOLATILE")

    def get_catalog(self) -> str:
        """Query DATA:CATalog?."""
        if self._mode == "hardware":
            return self._inst.query("DATA:CAT?").strip()
        return '"VOLATILE","EXP_RISE","EXP_FALL","NEG_RAMP","SINC","CARDIAC"'

    # ------------------------------------------------------------------
    # State snapshot (handy for sim / GUI status)
    # ------------------------------------------------------------------

    def get_channel_state(self, channel: int) -> dict:
        """Return a copy of the simulated/cached state for one channel."""
        return dict(self._sim_state[channel])

    # ------------------------------------------------------------------
    # Hardware internals
    # ------------------------------------------------------------------

    def _connect_hardware(self):
        # Linux USBTMC kernel char-device path (e.g. "/dev/usbtmc0"):
        # bypass pyvisa, talk to the kernel device directly. Saves having
        # to unbind the kernel driver so libusb can grab the device.
        if self._visa_str.startswith("/dev/"):
            self._inst = _LinuxUsbtmcShim(self._visa_str, timeout_ms=TIMEOUT_MS)
            self._rm   = None
            idn = self._inst.query("*IDN?")
            if IDN_EXPECTED not in idn:
                self._inst.close()
                raise RuntimeError(
                    f"IDN mismatch. Expected {IDN_EXPECTED!r}, got {idn!r}\n"
                    f"Check device path: {self._visa_str!r}"
                )
            return

        try:
            import pyvisa
        except ImportError as e:
            raise ImportError(
                "pyvisa not installed. Run: pip install pyvisa pyvisa-py"
            ) from e

        self._rm = pyvisa.ResourceManager()
        last_err = None
        for _ in range(3):
            try:
                self._inst = self._rm.open_resource(self._visa_str)
                break
            except Exception as e:
                last_err = e
                time.sleep(1)
        else:
            raise RuntimeError(
                f"Could not open VISA resource {self._visa_str!r} after 3 attempts: {last_err}"
            )

        self._inst.timeout = TIMEOUT_MS
        # USB termination — DG1022 uses '\n'
        try:
            self._inst.write_termination = "\n"
            self._inst.read_termination  = "\n"
        except Exception:
            pass

        idn = self._inst.query("*IDN?")
        if IDN_EXPECTED not in idn:
            self._inst.close()
            raise RuntimeError(
                f"IDN mismatch. Expected {IDN_EXPECTED!r}, got {idn!r}\n"
                f"Check VISA string: {self._visa_str!r}"
            )

    def _disconnect_hardware(self):
        if self._inst is not None:
            try:
                self.output_off(1)
                self.output_off(2)
                self._inst.close()
            except Exception:
                pass
        if self._rm is not None:
            try:
                self._rm.close()
            except Exception:
                pass

    # ------------------------------------------------------------------
    # Context manager
    # ------------------------------------------------------------------

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *_):
        self.disconnect()
