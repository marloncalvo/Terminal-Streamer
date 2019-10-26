from threading import Event, Thread
from queue import Queue
import httplib2

def post_http(data):
    print (data)

class TaskScheduler():
    
    def __init__(self):
        self.queue  = Queue()
        self.event  = Event()
        self.worker = Worker(self.queue, self.event)
        self.worker.daemon = True
        self.worker.start()

    def queue_job(self, data):
        # Enqueue the job first, so that an empty queue is not analyzed.
        self.queue.put(data, block=False)
        self.event.set()

class Worker(Thread):
    
    def __init__(self, queue, event):
        Thread.__init__(self)
        self.queue = queue
        self.event = event 
        self.http = httplib2.Http(".cache")

    def run(self):
        self.__process_jobs()

    def __process_jobs(self):
        while True:
            """ 
            By first checking if the queue is empty, it is very unlikely that
            the data was added in the time period between clearing the last event,
            and waiting. Regardless, if set() was called after clear, an item 
            must've been added, so wait() would be ignored.
            This would only break if the put() call was fired after the check for queue.empty(),
            and the put()/set() functions are called before wait(). Very unlikely though.
            If this occurs, the next queue_job call will fix that anyway.
            """ 
            if self.queue.empty():
                self.event.wait()
            while not self.queue.empty():
                url = self.queue.get_nowait()
                self.test_fun(url)
                self.queue.task_done()
            self.event.clear()

    def test_fun(self, data):
        content = self.http.request("http://localhost:3000/new", "POST", body=data, headers={'content-type':'text/html'})[1]
        content.decode()

# Testing
def main():
    ts = TaskScheduler()
    while True:
        data = input()
        ts.queue_job(post_http, data)

if __name__ == "__main__":
    main()
