import os
import subprocess
import sys

def exec_shell(command, path = None):
    if path is not None:
        safe_path = os.getcwd()
        if not os.path.isdir(path):
            os.makedirs(path, 0o766)
        os.chdir(path)

    rez = subprocess.Popen(
        command,
        shell = True,
        stdout = sys.stdout,
        stderr = sys.stderr,
        stdin = sys.stdin
    )
    rez.wait()
    if path is not None:
        os.chdir(safe_path)
    if rez.returncode != 0:
        raise Exception("Error: executing '" + command + "'")

def normalize_dir(path, pwd):
    return normalize_path(path, pwd) + '/'

def normalize_path(path, pwd):
    path = path.rstrip('/')
    pwd = pwd.rstrip('/') + '/'
    if path[0] != '/':
        path = pwd + path
    real = os.path.realpath(path)
    if real != False:
        return real
    return path

def merge_dict_recursive(data1, data2):
    if not isinstance(data1, dict) or not isinstance(data2, dict):
        return data2
    for key, value in data2.items():
        if key in data1:
            data1[key] = merge_dict_recursive(data1[key], value)
        else:
            data1[key] = value
    return data1
