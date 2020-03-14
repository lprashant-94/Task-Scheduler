from queue import PriorityQueue, Queue
from threading import Thread, currentThread
import time
import logging
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)

class Task:
    def run(self):
        pass

@dataclass(order=True)
class TaskWithTime:
    time: float
    task: Any=field(compare=False)

    def __init__(self, task, delay):
        self.task = task
        self.time = int(time.time()) + delay

class SchedulerService:
    def __init__(self, size):
        self.queue = PriorityQueue()
        self.ready_to_run=PriorityQueue()
        self.stop = False
        self.threads = []
        for i in range(size):
            t = Thread(name="Scheduler Thread #%d" % i, target=self.thread_function)
            self.threads.append(t)
            t.start()
        l = Thread(name="Looper", target=self.update_ready_to_run)
        l.start()

    def update_ready_to_run(self):
        while not self.stop:
            logger.debug("Looper: queue = %s" % self.queue)
            try:
                t = self.queue.get(block=True, timeout=0.2)
                if t.time <= int(time.time()):
                    self.ready_to_run.put(t)
                    logger.debug("Adding new t=%s to ready to run at %s : %d" % (t.task, time.time(), t.time))
                else:
                    self.queue.put(t)
                    time.sleep(0.1)
            except:
                pass

    def stop_scheduler(self):
        self.queue.join()
        self.ready_to_run.join()
        self.stop = True

    def thread_function(self):
        while not self.stop:
            try:
                task = self.ready_to_run.get(block=True, timeout=1)
                logger.debug("Thread: name%s time=%s msg=%s" % (currentThread().name, task.time, task.task ))
                task.task.run()
            except:
                time.sleep(0.1)

    def schedule(self, task, delay):
        self.queue.put(TaskWithTime(task, delay))