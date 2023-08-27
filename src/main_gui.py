import tkinter as tk
from tkinter import ttk

import backend
import settings_gui
import terminal
from __version__ import __version__

FRAME_PAD_X = 10
FRAME_PAD_Y = 5


class MainGUI:

    def __init__(self):
        self.backend = backend.Backend()

        self.root = tk.Tk()
        self.root.protocol('WM_DELETE_WINDOW', self.close)
        self.root.title('VLClipper v' + __version__)
        self.advanced_visible = tk.IntVar(value=self.backend.config.get_advanced_visible())
        self.terminal = terminal.Terminal(self.root)
        # ---Start Top Row Section---
        self.top_frame = ttk.Frame(self.root)
        self.top_frame.grid(row=0, column=0, padx=FRAME_PAD_X, pady=FRAME_PAD_Y)
        self.top_vlc_button = ttk.Button(self.top_frame, command=self.backend.handle_main__vlc_button, text='Open VLC')
        self.top_vlc_button.grid(row=0, column=0)
        self.top_settings_button = ttk.Button(self.top_frame, command=self.open_settings, text='Settings')
        self.top_settings_button.grid(row=0, column=1)
        self.top_defaults_button = ttk.Button(self.top_frame, command=self.load_defaults, text='Load Defaults')
        self.top_defaults_button.grid(row=0, column=2)
        # ---End Top Row Section---
        # ---Start Timing Section---
        self.timing_frame = ttk.Frame(self.root)
        self.timing_frame.grid(row=1, column=0, padx=FRAME_PAD_X, pady=FRAME_PAD_Y)
        ttk.Label(self.timing_frame, text='Timing').grid(row=0, column=0, columnspan=3, padx=5, pady=5)
        ttk.Label(self.timing_frame, text='Capture').grid(row=1, column=0)
        self.timing_length_field = ttk.Spinbox(self.timing_frame, from_=0)
        self.timing_length_field.grid(row=1, column=1)
        self.timing_units_combobox = ttk.Combobox(self.timing_frame, state='readonly')
        self.timing_units_combobox['values'] = ('Seconds', 'Frames')
        self.timing_units_combobox.grid(row=1, column=2)
        # ---End Timing Section---
        # ---Start Output Section---
        self.output_frame = ttk.Frame(self.root)
        self.output_frame.grid(row=2, column=0, padx=FRAME_PAD_X, pady=FRAME_PAD_Y)
        ttk.Label(self.output_frame, text='Output File').grid(row=0, column=0, columnspan=3, padx=5, pady=5)
        self.output_type_combobox = ttk.Combobox(self.output_frame, state='readonly')
        self.output_type_combobox['values'] = ('MP4 file', 'MKV file')
        self.output_path_field = ttk.Entry(self.output_frame)
        self.output_path_field.grid(row=1, column=1)
        self.output_browse_button = ttk.Button(self.output_frame, command=lambda: self.backend.handle_main__browse_button(self.output_path_field, self.output_type_combobox.get()), text='Browse')
        self.output_browse_button.grid(row=1, column=2)
        # ---End Output Section---
        # ---Start Toggle Section---
        self.toggle_hidden = ttk.Checkbutton(self.root, variable=self.advanced_visible, onvalue=True,
                                             command=self.update_hidden, text='Show More...')
        self.toggle_hidden.grid(row=3, column=0, padx=FRAME_PAD_X, pady=FRAME_PAD_Y)
        # ---End Toggle Section---
        # ---Start Advanced Section---
        self.advanced_frame = ttk.Frame(self.root)
        ttk.Label(self.advanced_frame, text='Advanced HandBrake Parameters').grid(row=0, column=0, padx=5, pady=5)
        self.advanced_handbrake_field = tk.Text(self.advanced_frame, width=60, wrap=tk.CHAR, height=10)
        self.advanced_handbrake_field.grid(row=1, column=0)
        self.update_hidden()
        # ---End Advanced Section---
        # ---Start Terminal Section---
        self.terminal.grid(row=5, column=0, padx=FRAME_PAD_X, pady=FRAME_PAD_Y)
        # ---End Terminal Section---
        # ---Start Capture Section---
        self.capture_button = ttk.Button(self.root, command=lambda: self.backend.handle_main__capture_button(
            length=self.timing_length_field.get(), time_units=self.timing_units_combobox.get(),
            output_file=self.output_path_field.get(), advanced_args=self.advanced_handbrake_field.get('1.0', tk.END),
            terminal=self.terminal), text='Capture')
        self.capture_button.grid(row=6, column=0, padx=FRAME_PAD_X, pady=FRAME_PAD_Y)
        # ---End Capture Section---

        self.fill_fields()
        self.root.mainloop()

    def open_settings(self):
        settings_gui.SettingsGUI(backend=self.backend)

    def load_defaults(self):
        self.backend.config.load_defaults(False)
        self.fill_fields()

    def update_hidden(self):
        if self.advanced_visible.get():
            self.advanced_frame.grid(row=4, column=0, padx=FRAME_PAD_X, pady=FRAME_PAD_Y)
        else:
            self.advanced_frame.grid_remove()

    def fill_fields(self):  # read in the values for each field from the preferences
        self.timing_length_field.delete(0, tk.END)
        self.timing_length_field.insert(0, self.backend.config.get_capture_length())

        if self.backend.config.get_time_units() == 'seconds':
            self.timing_units_combobox.current(0)
        else:
            self.timing_units_combobox.current(1)

        if self.backend.config.get_output_filetype() == 'mp4':
            self.output_type_combobox.current(0)
        else:
            self.output_type_combobox.current(1)

        self.advanced_handbrake_field.delete('1.0', tk.END)
        self.advanced_handbrake_field.insert('1.0', self.backend.config.get_advanced_options())

    def save_fields(self):  # save current user config
        self.backend.config.set_capture_length(self.timing_length_field.get())

        self.backend.config.set_time_units(self.timing_units_combobox.get().lower())

        if self.output_type_combobox.get() == 'MP4 file':
            self.backend.config.set_output_filetype('mp4')
        else:
            self.backend.config.set_output_filetype('mkv')

        self.backend.config.set_advanced_visible(self.advanced_visible.get())

        self.backend.config.set_advanced_options(self.advanced_handbrake_field.get('1.0', tk.END))

        self.backend.config.save_prefs()

    def close(self):
        # TODO: make sure all child processes are dead
        self.save_fields()
        self.root.destroy()
        self.root.quit()