import tkinter as tk

from screeninfo import get_monitors

from ..animation import Animation, AnimationStates, Animator
from ..window_utils import Canvas
from src import logger


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
            logger.debug("frame repeating")
            self.animator.frame_number += 1
        else:
            logger.debug("getting next state")
            self.animator.frame_number = 0
            self.set_animation_state(animation.next(self.animator))

        logger.debug(f"{self.animator.state.__repr__()}, {self.animator.frame_number}")

    def set_geometry(self):
        
        """Update the window position and scale to match that of the pet instance's location and size"""
        #size = self.animator.animations[self.animator.state].target_resolution
        monitor = get_monitors()[0]
        '''When at a resolution above 2560
            
            The window can be found by using the line of best fit from trial and error of 3264 and 3840'''
        
        #print("Width: " + str(monitor.width))
        if monitor.width > 2954:
            s = int(-0.046875*monitor.width+313)
        else:
            s = 200
        print("s: " + str(s))
        # match monitor.width:
        #     case 3840: #
        #         s=133
        #     case 3264: #
        #         s=160
        #     case 2954:
        #         s = 200 #WTF
        #     case _:
        #         s=200

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
