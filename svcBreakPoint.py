
#! /usr/bin/env python3

 #  ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ 
 # |______|______|______|______|______|______|______|______|______|______|______|______|______|______|______|______|______| 
 #  _      _      _____  ____   
 # | |    | |    |  __ \|  _ \  
 # | |    | |    | |  | | |_) | 
 # | |    | |    | |  | |  _ <  
 # | |____| |____| |__| | |_) | 
 # |______|______|_____/|____/                                                                                                                   
 #  ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ 
 # |______|______|______|______|______|______|______|______|______|______|______|______|______|______|______|______|______|

# https://opensource.apple.com/source/xnu/xnu-1504.3.12/bsd/kern/syscalls.master

import lldb
import os
import shlex
import optparse
import json
import re
from six import StringIO as SixStringIO
import six
import struct

def ILOG(log):
    print("[*] " + log)

def ELOG(log):
    print("[-] " + log)

def SLOG(log):
    print("[+] " + log)

def exe_script(debugger,command_script):
    res = lldb.SBCommandReturnObject()
    interpreter = debugger.GetCommandInterpreter()
    interpreter.HandleCommand('exp -lobjc -O -- ' + command_script, res)

    if not res.HasResult():
        # something error
        return res.GetError()

    response = res.GetOutput()
    return response


def lldbInternalCommand(debugger, command):
    res = lldb.SBCommandReturnObject()
    interpreter = debugger.GetCommandInterpreter()
    interpreter.HandleCommand(command, res)

    if not res.HasResult():
        # something error
        return res.GetError()

    response = res.GetOutput()
    return response

def print_registers(frame):
    register_set = frame.registers # Returns an SBValueList.
    for regs in register_set:
        if 'general purpose registers' in regs.name.lower():
            GPRs = regs
            print('%s (number of children = %d):' % (GPRs.name, GPRs.num_children))
            for reg in GPRs:
                print('\t', reg.name, ' = ', reg.value)
            break

def SvcBreakPointFinderCurrentPc(process, frame):
    error = lldb.SBError()
    pc = frame.register["pc"]
    content = process.ReadMemory(pc.unsigned, 4, error)
    if not error.Success():
        print(f"Failed to read memory at 0x{ptr:0>8x} of 0x{size:0>8x}")
    else:
        new_bytes = bytearray(content)
        linenr = struct.unpack("<I", new_bytes)[0]
        if linenr == 0xD4001001: # svc 0x80
            print('svc 0x80 Found!!!')
            # process.WriteMemory(pc.unsigned, struct.pack('<I',0xD503201F), error) # nop
            # if not error.Success() or result != len(bytes):
                # print('SBProcess.WriteMemory() failed!')
            return True
        if linenr == 0xD503201F: # nop
            return False
    return False


def mod_init_func_finder(debugger):
  process = debugger.GetSelectedTarget().GetProcess()
  target = debugger.GetSelectedTarget()
  module = target.GetModuleAtIndex(0)
  target.DeleteAllBreakpoints()
  section = module.FindSection("__mod_init_func")
  start_addr = section.GetLoadAddress(target)
  bytes_to_read = section.GetByteSize()
  err = lldb.SBError()
  print("start_addr: {}".format(hex(start_addr)))
  print("bytes to read: {}".format(hex(bytes_to_read)))
  linkedit_blob = process.ReadMemory(start_addr,bytes_to_read, err)
  num_blobs = len(linkedit_blob)
  try:
    current_offset = 0x0
    for i in range(0, num_blobs):
        addr = struct.unpack('<Q', linkedit_blob[current_offset:current_offset+8])[0]
        print("InitFunc function Offset of match: {}".format(hex(addr)))
        target.BreakpointCreateByAddress(addr)
        current_offset += 0x8
  except Exception as e:
      pass
  else:
      pass

def __lldb_init_module(debugger, internal_dict):
    # command script import path/xxx.py
    debugger.HandleCommand('command script add -f svcBreakPoint.step_func svcBreakPoint')
    debugger.HandleCommand('command script add -f svcBreakPoint.modInitFuncBreakPoint modInitFuncBreakPoint')
    # debugger.HandleCommand('process attach --name "Clash of Clans" --waitfor')
    # mod_init_func_finder(debugger)

def modInitFuncBreakPoint(debugger, command, result, internal_dict):
    mod_init_func_finder(debugger)

def step_func(debugger, command, result, internal_dict):
    target = debugger.GetSelectedTarget()
    process = target.GetProcess()
    thread = process.GetSelectedThread() # com.apple.main-thread
    start_num_frames = thread.GetNumFrames()
    if start_num_frames == 0:
        return

    while True:
        # thread.StepOver()
        # thread.StepInstruction(False)
        if thread.GetNumFrames() != start_num_frames:
            stream = lldb.SBStream()
            thread.GetStatus(stream)
            description = stream.GetData()
            print(result, "Call stack depth changed %d -> %d" % (start_num_frames, thread.GetNumFrames()))
            print(result, description)
            break
        else:
            debugger.HandleCommand('reg read')
            for frame in thread:
                print(str(frame))
                if SvcBreakPointFinderCurrentPc(process, frame) == True:
                    debugger.HandleCommand('s')
                    # debugger.HandleCommand('process interrupt')
                    return
                # print_registers(frame)
        debugger.HandleCommand('s')
    debugger.HandleCommand('svcBreakPoint')

