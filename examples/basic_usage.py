"""
DG1022 basic usage — simulation mode.

Demonstrates the main operating modes:
  1. Continuous sine on CH1
  2. Continuous pulse on CH2 with explicit period/width
  3. Burst (5 cycles per software trigger) on CH1
  4. Linear frequency sweep on CH1
  5. Arbitrary waveform download (sine^3) to CH1
"""

import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import numpy as np
from dg1022 import DG1022Controller


def main():
    with DG1022Controller(mode="simulation") as awg:
        print("IDN:", awg.identify())

        # --- 1. Continuous sine on CH1 ---
        print("\n1. CH1: sine 1 kHz, 5 Vpp, 0 VDC")
        awg.apply_sine(frequency=1_000, amplitude=5.0, offset=0.0, channel=1)
        awg.output_on(1)
        print("   state:", awg.get_channel_state(1))
        awg.output_off(1)

        # --- 2. Continuous pulse on CH2 ---
        print("\n2. CH2: 10 kHz pulse, 3.3 Vpp, 1.65 V offset, 20 us width")
        awg.apply_pulse(frequency=10_000, amplitude=3.3, offset=1.65, channel=2)
        awg.configure_pulse(period_s=100e-6, width_s=20e-6, channel=2)
        awg.output_on(2)
        print("   state:", awg.get_channel_state(2))
        awg.output_off(2)

        # --- 3. Burst on CH1 ---
        print("\n3. CH1: 5-cycle burst per *TRG, sine 1 kHz")
        awg.apply_sine(1_000, 5.0, 0.0, channel=1)
        awg.enable_burst(ncycles=5, mode="TRIG", trigger="BUS")
        awg.trigger()                       # software trigger
        print("   burst armed; *TRG sent")
        awg.disable_burst()

        # --- 4. Linear frequency sweep on CH1 ---
        print("\n4. CH1: linear sweep 100 Hz -> 10 kHz over 1 s")
        awg.apply_sine(1_000, 5.0, 0.0, channel=1)
        awg.enable_sweep(start_hz=100, stop_hz=10_000, time_s=1.0, spacing="LIN")
        print("   sweep enabled")
        awg.disable_sweep()

        # --- 5. Arbitrary waveform (sine cubed) ---
        print("\n5. CH1: arbitrary waveform - sine cubed (1024 pts)")
        t = np.linspace(0, 1, 1024, endpoint=False)
        samples = np.sin(2 * np.pi * t) ** 3
        awg.load_arbitrary(samples, channel=1, normalized=True)
        awg.apply_user(frequency=500, amplitude=5.0, offset=0.0, channel=1)
        awg.output_on(1)
        print("   user wave selected on CH1:", awg.get_channel_state(1)["user_wave"])
        awg.all_outputs_off()

    print("\nDone.")


if __name__ == "__main__":
    main()
