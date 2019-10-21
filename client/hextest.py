import subprocess
import threading
import time
import queue

q = queue.Queue(0)

# exec process for st.
proc = subprocess.Popen(["st"], stdout=subprocess.PIPE)

# have a thread that grabs latest stdout from st. pushes that onto queue.
def GrabStdinAndPushQ(q, proc):
    # Need to add timer to retry.
    while True:
        print ("This was called")
        insts = GrabNextBlock(proc)
        if not insts:
            return
        
        q.put(inst)

        time.sleep(.300)

def GrabNextBlock(s):
    for line in iter(proc.stdout.readline, ''):
        print (line)
    return line

# have a thread that grabs from top of queue, and pushes it to server.
def PostFromQ(q):
    # Need to add timer to retry.
    while True:
        while not q.empty():
            post(q.get())

        time.sleep(.300)

def post(s):
    print (bytearray.fromhex(s).decode())

pushthread = threading.Thread(target = GrabStdinAndPushQ, args = (q, proc,))
postthread = threading.Thread(target = PostFromQ, args = (q,))

pushthread.start()
postthread.start()
