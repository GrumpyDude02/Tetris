import pygame
from copy import deepcopy
import Globals as gp
from Tools.functions import mod
from Block import block
from pygame.math import Vector2 as v


class Tetrominos:
    is_set = "is_set"
    falling = "falling"
    hard_dropped = "hard_drop"
    locking = "locking"
    flashing = "flashing"
    destroy = "destroy"
    is_held = "is_held"
    preview = "preview"

    lock_delay = 500
    lock_start_time = 0
    animation_start = 0
    flashing_animation_time = 50
    last_key = None
    down_pressed = False

    def __init__(self, pivot_pos: pygame.Vector2, shape: str, block_width, block_spacing: int = 1, state="falling") -> None:
        self.state = Tetrominos.falling if state == "falling" else Tetrominos.preview
        self.pivot = pivot_pos
        self.shape = shape
        self.color = gp.SHAPES[self.shape][1]
        self.rotation_index = 0
        self.blocks = [
            block((pos + self.pivot), block_width, self.color, self, block_spacing) for pos in gp.SHAPES[self.shape][0]
        ]
        self.center = self.blocks[0]
        self.acc = 0
        self.collision_direction = [None, None]
        self.HUpdate = 0
        self.VUpdate = 0
        self.key_held_time = 0
        self.offset_list = None
        self.animate = False
        self.max_row = gp.SPAWN_LOCATION[1]
        if self.shape != "I" and self.shape != "O":
            self.offset_list = gp.OFFSETS_JLZST
        elif self.shape == "I":
            self.offset_list = gp.OFFSETS_I

    # (True -> hard-dropped | False -> going down, cell numbers to bottom, rotation_index)
    def handle_events(self, current_time, events: list[pygame.Event], placed_blocks: list[list], dt: float, sounds) -> tuple:
        if self.animate:
            return
        Tetrominos.down_pressed = False
        keys = pygame.key.get_pressed()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    sounds.play("rotate")
                    return (None, None, self.SRS_rotate(True, 1, placed_blocks, current_time))
                elif event.key == pygame.K_z:
                    sounds.play("rotate")
                    return (None, None, self.SRS_rotate(False, 1, placed_blocks, current_time))
                elif event.key == pygame.K_a:
                    sounds.play("rotate")
                    return (None, None, self.SRS_rotate(True, 2, placed_blocks, current_time))
                elif event.key == pygame.K_SPACE and not Tetrominos.down_pressed:
                    self.start_animation(current_time)
                    sounds.play("harddrop")
                    return (True, self.hard_drop(placed_blocks), None)

        self.key_held_time += dt * 1000
        if keys[pygame.K_RIGHT]:
            self.handle_hmov(current_time, sounds, "right", placed_blocks)
        if keys[pygame.K_LEFT]:
            self.handle_hmov(current_time, sounds, "left", placed_blocks)

        if not (keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]):
            Tetrominos.last_key = None
            self.key_held_time = 0

        if keys[pygame.K_DOWN] and current_time - self.VUpdate > gp.MOVE_DELAY and self.state != Tetrominos.locking:
            Tetrominos.down_pressed = True
            self.VUpdate = current_time
            return (False, self.move("down", current_time, placed_blocks), None)
        return None

    def handle_hmov(self, current_time, sounds, direction, placed_blocks):
        if Tetrominos.last_key is None:
            Tetrominos.last_key = 1
            sounds.play("hit")
            self.move(direction, current_time, placed_blocks)
        elif current_time - self.HUpdate > gp.MOVE_DELAY and self.key_held_time > 250:
            self.HUpdate = current_time
            sounds.play("hit")
            self.move(direction, current_time, placed_blocks)

    def update_animation(self, current_time, placed_blocks, sound):
        if self.state == Tetrominos.locking:
            self.color = (min(self.color[0] + 15, 255), min(self.color[1] + 15, 255), min(self.color[2] + 15, 255))
            self.set_color(self.color)
            if current_time - Tetrominos.lock_start_time > Tetrominos.lock_delay:
                self.state = Tetrominos.is_set
                sound.play("locking")

        elif self.state == Tetrominos.hard_dropped:
            self.set_color()
            if current_time - Tetrominos.animation_start > Tetrominos.flashing_animation_time:
                self.state = Tetrominos.is_set

        if self.state == Tetrominos.is_set:
            self.animate = False
            self.reset_color()
            self.set_blocks(placed_blocks)

    def update(self, level, dt, current_time, placed_blocks, sound):
        if max(self.blocks, key=lambda x: x.map_pos[1]) == 25:
            self.increment_score = False
        self.update_animation(current_time, placed_blocks, sound)
        self.acc += gp.LEVEL_SPEED[level] * dt * gp.GAME_SPEED
        if not self.blocks:
            self.state = Tetrominos.destroy
        if self.state == Tetrominos.is_set:
            return
        if self.acc > 1:
            self.acc = 0
            self.move("down", current_time, placed_blocks)

    def smooth_fall(self, level, dt, placed_blocks: list[list[block]] = None):
        movement = v(0, gp.LEVEL_SPEED[level - 1] * dt * gp.GAME_SPEED)
        if placed_blocks:
            if not self.collide(movement, placed_blocks):
                for block in self.blocks:
                    block.map_pos += movement
                self.pivot += movement
        else:
            for block in self.blocks:
                block.map_pos += movement
            self.pivot += movement

    def move(self, direction: pygame.Vector2, current_time, placed_blocks: list[list]) -> int:
        self.collision_direction = [direction, True]
        direction_vec = gp.MOVES[direction]

        if not self.collide(direction_vec, placed_blocks):
            self.collision_direction = [direction, False]

            if self.state == Tetrominos.locking:
                self.rest_lock_timer(current_time)

            for block in self.blocks:
                block.move(direction_vec)
            self.pivot += direction_vec
            a = min(self.blocks, key=lambda x: x.map_pos[1]).map_pos[1]
            if direction_vec == gp.MOVES["down"] and a > self.max_row:
                self.max_row = a
                return 1

        elif (
            direction_vec == gp.MOVES["down"]
            and not Tetrominos.down_pressed
            and self.state is not Tetrominos.hard_dropped
            and self.state is not Tetrominos.locking
        ):
            Tetrominos.lock_start_time = current_time
            self.state = Tetrominos.locking
            self.max_row = self.blocks[0].map_pos[1]
        return 0

    def hard_drop(self, placed_blocks: list[list]) -> int:
        translate = self.project(placed_blocks)
        for block in self.blocks:
            block.map_pos[1] = block.map_pos[1] + translate
            placed_blocks[int(block.map_pos[1])][int(block.map_pos[0])] = block
        self.state = Tetrominos.hard_dropped
        return translate

    def project(self, placed_blocks) -> int:
        translate = 0
        while translate < gp.BOARD_Y_CELL_NUMBER:
            if any(
                int(block.map_pos[1]) + translate >= gp.BOARD_Y_CELL_NUMBER
                or placed_blocks[int(block.map_pos[1]) + translate][int(block.map_pos[0])]
                for block in self.blocks
            ):
                break
            translate += 1
        return translate - 1

    def collide(self, dir: pygame.Vector2, placed_blocks) -> bool:
        for block in self.blocks:
            if block.collide(block.map_pos + dir, placed_blocks):
                return True
        return False

    def draw(self, window: pygame.Surface, shadow_surf: pygame.Surface = None, placed_blocks: list[list] = None) -> None:
        if self.state is Tetrominos.falling:
            for block in self.blocks:
                block.draw_highlight(window)
            pygame.draw.circle(
                window, (255, 255, 255), self.center.sc_pos + v(self.center.width / 2, self.center.width / 2), 2
            )
            if shadow_surf is not None:
                shadow = deepcopy(self)
                translate = self.project(placed_blocks)

                for block in shadow.blocks:
                    block.map_pos[1] += translate
                    block.draw(shadow_surf)
        else:
            for block in self.blocks:
                block.draw(window)

    # classic rotation but with wall kicks(boundaries only)
    def rotate(self, clockwise: bool, placed_blocks, current_time=0) -> None:
        if self.shape == "O":
            return
        old = deepcopy(self.blocks)
        rot = (1, 0) if clockwise else (-1, 0)
        for block in self.blocks:
            temp = block.map_pos - self.pivot
            block.map_pos[0] = round(temp[0] * rot[0] - temp[1] * rot[1] + self.pivot[0])
            block.map_pos[1] = round((temp[1]) * rot[0] + temp[0] * rot[1] + self.pivot[1])
        self.rotation_index = mod(self.rotation_index, 4)
        outside_right_block = max(self.blocks, key=lambda x: x.map_pos[0])
        outside_left_block = min(self.blocks, key=lambda x: x.map_pos[0])
        outside_y_axis = max(self.blocks, key=lambda x: x.map_pos[1])
        if outside_right_block.map_pos[0] >= gp.PLAYABLE_AREA_CELLS:
            shift_l = outside_right_block.map_pos[0] - gp.PLAYABLE_AREA_CELLS + 1
            self.pivot[0] -= shift_l
            for block in self.blocks:
                block.map_pos[0] -= shift_l
        elif outside_left_block.map_pos[0] < 0:
            shift_r = -(outside_left_block.map_pos[0])
            self.pivot[0] += shift_r
            for block in self.blocks:
                block.map_pos[0] += shift_r
        elif outside_y_axis.map_pos[1] >= gp.BOARD_Y_CELL_NUMBER:
            shift_y = outside_y_axis.map_pos[1] - gp.BOARD_Y_CELL_NUMBER + 1
            self.pivot[1] -= shift_y
            for block in self.blocks:
                block.map_pos[1] -= shift_y
        for block in self.blocks:
            if block.overlap(block.map_pos, placed_blocks):
                self.blocks = old
                return

    # Super Rotation System
    def SRS_rotate(self, clockwise: bool, turns, placed_blocks: list[list[block]] = None, current_time: float = 0) -> int:
        if self.shape == "O" or not placed_blocks or self.state not in (Tetrominos.falling, Tetrominos.locking):
            return 0
        old_blocks = deepcopy(self.blocks)
        old_r_index = self.rotation_index
        self.rotation_index = mod(self.rotation_index + turns, 4) if clockwise else mod(self.rotation_index - turns, 4)
        rot = 1 if clockwise else -1
        for i in range(0, turns):
            for block in self.blocks:
                temp = block.map_pos - self.pivot
                block.map_pos[0] = -temp[1] * rot + self.pivot[0]
                block.map_pos[1] = temp[0] * rot + self.pivot[1]
        for i in range(0, 5):
            offset = self.offset_list[old_r_index][i] - self.offset_list[self.rotation_index][i]
            if not self.collide(offset, placed_blocks):
                self.pivot += offset
                if self.state is Tetrominos.locking:
                    self.rest_lock_timer(current_time)
                for block in self.blocks:
                    block.move(offset)
                return i
        self.blocks = old_blocks
        self.rotation_index = old_r_index
        self.center = self.blocks[0]
        return 0

    def set_pos(self, new_pos: pygame.Vector2) -> None:
        for block in self.blocks:
            block.map_pos -= self.pivot
            block.map_pos += new_pos
        self.pivot = new_pos
        self.max_row = new_pos[1]

    def set_blocks(self, placed_blocks):
        self.state = Tetrominos.is_set
        for block in self.blocks:
            placed_blocks[int(block.map_pos[1])][int(block.map_pos[0])] = block
            block.sc_pos = v((block.map_pos[0] + 1) * block.width, (block.map_pos[1] - gp.Y_BORDER_OFFSET - 1) * block.width)

    def set_shape(
        self, new_shape: str, boundary_size: tuple = None, center_horizontal: bool = True, center_vert: bool = True
    ) -> None:
        if boundary_size is not None:
            self.center_tetromino(new_shape, (0, 0), boundary_size, center_horizontal, center_vert)

        block_size = self.blocks[0].width
        self.blocks = [block(pos + self.pivot, block_size, gp.SHAPES[new_shape][1], self) for pos in gp.SHAPES[new_shape][0]]
        # TODO: change color

    def resize(self, block_size: int = None):
        for block in self.blocks:
            block.resize(block_size)

    def get_dim(self):
        if self.rotation_index % 2 == 0:
            return gp.SHAPES_DIM[self.shape]
        return (gp.SHAPES_DIM[self.shape][1], gp.SHAPES_DIM[self.shape][0])

    def center_tetromino(self, shape, boundary_pos, boundary_size, center_horizontal: bool = True, center_vert: bool = True):
        self.shape = shape
        dim = self.get_dim()
        l = [self.pivot[0], self.pivot[1]]
        if center_horizontal:
            l[0] = boundary_pos[0] + (boundary_size[0] - dim[0] - gp.MIN_SHAPES_BLOCK_POS[shape][0]) / 2
        if center_vert:
            l[1] = boundary_pos[1] + (boundary_size[1] - dim[1] - gp.MIN_SHAPES_BLOCK_POS[shape][1]) / 2
        self.pivot = tuple(l)

    def set_color(self, color: tuple = (255, 255, 255)):
        for block in self.blocks:
            block.color = color

    def reset_color(self):
        self.color = gp.SHAPES[self.shape][1]
        self.set_color(self.color)

    def start_animation(self, start_time):
        self.animate = True
        Tetrominos.animation_start = start_time

    def rest_lock_timer(self, current_time):
        self.reset_color()
        self.state = Tetrominos.falling
        Tetrominos.lock_start_time = current_time
