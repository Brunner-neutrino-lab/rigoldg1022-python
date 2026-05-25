"""
dg1022/controller.py

High-level controller for the Rigol DG1022 dual-channel arbitrary waveform generator.

Operating modes (any combination on either channel):
  1. Continuous waveform   — sine/square/ramp/pulse/noise/DC at fixed parameters
  2. Pulse                 — period, width, duty cycle
  3. Arbitrary waveform    — download samples to volatile memory and play
  4. Burst (CH1 only)      — N cycles per trigger
  5. Frequency sweep (CH1) — linear or logarithmic between start and stop

Usage (headless):

    from dg1022 import DG1022Controller

    with DG1022Controller(mode="simulation") as awg:

        # 1. Continuous sine on CH1
        awg.apply_sine(1000.0, 5.0, 0.0, channel=1)
        awg.output_on(1)

        # 2. Pulse on CH2
        awg.apply_pulse(frequency=10e3, amplitude=3.3, offset=1.65, channel=2)
        awg.configure_pulse(period_s=100e-6, width_s=20e-6, channel=2)
        awg.output_on(2)

        # 3. Burst — 5 cycles per software trigger on CH1
        awg.apply_sine(1e3, 5.0, 0.0, channel=1)
        awg.enable_burst(ncycles=5, mode="TRIG", trigger="BUS")
        awg.trigger()

        # 4. Arbitrary waveform on CH1
        import numpy as np
        samples = np.sin(2*np.pi*np.linspace(0, 1, 1024))**3
        awg.load_arbitrary(samples, channel=1)
        awg.apply_user(1e3, 5.0, 0.0, channel=1)
        awg.output_on(1)
"""

import time
import numpy as np

from .driver import (
    DG1022Driver, DEFAULT_VISA, FUNCTIONS, VOLT_UNITS, TRIG_SOURCES,
)


