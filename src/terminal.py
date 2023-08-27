import queue
import tkinter as tk
from tkinter import ttk

import util
import terminal_process


class Terminal:
    NUM_HISTORY_LINES = 100  # TODO: actually use this and remove old lines
    REFRESH_RATE = 100  # milliseconds between updates. Lower numbers can make the GUI lag

    def __init__(self, enclosing_frame, title='Terminal', width=60, height=20):
        self.terminal_frame = ttk.Frame(enclosing_frame)
        ttk.Label(self.terminal_frame, text=title).grid(row=1, column=0, padx=0, pady=5)
        self.terminal_text = tk.Text(self.terminal_frame, width=width, wrap=tk.CHAR, height=height)
        self.terminal_text.bind('<Key>', lambda e: 'break')  # prevent typing in the terminal
        self.terminal_text.grid(row=2, column=0)
        self.root = enclosing_frame
        self.message_queue = queue.Queue()
        self.root.after(self.REFRESH_RATE, self.process_queue)

    def grid(self, *args, **kwargs):
        # passthrough to the GUI part
        self.terminal_frame.grid(*args, **kwargs)

    def output(self, line):
        if line:
            print('TERM: ' + line.strip())
            self.terminal_text.insert(tk.END, '\n' + line.strip())
            self.terminal_text.see(tk.END)  # scroll to the newly inserted line

    def process_queue(self):
        # Tkinter doesn't like being multithreaded, so instead, each process that has its own thread just throws their
        # output onto a single queue, which is printed onto the screen every hundred milliseconds or so
        while self.message_queue.qsize() > 0:
            item = self.message_queue.get_nowait()
            # this is a tuple of either 'stdout' and a message for the terminal, or 'callback' and a callback function,
            # used for when a process finishes
            if item[0] == 'stdout':
                self.output(item[1])
            elif item[0] == 'callback':
                item[1]()
        self.root.after(self.REFRESH_RATE, self.process_queue)  # check the queue again in a set amount of time

    def run_command(self, args):
        tp = terminal_process.TerminalProcess(args, self.message_queue, self.root, lambda: util.throw_alert(message='Encode Completed.'))
        return tp.process
