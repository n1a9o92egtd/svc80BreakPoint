
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
import time
from six import StringIO as SixStringIO
import six
import struct

# process connect connect://127.0.0.1:1234
# process attach --name "KeePass" --waitfor
# b class_getInstanceMethod
# command script import /Users/my_anonymous/Desktop/my_projects/svcBreakPoint/FunctionBP.py
# FunctionBP

def ILOG(log):
    print("[*] " + log)

def ELOG(log):
    print("[-] " + log)

def SLOG(log):
    print("[+] " + log)

def __lldb_init_module(debugger, internal_dict):
    # command script import path/xxx.py
    debugger.HandleCommand('command script add -f FunctionBP.step_func FunctionBP')
    # debugger.HandleCommand('process attach --name "Clash of Clans" --waitfor')
    # mod_init_func_finder(debugger)

def step_func(debugger, command, result, internal_dict):
    while True:
        debugger.HandleCommand('po $x0')
        debugger.HandleCommand('po (char*)$x1')
        time.sleep(2)
        debugger.HandleCommand('continue')