class DG1022Controller:
    """
    High-level controller for the Rigol DG1022.

    Parameters
    ----------
    visa : str
        VISA resource string.
    mode : str
        "hardware" or "simulation".
    """

    # ------------------------------------------------------------------
    # Plugin interface (matches the b2987b style for ETS DAQ discovery)
    # ------------------------------------------------------------------
    MODULE_NAME = "DG1022"
    DEVICE_NAME = "Rigol DG1022 Function/Arbitrary Waveform Generator"
    CONFIG_FIELDS = [
        {"key": "visa", "label": "VISA Resource", "type": "str",    "default": DEFAULT_VISA},
        {"key": "mode", "label": "Mode",          "type": "choice", "default": "simulation",
         "choices": ["simulation", "hardware"]},
    ]
    DEFAULTS = {"visa": DEFAULT_VISA, "mode": "simulation"}

    @staticmethod
    def test(config: dict) -> tuple[bool, str]:
        try:
            ctrl = DG1022Controller(
                visa=config.get("visa", DEFAULT_VISA),
                mode=config.get("mode", "simulation"),
            )
            ctrl.connect()
            idn = ctrl.identify()
            ctrl.disconnect()
            return True, f"OK — {idn}"
        except Exception as e:
            return False, f"{type(e).__name__}: {e}"

    @staticmethod
    def read(config: dict) -> dict:
        return {
            "visa": config.get("visa", ""),
            "mode": config.get("mode", "simulation"),
        }

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def __init__(self, visa: str = DEFAULT_VISA, mode: str = "simulation"):
        self._driver = DG1022Driver(visa=visa, mode=mode)

    def connect(self):
        self._driver.connect()

    def disconnect(self):
        # Safety: turn off outputs before disconnecting hardware
        try:
            self._driver.output_off(1)
            self._driver.output_off(2)
        except Exception:
            pass
        self._driver.disconnect()

    def identify(self) -> str:
        return self._driver.identify()

    def reset(self):
        self._driver.reset()

    @property
    def driver(self) -> DG1022Driver:
        return self._driver

    # ------------------------------------------------------------------
    # 1. Continuous waveform — APPLy convenience wrappers
    # ------------------------------------------------------------------

    def apply_sine(self, frequency: float, amplitude: float = 5.0,
                   offset: float = 0.0, channel: int = 1):
        """Sine wave at the given frequency (Hz), amplitude (Vpp), offset (V)."""
        self._driver.apply("SIN", frequency, amplitude, offset, channel)

    def apply_square(self, frequency: float, amplitude: float = 5.0,
                     offset: float = 0.0, duty_cycle: float | None = None,
                     channel: int = 1):
        """Square wave. APPLy resets duty to 50%; pass duty_cycle to override after."""
        self._driver.apply("SQU", frequency, amplitude, offset, channel)
        if duty_cycle is not None:
            self._driver.set_square_duty_cycle(duty_cycle, channel)

    def apply_ramp(self, frequency: float, amplitude: float = 5.0,
                   offset: float = 0.0, symmetry: float | None = None,
                   channel: int = 1):
        """Ramp wave. APPLy resets symmetry to 50%; pass symmetry to override after."""
        self._driver.apply("RAMP", frequency, amplitude, offset, channel)
        if symmetry is not None:
            self._driver.set_ramp_symmetry(symmetry, channel)

    def apply_pulse(self, frequency: float, amplitude: float = 5.0,
                    offset: float = 0.0, channel: int = 1):
        """Pulse. Period/width/duty must be configured via configure_pulse()."""
        self._driver.apply("PULS", frequency, amplitude, offset, channel)

    def apply_noise(self, amplitude: float = 5.0, offset: float = 0.0,
                    channel: int = 1):
        """Gaussian noise (5 MHz BW)."""
        self._driver.apply("NOIS", 1000.0, amplitude, offset, channel)

    def apply_dc(self, offset: float, channel: int = 1):
        """DC level only (amplitude/frequency ignored by the instrument)."""
        self._driver.apply("DC", 1000.0, 5.0, offset, channel)

    def apply_user(self, frequency: float, amplitude: float = 5.0,
                   offset: float = 0.0, channel: int = 1):
        """Play the currently-selected arbitrary waveform (see load_arbitrary)."""
        self._driver.apply("USER", frequency, amplitude, offset, channel)

    # ------------------------------------------------------------------
    # 2. Pulse parameters
    # ------------------------------------------------------------------

    def configure_pulse(self,
                        period_s:  float | None = None,
                        width_s:   float | None = None,
                        duty_pct:  float | None = None,
                        channel:   int = 1):
        """
        Set pulse period, width, and/or duty cycle on a channel.

        Specify period_s + (width_s or duty_pct).
        """
        if period_s is not None:
            self._driver.set_pulse_period(period_s, channel)
        if width_s is not None:
            self._driver.set_pulse_width(width_s, channel)
        if duty_pct is not None:
            self._driver.set_pulse_duty_cycle(duty_pct, channel)

    # ------------------------------------------------------------------
    # 3. Voltage / output configuration
    # ------------------------------------------------------------------

    def set_amplitude(self, amplitude: float, channel: int = 1):
        self._driver.set_amplitude(amplitude, channel)

    def set_offset(self, offset: float, channel: int = 1):
        self._driver.set_offset(offset, channel)

    def set_frequency(self, frequency: float, channel: int = 1):
        self._driver.set_frequency(frequency, channel)

    def set_high_low(self, high_v: float, low_v: float, channel: int = 1):
        """Set amplitude/offset via high and low levels."""
        self._driver.set_high_level(high_v, channel)
        self._driver.set_low_level(low_v, channel)

    def set_phase(self, degrees: float, channel: int = 1):
        self._driver.set_phase(degrees, channel)

    def align_phase(self):
        """Realign CH1/CH2 phase output (PHAS:ALIGN)."""
        self._driver.align_phase()

    def set_voltage_unit(self, unit: str, channel: int = 1):
        """unit in {'VPP', 'VRMS', 'DBM'}."""
        self._driver.set_voltage_unit(unit, channel)

    def set_load(self, load_ohms: float | str, channel: int = 1):
        """Set output load — ohm value or 'INF'/float('inf') for high-Z."""
        self._driver.set_load(load_ohms, channel)

    def set_polarity(self, polarity: str, channel: int = 1):
        """polarity in {'NORM', 'INV'}."""
        self._driver.set_polarity(polarity, channel)

    def output_on(self, channel: int = 1):
        self._driver.output_on(channel)

    def output_off(self, channel: int = 1):
        self._driver.output_off(channel)

    def all_outputs_off(self):
        self._driver.output_off(1)
        self._driver.output_off(2)

    def get_output_state(self, channel: int = 1) -> bool:
        return self._driver.get_output_state(channel)

    # ------------------------------------------------------------------
    # 4. Burst (CH1 only)
    # ------------------------------------------------------------------

    def enable_burst(self,
                     ncycles:    int | str = 1,
                     mode:       str = "TRIG",
                     period_s:   float = 0.01,
                     phase_deg:  float = 0.0,
                     trigger:    str = "IMM"):
        """
        Configure and enable burst mode on CH1.

        Parameters
        ----------
        ncycles : int or 'INF'
            Number of cycles per trigger (TRIG mode). 1..50000, or 'INF'.
        mode : str
            'TRIG' — N cycles on each trigger.
            'GAT'  — output gated by external level.
        period_s : float
            Internal burst period (between trigger events) when trigger='IMM'.
        phase_deg : float
            Initial phase in degrees.
        trigger : str
            'IMM', 'EXT', or 'BUS'.
        """
        self._driver.set_burst_mode(mode)
        self._driver.set_burst_ncycles(ncycles)
        self._driver.set_burst_internal_period(period_s)
        self._driver.set_burst_phase(phase_deg)
        self._driver.set_trigger_source(trigger)
        self._driver.burst_enable(True)

    def disable_burst(self):
        self._driver.burst_enable(False)

    def trigger(self):
        """Issue a software trigger (*TRG); valid when trigger source is BUS."""
        self._driver.trigger()

    # ------------------------------------------------------------------
    # 5. Frequency sweep (CH1 only)
    # ------------------------------------------------------------------

    def enable_sweep(self,
                     start_hz:  float,
                     stop_hz:   float,
                     time_s:    float = 1.0,
                     spacing:   str   = "LIN",
                     trigger:   str   = "IMM"):
        """
        Configure and enable a frequency sweep on CH1.

        Parameters
        ----------
        start_hz : float
            Start frequency (Hz).
        stop_hz : float
            Stop frequency (Hz). Sweep goes up if stop > start.
        time_s : float
            Sweep duration (s). 1 ms .. 500 s.
        spacing : str
            'LIN' or 'LOG'.
        trigger : str
            'IMM', 'EXT', or 'BUS'.
        """
        self._driver.set_sweep_spacing(spacing)
        self._driver.set_frequency_start(start_hz)
        self._driver.set_frequency_stop(stop_hz)
        self._driver.set_sweep_time(time_s)
        self._driver.set_trigger_source(trigger)
        self._driver.sweep_enable(True)

    def disable_sweep(self):
        self._driver.sweep_enable(False)

    # ------------------------------------------------------------------
    # 6. Arbitrary waveform
    # ------------------------------------------------------------------

    def load_arbitrary(self,
                       samples:    np.ndarray,
                       channel:    int = 1,
                       normalized: bool = True,
                       save_as:    str | None = None):
        """
        Download arbitrary waveform samples to volatile memory and select for output.

        Parameters
        ----------
        samples : np.ndarray
            1-D array. Length 1..524,288.
            If normalized=True, values in [-1, 1].
            If normalized=False, integer DAC codes in [0, 16383].
        channel : int
            Channel to assign the user wave to. The same volatile buffer can be
            selected by either channel.
        normalized : bool
            See above.
        save_as : str, optional
            If given, also copy volatile to a non-volatile slot under this name
            (up to 12 chars, first char must be a letter).
        """
        self._driver.download_arbitrary(samples, normalized=normalized)
        self._driver.set_user_wave("VOLATILE", channel)
        if save_as is not None:
            self._driver.copy_to_nonvolatile(save_as)

    def select_user_wave(self, name: str, channel: int = 1):
        """Select a built-in or saved arbitrary waveform by name (no download)."""
        self._driver.set_user_wave(name, channel)

    def list_waves(self) -> list[str]:
        """Return the names available via DATA:CAT?."""
        raw = self._driver.get_catalog()
        # Response is comma-separated quoted names
        return [s.strip().strip('"') for s in raw.split(",") if s.strip()]

    # ------------------------------------------------------------------
    # Misc
    # ------------------------------------------------------------------

    def get_channel_state(self, channel: int = 1) -> dict:
        """Snapshot of cached/simulated channel parameters (for status display)."""
        return self._driver.get_channel_state(channel)

    # ------------------------------------------------------------------
    # Context manager
    # ------------------------------------------------------------------

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *_):
        self.disconnect()
