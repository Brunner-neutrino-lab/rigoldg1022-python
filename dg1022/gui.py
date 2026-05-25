"""
dg1022/gui.py

Standalone PyQt5 GUI for the Rigol DG1022 arbitrary waveform generator.

Launch directly:
    python -m dg1022.gui

Tabs:
    Connection  — VISA string, mode, connect/disconnect, *IDN?
    Channel 1   — function, freq, amp, offset, phase, load, output on/off
    Channel 2   — same as Channel 1, for CH2
    Burst       — N-cycle burst configuration (CH1 only)
    Sweep       — frequency sweep configuration (CH1 only)
    Arbitrary   — load samples to volatile memory and play them
"""

import sys
import time
import numpy as np

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGroupBox, QLabel, QLineEdit, QComboBox, QPushButton, QSpinBox,
    QDoubleSpinBox, QCheckBox, QTextEdit, QTabWidget, QGridLayout,
    QFileDialog,
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject
from PyQt5.QtGui import QFont

try:
    import matplotlib
    matplotlib.use("Qt5Agg")
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.figure import Figure
    HAS_MPL = True
except ImportError:
    HAS_MPL = False

from .controller import DG1022Controller
from .driver import DEFAULT_VISA, FUNCTIONS


# ---------------------------------------------------------------------------
# Worker signals
# ---------------------------------------------------------------------------

class _Signals(QObject):
    status     = pyqtSignal(str)
    connected  = pyqtSignal(bool, str)
    op_done    = pyqtSignal(str)             # short summary message


class _ConnectWorker(QThread):
    def __init__(self, ctrl, signals):
        super().__init__()
        self._ctrl = ctrl; self._signals = signals

    def run(self):
        try:
            self._ctrl.connect()
            self._signals.connected.emit(True, self._ctrl.identify())
        except Exception as e:
            self._signals.connected.emit(False, str(e))


class _CallWorker(QThread):
    """Run a single (fn, args, kwargs) on the controller off the GUI thread."""

    def __init__(self, fn, args, kwargs, signals, label):
        super().__init__()
        self._fn = fn; self._args = args; self._kwargs = kwargs
        self._signals = signals; self._label = label

    def run(self):
        try:
            self._fn(*self._args, **self._kwargs)
            self._signals.op_done.emit(self._label)
        except Exception as e:
            self._signals.status.emit(f"{self._label} error: {e}")


# ---------------------------------------------------------------------------
# Reusable channel control panel
# ---------------------------------------------------------------------------

