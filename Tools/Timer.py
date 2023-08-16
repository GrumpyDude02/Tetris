import time


class Timer:
    def __init__(self) -> None:
        self.starting_time = 0
        self.last_update_time = 0
        self.time = 0
        self.dt = 0
        self.last_tick = 0
        self.running = False

    def current_time(self) -> float:
        return time.time()

    def update_dt(self):
        curr_time = time.time()
        self.dt = curr_time - self.last_update_time
        self.last_update_time = curr_time

    def delta_time(self) -> float:
        return self.dt

    def start_timer(self) -> float:
        self.running = True
        self.starting_time = time.time() * 1000

    def pause_timer(self):
        self.last_tick = self.time
        self.running = False

    def update_timer(self) -> float:
        if self.running:
            self.time = self.last_tick + time.time() * 1000 - self.starting_time
        return self.time

    def reset(self):
        self.time = self.last_tick = self.last_tick = self.last_update_time = 0
        self.running = False
