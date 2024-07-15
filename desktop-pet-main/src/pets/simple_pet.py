import tkinter as tk
from screeninfo import get_monitors
from ..animation import Animation, AnimationStates, Animator
from ..window_utils import Canvas
import ctypes

class SimplePet:
    x: int
    y: int

    canvas: Canvas
    animator: Animator

    def __init__(self, x, y, canvas, animator):
        self.x = x
        self.y = y
        self.canvas = canvas
        self.animator = animator

    def update(self):
        """progress to next frame of animation"""
        self.progress_animation()

    def get_current_animation(self) -> Animation:
        """Returns the current animation of the Pet instance

        Returns:
            Animation
        """
        return self.animator.animations[self.animator.state]

    def get_curent_animation_frame(self) -> tk.PhotoImage:
        """get and return the current animation

        Returns:
            tk.PhotoImage: image of animation to draw
        """
        animation = self.get_current_animation()
        return animation.frames[self.animator.frame_number]

    def set_animation_state(self, state: AnimationStates) -> bool:
        """Sets the animation state for this pet

        Args:
            state (AnimationStates): Animation state to try to set

        Returns:
            bool: Whether or not the state actually changed values
        """
        changed = self.animator.set_animation_state(state)
        if changed:
            self.reset_movement()
        return changed

    # making gif work
    def progress_animation(self):
        """Move the animation forward one frame. If the animation has finished (ie current frame is
        the last frame) then try to progress to the next animation
        """
        animation = self.get_current_animation()
        if self.animator.frame_number < len(animation.frames) - 1:
            #print("frame repeating")
            self.animator.frame_number += 1
        else:
            #print("getting next state")
            self.animator.frame_number = 0
            self.set_animation_state(animation.next(self.animator))

        #print(f"{self.animator.state.__repr__()}, {self.animator.frame_number}")

    def set_geometry(self):
        """Update the window position and scale to match that of the pet instance's location and size"""
        size = self.animator.animations[self.animator.state].target_resolution
        scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
        s = 200
        if(scale_factor > 150):
            s = int(s - (29*((scale_factor-150)/25)))
        self.canvas.window.geometry(
            str(s) + "x" + str(s) + "+" + str(self.x) + "+" + str(self.y)
        )

    def handle_event(self):
        """Part of animation loop, after delay between frames in animation
        proceed to begin logic of drawing next frame
        """
        self.canvas.window.after(
            self.animator.animations[self.animator.state].frame_timer, self.on_tick
        )
