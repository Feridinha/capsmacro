import struct
import sys
import time

# Input event struct format
INPUT_EVENT = struct.Struct('llHHI')
# Output event struct format
OUTPUT_EVENT = struct.Struct('llHHI')

# Key codes
KEY_I = 23  # Up arrow
KEY_K = 37  # Down arrow
KEY_J = 36  # Left arrow
KEY_L = 38  # Right arrow
KEY_CAPSLOCK = 58

KEY_UP = 103
KEY_LEFT = 105
KEY_RIGHT = 106
KEY_DOWN = 108


# Event types
EV_KEY = 1

def get_state_by_id(state_id: int) -> str:
    if state_id == 0:
        return "RELEASED"
    elif state_id == 1:
        return "PRESSED"
    elif state_id == 2:
        return "HOLDED"
    else:
        return "UNKNOWN"

IS_CAPS_ON = False

while True:
    data = sys.stdin.buffer.read(INPUT_EVENT.size)
    if len(data) < INPUT_EVENT.size:
        continue

    event_in = INPUT_EVENT.unpack(data)
    _, _, event_type, key_id, state_id = event_in

    state = get_state_by_id(state_id)

    if key_id == KEY_CAPSLOCK:
        if state == "RELEASED":
            IS_CAPS_ON = False
        else:
            IS_CAPS_ON = True

    # Preserve the original event type
    event_time = time.time()
    sec = int(event_time)
    usec = int((event_time - sec) * 1e6)

    if IS_CAPS_ON:
        if key_id == KEY_I:
            key_id = KEY_UP
        elif key_id == KEY_K:
            key_id = KEY_DOWN
        elif key_id == KEY_J:
            key_id = KEY_LEFT
        elif key_id == KEY_L:
            key_id = KEY_RIGHT

    if key_id == KEY_CAPSLOCK and state == "PRESSED": 
        continue
    else:
        event_out = OUTPUT_EVENT.pack(sec, usec, event_type, key_id, state_id)
        sys.stdout.buffer.write(event_out)
        sys.stdout.buffer.flush()

    # Pack the modified event
    
