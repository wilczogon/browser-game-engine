class Schedule:
    def __init__(self, task_id, start_in, args=[], interval=None):
        self.task_id = task_id
        self.start_in = start_in
        self.args = args
        self.interval = interval


class TaskDefinition:
    def __init__(self, id, func):
        self.id = id
        self.func = func
