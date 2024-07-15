from itertools import repeat
import pathlib
import os
from typing import Tuple, Dict
from .animation_states import AnimationStates
from .animation import Animation


def get_animations(
    pet_name: str, target_resolution: Tuple[int, int], should_run_preprocessing: bool
) -> Dict[AnimationStates, Animation]:
    """Loads all of the animations for a pet and their source files into a dictionary
    Args:
        pet_name (str): name of the pet, ie the name of folder its animations are in
        target_resolution (Tuple[int, int]): target size of the animations
    Returns:
        Dict[AnimationStates, Animation]
    """
    # Load the animation gifs from the sprite folder and make each of the gifs into a list of frames
    # Path to sprites we want to use
    impath = pathlib.Path().resolve()
    impath = os.path.join(impath, "src", "sprites")
    Animation.should_run_preprocessing = should_run_preprocessing
    # **** This can be whatever set of animations you want it to be
    # **** I just like horses so I have set it to that
    if pet_name == "Loki":
        animations = get_cat_animations(impath, target_resolution)
    elif pet_name == "Hershey":
        animations = get_horse_animations(impath, target_resolution)
    elif pet_name == "Jerry":
        animations = get_blob_animations(impath, target_resolution)


    return animations


def get_cat_animations(impath: str, target_resolution: Tuple[int, int]):
    """Loads all of the animations for a horse
    Args:
        impath (str): path to the folder the animations are in
        target_resolution (Tuple[int, int]): target size of the animations
    Returns:
        Dict[AnimationStates, Animation]
    """
    pj = os.path.join
    impath = pj(impath, "cat")
    standing_actions = [AnimationStates.IDLE_TO_SLEEP]
    standing_actions.extend(repeat(AnimationStates.IDLE, 3))
    standing_actions.extend(repeat(AnimationStates.WALK_NEGATIVE, 4))
    standing_actions.extend(repeat(AnimationStates.WALK_POSITIVE, 4))

    # These are the animations that our spite can do.
    # ! IMPORTANT:
    # ! NOTE: in order to have the pet fall after being grabbed, there must be key value pair in the animations dict for
    # ! AnimationStates.FALLING, and then for the falling animation to end there must be an animation for AnimationStates.LANDED.
    # ! See the example in src.animations.get_cat_animations where although not having gif files for falling and landing animations
    # ! other animations are repurposed for these animation states.
    animations: Dict[AnimationStates, Animation] = {
        ######### IDLE
        AnimationStates.IDLE: Animation(
            standing_actions,
            gif_location=pj(impath, "catidle.gif"),
            frame_timer=400,
            target_resolution=target_resolution,
        ),
        ######### SLEEP
        AnimationStates.IDLE_TO_SLEEP: Animation(
            [AnimationStates.SLEEP],
            gif_location=pj(impath, "catidletosleep.gif"),
            target_resolution=target_resolution,
        ),
        AnimationStates.SLEEP: Animation(
            [
                AnimationStates.SLEEP,
                AnimationStates.SLEEP,
                AnimationStates.SLEEP,
                AnimationStates.SLEEP,
                AnimationStates.SLEEP_TO_IDLE,
            ],
            gif_location=pj(impath, "catsleeping.gif"),
            frame_timer=1000,
            target_resolution=target_resolution,
        ),
        AnimationStates.SLEEP_TO_IDLE: Animation(
            [AnimationStates.IDLE],
            gif_location=pj(impath, "catsleeptoidle.gif"),
            target_resolution=target_resolution,
        ),
        ######### WALKING
        AnimationStates.WALK_POSITIVE: Animation(
            standing_actions,
            gif_location=pj(impath, "catwalkingright.gif"),
            v_x=3,
            target_resolution=target_resolution,
        ),
        AnimationStates.WALK_NEGATIVE: Animation(
            standing_actions,
            gif_location=pj(impath, "catwalkingleft.gif"),
            v_x=-3,
            target_resolution=target_resolution,
        ),
        ########### MOUSE INTERACTIONS
        AnimationStates.GRABBED: Animation(
            [AnimationStates.GRABBED],
            gif_location=pj(impath, "catgrabbed.gif"),
            frame_timer=50,
            target_resolution=target_resolution,
        ),
        AnimationStates.GRAB_TO_FALL: Animation(
            [AnimationStates.FALLING],
            gif_location=pj(impath, "catgrabtofall.gif"),
            target_resolution=target_resolution,
        ),
        AnimationStates.FALLING: Animation(
            [AnimationStates.FALLING],
            gif_location=pj(impath, "catfalling.gif"),
            frame_timer=50,
            frame_multiplier=2,
            target_resolution=target_resolution,
            a_y=2,
        ),
        AnimationStates.LANDED: Animation(
            [AnimationStates.IDLE],
            gif_location=pj(impath, "catfallingtoidle.gif"),
            frame_timer=100,
            target_resolution=target_resolution,
        ),
    }

    return animations

