# dg1022

Python driver and GUI for the Rigol DG1022 dual-channel function/arbitrary
waveform generator.

Same architecture as the reference [keysight2987b-python](references/keysight2987b-python)
driver: low-level SCPI driver, high-level controller, standalone PyQt5 GUI,
and a simulation mode so the API exercises without hardware attached.

## Operating modes

| Mode | Method | Use case |
|------|--------|----------|
| **Continuous waveform** | `apply_sine` / `apply_square` / `apply_ramp` / `apply_pulse` / `apply_noise` / `apply_dc` | Free-running output on CH1/CH2 |
| **Pulse** | `apply_pulse` + `configure_pulse(period_s, width_s)` | TTL-style pulses, gates |
| **Arbitrary** | `load_arbitrary(samples)` + `apply_user(...)` | Custom waveforms downloaded to volatile memory |
| **Burst** (CH1) | `enable_burst(ncycles, mode, trigger)` + optional `trigger()` | N-cycle pulses on each trigger |
| **Frequency sweep** (CH1) | `enable_sweep(start_hz, stop_hz, time_s, spacing)` | Linear/log frequency sweep |

## Quick start

```bash
pip install -r requirements.txt

python -m dg1022.gui              # standalone GUI
python examples/basic_usage.py    # headless example
```

## API

```python
from dg1022 import DG1022Controller
import numpy as np

with DG1022Controller(visa="USB0::...", mode="simulation") as awg:

    # 1. Continuous sine on CH1
    awg.apply_sine(frequency=1_000, amplitude=5.0, offset=0.0, channel=1)
    awg.output_on(1)

    # 2. Pulse on CH2
    awg.apply_pulse(frequency=10_000, amplitude=3.3, offset=1.65, channel=2)
    awg.configure_pulse(period_s=100e-6, width_s=20e-6, channel=2)
    awg.output_on(2)

    # 3. Burst — 5 cycles per software trigger
    awg.apply_sine(1_000, 5.0, 0.0, channel=1)
    awg.enable_burst(ncycles=5, mode="TRIG", trigger="BUS")
    awg.trigger()

    # 4. Linear frequency sweep CH1
    awg.enable_sweep(start_hz=100, stop_hz=10_000, time_s=1.0, spacing="LIN")

    # 5. Arbitrary waveform — sine cubed
    samples = np.sin(2*np.pi*np.linspace(0, 1, 1024)) ** 3
    awg.load_arbitrary(samples, channel=1, normalized=True)
    awg.apply_user(frequency=500, amplitude=5.0, offset=0.0, channel=1)
    awg.output_on(1)
```

## Channel convention

`channel=1` maps to CH1 (SCPI commands with no `:CH2` suffix).
`channel=2` maps to CH2 (commands with the `:CH2` suffix).
Burst, sweep, and modulation features are CH1-only on the DG1022.

## Notes on the SCPI mapping

The driver follows the command set documented in
`docs/DG1022_ProgrammingGuide_EN.md` (extracted from the Rigol programming
guide). Key choices:

- `APPLy:SIN[…]` is used as the primary set-everything-at-once command.
- After `APPL:SQU`, the duty cycle is forced to 50 % by the instrument
  (per spec); pass `duty_cycle=` to `apply_square` to override after.
- `OUTP:LOAD INF` (or `set_load("INF")`) selects high-impedance output.
- `DATA VOLATILE,...` downloads normalized floats; `DATA:DAC VOLATILE,...`
  downloads integer DAC codes (0..16383). Use `normalized=False` to choose
  the integer path.
- Simulation mode never opens VISA; it caches the channel state so the
  full API can be exercised offline (used by the GUI and tests).

## Files

```
dg1022/
  __init__.py
  driver.py       # low-level SCPI + sim
  controller.py   # high-level API
  gui.py          # PyQt5 standalone GUI
examples/
  basic_usage.py
docs/
  DG1022_ProgrammingGuide_EN.pdf
  DG1022_ProgrammingGuide_EN.md   # extracted plain-text reference
references/
  keysight2987b-python/            # reference architecture
```
