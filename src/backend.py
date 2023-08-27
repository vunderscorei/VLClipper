import os
import tkinter as tk
from tkinter import filedialog
import subprocess
import time
from python_telnet_vlc import VLCTelnet

import config
import util


class Backend:

    def __init__(self):
        self.config = config.Config(util.get_real_filepath('conf/config.ini'))
        self.vlc_gui_proc = None
        self.vlc_telnet = None
        self.handbrake_proc = None
        self.capture_info = None

    def connect_telnet(self):
        self.vlc_telnet = VLCTelnet(self.config.get_vlc_host(), self.config.get_vlc_password(), self.config.get_vlc_port())

    def open_vlc_gui(self):
        # TODO: kill upon exit
        if (self.vlc_gui_proc is not None) and (self.vlc_gui_proc.poll() is None):
            util.throw_alert('warning', message='VLC already open')
        else:
            if util.get_os() == 'win':
                vlc_command = [self.config.get_vlc_path(), '--extraintf=telnet', '--telnet-password=' +
                               self.config.get_vlc_password(), '--telnet-host=' + self.config.get_vlc_host(),
                               '--telnet-port=' + str(self.config.get_vlc_port())]
            elif util.get_os() == 'mac':
                vlc_command = [self.config.get_vlc_path() + '/Contents/MacOS/VLC', '--extraintf', 'telnet',
                               '--telnet-password', self.config.get_vlc_password(), '--telnet-host',
                               self.config.get_vlc_host(), '--telnet-port', str(self.config.get_vlc_port())]
            else:
                vlc_command = [self.config.get_vlc_path(), '--extraintf', 'telnet', '--telnet-password',
                               self.config.get_vlc_password(), '--telnet-host', self.config.get_vlc_host(),
                               '--telnet-port', str(self.config.get_vlc_port())]
            self.vlc_gui_proc = subprocess.Popen(vlc_command)
        # TODO: set active window to VLC

    def process_video(self, clip_length, time_units, output_file, advanced_args, terminal):
        if self.capture_info is not None:
            disc_location = self.capture_info['filepath']
            if util.get_os() != 'win':
                # while Windows gives a drive letter, Unix only gives us 'disk2' or something
                disc_location = '/dev/' + disc_location  # TODO: make work with virtual discs on Unix
            title_num = str(self.capture_info['title'])
            start_time = time_units.lower() + ':' + str(self.capture_info['time'])  # seconds:123 or frames:123
            stop_time = time_units.lower() + ':' + str((self.capture_info['time'] + int(clip_length)))
            audio_track = self.capture_info['audio_track']
            sub_track = self.capture_info['sub_track']

            handbrake_command = [self.config.get_handbrake_path(), '--input', disc_location, '--title', title_num,
                                 '--start-at', start_time, '--stop-at', stop_time, '--output', output_file, '--verbose']
            if audio_track > 0:
                handbrake_command.append('--audio')
                handbrake_command.append(str(audio_track))
            if sub_track > 0:
                handbrake_command.append('--subtitle')
                handbrake_command.append(str(sub_track))
            handbrake_command += advanced_args.strip().split(' ')  # add all the advanced args onto the end
            print('INFO:Running HandBrake command: ' + str(handbrake_command))

            if (self.handbrake_proc is not None) and (self.handbrake_proc.poll() is None):
                util.throw_alert(level='error', message='HandBrake already running.')
            else:
                self.handbrake_proc = terminal.run_command(handbrake_command)
        else:
            util.throw_alert(level='error', message='No video information found.')

    # ---MainGUI handlers---

    def handle_main__vlc_button(self):
        self.open_vlc_gui()
        time.sleep(1)  # wait for VLC to finish opening before we try and telnet into it
        self.connect_telnet()

    def handle_main__browse_button(self, entry_field, filetype):
        if filetype == 'MP4 file':
            path = filedialog.asksaveasfilename(title='Set capture file', initialfile='Clip', defaultextension='.mp4',
                                                filetypes=[('MP4 file', '*.mp4')])
        else:  # filetype == 'MKV file'
            path = filedialog.asksaveasfilename(title='Set capture file', initialfile='Clip', defaultextension='.mkv',
                                                filetypes=[('MKV file', '*.mkv')])

        if (path is not None) and (len(path) != 0):
            entry_field.delete(0, tk.END)
            entry_field.insert(0, path)

    def handle_main__capture_button(self, length, time_units, output_file, advanced_args, terminal):
        # TODO: handle things other than DVDs
        if (self.vlc_gui_proc is not None) and (self.vlc_gui_proc.poll() is None):
            if self.vlc_telnet is not None:
                if (output_file is not None) and(len(output_file) != 0):
                    audio_track = -1  # -1 if a stream has no audio. 0 if no audio selected then 1+ for each audio track
                    # find the audio track with a * in the name, indicating it's the active track
                    audio_info = [index for index, s in enumerate(self.vlc_telnet.run_command('atrack')) if '*' in s]
                    if len(audio_info) != 0:
                        # first element in audio_info is just a label, so we need to ignore it
                        audio_track = audio_info[0] - 1
                    # now repeat the above for subtitle tracks
                    sub_track = -1
                    sub_info = [index for index, s in enumerate(self.vlc_telnet.run_command('strack')) if '*' in s]
                    if len(sub_info) != 0:
                        sub_track = sub_info[0] - 1
                    self.capture_info = {
                        'title': self.vlc_telnet.run_command('title')[0],
                        'time': self.vlc_telnet.get_time(),
                        'title_length': self.vlc_telnet.get_length(),
                        'audio_track': audio_track,
                        'sub_track': sub_track,
                        'filepath': self.vlc_telnet.info()['data']['filename']
                    }
                    print('INFO: Capture Info = ' + str(self.capture_info))
                    if self.vlc_telnet.status()['state'] != 'paused':
                        self.vlc_telnet.pause()  # pause the video so the encode can happen. Doing both at once is slow
                    self.process_video(clip_length=length, time_units=time_units, output_file=output_file,
                                       advanced_args=advanced_args, terminal=terminal)
                else:
                    util.throw_alert(level='error', message='No output file specified.')
            else:
                print('INFO: VLC still loading...')
                time.sleep(1)
                self.handle_main__capture_button(length, time_units, output_file, advanced_args, terminal)
        else:
            util.throw_alert(level='error', message='VLC not open!')

    # ---SettingsGUI handlers---

    def handle_settings__vlc_browse_button(self, entry_field):
        if util.get_os() == 'win':
            path = filedialog.askopenfilename(title='Select VLC executable', initialdir='C:/Program Files/',
                                              filetypes=[('EXE file', '*.exe')])
        elif util.get_os() == 'mac':
            # TODO: selecting '.app' files is currently broken on macOS, so this selector can't be any more specific
            path = filedialog.askopenfilename(title='Select VLC application', initialdir='/Applications/')
        else:
            path = filedialog.askopenfilename(title='Select VLC executable', initialdir='/usr/bin/')
        if (path is not None) and (len(path) != 0):
            entry_field.delete(0, tk.END)
            entry_field.insert(0, path)

    def handle_settings__handbrake_browse_button(self, entry_field):
        if util.get_os() == 'win':
            path = filedialog.askopenfilename(title='Select HandbrakeCLI executable', initialdir='C:/Program Files/',
                                              filetypes=[('EXE file', '*.exe')])
        elif util.get_os() == 'mac':
            path = filedialog.askopenfilename(title='Select HandBrakeCLI program', initialdir='/usr/local/bin/',
                                              filetypes=[('UNIX program', '*')])
        else:
            path = filedialog.askopenfilename(title='Select HandBrakeCLI executable', initialdir='/usr/bin/')
        if (path is not None) and (len(path) != 0):
            entry_field.delete(0, tk.END)
            entry_field.insert(0, path)

    def handle_settings__locate_button(self, vlc_field, handbrake_field):
        # TODO: currently broken, do not use
        vlc_loc = util.locate_program('vlc')
        vlc_field.delete(0, tk.END)
        if vlc_loc is not None:
            vlc_field.insert(0, vlc_loc)
        handbrake_loc = util.locate_program('handbrakecli')
        handbrake_field.delete(0, tk.END)
        if handbrake_loc is not None:
            handbrake_field.insert(0, handbrake_loc)

    def handle_settings__save_button(self, vlc_field, handbrake_field):
        if vlc_field is not None:
            self.config.set_vlc_path(vlc_field)
        if handbrake_field is not None:
            self.config.set_handbrake_path(handbrake_field)
        self.config.save_prefs()
