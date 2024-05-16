# Ooga booga

```sh
intercept -g /dev/input/event9 | python macro.py | tee /dev/tty | uinput -d /dev/input/event9
```