class _ChannelPanel(QWidget):
    """Function/frequency/amplitude/offset/phase/output controls for one channel."""

    def __init__(self, channel: int, get_ctrl, signals, log_fn, parent=None):
        super().__init__(parent)
        self._channel  = channel
        self._get_ctrl = get_ctrl       # callable: returns DG1022Controller or None
        self._signals  = signals
        self._log_fn   = log_fn
        self._worker   = None
        self._build()

    def _build(self):
        lay = QVBoxLayout(self)

        # Waveform parameters
        wbox = QGroupBox(f"CH{self._channel} Waveform")
        wg   = QGridLayout(wbox)

        wg.addWidget(QLabel("Function:"), 0, 0)
        self._fn_combo = QComboBox()
        self._fn_combo.addItems(["SIN", "SQU", "RAMP", "PULS", "NOIS", "DC", "USER"])
        wg.addWidget(self._fn_combo, 0, 1)

        wg.addWidget(QLabel("Frequency (Hz):"), 1, 0)
        self._freq = QDoubleSpinBox()
        self._freq.setRange(1e-6, 20e6); self._freq.setDecimals(6)
        self._freq.setValue(1000.0)
        wg.addWidget(self._freq, 1, 1)

        wg.addWidget(QLabel("Amplitude (Vpp):"), 2, 0)
        self._amp = QDoubleSpinBox()
        self._amp.setRange(0.0, 20.0); self._amp.setDecimals(4)
        self._amp.setValue(5.0)
        wg.addWidget(self._amp, 2, 1)

        wg.addWidget(QLabel("Offset (V):"), 3, 0)
        self._offs = QDoubleSpinBox()
        self._offs.setRange(-10.0, 10.0); self._offs.setDecimals(4)
        self._offs.setValue(0.0)
        wg.addWidget(self._offs, 3, 1)

        wg.addWidget(QLabel("Phase (deg):"), 4, 0)
        self._phase = QDoubleSpinBox()
        self._phase.setRange(-360.0, 360.0); self._phase.setDecimals(2)
        self._phase.setValue(0.0)
        wg.addWidget(self._phase, 4, 1)

        wg.addWidget(QLabel("Voltage unit:"), 5, 0)
        self._unit_combo = QComboBox()
        self._unit_combo.addItems(["VPP", "VRMS", "DBM"])
        wg.addWidget(self._unit_combo, 5, 1)

        wg.addWidget(QLabel("Output load:"), 6, 0)
        self._load_combo = QComboBox()
        self._load_combo.addItems(["50", "INF (High-Z)"])
        wg.addWidget(self._load_combo, 6, 1)

        lay.addWidget(wbox)

        # Pulse parameters (only matter when function == PULS)
        pbox = QGroupBox(f"CH{self._channel} Pulse Parameters (when Function = PULS)")
        pg   = QGridLayout(pbox)

        pg.addWidget(QLabel("Period (s):"), 0, 0)
        self._pper = QDoubleSpinBox()
        self._pper.setRange(1e-9, 500.0); self._pper.setDecimals(9)
        self._pper.setValue(1e-3)
        pg.addWidget(self._pper, 0, 1)

        pg.addWidget(QLabel("Width (s):"), 1, 0)
        self._pwid = QDoubleSpinBox()
        self._pwid.setRange(1e-9, 500.0); self._pwid.setDecimals(9)
        self._pwid.setValue(500e-6)
        pg.addWidget(self._pwid, 1, 1)

        lay.addWidget(pbox)

        # Action buttons
        btn_row = QHBoxLayout()
        self._apply_btn = QPushButton("Apply Settings")
        self._on_btn    = QPushButton("Output ON")
        self._off_btn   = QPushButton("Output OFF")
        for b in (self._apply_btn, self._on_btn, self._off_btn):
            b.setEnabled(False)
            btn_row.addWidget(b)
        lay.addLayout(btn_row)

        # Status
        self._status = QLabel(f"CH{self._channel} Output: OFF")
        self._status.setStyleSheet("color: red;")
        lay.addWidget(self._status)
        lay.addStretch()

        # Wiring
        self._apply_btn.clicked.connect(self._on_apply)
        self._on_btn.clicked.connect(self._on_output_on)
        self._off_btn.clicked.connect(self._on_output_off)

    # --- API ---

    def set_enabled(self, enabled: bool):
        for b in (self._apply_btn, self._on_btn, self._off_btn):
            b.setEnabled(enabled)
        if not enabled:
            self._status.setText(f"CH{self._channel} Output: OFF")
            self._status.setStyleSheet("color: red;")

    # --- Slots ---

    def _do(self, fn, args=(), kwargs=None, label: str = ""):
        if kwargs is None:
            kwargs = {}
        w = _CallWorker(fn, args, kwargs, self._signals, label)
        w.start()
        self._worker = w

    def _on_apply(self):
        ctrl = self._get_ctrl()
        if ctrl is None: return
        ch  = self._channel
        fn  = self._fn_combo.currentText()
        f   = self._freq.value()
        a   = self._amp.value()
        o   = self._offs.value()
        ph  = self._phase.value()
        unit = self._unit_combo.currentText()
        load = self._load_combo.currentText()
        load_arg: float | str = "INF" if load.startswith("INF") else 50.0

        def _go():
            ctrl.set_voltage_unit(unit, channel=ch)
            ctrl.set_load(load_arg, channel=ch)
            if fn == "SIN":
                ctrl.apply_sine(f, a, o, channel=ch)
            elif fn == "SQU":
                ctrl.apply_square(f, a, o, channel=ch)
            elif fn == "RAMP":
                ctrl.apply_ramp(f, a, o, channel=ch)
            elif fn == "PULS":
                ctrl.apply_pulse(f, a, o, channel=ch)
                ctrl.configure_pulse(period_s=self._pper.value(),
                                     width_s =self._pwid.value(),
                                     channel =ch)
            elif fn == "NOIS":
                ctrl.apply_noise(a, o, channel=ch)
            elif fn == "DC":
                ctrl.apply_dc(o, channel=ch)
            elif fn == "USER":
                ctrl.apply_user(f, a, o, channel=ch)
            ctrl.set_phase(ph, channel=ch)

        self._do(_go, label=f"CH{ch} apply")

    def _on_output_on(self):
        ctrl = self._get_ctrl()
        if ctrl is None: return
        ch = self._channel

        def _go():
            ctrl.output_on(ch)
        self._do(_go, label=f"CH{ch} output ON")
        self._status.setText(f"CH{ch} Output: ON")
        self._status.setStyleSheet("color: green;")

    def _on_output_off(self):
        ctrl = self._get_ctrl()
        if ctrl is None: return
        ch = self._channel

        def _go():
            ctrl.output_off(ch)
        self._do(_go, label=f"CH{ch} output OFF")
        self._status.setText(f"CH{ch} Output: OFF")
        self._status.setStyleSheet("color: red;")


