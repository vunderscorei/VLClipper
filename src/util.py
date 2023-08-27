import os
import platform
import subprocess
import tkinter as tk
from tkinter import messagebox


SEARCH_LOCATIONS = {
    'win': {
        'vlc': {
            'C:/Program Files (x86)/VideoLAN/VLC/vlc.exe'
            'C:/Program Files/VideoLAN/VLC/vlc.exe'
        },
        'handbrakecli': {
            'C:/Program Files (x86)/HandBrake/HandBrakeCLI.exe'
            'C:/Program Files/HandBrake/HandBrakeCLI.exe'
        }
    },
    'mac': {
        'vlc': {
            '/Applications/VLC.app'
        },
        'handbrakecli': {
            '/usr/local/bin/handbrakecli'
            '/Applications/HandBrakeCLI'
        }
    },
    'linux': {
        'vlc': {
            '/usr/bin/vlc'
        },
        'handbrakecli': {
            '/usr/bin/handbrakecli'
        }
    }
}


def locate_program(program):
    # TODO: do not use, currently broken
    loc = None
    if get_os() != 'win':
        loc = subprocess.run(['which', program], stdout=subprocess.PIPE).stdout.decode('utf-8')
    if loc is None:  # 'which' command didn't find it (or we're on Windows)
        for path in SEARCH_LOCATIONS[get_os()][program]:
            if os.path.exists(path):
                loc = path
                break
    return loc


def get_os():
    if platform.system() == 'Windows':
        return 'win'
    if platform.system() == 'Darwin':
        return 'mac'
    else:
        return 'linux'


def throw_alert(level='info', title='VLClipper', message=None):
    if level.lower() == 'warning':
        tk.messagebox.showwarning(title=title, message=message)
    elif level.lower() == 'error':
        tk.messagebox.showerror(title=title, message=message)
    else:
        tk.messagebox.showinfo(title=title, message=message)


def get_real_filepath(filepath):
    return os.path.join(os.path.dirname(__file__), filepath)