def get_horse_animations(impath: str, target_resolution: Tuple[int, int]):
    """Loads all of the animations for a horse
    Args:
        impath (str): path to the folder the animations are in
        target_resolution (Tuple[int, int]): target size of the animations
    Returns:
        Dict[AnimationStates, Animation]
    """
    pj = os.path.join
    impath = pj(impath, "horse", "Horse")
    standing_actions = [AnimationStates.IDLE_TO_SLEEP, AnimationStates.GRAZING_START]
    standing_actions.extend(repeat(AnimationStates.IDLE, 3))
    standing_actions.extend(repeat(AnimationStates.WALK_NEGATIVE, 5))
    standing_actions.extend(repeat(AnimationStates.WALK_POSITIVE, 5))

    # These are the animations that our spite can do.
    # ! IMPORTANT:
    # ! NOTE: in order to have the pet fall after being grabbed, there must be key value pair in the animations dict for
    # ! AnimationStates.FALLING, and then for the falling animation to end there must be an animation for AnimationStates.LANDED.
    # ! See the example in src.animations.get_cat_animations where although not having gif files for falling and landing animations
    # ! other animations are repurposed for these animation states.
    animations: Dict[AnimationStates, Animation] = {
        ######### IDLE
        AnimationStates.IDLE: Animation(
            standing_actions,
            images_location=pj(impath, "Idle", "Right"),
            target_resolution=target_resolution,
            repititions=3,
        ),
        ######### SLEEP
        AnimationStates.IDLE_TO_SLEEP: Animation(
            [AnimationStates.SLEEP],
            images_location=pj(impath, "Sleep", "IdleToSleep"),
            target_resolution=target_resolution,
        ),
        AnimationStates.SLEEP: Animation(
            [
                AnimationStates.SLEEP,
                AnimationStates.SLEEP,
                AnimationStates.SLEEP,
                AnimationStates.SLEEP,
                AnimationStates.SLEEP_TO_IDLE,
            ],
            images_location=pj(impath, "Sleep", "Sleeping"),
            frame_timer=1000,
            repititions=2,
            target_resolution=target_resolution,
        ),
        AnimationStates.SLEEP_TO_IDLE: Animation(
            [AnimationStates.IDLE],
            images_location=pj(impath, "Sleep", "IdleToSleep"),
            target_resolution=target_resolution,
            reverse=True,
        ),
        ######### WALKING
        AnimationStates.WALK_POSITIVE: Animation(
            standing_actions,
            images_location=pj(impath, "Walking", "Right"),
            v_x=3,
            repititions=7,
            target_resolution=target_resolution,
        ),
        AnimationStates.WALK_NEGATIVE: Animation(
            standing_actions,
            images_location=pj(impath, "Walking", "Left"),
            v_x=-3,
            repititions=7,
            target_resolution=target_resolution,
        ),
        ########## GRAZING
        AnimationStates.GRAZING_START: Animation(
            [AnimationStates.GRAZING],
            images_location=pj(impath, "Grazing", "Transition"),
            target_resolution=target_resolution,
        ),
        AnimationStates.GRAZING_END: Animation(
            standing_actions,
            images_location=pj(impath, "Grazing", "Transition"),
            target_resolution=target_resolution,
            reverse=True,
        ),
        AnimationStates.GRAZING: Animation(
            [AnimationStates.GRAZING, AnimationStates.GRAZING_END],
            images_location=pj(impath, "Grazing", "Active"),
            repititions=1,
            frame_timer=200,
            target_resolution=target_resolution,
        ),
        ########### MOUSE INTERACTIONS
        AnimationStates.GRABBED: Animation(
            [AnimationStates.GRABBED],
            images_location=pj(impath, "MouseInteractions", "Grabbed"),
            frame_timer=50,
            target_resolution=target_resolution,
        ),
        AnimationStates.GRAB_TO_FALL: Animation(
            [AnimationStates.FALLING],
            images_location=pj(impath, "MouseInteractions", "GrabToFall"),
            target_resolution=target_resolution,
        ),
        AnimationStates.FALLING: Animation(
            [AnimationStates.FALLING],
            images_location=pj(impath, "MouseInteractions", "Falling"),
            frame_timer=50,
            frame_multiplier=2,
            a_y=1,
            target_resolution=target_resolution,
        ),
        AnimationStates.LANDED: Animation(
            [AnimationStates.IDLE],
            images_location=pj(impath, "MouseInteractions", "Landed"),
            frame_timer=100,
            target_resolution=target_resolution,
        ),
    }
    return animations

