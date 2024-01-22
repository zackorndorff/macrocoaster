# This is a heavily modified version of the OLED code in KMK.
import busio
import displayio
from supervisor import ticks_ms
import terminalio

import adafruit_displayio_ssd1306
from adafruit_display_text import label

from kmk.extensions import Extension


class Oled(Extension):
    def __init__(
        self,
        layer_names,
        oWidth=128,
        oHeight=64, # TODO actually behave with different sizes
        flip: bool=False,
        caps_lock_watcher=None,
        timeout_ms=60000,
    ):
        displayio.release_displays()
        self.rotation = 180 if flip else 0
        self._width = oWidth
        self._height = oHeight
        self._prevLayers = 0
        self._layer_names = layer_names
        self._caps_lock_watcher = caps_lock_watcher
        if self._caps_lock_watcher:
            self._caps_lock_watcher.register_caps_callback(
                    lambda watcher, sandbox: self.updateOLED(sandbox))
        self._update_count = 0
        self._last_event = ticks_ms()
        self._timeout_ms = timeout_ms

        # Set to True to display number of times the display is updated
        # This allows us to make sure we're only updating the display when
        # necessary.
        self._debug = False

    def updateOLED(self, sandbox):
        # TODO: this isn't sufficient: encoder rotations don't cause us to be
        # notified. This class will have to become a Module I think.
        self._last_event = ticks_ms()
        self._update_count += 1

        if self._caps_lock_watcher:
            caps_lock = self._caps_lock_watcher.get_caps_lock()
        else:
            caps_lock = True
        layer = self._layer_names[sandbox.active_layers[0]]
        splash = displayio.Group()
        splash.append(
            label.Label(
                terminalio.FONT,
                text="MACROCOASTER-PY 0.1",
                color=0xFFFFFF,
                x=1,
                y=10*1,
            )
        )
        if caps_lock:
            splash.append(
                label.Label(
                    terminalio.FONT,
                    text="[CAPS LOCK]",
                    color=0xFFFFFF,
                    x=5*6,
                    y=10*2,
                )
            )
        if self._debug:
            splash.append(
                label.Label(
                    terminalio.FONT,
                    text="Updates: " + str(self._update_count),
                    color=0xFFFFFF,
                    x=0,
                    y=10*3,
                )
            )
        splash.append(
            label.Label(
                terminalio.FONT,
                text="Current Layer:",
                color=0xFFFFFF,
                x=0,
                y=10*4,
            )
        )
        splash.append(
            label.Label(
                terminalio.FONT,
                text=layer,
                color=0xFFFFFF,
                x=0,
                y=53, # This gets it into yellow
            )
        )
        self._display.show(splash)

    def on_runtime_enable(self, sandbox):
        pass

    def on_runtime_disable(self, sandbox):
        pass

    def during_bootup(self, keyboard):
        displayio.release_displays()
        i2c = busio.I2C(keyboard.SCL, keyboard.SDA)
        self._display = adafruit_displayio_ssd1306.SSD1306(
            displayio.I2CDisplay(i2c, device_address=0x3C),
            width=self._width,
            height=self._height,
            rotation=self.rotation,
        )
        # Can't use keyboard.sandbox here -- it's not yet populated.
        self.updateOLED(keyboard)

    def before_matrix_scan(self, sandbox):
        if sandbox.active_layers[0] != self._prevLayers:
            self._prevLayers = sandbox.active_layers[0]
            self.updateOLED(sandbox)

    def after_matrix_scan(self, sandbox):
        difference = ticks_ms() - self._last_event

        # Handle rollover, just in case
        if difference < 0:
            self._last_event = ticks_ms()
            difference = 0

        if difference > self._timeout_ms:
            if self._display.is_awake:
                self._display.sleep()
        else:
            if not self._display.is_awake:
                self._display.wake()

    def before_hid_send(self, sandbox):
        pass

    def after_hid_send(self, sandbox):
        pass

    def on_powersave_enable(self, sandbox):
        pass

    def on_powersave_disable(self, sandbox):
        pass

    def deinit(self, sandbox):
        if self._display and not self._display.is_awake:
            self._display.wake()
