class Particle:
    def __init__(
        self,
        pos: list,
        speed: list,
        duration: float,
        size: int,
        start_time,
        acc: list = [0, 200],
        color: list = [255, 255, 255],
    ) -> None:
        self.pos = pos
        self.speed = speed
        self.duration = duration
        self.acc = acc
        self.size = size
        self.start_time = start_time
        self.color = color
        self.done = False

    def update(self, dt, size_decrease, curr_time=None):
        self.speed[0] += self.acc[0] * dt
        self.speed[1] += self.acc[1] * dt
        self.pos[0] += self.speed[0] * dt
        self.pos[1] += self.speed[1] * dt
        self.size -= size_decrease * dt
        if (curr_time is not None and curr_time - self.start_time > self.duration) or self.size < 0:
            self.done = True
