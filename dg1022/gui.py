"""
dg1022/gui.py

NiceGUI control panel for the Rigol DG1022 arbitrary waveform generator.

Same two-mode pattern as the b2987b / vx2740 / pulse_mux /
phidget_stage / keithley6485 GUIs:

  - Standalone (`python -m dg1022.gui`): opens a browser served by
    NiceGUI with a Connection card that creates and owns its own
    DG1022Controller. Useful for bench bring-up without the rest
    of the DAQ.

  - Embedded (`build_page(get_controller=..., show_connection=False)`):
    called from a parent NiceGUI app (the ETS DAQ web shell). The
    parent passes a getter that returns the shared controller; this
    panel hides its Connection card and drives the parent's
    controller.

Tabs: connection (standalone), ch1, ch2, burst (ch1 only),
sweep (ch1 only), arbitrary.
"""

from __future__ import annotations

import asyncio
import time
from typing import Callable, Optional

import numpy as np
from nicegui import ui

from .controller import DG1022Controller
from .driver     import DEFAULT_VISA


# ---------------------------------------------------------------------------
# Style — xsphere/DAQ palette
# ---------------------------------------------------------------------------

_CSS = """
:root {
  --bg:#11151c; --panel:#1b2230; --panel2:#232c3d;
  --fg:#dde3ee; --mut:#8a93a6;
  --ok:#3fb950; --warn:#d29922; --bad:#f85149; --acc:#58a6ff;
  --line:#2d3648;
}
html, body, .nicegui-content { background:var(--bg) !important; color:var(--fg);
  font:14px/1.45 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif; margin:0; }
.pill { padding:.15rem .55rem; border-radius:999px; font-size:.78rem;
  font-weight:600; white-space:nowrap; display:inline-flex; align-items:center; gap:.3rem; }
.pill.ok   { background:rgba(63,185,80,.18);  color:var(--ok); }
.pill.bad  { background:rgba(248,81,73,.18);  color:var(--bad); }
.pill.warn { background:rgba(210,153,34,.18); color:var(--warn); }
.pill.mut  { background:rgba(138,147,166,.15);color:var(--mut); }
.q-card, .dg-card {
  background:var(--panel) !important; color:var(--fg) !important;
  border:1px solid var(--line); border-radius:10px;
  box-shadow:none !important; padding:.55rem .85rem .7rem !important;
}
.dg-card h2 { font-size:.92rem; margin:.05rem 0 .45rem; color:var(--acc);
  font-weight:600; letter-spacing:.3px; }
.q-btn { background:var(--panel2) !important; color:var(--fg) !important;
  border:1px solid var(--line) !important; border-radius:6px !important;
  box-shadow:none !important; padding:.18rem .65rem !important;
  min-height:32px !important; text-transform:none !important; }
.q-btn:hover { border-color:var(--acc) !important; }
.q-btn[data-q-color="primary"], .q-btn.bg-primary {
  background:var(--acc) !important; color:#08111f !important;
  border-color:var(--acc) !important; font-weight:600 !important; }
.q-btn[data-q-color="negative"], .q-btn.bg-negative {
  background:transparent !important; color:var(--bad) !important;
  border-color:var(--bad) !important; }
.q-field__control, .q-field--filled .q-field__control {
  background:var(--panel2) !important; border:1px solid var(--line) !important;
  border-radius:6px !important; min-height:32px !important; color:var(--fg) !important; }
.q-field__label, .q-field__native, .q-field input { color:var(--fg) !important; }
.q-field__label { color:var(--mut) !important; }
.q-field--filled .q-field__control:before,
.q-field--filled .q-field__control:after { display:none !important; }
.q-tab { color:var(--mut) !important; text-transform:none !important; }
.q-tab--active { color:var(--acc) !important; }
.q-tab__indicator { background:var(--acc) !important; }
.q-log, .nicegui-log { background:var(--panel2) !important; color:var(--fg) !important;
  border:1px solid var(--line); border-radius:6px;
  font-family:ui-monospace,Menlo,Consolas,monospace; font-size:.82rem; }
.num { font-variant-numeric:tabular-nums; }
"""


