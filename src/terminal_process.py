import subprocess
import threading


class TerminalProcess:

    def __init__(self, args, queue, root, on_exit=None):
        # subprocess actually spawns a new thread, so there are actually 3 threads (GUI, process, listener) running
        self.process = subprocess.Popen(args, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.queue = queue
        self.root = root
        self.on_exit = on_exit
        self.listen_thread = threading.Thread(target=self.listen).start()

    def listen(self):
        # for as long as the process is running, read in the values from stdout, and add them to the terminal's queue in
        # the main thread. Once the process is done, send over the callback function if there is one
        while True:
            output = self.process.stdout.readline()
            if output:
                self.queue.put(('stdout', output))
            elif self.process.poll() is not None:
                if self.on_exit is not None:
                    self.queue.put(('callback', self.on_exit))
                    break


