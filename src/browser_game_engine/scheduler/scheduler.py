from browser_game_engine import EngineModule
from threading import Timer


class Scheduler(EngineModule):
    def __init__(self, task_definitions, schedules):
        self.task_definitions = task_definitions
        self.schedules = schedules

    def set_engine(self, engine):
        EngineModule.set_engine(self, engine)

        for schedule in self.schedules:
            self.schedule(
                schedule.task_id,
                schedule.start_in,
                schedule.args,
                schedule.interval
            )

    def schedule(self, task_id, start_in, args=[], interval=None):
        task = list(filter(lambda x: x.id == task_id, self.task_definitions))[0].func
        if interval is None:
            Timer(start_in, task, args=args).start()
        else:
            def periodical():
                def task_wrapper(*args):
                    self.engine.push_context()
                    try:
                        task(*args)
                    except Exception as e:
                        print("Error occured in task {}:".format(task_id), e)

                    Timer(interval, task_wrapper, args=args).start()

                Timer(interval, task_wrapper, args=args).start()
            Timer(start_in, periodical).start()

# class SchedulerAction(Thread):
#     def __init__(self, task_func, start, args=[], interval=None):
#         self.task_func = task_func
#         self.start = start
#         self.args = args
#         self.interval = interval
#
#     def start(self):