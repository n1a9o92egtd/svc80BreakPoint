# svc80BreakPoint
The svc80BreakPoint is an automated lldb script designed to trace and detect anti-debugging and jailbreak attempts in iOS apps that directly use the assembly instruction svc 0x80.

# LLDB Debugger Functions

This repository contains two Python functions for the LLDB debugger:
- `modInitFuncBreakPoint`: searches for the address of the `__mod_init_func` function in the selected target and creates breakpoints at each function address found until a breakpoint at an SVC instruction with opcode `0x80` is hit.
- `svcBreakPoint`: steps through instructions in the selected thread until a breakpoint at an SVC instruction with opcode `0x80` is hit.

## How It Works

### `modInitFuncBreakPoint`

`modInitFuncBreakPoint` is a Python function for the LLDB debugger that searches for the address of the `__mod_init_func` function in the selected target, reads the corresponding memory section, and creates breakpoints at each of the function addresses found.

When a kernel module is loaded, `__mod_init_func` is called to initialize its state. By setting breakpoints at each function address found, `modInitFuncBreakPoint` allows you to step through the initialization code and debug any issues.

This can be useful for debugging userland code on macOS/iOS, as many system calls are made using the `svc` instruction with opcode `0x80`.

### `svcBreakPoint`

`svcBreakPoint` is a Python function for the LLDB debugger that steps through instructions in the selected thread until a breakpoint at an SVC instruction with opcode `0x80` is hit.

This can be useful for debugging userland code on macOS/iOS, as many system calls are made using the `svc` instruction with opcode `0x80`.

## Usage

To use either function, load it into the LLDB debugger and call the function. Full usage details can be found in the function documentation.

For example:

```
(lldb) command script import svcBreakPoint.py
(lldb) modInitFuncBreakPoint

(lldb) command script import svcBreakPoint.py
(lldb) svcBreakPoint
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