async def _in_thread(fn, *a, **kw):
    return await asyncio.to_thread(fn, *a, **kw)


# ---------------------------------------------------------------------------
# Per-channel control sub-component
# ---------------------------------------------------------------------------

def _channel_card(ch: int, get_ctrl, log_msg):
    """Build a card with waveform + pulse + apply/output for CH `ch`."""
    with ui.card().classes("dg-card"):
        ui.html(f"<h2>ch{ch} waveform</h2>")
        fn_sel = ui.select(["SIN", "SQU", "RAMP", "PULS", "NOIS", "DC", "USER"],
                           value="SIN", label="function").classes("w-32")
        freq = ui.number(label="frequency (Hz)", value=1000.0,
                         step=1.0, format="%.6f").classes("w-40 num")
        amp  = ui.number(label="amplitude (Vpp)", value=1.0,
                         step=0.1, format="%.4f").classes("w-40 num")
        offs = ui.number(label="offset (V)", value=0.0,
                         step=0.1, format="%.4f").classes("w-40 num")
        phase= ui.number(label="phase (deg)", value=0.0,
                         step=1.0, format="%.2f").classes("w-40 num")
        unit = ui.select(["VPP", "VRMS", "DBM"], value="VPP",
                         label="voltage unit").classes("w-32")
        load = ui.select(["50", "INF (High-Z)"], value="50",
                         label="output load").classes("w-40")

        with ui.expansion("pulse parameters (Function = PULS only)").classes("w-full"):
            pulse_per = ui.number(label="period (s)", value=1e-3,
                                  step=1e-6, format="%.9f").classes("w-40 num")
            pulse_wid = ui.number(label="width (s)", value=500e-6,
                                  step=1e-6, format="%.9f").classes("w-40 num")

        out_pill = ui.html(f'<span class="pill mut">ch{ch} output: off</span>')

    def _do_apply():
        c = get_ctrl()
        if c is None: log_msg(f"ch{ch} apply: not connected"); return None
        try:
            c.set_voltage_unit(str(unit.value), channel=ch)
            ld = "INF" if "INF" in str(load.value) else 50.0
            c.set_load(ld, channel=ch)
            fn = str(fn_sel.value)
            if fn == "SIN":
                c.apply_sine (float(freq.value), float(amp.value), float(offs.value), channel=ch)
            elif fn == "SQU":
                c.apply_square(float(freq.value), float(amp.value), float(offs.value), channel=ch)
            elif fn == "RAMP":
                c.apply_ramp (float(freq.value), float(amp.value), float(offs.value), channel=ch)
            elif fn == "PULS":
                c.apply_pulse(float(freq.value), float(amp.value), float(offs.value), channel=ch)
                c.configure_pulse(period_s=float(pulse_per.value),
                                  width_s =float(pulse_wid.value),
                                  channel =ch)
            elif fn == "NOIS":
                c.apply_noise(float(amp.value), float(offs.value), channel=ch)
            elif fn == "DC":
                c.apply_dc(float(offs.value), channel=ch)
            elif fn == "USER":
                c.apply_user(float(freq.value), float(amp.value), float(offs.value), channel=ch)
            c.set_phase(float(phase.value), channel=ch)
            log_msg(f"ch{ch} apply {fn}  f={freq.value}  A={amp.value}  off={offs.value}")
            return c
        except Exception as e:
            log_msg(f"ch{ch} apply FAIL: {type(e).__name__}: {e}")
            return None

    async def apply():
        await _in_thread(_do_apply)

    async def out_on():
        c = get_ctrl()
        if c is None: log_msg(f"ch{ch} output_on: not connected"); return
        try:
            await _in_thread(c.output_on, ch)
            out_pill.content = f'<span class="pill ok">ch{ch} output: on</span>'
            log_msg(f"ch{ch} output ON")
        except Exception as e:
            log_msg(f"ch{ch} output_on FAIL: {type(e).__name__}: {e}")

    async def out_off():
        c = get_ctrl()
        if c is None: log_msg(f"ch{ch} output_off: not connected"); return
        try:
            await _in_thread(c.output_off, ch)
            out_pill.content = f'<span class="pill mut">ch{ch} output: off</span>'
            log_msg(f"ch{ch} output OFF")
        except Exception as e:
            log_msg(f"ch{ch} output_off FAIL: {type(e).__name__}: {e}")

    with ui.row().classes("gap-2 mt-1"):
        ui.button(f"apply ch{ch}", on_click=apply).props("color=primary")
        ui.button("output on",     on_click=out_on).props("color=primary")
        ui.button("output off",    on_click=out_off).props("color=negative")


