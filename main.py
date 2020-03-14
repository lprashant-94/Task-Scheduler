from task_scheduler import Task, SchedulerService
import time

class PrintingTask(Task):
    def __init__(self, msg):
        self.msg=msg
    
    def run(self):
        print("Task started msg=%s" % self.msg)
        time.sleep(2)
        print("Task completed msg=%s" % self.msg)
    
    def __str__(self):
        return self.msg

scheduler = SchedulerService(1)
scheduler.schedule(PrintingTask("hello"), 2)
scheduler.schedule(PrintingTask("How are you"), 2)
scheduler.stop_scheduler()