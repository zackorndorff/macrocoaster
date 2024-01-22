# KMK firmware configuration

[KMK](https://github.com/KMKfw/kmk_firmware) is an open-source keyboard firmware
written in CircuitPython.

If you don't know C (or are on M1 and don't want to compile QMK), here's a KMK
port that roughly matches the QMK firmware's features. The C firmware in QMK is
arguably better and you should use it. However, if you prefer Python, this port
has you covered.

## Setup

Short version: follow the KMK directions then copy in a few files from here, as
well as our library dependencies.

1. Follow [KMK's Quick Start Guide](https://github.com/KMKfw/kmk_firmware/blob/master/docs/en/Getting_Started.md).
2. Instead of looking for a `kb.py` file in the KMK repo or writing your own
   `code.py` file, pick up here.
3. Copy 2 Adafruit libraries (`adafruit_displayio_ssd1306.mpy` and
   the `adafruit_display_text/` folder) out of the giant zip linked here: https://github.com/adafruit/Adafruit_CircuitPython_Bundle
   and drop them in the `lib` directory in your CIRCUITPY drive.
4. Copy kb.py, custom_oled.py, code.py from this directory into the root of your
   CIRCUITPY drive.
5. Customize to your heart's content.

## Caveats

1. I'm assuming you're using the [Adafruit KB2040 board](https://www.adafruit.com/product/5302).
   If you're not, double-check the pinout in `kb.py`.
2. There is currently a bug with the rotary encoder handling. I need to read
   some datasheets and documentation and figure out where the bug is.
3. Python is slower than C.
4. If your display is not 128x64 you will have some coordinates to adjust.
