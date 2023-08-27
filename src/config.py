import configparser
import os

import util


class Config:
    def __init__(self, filepath):
        print(os.getcwd())
        self.config_path = filepath
        self.defaults_path = util.get_real_filepath('conf/defaults_' + util.get_os() + '.ini')
        self.parser = configparser.ConfigParser()
        self.load_prefs()

    def load_defaults(self, full_default):
        # if full_default is false, only override the front end (state)
        if full_default:
            self.parser.read(self.defaults_path)
        else:
            defaults_parser = configparser.ConfigParser()
            defaults_parser.read(self.defaults_path)
            for k in self.parser['state']:
                self.parser.set('state', k, defaults_parser.get('state', k))
        self.save_prefs()

    def load_prefs(self):
        # first try and load the existing settings file
        if os.path.isfile(self.config_path):
            self.parser.read(self.config_path)
        else:
            # couldn't find/open prefs, load from defaults
            print('INFO: loading default settings')
            self.load_defaults(True)

    def save_prefs(self):
        with open(self.config_path, 'w') as f:
            self.parser.write(f)
            print('INFO: config saved')

    def get_vlc_path(self):
        return self.parser.get('executables', 'vlc_path')

    def set_vlc_path(self, path):
        self.parser.set('executables', 'vlc_path', path)

    def get_handbrake_path(self):
        return self.parser.get('executables', 'handbrake_path')

    def set_handbrake_path(self, path):
        self.parser.set('executables', 'handbrake_path', path)

    def get_vlc_host(self):
        return self.parser.get('telnet', 'vlc_host')

    def set_vlc_host(self, host):
        self.parser.set('telnet', 'vlc_host', host)

    def get_vlc_port(self):
        return self.parser.getint('telnet', 'vlc_port')

    def set_vlc_port(self, port):
        self.parser.set('telnet', 'vlc_port', str(port))

    def get_vlc_password(self):
        return self.parser.get('telnet', 'vlc_password')

    def set_vlc_password(self, password):
        self.parser.set('telnet', 'vlc_password', password)

    def get_capture_length(self):
        return self.parser.getint('state', 'capture_length')

    def set_capture_length(self, length):
        self.parser.set('state', 'capture_length', str(length))

    def get_time_units(self):
        return self.parser.get('state', 'time_units')

    def set_time_units(self, units):
        self.parser.set('state', 'time_units', units)

    def get_output_filetype(self):
        return self.parser.get('state', 'output_filetype')

    def set_output_filetype(self, filetype):
        self.parser.set('state', 'output_filetype', filetype)

    def get_advanced_visible(self):
        return self.parser.getboolean('state', 'advanced_visible')

    def set_advanced_visible(self, is_visible):
        self.parser.set('state', 'advanced_visible', str(is_visible))

    def get_advanced_options(self):
        return self.parser.get('state', 'advanced_options')

    def set_advanced_options(self, opts):
        self.parser.set('state', 'advanced_options', opts)
