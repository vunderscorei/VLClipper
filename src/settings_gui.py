import tkinter as tk
import webbrowser
from tkinter import ttk


class SettingsGUI:

    def __init__(self, backend):
        self.backend = backend

        self.root = tk.Toplevel()
        self.root.grab_set()
        self.root.title('VLClipper Settings')
        # ---Start Top Text Section---
        ttk.Label(self.root, text='Configure VLC and HandBrakeCLI executable paths').grid(row=0, column=0, columnspan=3)
        # ---End Top Text Section---
        # ---Start VLC Section---
        ttk.Label(self.root, text='VLC').grid(row=1, column=0)
        self.vlc_field = ttk.Entry(self.root)
        self.vlc_field.insert(0, self.backend.config.get_vlc_path())
        self.vlc_field.grid(row=1, column=1)
        self.vlc_browse_button = ttk.Button(self.root, command=lambda: self.backend.handle_settings__vlc_browse_button(self.vlc_field), text='Browse')
        self.vlc_browse_button.grid(row=1, column=2)
        # ---End VLC Section---
        # ---Start HandBrake Section---
        ttk.Label(self.root, text='HandBrakeCLI').grid(row=2, column=0)
        self.handbrake_field = ttk.Entry(self.root)
        self.handbrake_field.insert(0, self.backend.config.get_handbrake_path())
        self.handbrake_field.grid(row=2, column=1)
        self.handbrake_browse_button = ttk.Button(self.root, command=lambda: self.backend.handle_settings__handbrake_browse_button(self.handbrake_field), text='Browse')
        self.handbrake_browse_button.grid(row=2, column=2)
        ttk.Label(self.root, text='Note: HandBrakeCLI and regular HandBrake are not the same!').grid(row=3, column=0,
                                                                                                     columnspan=3)
        # ---End HandBrake Section---
        # ---Start Bottom Section---
        # self.bottom_locate_button = ttk.Button(self.root, command=lambda: self.backend.handle_settings__locate_button(self.vlc_field, self.handbrake_field), text='Attempt to auto-locate')
        # self.bottom_locate_button.grid(row=4, column=0, columnspan=3)
        self.bottom_exit_button = ttk.Button(self.root, command=self.close, text='Exit')
        self.bottom_exit_button.grid(row=5, column=0)
        self.bottom_dev_link = tk.Label(self.root, text='Powered by vi', fg='blue', cursor='hand')
        self.bottom_dev_link.bind('<Button-1>', lambda e: webbrowser.open_new_tab('https://v-i.dev'))
        self.bottom_dev_link.grid(row=5, column=1)
        self.bottom_save_button = ttk.Button(self.root, command=self.save, text='Save')
        self.bottom_save_button.grid(row=5, column=2)
        # ---End Bottom Section---

        self.root.mainloop()

    def close(self):
        self.root.grab_release()
        self.root.destroy()
        self.root.quit()

    def save(self):
        self.backend.handle_settings__save_button(self.vlc_field.get(), self.handbrake_field.get())
        self.close()