print("Starting")

from kb import KMKKeyboard, encoder_pins

from kmk.extensions.media_keys import MediaKeys
from kmk.extensions.lock_status import LockStatus
from kmk.handlers.sequences import send_string, simple_key_sequence
from kmk.keys import KC
from kmk.keys import make_key
from kmk.modules import Module
from kmk.modules.encoder import EncoderHandler
from kmk.modules.layers import Layers

from custom_oled import Oled


### UNCOMMENT FOR DEBUGGING

#def debug_error(module, message: str, error: Exception):
#    # This doesn't work, but it causes an exception that gets us an actual stack
#    # trace.
#    import traceback; traceback.print_exc()
#
## monkeypatch KMK's error handler so we get more verbose errors
#import kmk.kmk_keyboard as monkeypatch
#monkeypatch.debug_error = debug_error

### END UNCOMMENT FOR DEBUGGING


keyboard = KMKKeyboard()

keyboard.extensions.append(MediaKeys())

# Borrowed from the file containing send_string
def make_sequence(s):
    seq = []

    for char in s:
        kc = getattr(KC, char.upper())
        if char.isupper():
            kc = KC.LSHIFT(kc)

        seq.append(kc)

    return seq

# sequences
M_HELLO = send_string("# Hello world!\n")
M_PARTY = simple_key_sequence(
    make_sequence(":partyparrot:") + [
        KC.MACRO_SLEEP_MS(100),
        KC.ENTER,
])
M_OKAY = simple_key_sequence(
    make_sequence(":ok:") + [
        KC.MACRO_SLEEP_MS(100),
        KC.ENTER,
])
M_DITO = simple_key_sequence(
    make_sequence(":ditto_party:") + [
        KC.MACRO_SLEEP_MS(100),
        KC.ENTER,
])
M_PUGD = simple_key_sequence(
    make_sequence(":pug_dance_fast:") + [
        KC.MACRO_SLEEP_MS(100),
        KC.ENTER,
])

DIS_VERT = send_string(";");
DIS_HORZ = send_string(".");
ALGN_VERT = send_string("\"");
ALGN_HORZ = send_string("?");
FLIP_BRD = send_string("]");
GIT_PUSH = send_string("git push\n");
GIT_PULL = send_string("git pull\n");
GIT_COMM = simple_key_sequence(
    make_sequence("git commit -m \"\"") + [
    KC.LEFT, # SS_TAP(X_LEFT)
])
GIT_ADD = send_string("git add -A\n");
VIM_WQF = send_string("\e:wq\n");
CTR_C = simple_key_sequence([KC.LCTL(KC.C)]);
CTR_U = simple_key_sequence([KC.LCTL(KC.U)]);
NEW_WIN = simple_key_sequence([KC.LCTL(KC.T)]);
NEW_TAB = simple_key_sequence([KC.LCTL(KC.N)]);
OPN_TERM = simple_key_sequence([
    KC.LGUI,
    ] + make_sequence("terminal\n"))
# TODO
FLSH_ATML = KC.NO
#        case FLSH_ATML:
#        if (record->event.pressed) {
#            // #if defined(QMK_MCU)
#            //     #if (QMK_MCU == atmega32u4)
#            //         SEND_STRING("qmk compile -kb macrocoaster -km default && qmk flash -bl dfu -km default -kb macrocoaster\n");
#            //     #elif (QMK_MCU == asd)
#            //         SEND_STRING("qmk compile -kb macrocoaster -km default && qmk flash -bl dfu -km default -kb macrocoaster -e CONVERT_TO=kb2040\n");
#            //     #else
#            //         SEND_STRING("# [FAIL] Unknown MCU detected\n");
#            //     #endif
#            // #endif
#            SEND_STRING("qmk compile -kb macrocoaster -km default && qmk flash -bl dfu -km default -kb macrocoaster\n");
#        }
#        break;
FLSH_KB24 = send_string("qmk compile -kb macrocoaster -km default && qmk flash -km default -kb macrocoaster -e CONVERT_TO=kb2040\n");

keyboard.keymap = [
    [
        KC.BRIGHTNESS_DOWN,  KC.BRIGHTNESS_UP,    KC.NO,
        KC.AUDIO_VOL_DOWN,   KC.AUDIO_VOL_UP,     KC.AUDIO_MUTE,
        KC.MEDIA_PREV_TRACK, KC.MEDIA_NEXT_TRACK, KC.MEDIA_PLAY_PAUSE,
        KC.NO,               KC.NO,               KC.NO,
    ],
    [
        GIT_PULL, GIT_PUSH, KC.NO,
        GIT_COMM, GIT_ADD,  KC.NO,
        KC.NO,    KC.NO,    KC.NO,
        KC.NO,    KC.NO,    KC.NO,
    ],
    [
        CTR_U,     CTR_C,     KC.NO,
        VIM_WQF,   KC.NO,     KC.NO,
        FLSH_ATML, FLSH_KB24, KC.NO,
        NEW_WIN,   NEW_TAB,   OPN_TERM,
    ],
    [
        M_PARTY, M_OKAY, KC.NO,
        KC.NO,   M_PUGD, M_DITO,
        KC.NO,   KC.NO,  KC.NO,
        KC.SPC,  KC.ENT, KC.BSPC
    ],
    [

        DIS_VERT, ALGN_VERT, KC.NO,
        DIS_HORZ, ALGN_HORZ, FLIP_BRD,
        KC.F8,    KC.NO,     KC.NO,
        KC.NO,    KC.NO,     KC.NO
    ],
    [
        KC.N1, KC.N2, KC.NO,
        KC.N3, KC.N4, KC.N5,
        KC.N6, KC.N7, KC.N8,
        KC.N9, KC.N0, KC.EQL,
    ],
    [
        KC.A, KC.B, KC.NO,
        KC.C, KC.D, KC.E,
        KC.F, KC.G, KC.H,
        KC.I, KC.J, KC.K,
    ],
]

