#!/usr/bin/env python3


import time
import asyncio
import cozmo
from cozmo.util import degrees, Pose
from cozmo.objects import CustomObject, CustomObjectMarkers, CustomObjectTypes

def custom_objects(robot: cozmo.robot.Robot):
    wall_obj0 = robot.world.define_custom_wall(CustomObjectTypes.CustomType00,
                                              CustomObjectMarkers.Circles2,
                                              121, 140,
                                              51, 51, False)

    wall_obj1 = robot.world.define_custom_wall(CustomObjectTypes.CustomType01,
                                              CustomObjectMarkers.Triangles2,
                                              121, 140,
                                              51, 51, False)

    wall_obj2 = robot.world.define_custom_wall(CustomObjectTypes.CustomType02,
                                              CustomObjectMarkers.Diamonds2,
                                              121, 140,
                                              51, 51, False)

    wall_obj3 = robot.world.define_custom_wall(CustomObjectTypes.CustomType03,
                                              CustomObjectMarkers.Diamonds5,
                                              121, 265,
                                              51, 51, False)

    wall_obj4 = robot.world.define_custom_wall(CustomObjectTypes.CustomType04,
                                              CustomObjectMarkers.Triangles4,
                                              121, 265,
                                              51, 51, False)

    wall_obj5 = robot.world.define_custom_wall(CustomObjectTypes.CustomType05,
                                              CustomObjectMarkers.Hexagons4,
                                              121, 265,
                                              51, 51, False)

    wall_obj6 = robot.world.define_custom_wall(CustomObjectTypes.CustomType06,
                                              CustomObjectMarkers.Circles4,
                                              159, 400,
                                              51, 51, False)

    wall_obj7 = robot.world.define_custom_wall(CustomObjectTypes.CustomType07,
                                              CustomObjectMarkers.Hexagons3,
                                              159, 400,
                                              51, 51, False)

    wall_obj8 = robot.world.define_custom_wall(CustomObjectTypes.CustomType08,
                                              CustomObjectMarkers.Diamonds4,
                                              159, 400,
                                              51, 51, False)

def cozmo_program(robot: cozmo.robot.Robot):
#    cube = None
    fixed_object = custom_objects(robot)
    time.sleep(60)
    look_around = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)

    # try to find a block
    xpose = 500
    cube = None
    while not cube: 
        try:
            cube = robot.world.wait_for_observed_light_cube(timeout=30)
            print("Found it", cube)

        except asyncio.TimeoutError:
            print("Didn't find it")
            look_around.stop()
            robot.go_to_pose(Pose(xpose, 0, 0, angle_z=degrees(0)), relative_to_robot=False).wait_for_completed()
            look_around = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
            xpose = 1000


    print("Yay")
    look_around.stop()

    cube.set_lights(cozmo.lights.green_light.flash())

    anim = robot.play_anim_trigger(cozmo.anim.Triggers.BlockReact)
    anim.wait_for_completed()


    action = robot.pickup_object(cube)
    print("got action", action)
    result = action.wait_for_completed(timeout=30)
    print("got action result", result)

    robot.turn_in_place(degrees(90)).wait_for_completed()

    action = robot.place_object_on_ground_here(cube)
    print("got action", action)
    result = action.wait_for_completed(timeout=30)
    print("got action result", result)

    anim = robot.play_anim_trigger(cozmo.anim.Triggers.MajorWin)
    cube.set_light_corners(None, None, None, None)
    anim.wait_for_completed()

cozmo.run_program(cozmo_program, use_3d_viewer=True, use_viewer=True)