# ---------------------------------------------------------------------------
# Main window
# ---------------------------------------------------------------------------

class DG1022Window(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Rigol DG1022 AWG Control")
        self.resize(900, 720)

        self._ctrl:    DG1022Controller | None = None
        self._signals = _Signals()
        self._worker  = None

        self._build_ui()
        self._connect_signals()

    # ------------------------------------------------------------------
    # UI
    # ------------------------------------------------------------------

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        lay = QVBoxLayout(central)

        tabs = QTabWidget()
        tabs.addTab(self._build_connection_tab(), "Connection")
        self._ch1_panel = _ChannelPanel(1, lambda: self._ctrl, self._signals, self._log_msg)
        self._ch2_panel = _ChannelPanel(2, lambda: self._ctrl, self._signals, self._log_msg)
        tabs.addTab(self._ch1_panel, "Channel 1")
        tabs.addTab(self._ch2_panel, "Channel 2")
        tabs.addTab(self._build_burst_tab(),  "Burst (CH1)")
        tabs.addTab(self._build_sweep_tab(),  "Sweep (CH1)")
        tabs.addTab(self._build_arb_tab(),    "Arbitrary")

        lay.addWidget(tabs)
        lay.addWidget(self._build_log())

    def _build_connection_tab(self) -> QWidget:
        w   = QWidget()
        lay = QVBoxLayout(w)
        box = QGroupBox("Instrument Connection")
        g   = QGridLayout(box)

        g.addWidget(QLabel("VISA Resource:"), 0, 0)
        self._visa_edit = QLineEdit(DEFAULT_VISA)
        g.addWidget(self._visa_edit, 0, 1)

        g.addWidget(QLabel("Mode:"), 1, 0)
        self._mode_combo = QComboBox()
        self._mode_combo.addItems(["simulation", "hardware"])
        g.addWidget(self._mode_combo, 1, 1)

        btn_row = QHBoxLayout()
        self._connect_btn    = QPushButton("Connect")
        self._disconnect_btn = QPushButton("Disconnect")
        self._test_btn       = QPushButton("Test")
        self._reset_btn      = QPushButton("*RST")
        self._disconnect_btn.setEnabled(False)
        self._reset_btn.setEnabled(False)
        btn_row.addWidget(self._connect_btn)
        btn_row.addWidget(self._disconnect_btn)
        btn_row.addWidget(self._test_btn)
        btn_row.addWidget(self._reset_btn)
        g.addLayout(btn_row, 2, 0, 1, 2)

        self._conn_label = QLabel("Not connected")
        self._conn_label.setStyleSheet("color: red; font-weight: bold;")
        g.addWidget(self._conn_label, 3, 0, 1, 2)

        lay.addWidget(box)
        lay.addStretch()
        return w

    def _build_burst_tab(self) -> QWidget:
        w   = QWidget()
        lay = QVBoxLayout(w)
        box = QGroupBox("Burst Mode (CH1 only)")
        g   = QGridLayout(box)

        g.addWidget(QLabel("Mode:"), 0, 0)
        self._burst_mode = QComboBox()
        self._burst_mode.addItems(["TRIG", "GAT"])
        g.addWidget(self._burst_mode, 0, 1)

        g.addWidget(QLabel("N cycles:"), 1, 0)
        self._burst_n = QSpinBox()
        self._burst_n.setRange(1, 50_000); self._burst_n.setValue(1)
        g.addWidget(self._burst_n, 1, 1)

        g.addWidget(QLabel("Internal period (s):"), 2, 0)
        self._burst_per = QDoubleSpinBox()
        self._burst_per.setRange(1e-6, 500.0); self._burst_per.setDecimals(6)
        self._burst_per.setValue(0.01)
        g.addWidget(self._burst_per, 2, 1)

        g.addWidget(QLabel("Initial phase (deg):"), 3, 0)
        self._burst_ph = QDoubleSpinBox()
        self._burst_ph.setRange(-180.0, 180.0); self._burst_ph.setValue(0.0)
        g.addWidget(self._burst_ph, 3, 1)

        g.addWidget(QLabel("Trigger source:"), 4, 0)
        self._burst_trig = QComboBox()
        self._burst_trig.addItems(["IMM", "EXT", "BUS"])
        g.addWidget(self._burst_trig, 4, 1)

        btn_row = QHBoxLayout()
        self._burst_apply = QPushButton("Enable Burst")
        self._burst_off   = QPushButton("Disable Burst")
        self._burst_trgbtn = QPushButton("Trigger Now (*TRG)")
        for b in (self._burst_apply, self._burst_off, self._burst_trgbtn):
            b.setEnabled(False)
            btn_row.addWidget(b)
        g.addLayout(btn_row, 5, 0, 1, 2)
        lay.addWidget(box)
        lay.addStretch()

        self._burst_apply.clicked.connect(self._on_burst_apply)
        self._burst_off.clicked.connect(self._on_burst_off)
        self._burst_trgbtn.clicked.connect(self._on_burst_trigger)
        return w

    def _build_sweep_tab(self) -> QWidget:
        w   = QWidget()
        lay = QVBoxLayout(w)
        box = QGroupBox("Frequency Sweep (CH1 only)")
        g   = QGridLayout(box)

        g.addWidget(QLabel("Start (Hz):"), 0, 0)
        self._sw_start = QDoubleSpinBox()
        self._sw_start.setRange(1e-6, 20e6); self._sw_start.setDecimals(3)
        self._sw_start.setValue(100.0)
        g.addWidget(self._sw_start, 0, 1)

        g.addWidget(QLabel("Stop (Hz):"), 1, 0)
        self._sw_stop = QDoubleSpinBox()
        self._sw_stop.setRange(1e-6, 20e6); self._sw_stop.setDecimals(3)
        self._sw_stop.setValue(10_000.0)
        g.addWidget(self._sw_stop, 1, 1)

        g.addWidget(QLabel("Time (s):"), 2, 0)
        self._sw_time = QDoubleSpinBox()
        self._sw_time.setRange(1e-3, 500.0); self._sw_time.setDecimals(3)
        self._sw_time.setValue(1.0)
        g.addWidget(self._sw_time, 2, 1)

        g.addWidget(QLabel("Spacing:"), 3, 0)
        self._sw_spc = QComboBox()
        self._sw_spc.addItems(["LIN", "LOG"])
        g.addWidget(self._sw_spc, 3, 1)

        g.addWidget(QLabel("Trigger source:"), 4, 0)
        self._sw_trig = QComboBox()
        self._sw_trig.addItems(["IMM", "EXT", "BUS"])
        g.addWidget(self._sw_trig, 4, 1)

        btn_row = QHBoxLayout()
        self._sw_apply = QPushButton("Enable Sweep")
        self._sw_off   = QPushButton("Disable Sweep")
        for b in (self._sw_apply, self._sw_off):
            b.setEnabled(False)
            btn_row.addWidget(b)
        g.addLayout(btn_row, 5, 0, 1, 2)
        lay.addWidget(box)
        lay.addStretch()

        self._sw_apply.clicked.connect(self._on_sweep_apply)
        self._sw_off.clicked.connect(self._on_sweep_off)
        return w

    def _build_arb_tab(self) -> QWidget:
        w   = QWidget()
        lay = QVBoxLayout(w)

        box = QGroupBox("Arbitrary Waveform")
        g   = QGridLayout(box)

        g.addWidget(QLabel("Built-in waveform:"), 0, 0)
        self._arb_name = QComboBox()
        # Subset of common built-ins (from FUNCtion:USER docs)
        self._arb_name.addItems([
            "EXP_RISE", "EXP_FALL", "SINC", "GAUSS", "HAVERSINE",
            "LORENTZ", "CARDIAC", "NEG_RAMP", "STAIRUP", "STAIRDOWN",
            "VOLATILE",
        ])
        g.addWidget(self._arb_name, 0, 1)

        g.addWidget(QLabel("Apply to channel:"), 1, 0)
        self._arb_ch = QComboBox()
        self._arb_ch.addItems(["1", "2"])
        g.addWidget(self._arb_ch, 1, 1)

        g.addWidget(QLabel("Generate test wave:"), 2, 0)
        self._arb_test = QComboBox()
        self._arb_test.addItems(["Sine cubed", "Triangle", "Gaussian pulse"])
        g.addWidget(self._arb_test, 2, 1)

        g.addWidget(QLabel("Samples:"), 3, 0)
        self._arb_npts = QSpinBox()
        self._arb_npts.setRange(8, 16_384); self._arb_npts.setValue(1024)
        g.addWidget(self._arb_npts, 3, 1)

        btn_row = QHBoxLayout()
        self._arb_load_btn   = QPushButton("Generate + Download")
        self._arb_file_btn   = QPushButton("Load from .csv/.npy")
        self._arb_select_btn = QPushButton("Select Built-in")
        for b in (self._arb_load_btn, self._arb_file_btn, self._arb_select_btn):
            b.setEnabled(False)
            btn_row.addWidget(b)
        g.addLayout(btn_row, 4, 0, 1, 2)
        lay.addWidget(box)

        if HAS_MPL:
            self._arb_fig    = Figure(figsize=(7, 2.5))
            self._arb_canvas = FigureCanvas(self._arb_fig)
            self._arb_ax     = self._arb_fig.add_subplot(111)
            self._arb_ax.set_xlabel("Sample"); self._arb_ax.set_ylabel("Amplitude")
            self._arb_ax.set_title("Arbitrary waveform preview")
            self._arb_ax.grid(True, alpha=0.3)
            lay.addWidget(self._arb_canvas)

        self._arb_load_btn.clicked.connect(self._on_arb_generate)
        self._arb_file_btn.clicked.connect(self._on_arb_file)
        self._arb_select_btn.clicked.connect(self._on_arb_select_builtin)

        return w

    def _build_log(self) -> QWidget:
        box = QGroupBox("Status Log")
        lay = QVBoxLayout(box)
        self._log = QTextEdit()
        self._log.setReadOnly(True)
        self._log.setMaximumHeight(120)
        self._log.setFont(QFont("Courier", 9))
        lay.addWidget(self._log)
        return box

    # ------------------------------------------------------------------
    # Signal wiring
    # ------------------------------------------------------------------

    def _connect_signals(self):
        self._connect_btn.clicked.connect(self._on_connect)
        self._disconnect_btn.clicked.connect(self._on_disconnect)
        self._test_btn.clicked.connect(self._on_test)
        self._reset_btn.clicked.connect(self._on_reset)
        self._signals.connected.connect(self._on_connect_result)
        self._signals.status.connect(self._log_msg)
        self._signals.op_done.connect(lambda label: self._log_msg(f"OK: {label}"))

    # ------------------------------------------------------------------
    # Slots
    # ------------------------------------------------------------------

    def _set_action_buttons_enabled(self, enabled: bool):
        self._ch1_panel.set_enabled(enabled)
        self._ch2_panel.set_enabled(enabled)
        for b in (self._burst_apply, self._burst_off, self._burst_trgbtn,
                  self._sw_apply, self._sw_off,
                  self._arb_load_btn, self._arb_file_btn, self._arb_select_btn,
                  self._reset_btn):
            b.setEnabled(enabled)

    def _on_connect(self):
        self._ctrl = DG1022Controller(
            visa=self._visa_edit.text().strip(),
            mode=self._mode_combo.currentText(),
        )
        self._log_msg("Connecting...")
        self._connect_btn.setEnabled(False)
        w = _ConnectWorker(self._ctrl, self._signals)
        w.start(); self._worker = w

    def _on_connect_result(self, ok: bool, msg: str):
        self._connect_btn.setEnabled(True)
        if ok:
            self._conn_label.setText(f"Connected: {msg}")
            self._conn_label.setStyleSheet("color: green; font-weight: bold;")
            self._disconnect_btn.setEnabled(True)
            self._set_action_buttons_enabled(True)
            self._log_msg(f"Connected: {msg}")
        else:
            self._conn_label.setText("Failed")
            self._conn_label.setStyleSheet("color: red; font-weight: bold;")
            self._ctrl = None
            self._log_msg(f"FAILED: {msg}")

    def _on_disconnect(self):
        if self._ctrl:
            try:
                self._ctrl.disconnect()
            except Exception as e:
                self._log_msg(f"Disconnect: {e}")
            self._ctrl = None
        self._conn_label.setText("Not connected")
        self._conn_label.setStyleSheet("color: red; font-weight: bold;")
        self._disconnect_btn.setEnabled(False)
        self._set_action_buttons_enabled(False)
        self._log_msg("Disconnected.")

    def _on_test(self):
        config = {"visa": self._visa_edit.text().strip(),
                  "mode": self._mode_combo.currentText()}

        class _T(QThread):
            done = pyqtSignal(bool, str)
            def run(self_):
                ok, msg = DG1022Controller.test(config)
                self_.done.emit(ok, msg)
        t = _T(self)
        t.done.connect(lambda ok, m: self._log_msg(f"Test {'OK' if ok else 'FAILED'}: {m}"))
        t.start(); self._worker = t

    def _on_reset(self):
        if self._ctrl is None: return
        try:
            self._ctrl.reset()
            self._log_msg("Reset (*RST) done.")
        except Exception as e:
            self._log_msg(f"Reset error: {e}")

    # --- Burst ---

    def _on_burst_apply(self):
        if self._ctrl is None: return
        kwargs = dict(
            ncycles  = self._burst_n.value(),
            mode     = self._burst_mode.currentText(),
            period_s = self._burst_per.value(),
            phase_deg= self._burst_ph.value(),
            trigger  = self._burst_trig.currentText(),
        )
        w = _CallWorker(self._ctrl.enable_burst, (), kwargs,
                        self._signals, "burst enable")
        w.start(); self._worker = w

    def _on_burst_off(self):
        if self._ctrl is None: return
        w = _CallWorker(self._ctrl.disable_burst, (), {},
                        self._signals, "burst disable")
        w.start(); self._worker = w

    def _on_burst_trigger(self):
        if self._ctrl is None: return
        try:
            self._ctrl.trigger()
            self._log_msg("*TRG sent.")
        except Exception as e:
            self._log_msg(f"Trigger error: {e}")

    # --- Sweep ---

    def _on_sweep_apply(self):
        if self._ctrl is None: return
        kwargs = dict(
            start_hz = self._sw_start.value(),
            stop_hz  = self._sw_stop.value(),
            time_s   = self._sw_time.value(),
            spacing  = self._sw_spc.currentText(),
            trigger  = self._sw_trig.currentText(),
        )
        w = _CallWorker(self._ctrl.enable_sweep, (), kwargs,
                        self._signals, "sweep enable")
        w.start(); self._worker = w

    def _on_sweep_off(self):
        if self._ctrl is None: return
        w = _CallWorker(self._ctrl.disable_sweep, (), {},
                        self._signals, "sweep disable")
        w.start(); self._worker = w

    # --- Arbitrary ---

    def _on_arb_generate(self):
        if self._ctrl is None: return
        kind = self._arb_test.currentText()
        n    = self._arb_npts.value()
        t    = np.linspace(0, 1, n, endpoint=False)
        if kind == "Sine cubed":
            samples = np.sin(2*np.pi*t) ** 3
        elif kind == "Triangle":
            samples = 2 * np.abs(2*(t - np.floor(t + 0.5))) - 1
        else:  # Gaussian pulse
            samples = np.exp(-((t - 0.5) / 0.1) ** 2)
            samples = 2 * samples - 1
        # Normalize to [-1, 1]
        mx = np.max(np.abs(samples))
        if mx > 0:
            samples = samples / mx

        ch = int(self._arb_ch.currentText())
        try:
            self._ctrl.load_arbitrary(samples, channel=ch, normalized=True)
            self._log_msg(f"Downloaded {n}-pt {kind!r} to volatile, assigned to CH{ch}.")
            if HAS_MPL:
                self._arb_ax.clear()
                self._arb_ax.plot(samples, lw=1)
                self._arb_ax.set_xlabel("Sample"); self._arb_ax.set_ylabel("Amplitude")
                self._arb_ax.set_title(f"Arbitrary waveform: {kind}")
                self._arb_ax.grid(True, alpha=0.3)
                self._arb_fig.tight_layout()
                self._arb_canvas.draw()
        except Exception as e:
            self._log_msg(f"Arbitrary download error: {e}")

    def _on_arb_file(self):
        if self._ctrl is None: return
        path, _ = QFileDialog.getOpenFileName(
            self, "Load arbitrary waveform", "",
            "Waveform (*.csv *.npy *.txt);;All files (*)"
        )
        if not path: return
        try:
            if path.lower().endswith(".npy"):
                samples = np.load(path)
            else:
                samples = np.loadtxt(path, delimiter=",")
            samples = np.asarray(samples).flatten()
            mx = np.max(np.abs(samples))
            if mx > 0:
                samples = samples / mx
            ch = int(self._arb_ch.currentText())
            self._ctrl.load_arbitrary(samples, channel=ch, normalized=True)
            self._log_msg(f"Loaded {samples.size}-pt waveform from {path!r}, assigned to CH{ch}.")
            if HAS_MPL:
                self._arb_ax.clear()
                self._arb_ax.plot(samples, lw=1)
                self._arb_ax.set_xlabel("Sample"); self._arb_ax.set_ylabel("Amplitude")
                self._arb_ax.set_title(f"Arbitrary waveform (from file)")
                self._arb_ax.grid(True, alpha=0.3)
                self._arb_fig.tight_layout()
                self._arb_canvas.draw()
        except Exception as e:
            self._log_msg(f"File load error: {e}")

    def _on_arb_select_builtin(self):
        if self._ctrl is None: return
        name = self._arb_name.currentText()
        ch   = int(self._arb_ch.currentText())
        try:
            self._ctrl.select_user_wave(name, channel=ch)
            self._log_msg(f"Selected built-in arb {name!r} on CH{ch}.")
        except Exception as e:
            self._log_msg(f"Select-arb error: {e}")

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------

    def _log_msg(self, msg: str):
        ts = time.strftime("%H:%M:%S")
        self._log.append(f"[{ts}] {msg}")

    def closeEvent(self, event):
        if self._ctrl:
            try: self._ctrl.disconnect()
            except Exception: pass
        super().closeEvent(event)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    app = QApplication(sys.argv)
    win = DG1022Window()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
