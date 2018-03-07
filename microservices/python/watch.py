#!/usr/bin/env python

from __future__ import print_function

import os
import sys
import subprocess
import time
import psutil


'''
restart running python script.py when file script.py has changed

example: python watch.py python script.py [arg,..]
'''

def modif_epoch(filepath):
    return os.stat(filepath).st_mtime


def print_stdout(process):
    stdout = process.stdout
    if stdout != None:
        print(stdout)


def killme(proc_id):
    process = psutil.Process(proc_id)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()


script_abs_path = sys.argv[2]


command = ' '.join(sys.argv[1:])

last_modified = modif_epoch(script_abs_path)

wait = 0.5

print('watcher: running', script_abs_path, '...')
process = subprocess.Popen(command, shell=True)

print_stdout(process)


while True:
    now_modify = modif_epoch(script_abs_path)
    print_stdout(process)
    if now_modify > last_modified:
        print('watcher: restarting...')
        last_modified = now_modify
        killme(process.pid)
        process = subprocess.Popen(command, shell=True)
    if process.poll() is not None:
        print('watcher: ended')
        sys.exit()
    time.sleep(wait)