layer_names = [
        "Multimedia",
        "Git",
        "Term",
        "Slack",
        "KiCAD",
        "Numpad",
        "TEST12345678912345678",
]

if len(layer_names) != len(keyboard.keymap):
    raise Exception("Layer names count must equal the number of layers in keymap.")


# Support for cycling layers (somewhat as opposed to stacking them)
class LayerCycle(Module):
    def __init__(self, *args, **kwargs):
        make_key(
            names=('NEXT_LAYER',),
            on_release=self._next_layer_released,
        )
        make_key(
            names=('PREV_LAYER',),
            on_release=self._prev_layer_released,
        )

    def _next_layer_released(self, key, keyboard, *args, **kwargs):
        self._cycle_layer(1, keyboard)

    def _prev_layer_released(self, key, keyboard, *args, **kwargs):
        self._cycle_layer(-1, keyboard)

    def _cycle_layer(self, distance, keyboard):
        # keyboard.active_layers is a list of indices into keyboard.keymap
        if len(keyboard.active_layers) > 1:
            print("Invalid to cycle layers with more than one active layer")
            return

        active = keyboard.active_layers[0]
        total = len(keyboard.keymap)
        new_layer = (active + distance) % total

        keyboard.active_layers = [new_layer]

    # TODO: we aren't using any of these callbacks: do we even need to be a
    # module?
    def during_bootup(self, keyboard):
        pass

    def before_matrix_scan(self, keyboard):
        '''
        Return value will be injected as an extra matrix update
        '''
        pass

    def after_matrix_scan(self, keyboard):
        '''
        Return value will be replace matrix update if supplied
        '''
        pass

    def process_key(self, keyboard, key, is_pressed, int_coord):
        return key

    def before_hid_send(self, keyboard):
        pass

    def after_hid_send(self, keyboard):
        pass

    def on_powersave_enable(self, keyboard):
        pass

    def on_powersave_disable(self, keyboard):
        pass

keyboard.modules.append(LayerCycle())


# Rotary encoder handling
# TODO: If the encoder is spun quickly, we miss presses.
# Also sometimes we spin backwards.
encoder_handler = EncoderHandler()
encoder_handler.divisor = 4
encoder_handler.pins = encoder_pins

# This can be overwritten for a particular layer if the encoder(s) should behave
# differently if that layer is active.
default_encoder_map = [
    #    CCW,                  CW,   PRESS
    (KC.VOLD,             KC.VOLU, KC.MUTE), # first encoder
    #     CW,                 CCW,   PRESS # yes this is inverted
    (KC.NEXT_LAYER, KC.PREV_LAYER, KC.MUTE), # second encoder
]

encoder_handler.map = [default_encoder_map] * len(keyboard.keymap)
layer_name_map = {v:k for k, v in enumerate(layer_names)}

encoder_handler.map[layer_name_map["KiCAD"]][0] = (
        KC.N, KC.LSHIFT(KC.N), default_encoder_map[0][2],
)

if len(encoder_handler.map) != len(keyboard.keymap):
    raise Exception(f"Encoder handler map must have same layer count as keymap. Keymap has {len(keyboard.keymap)} but encoder handler map has {len(encoder_handler.map)}")

keyboard.modules.append(encoder_handler)


# Watch for changes in Caps Lock status
class LockStatusWatcher(LockStatus):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._last_caps_status = self.get_caps_lock()
        self._callbacks = []

    def register_caps_callback(self, callback):
        # Callback will be called as callback(self, sandbox)
        # From there the callback can call param.get_caps_lock() to get the new
        # state.
        self._callbacks.append(callback)

    def after_hid_send(self, sandbox):
        super().after_hid_send(sandbox)
        last = self._last_caps_status
        self._last_caps_status = self.get_caps_lock()
        if last != self._last_caps_status:
            for cb in self._callbacks:
                cb(self, sandbox)

caps_lock_watcher = LockStatusWatcher()

keyboard.extensions.append(caps_lock_watcher)


# Oled support
oled = Oled(
        layer_names=layer_names,
        oWidth=128,
        oHeight=64,
        flip=True,
        caps_lock_watcher=caps_lock_watcher,
        )
keyboard.extensions.append(oled)


if __name__ == '__main__':
    keyboard.go()

