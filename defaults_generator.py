import configparser
'''
INI files seemingly don't like the escape character PyCharm is generating, so for now, the "defaults" files are being
made here
'''
# ---Defaults---
WIN_VLC_PATH = 'C:/Program Files/VideoLAN/VLC/vlc.exe'
MAC_VLC_PATH = '/Applications/VLC.app'
LINUX_VLC_PATH = '/usr/bin/vlc'
WIN_HANDBRAKE_PATH = 'C:/Program Files/HandBrake/HandBrakeCLI.exe'
MAC_HANDBRAKE_PATH = '/usr/local/bin/handbrakecli'
LINUX_HANDBRAKE_PATH = '/usr/bin/handbrakecli'
VLC_HOST = '127.0.0.1'
VLC_PORT = 8000
VLC_PASSWORD = 'drowssap'
CAPTURE_LENGTH = 30
TIME_UNITS = 'seconds'
OUTPUT_FILETYPE = 'mkv'
ADVANCED_VISIBLE = 1
ADVANCED_OPTIONS = '--encoder x264 --quality 22.0 --vfr --aencoder ca_aac --crop 0:0:0:0 --auto-anamorphic --no-comb-detect --no-deinterlace --no-bwdif --no-decomb --no-detelecine --no-chroma-smooth --no-unsharp --no-lapsharp --no-deblock --no-grayscale'

WIN_FILE = 'src/conf/defaults_win.ini'
MAC_FILE = 'src/conf/defaults_mac.ini'
LINUX_FILE = 'src/conf/defaults_linux.ini'


def make_defaults(vlc_path, handbrake_path):
    return {
        'executables': {
            'vlc_path': vlc_path,
            'handbrake_path': handbrake_path
        },
        'telnet': {
            'vlc_host': VLC_HOST,
            'vlc_port': VLC_PORT,
            'vlc_password': VLC_PASSWORD
        },
        'state': {
            'capture_length': CAPTURE_LENGTH,
            'time_units': TIME_UNITS,
            'output_filetype': OUTPUT_FILETYPE,
            'advanced_visible': ADVANCED_VISIBLE,
            'advanced_options': ADVANCED_OPTIONS
        }
    }


def run():
    parser = configparser.ConfigParser()
    # windows
    parser.read_dict(make_defaults(vlc_path=WIN_VLC_PATH, handbrake_path=WIN_HANDBRAKE_PATH))
    with open(WIN_FILE, 'w') as f:
        parser.write(f)
    # mac
    parser.read_dict(make_defaults(vlc_path=MAC_VLC_PATH, handbrake_path=MAC_HANDBRAKE_PATH))
    with open(MAC_FILE, 'w') as f:
        parser.write(f)
    # linux
    parser.read_dict(make_defaults(vlc_path=LINUX_VLC_PATH, handbrake_path=LINUX_HANDBRAKE_PATH))
    with open(LINUX_FILE, 'w') as f:
        parser.write(f)


run()
