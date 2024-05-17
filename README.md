# CAPS + MACRO
![preview](https://f.feridinha.com/ySa3H.png)
This is a script that transforms capslock into a modifier key,
enabling you to use capslock + ijkl as your arrow keys.

- caps + L = arrow right
- caps + K = arrow down
- caps + J = arrow left
- caps + I = arrow up
- caps + shift + h = slash
- caps + ; = \
- caps + shift + ; = | 

## Dependencies
This script depends on [intercept-tools](https://wiki.archlinux.org/title/interception-tools), which is used to intercept every keystroke and send it to `macro.py`, which acts like a proxy.
You will also need to install `python-uinput`.

## How to run
In the command below, `/dev/input/event9` is the keyboard target. Please use the command evtest to identify your input device and replace the device path accordingly before running the script.

```sh
intercept -g /dev/input/event9 | python macro.py | uinput -d /dev/input/event9
```

If this script doesnt work, try changing the keycodes hardcoded into the file `macro.py`. Example change KEY_I to `KEY_I=999`, which 999 is the keycode for the letter i in your keyboard