def get_blob_animations(impath: str, target_resolution: Tuple[int, int]):
    """Loads all of the animations for a horse
    Args:
        impath (str): path to the folder the animations are in
        target_resolution (Tuple[int, int]): target size of the animations
    Returns:
        Dict[AnimationStates, Animation]
    """
    pj = os.path.join
    impath = pj(impath, "blob")
    standing_actions = [AnimationStates.IDLE_TO_SLEEP]
    standing_actions.extend(repeat(AnimationStates.IDLE, 3))
    standing_actions.extend(repeat(AnimationStates.WALK_NEGATIVE, 4))
    standing_actions.extend(repeat(AnimationStates.WALK_POSITIVE, 4))

    # These are the animations that our spite can do.
    # ! IMPORTANT:
    # ! NOTE: in order to have the pet fall after being grabbed, there must be key value pair in the animations dict for
    # ! AnimationStates.FALLING, and then for the falling animation to end there must be an animation for AnimationStates.LANDED.
    # ! See the example in src.animations.get_cat_animations where although not having gif files for falling and landing animations
    # ! other animations are repurposed for these animation states.
    animations: Dict[AnimationStates, Animation] = {
        ######### IDLE
        AnimationStates.IDLE: Animation(
            standing_actions,
            gif_location=pj(impath, "slimeidle.gif"),
            frame_timer=400,
            target_resolution=target_resolution,
        ),
        ######### SLEEP
        AnimationStates.IDLE_TO_SLEEP: Animation(
            [AnimationStates.SLEEP],
            gif_location=pj(impath, "slimeidletosleep.gif"),
            target_resolution=target_resolution,
        ),
        AnimationStates.SLEEP: Animation(
            [
                AnimationStates.SLEEP,
                AnimationStates.SLEEP,
                AnimationStates.SLEEP,
                AnimationStates.SLEEP,
                AnimationStates.SLEEP_TO_IDLE,
            ],
            gif_location=pj(impath, "slimesleep.gif"),
            frame_timer=1000,
            target_resolution=target_resolution,
        ),
        AnimationStates.SLEEP_TO_IDLE: Animation(
            [AnimationStates.IDLE],
            gif_location=pj(impath, "slimesleeptoidle.gif"),
            target_resolution=target_resolution,
        ),
        ######### WALKING
        AnimationStates.WALK_POSITIVE: Animation(
            standing_actions,
            gif_location=pj(impath, "slimemoveright.gif"),
            v_x=3,
            target_resolution=target_resolution,
        ),
        AnimationStates.WALK_NEGATIVE: Animation(
            standing_actions,
            gif_location=pj(impath, "slimemoveleft.gif"),
            v_x=-3,
            target_resolution=target_resolution,
        ),
        ########### MOUSE INTERACTIONS
        AnimationStates.GRABBED: Animation(
            [AnimationStates.GRABBED],
            gif_location=pj(impath, "slimegrabbed.gif"),
            frame_timer=50,
            target_resolution=target_resolution,
        ),
        AnimationStates.GRAB_TO_FALL: Animation(
            [AnimationStates.FALLING],
            gif_location=pj(impath, "slimegrabbedtofall.gif"),
            target_resolution=target_resolution,
        ),
        AnimationStates.FALLING: Animation(
            [AnimationStates.FALLING],
            gif_location=pj(impath, "slimefalling.gif"),
            frame_timer=50,
            frame_multiplier=2,
            target_resolution=target_resolution,
            a_y=2,
        ),
        AnimationStates.LANDED: Animation(
            [AnimationStates.IDLE],
            gif_location=pj(impath, "slimelanding.gif"),
            frame_timer=100,
            target_resolution=target_resolution,
        ),
    }

    return animations