# ===========================================================================
# build_page
# ===========================================================================

def build_page(get_controller: Optional[Callable[[], Optional[DG1022Controller]]] = None,
               *, show_connection: Optional[bool] = None) -> None:
    """Render the DG1022 control panel into the current container."""
    if show_connection is None:
        show_connection = (get_controller is None)

    _own = {"ctrl": None, "arb_samples": None}
    if get_controller is None:
        def get_controller():
            return _own["ctrl"]

    log = ui.log(max_lines=120).classes("h-32 w-full")
    def log_msg(s: str): log.push(f"[{time.strftime('%H:%M:%S')}] {s}")

    with ui.tabs().classes("w-full") as tabs:
        t_conn  = ui.tab("connection") if show_connection else None
        t_ch1   = ui.tab("ch1")
        t_ch2   = ui.tab("ch2")
        t_burst = ui.tab("burst (ch1)")
        t_sweep = ui.tab("sweep (ch1)")
        t_arb   = ui.tab("arbitrary")

    initial = t_conn if t_conn is not None else t_ch1
    with ui.tab_panels(tabs, value=initial).classes("w-full"):

        # ----------- Connection (standalone only) -----------
        if t_conn is not None:
            with ui.tab_panel(t_conn):
                with ui.card().classes("dg-card"):
                    ui.html("<h2>instrument connection</h2>")
                    visa_in = ui.input(label="VISA / device path",
                                       value=DEFAULT_VISA).classes("w-96 num")
                    mode_in = ui.select(["simulation", "hardware"],
                                        value="simulation", label="mode").classes("w-40")
                    conn_pill = ui.html('<span class="pill mut">disconnected</span>')

                    def set_pill(text: str, cls: str):
                        conn_pill.content = f'<span class="pill {cls}">{text}</span>'

                    async def do_connect():
                        c = DG1022Controller(visa=visa_in.value.strip(),
                                             mode=mode_in.value)
                        set_pill("connecting…", "warn")
                        try:
                            await _in_thread(c.connect)
                            _own["ctrl"] = c
                            set_pill(f"OK — {c.identify()[:60]}", "ok")
                            log_msg(f"connected: {c.identify()}")
                        except Exception as e:
                            set_pill(f"FAIL: {type(e).__name__}", "bad")
                            log_msg(f"connect FAIL: {type(e).__name__}: {e}")

                    async def do_disconnect():
                        c = _own["ctrl"]
                        if c is None: return
                        try: await _in_thread(c.disconnect)
                        except Exception as e: log_msg(f"disconnect warn: {e}")
                        _own["ctrl"] = None
                        set_pill("disconnected", "mut")
                        log_msg("disconnected")

                    with ui.row().classes("mt-1 gap-2"):
                        ui.button("connect",    on_click=do_connect).props("color=primary")
                        ui.button("disconnect", on_click=do_disconnect).props("color=negative flat")

        # ----------- ch1 / ch2 -----------
        with ui.tab_panel(t_ch1):
            _channel_card(1, get_controller, log_msg)
        with ui.tab_panel(t_ch2):
            _channel_card(2, get_controller, log_msg)

        # ----------- Burst (CH1 only) -----------
        with ui.tab_panel(t_burst):
            with ui.card().classes("dg-card"):
                ui.html("<h2>burst mode (CH1 only)</h2>")
                b_mode = ui.select(["TRIG", "GAT"], value="TRIG",
                                   label="mode").classes("w-32")
                b_n    = ui.number(label="N cycles", value=1, step=1).classes("w-32 num")
                b_per  = ui.number(label="internal period (s)", value=0.01,
                                   step=0.001, format="%.6f").classes("w-40 num")
                b_ph   = ui.number(label="initial phase (deg)", value=0.0,
                                   step=1.0).classes("w-40 num")
                b_trig = ui.select(["IMM", "EXT", "BUS"], value="IMM",
                                   label="trigger source").classes("w-32")

                async def burst_apply():
                    c = get_controller()
                    if c is None: log_msg("burst: not connected"); return
                    try:
                        await _in_thread(c.enable_burst,
                                          int(b_n.value), str(b_mode.value),
                                          float(b_per.value), float(b_ph.value),
                                          str(b_trig.value))
                        log_msg(f"burst enabled n={b_n.value} mode={b_mode.value} trig={b_trig.value}")
                    except Exception as e:
                        log_msg(f"burst_apply FAIL: {type(e).__name__}: {e}")

                async def burst_off():
                    c = get_controller()
                    if c is None: log_msg("burst: not connected"); return
                    try:
                        await _in_thread(c.disable_burst)
                        log_msg("burst disabled")
                    except Exception as e:
                        log_msg(f"burst_off FAIL: {type(e).__name__}: {e}")

                async def burst_trg():
                    c = get_controller()
                    if c is None: log_msg("burst: not connected"); return
                    try:
                        await _in_thread(c.trigger)
                        log_msg("*TRG sent")
                    except Exception as e:
                        log_msg(f"trigger FAIL: {type(e).__name__}: {e}")

                with ui.row().classes("gap-2 mt-1"):
                    ui.button("enable burst",     on_click=burst_apply).props("color=primary")
                    ui.button("disable burst",    on_click=burst_off).props("color=negative")
                    ui.button("trigger now (*TRG)", on_click=burst_trg)

        # ----------- Sweep (CH1 only) -----------
        with ui.tab_panel(t_sweep):
            with ui.card().classes("dg-card"):
                ui.html("<h2>frequency sweep (CH1 only)</h2>")
                sw_start = ui.number(label="start (Hz)", value=100.0,
                                     step=1.0, format="%.3f").classes("w-40 num")
                sw_stop  = ui.number(label="stop (Hz)",  value=10_000.0,
                                     step=1.0, format="%.3f").classes("w-40 num")
                sw_time  = ui.number(label="time (s)",   value=1.0,
                                     step=0.1, format="%.3f").classes("w-32 num")
                sw_spc   = ui.select(["LIN", "LOG"], value="LIN",
                                     label="spacing").classes("w-32")
                sw_trig  = ui.select(["IMM", "EXT", "BUS"], value="IMM",
                                     label="trigger source").classes("w-32")

                async def sweep_apply():
                    c = get_controller()
                    if c is None: log_msg("sweep: not connected"); return
                    try:
                        await _in_thread(c.enable_sweep,
                                          float(sw_start.value), float(sw_stop.value),
                                          float(sw_time.value), str(sw_spc.value),
                                          str(sw_trig.value))
                        log_msg(f"sweep {sw_start.value}→{sw_stop.value} Hz {sw_spc.value} in {sw_time.value} s")
                    except Exception as e:
                        log_msg(f"sweep_apply FAIL: {type(e).__name__}: {e}")

                async def sweep_off():
                    c = get_controller()
                    if c is None: log_msg("sweep: not connected"); return
                    try:
                        await _in_thread(c.disable_sweep)
                        log_msg("sweep disabled")
                    except Exception as e:
                        log_msg(f"sweep_off FAIL: {type(e).__name__}: {e}")

                with ui.row().classes("gap-2 mt-1"):
                    ui.button("enable sweep",  on_click=sweep_apply).props("color=primary")
                    ui.button("disable sweep", on_click=sweep_off).props("color=negative")

        # ----------- Arbitrary -----------
        with ui.tab_panel(t_arb):
            with ui.card().classes("dg-card w-full"):
                ui.html("<h2>built-in arbitrary waveform</h2>")
                arb_name = ui.select(
                    ["EXP_RISE", "EXP_FALL", "SINC", "GAUSS", "HAVERSINE",
                     "LORENTZ", "CARDIAC", "NEG_RAMP", "STAIRUP", "STAIRDOWN",
                     "VOLATILE"],
                    value="EXP_RISE", label="built-in").classes("w-40")
                arb_ch = ui.select(["1", "2"], value="1", label="channel").classes("w-24")

                async def select_builtin():
                    c = get_controller()
                    if c is None: log_msg("arb: not connected"); return
                    try:
                        await _in_thread(c.select_user_wave,
                                          str(arb_name.value), int(arb_ch.value))
                        log_msg(f"selected built-in {arb_name.value} on ch{arb_ch.value}")
                    except Exception as e:
                        log_msg(f"select_user_wave FAIL: {type(e).__name__}: {e}")

                ui.button("select built-in", on_click=select_builtin).props("color=primary")

            with ui.card().classes("dg-card w-full"):
                ui.html("<h2>generate and download a test waveform</h2>")
                with ui.row().classes("items-center gap-2"):
                    arb_test = ui.select(["Sine cubed", "Triangle", "Gaussian pulse"],
                                          value="Sine cubed",
                                          label="generator").classes("w-40")
                    arb_npts = ui.number(label="samples", value=1024,
                                          step=64, min=8, max=16384).classes("w-32 num")
                arb_plot = ui.matplotlib(figsize=(8, 2.6)).classes("w-full")
                arb_ax   = arb_plot.figure.add_subplot(111)
                arb_ax.set_xlabel("sample"); arb_ax.set_ylabel("amplitude (normalised)")
                arb_ax.grid(True, alpha=.3); arb_plot.figure.tight_layout()

                def _gen():
                    n = int(arb_npts.value)
                    t = np.linspace(0.0, 1.0, n)
                    name = str(arb_test.value)
                    if name == "Sine cubed":
                        return np.sin(2 * np.pi * t) ** 3
                    elif name == "Triangle":
                        return 2 * np.abs(2 * (t - np.floor(t + 0.5))) - 1
                    else:  # Gaussian pulse
                        return np.exp(-((t - 0.5) / 0.07) ** 2)

                def generate_and_preview():
                    samples = _gen()
                    _own["arb_samples"] = samples
                    arb_ax.clear()
                    arb_ax.plot(samples, lw=1, color="#58a6ff")
                    arb_ax.set_xlabel("sample"); arb_ax.set_ylabel("amplitude (normalised)")
                    arb_ax.grid(True, alpha=.3); arb_plot.figure.tight_layout()
                    arb_plot.update()
                    log_msg(f"generated {len(samples)} samples ({arb_test.value})")

                async def download():
                    samples = _own["arb_samples"]
                    if samples is None:
                        log_msg("no samples — click 'generate + preview' first"); return
                    c = get_controller()
                    if c is None: log_msg("arb: not connected"); return
                    try:
                        await _in_thread(c.load_arbitrary,
                                          samples, int(arb_ch.value), True)
                        log_msg(f"downloaded {len(samples)} samples to VOLATILE on ch{arb_ch.value}")
                    except Exception as e:
                        log_msg(f"load_arbitrary FAIL: {type(e).__name__}: {e}")

                with ui.row().classes("gap-2 mt-1"):
                    ui.button("generate + preview", on_click=generate_and_preview).props("color=primary")
                    ui.button("download to instrument", on_click=download).props("color=primary")


# ---------------------------------------------------------------------------
# Standalone entry — `python -m dg1022.gui`
# ---------------------------------------------------------------------------

def main():
    import argparse
    p = argparse.ArgumentParser(description="Rigol DG1022 web GUI")
    p.add_argument("--host", default="0.0.0.0")
    p.add_argument("--port", type=int, default=8771)
    args = p.parse_args()

    @ui.page("/")
    def index():
        ui.add_head_html(f"<style>{_CSS}</style>")
        ui.dark_mode().enable()
        with ui.element("header").style(
            "display:flex;align-items:center;gap:.8rem;"
            "padding:.55rem 1rem;background:var(--panel);"
            "border-bottom:1px solid var(--line);position:sticky;top:0;z-index:5"
        ):
            ui.html("<h1 style='font-size:1.05rem;font-weight:600;margin:0'>"
                    "DG1022 · waveform generator</h1>")
        build_page()

    ui.run(host=args.host, port=args.port, reload=False,
           title="DG1022 WFG", show=False)


if __name__ in {"__main__", "__mp_main__"}:
    main()
