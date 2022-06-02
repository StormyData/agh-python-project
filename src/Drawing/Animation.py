from typing import List

from pygame import Surface
from dataclasses import dataclass

from src.Vector import Vector


@dataclass
class AnimationFrame:
    def __init__(self, img: Surface | str, length: float, offset: Vector):
        self.img = img
        self.length = length
        self.offset = offset


@dataclass
class AnimationBuffer:
    def __init__(self, frames: List[AnimationFrame]):
        self.frames = frames


class Animation:
    def __init__(self, buffer: AnimationBuffer, on_loop=None):
        self.buffer = buffer
        self.frame_no = 0
        self.timer = 0
        self.on_loop = on_loop

    def get_frame(self) -> (Surface, Vector):
        return self.buffer.frames[self.frame_no].img, self.buffer.frames[self.frame_no].offset

    def update(self, dt: float) -> None:
        self.timer += dt
        while self.timer > self.buffer.frames[self.frame_no].length:
            self.timer -= self.buffer.frames[self.frame_no].length
            self.frame_no += 1
            if self.frame_no >= len(self.buffer.frames):
                self.frame_no = 0
                if self.on_loop is not None:
                    self.on_loop()

    def reset(self):
        self.timer = 0
        self.frame_no = 0
