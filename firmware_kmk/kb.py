import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.scanners import DiodeOrientation


# KMKKeyboard class for the Macrocoaster using an Adafruit KB2040 board.
# If your board differs you may need to adjust these pins.
class KMKKeyboard(_KMKKeyboard):
    col_pins = (
        board.A0,
        board.A1,
        board.A2
    )

    row_pins = (
        board.SCK,
        board.MISO,
        board.MOSI,
        board.D10
    )

    diode_orientation = DiodeOrientation.COL2ROW

    # Define i2c pins for Oled
    SDA = board.D2
    SCL = board.D3

# This doesn't seem to be standard, but I want all the board-specific stuff in
# one file.
encoder_pins = (
        # top-right encoder
        #   PAD A,    PAD B,   BUTTON
        (board.D6, board.D5, board.D4),
        # middle-left encoder, near OLED
        #   PAD A,    PAD B,   BUTTON
        (board.D8, board.D7, board.D9, False),
)
