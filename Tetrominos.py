import pygame
from copy import deepcopy
import game_parameters as gp
from Tools.functions import mod
from block import block
from pygame.math import Vector2 as v

lock_delay = 500
shared_lock_timer = 0
down_pressed = False


class Tetrominos:
    def __init__(self, pivot_pos: pygame.Vector2, shape: str, block_width, block_spacing: int = 1) -> None:
        self.isSet = False
        self.isHeld = False
        self.destroy = False
        self.pivot = pivot_pos
        self.shape = shape
        self.color = gp.shapes[self.shape][1]
        self.rotation_index = 0
        self.blocks = [
            block((pos + self.pivot), block_width, self.color, self, block_spacing) for pos in gp.shapes[self.shape][0]
        ]
        self.center = self.blocks[0]
        self.acc = 0
        self.keys_held = [False, False]
        self.HUpdate = 0
        self.VUpdate = 0
        self.key_held_time = 0
        self.offset_list = None
        if self.shape != "I" and self.shape != "O":
            self.offset_list = gp.offsets_JLZST
        elif self.shape == "I":
            self.offset_list = gp.offsets_I

    def handle_events(self, current_time, events: list[pygame.Event], placed_blocks: list[list], dt: float) -> tuple:
        global down_pressed
        down_pressed = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN] and current_time - self.VUpdate > gp.MOVE_DELAY:
            down_pressed = True
            self.VUpdate = current_time
            return (False, self.move(gp.moves["down"], current_time, placed_blocks), None)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    return (None, None, self.SRS_rotate(True, 1, placed_blocks, current_time))
                elif event.key == pygame.K_z:
                    return (None, None, self.SRS_rotate(False, 1, placed_blocks, current_time))
                elif event.key == pygame.K_a:
                    return (None, None, self.SRS_rotate(True, 2, placed_blocks, current_time))
                elif event.key == pygame.K_SPACE and not down_pressed:
                    return (True, self.hard_drop(placed_blocks), None)
                elif event.key == pygame.K_LEFT:
                    self.keys_held[0] = True
                    self.key_held_time = 0
                    self.move(gp.moves["left"], current_time, placed_blocks)
                elif event.key == pygame.K_RIGHT:
                    self.keys_held[1] = True
                    self.key_held_time = 0
                    self.move(gp.moves["right"], current_time, placed_blocks)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.keys_held[0] = False
                    self.key_held_time = 0
                if event.key == pygame.K_RIGHT:
                    self.keys_held[1] = False
                    self.key_held_time = 0
        if self.keys_held[1]:
            self.key_held_time += dt * 1000
            if self.key_held_time > 250:
                if keys[pygame.K_RIGHT] and current_time - self.HUpdate > gp.MOVE_DELAY:
                    self.HUpdate = current_time
                    self.move(gp.moves["right"], current_time, placed_blocks)
        elif self.keys_held[0]:
            self.key_held_time += dt * 1000
            if self.key_held_time > 250:
                if keys[pygame.K_LEFT] and current_time - self.HUpdate > gp.MOVE_DELAY:
                    self.HUpdate = current_time
                    self.move(gp.moves["left"], current_time, placed_blocks)
        return None

    def update(self, level, dt, current_time, placed_blocks):
        global down_pressed
        self.acc += gp.level_speed[level] * dt * gp.game_speed
        if not self.blocks:
            self.destroy = True
        if self.isSet:
            return
        if self.acc > 1:
            self.acc = 0
            self.move(gp.moves["down"], current_time, placed_blocks)

    def smooth_fall(self, level, dt, placed_blocks: list[list[block]] = None):
        movement = v(0, gp.level_speed[level - 1] * dt * gp.game_speed)
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
        global shared_lock_timer, down_pressed
        if not self.collide(direction, placed_blocks):
            shared_lock_timer = current_time
            for block in self.blocks:
                block.move(direction)
            self.pivot += direction
            if direction == gp.moves["down"]:
                return 1
        # elif direction==moves['left'] or direction==moves['right']:
        #     successful_move=False
        elif direction == gp.moves["down"]:
            if down_pressed or current_time - shared_lock_timer > lock_delay:
                self.set_blocks(placed_blocks)
        return 0

    def hard_drop(self, placed_blocks: list[list]) -> int:
        translate = self.project(placed_blocks)
        for block in self.blocks:
            block.map_pos[1] += translate
            placed_blocks[int(block.map_pos[1])][int(block.map_pos[0])] = block
        self.isSet = True
        return translate

    def project(self, placed_blocks) -> int:
        translate = 0
        while translate < gp.boardy_cell_number:
            if any(
                int(block.map_pos[1]) + translate >= gp.boardy_cell_number
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
        for block in self.blocks:
            if block.map_pos - self.pivot == v():
                block.draw(window)
            else:
                block.draw(window)
        if shadow_surf is None:
            return
        if not self.isSet and placed_blocks:
            pygame.draw.circle(window, (255, 255, 255), self.center.sc_pos + v(self.center.width / 2, self.center.width / 2), 2)
            shadow = deepcopy(self)
            translate = self.project(placed_blocks)
            for block in shadow.blocks:
                block.map_pos[1] += translate
                block.draw(shadow_surf)

    # classic rotation but with wall kicks(boundaries only)
    def rotate(self, clockwise: bool, placed_blocks) -> None:
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
        if outside_right_block.map_pos[0] >= gp.playable_num:
            shift_l = outside_right_block.map_pos[0] - gp.playable_num + 1
            self.pivot[0] -= shift_l
            for block in self.blocks:
                block.map_pos[0] -= shift_l
        elif outside_left_block.map_pos[0] < 0:
            shift_r = -(outside_left_block.map_pos[0])
            self.pivot[0] += shift_r
            for block in self.blocks:
                block.map_pos[0] += shift_r
        elif outside_y_axis.map_pos[1] >= gp.boardy_cell_number:
            shift_y = outside_y_axis.map_pos[1] - gp.boardy_cell_number + 1
            self.pivot[1] -= shift_y
            for block in self.blocks:
                block.map_pos[1] -= shift_y
        for block in self.blocks:
            if block.overlap(block.map_pos, placed_blocks):
                self.blocks = old
                return

    # Super Rotation System
    def SRS_rotate(self, clockwise: bool, turns, placed_blocks: list[list[block]] = None, current_time: float = 0) -> int:
        global shared_lock_timer
        if self.shape == "O" or not placed_blocks:
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
                shared_lock_timer = current_time
                self.pivot += offset
                for block in self.blocks:
                    block.move(offset)
                return i
        self.blocks = old_blocks
        self.rotation_index = old_r_index
        return 0

    def set_pos(self, new_pos: pygame.Vector2) -> None:
        for block in self.blocks:
            block.map_pos -= self.pivot
            block.map_pos += new_pos
        self.pivot = new_pos

    def set_blocks(self, placed_blocks):
        self.isSet = True
        for block in self.blocks:
            placed_blocks[int(block.map_pos[1])][int(block.map_pos[0])] = block

    def set_shape(self, new_shape: str) -> None:
        block_size = self.blocks[0].width
        self.blocks = [block(pos + self.pivot, block_size, gp.shapes[new_shape][1], self) for pos in gp.shapes[new_shape][0]]

    def resize(self, block_size: int = None):
        for block in self.blocks:
            block.resize(block_size)
