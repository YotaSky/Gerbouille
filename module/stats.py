#!/usr/bin/python
#Bot Gerbouille Discord/ARK
#France-Evolved https://discord.gg/gVsveNY
#2017 By YotaSky https://github.com/YotaSky

import threading, subprocess, Queue

fn = ''
stdout.readline()

class Stats(object):
    def __init__(self, safe=False):
        self.safe = safe
        self.pid_file = ""
        
        #Rendre multi-instance

    def tail(self):
        tailq = Queue.Queue(maxsize=10) # buffer at most 100 lines

        def tail_forever(fn):
            p = subprocess.Popen(["tail", "-f", fn], stdout=subprocess.PIPE)
            while 1:
                line = p.stdout.readline()
                tailq.put(line)
                if not line:
                    break

threading.Thread(target=tail_forever, args=(fn,)).start()

print tailq.get() # blocks
print tailq.get_nowait() # throws Queue.Empty if there are no lines to read
