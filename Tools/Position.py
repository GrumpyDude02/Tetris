class Position:
    def __init__(self, x, y, width, height):
        self.normalized_x = x
        self.normalized_y = y
        self.sc_pos_x = round(self.normalized_x * width)
        self.sc_pos_y = round(self.normalized_y * height)

    def get_pos(self) -> tuple:
        return (self.sc_pos_x, self.sc_pos_y)

    def update(self, new_width, new_height) -> None:
        self.sc_pos_x = round(self.normalized_x * new_width)
        self.sc_pos_y = round(self.normalized_y * new_height)
