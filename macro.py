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
KEY_H = 35  # /
KEY_ON_RIGHT_OF_L = 39
KEY_PIPE = 86
KEY_SLASH = 98
KEY_BACKSLASH = 86
KEY_SHIFT = 42
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
IS_SHIFT_ON = False
last_remapped_key = None

while True:
    data = sys.stdin.buffer.read(INPUT_EVENT.size)
    if len(data) < INPUT_EVENT.size:
        continue
    
    event_in = INPUT_EVENT.unpack(data)
    _, _, event_type, key_id, state_id = event_in
    state = get_state_by_id(state_id)
    
    # Handle CAPSLOCK state changes
    if key_id == KEY_CAPSLOCK:
        if state == "RELEASED":
            IS_CAPS_ON = False
            # Send a release event for the last remapped key if it exists
            if last_remapped_key:
                event_time = time.time()
                sec = int(event_time)
                usec = int((event_time - sec) * 1e6)
                release_event = OUTPUT_EVENT.pack(sec, usec, EV_KEY, last_remapped_key, 0)  # 0 for RELEASED
                sys.stdout.buffer.write(release_event)
                sys.stdout.buffer.flush()
                last_remapped_key = None
        else:
            IS_CAPS_ON = True
    elif key_id == KEY_SHIFT:
        IS_SHIFT_ON = state != "RELEASED"
    
    event_time = time.time()
    sec = int(event_time)
    usec = int((event_time - sec) * 1e6)
    
    original_key_id = key_id
    if IS_CAPS_ON:
        if key_id == KEY_I:
            key_id = KEY_UP
        elif key_id == KEY_K:
            key_id = KEY_DOWN
        elif key_id == KEY_J:
            key_id = KEY_LEFT
        elif key_id == KEY_L:
            key_id = KEY_RIGHT
        elif key_id == KEY_H:
            key_id = KEY_SLASH
        
        if key_id != original_key_id:
            last_remapped_key = key_id
    elif IS_SHIFT_ON and key_id == KEY_ON_RIGHT_OF_L:
        key_id = KEY_PIPE
    
    if key_id == KEY_CAPSLOCK and state == "PRESSED":
        continue
    else:
        event_out = OUTPUT_EVENT.pack(sec, usec, event_type, key_id, state_id)
        sys.stdout.buffer.write(event_out)
        sys.stdout.buffer.flush()

    # If CAPS is released and we're processing a remapped key, send a release event
    if not IS_CAPS_ON and original_key_id != key_id:
        release_event = OUTPUT_EVENT.pack(sec, usec, EV_KEY, key_id, 0)  # 0 for RELEASED
        sys.stdout.buffer.write(release_event)
        sys.stdout.buffer.flush()