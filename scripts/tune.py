"""
This script runs through the tuning processed described in the ODrive documentation:
https://docs.odriverobotics.com/control
"""

import odrive
from odrive.enums import *
from odrive.utils import start_liveplotter
import time

def startup():
    """
    Connects to the ODrive and returns the odrv object.
    Also prompts user to select which axis to tune. Returns it too.         Logan Daniel lmd328
    """
    pass
        
    drive0 = odrive.find_any()    #Starts odrive
    
    selected_axis = int(input("Select Axis 0/1: "))     #User prompt to select axis 0 or 1
    
    if selected_axis == 0:      #Based on user input, selects axis 0 or 1
        axis = drive0.axis0
    elif selected_axis == 1:
        axis = drive0.axis1

    return drive0, axis

def yesnoquery(message):
    """
    Displays `message` and waits for user Y/N input.
    Returns Boolean where true means Y.
    """
    useryn = None

    while useryn is None:

        if not isinstance(message, str):
            raise ValueError("Must pass a valid string to query")
                
        useryn = input(message).lower()
            
        if useryn != "y" and useryn != "n":
            print("Must enter either a 'Y' or 'N'", useryn)
            useryn = None

    if useryn == "y":
        return True
    elif useryn == "n":
        return False
    else:
        return -1

def initialize(odrv, axis):
    #Jonathan Windham
    """
    Calibrate ODrive.
    Reset ODrive gains to initial values. Namely, set vel_integrator_gain to 0.
    Sets to closed loop position control mode.
    Also launches the liveplotter.
    """

    axis.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE

    while (axis.current_state != AXIS_STATE_IDLE):
        time.sleep(0.1)

    axis.controller.config.vel_gain = 10.0/10000.0 #5.0/10000.0
    axis.controller.config.vel_integrator_gain = 0
    axis.controller.config.pos_gain = 20

    axis.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

    axis.controller.config.control_mode = CTRL_MODE_POSITION_CONTROL

    axis.controller.config.vel_limit = 8192.0 * 10

    start_liveplotter(lambda: 
    [ axis.encoder.pos_estimate,
    axis.controller.pos_setpoint
    ])



    pass #code here
    return None

def test(odrv, axis):  #Andrew Byers is trying to work on it :)
    """
    Runs a test function through the ODrive.
    50% duty cycle square wave with a 2-second period and 0,2*pi radian amplitude.
    Runs for 30 seconds.
    NOTE: must convert from radians to encoder counts!
    """
    for i in range(3):
        axis.controller.pos_setpoint = axis.encoder.config.cpr 
        time.sleep(1)
        axis.controller.pos_setpoint = 0
        time.sleep(1)

    return None

def change_all_gains(odrv, axis, pct=0.5):
    """
    Change all odrive gains by pct factor.
    Mia lives here
    """
    axis_config = axis.controller.config # shorten that

    axis_config.pos_gain = axis_config.pos_gain * pct
    axis_config.vel_gain = axis_config.vel_gain * pct
    axis_config.vel_integrator_gain = axis_config.vel_integrator_gain * pct

    return None

def update_vel_gain(odrv, axis, pct=1, bias=0): #andrew Byers
    """
    Updates vel_gain by multiplying by pct and adding bias.
    """

    #Isaac's Function
    pass #code here
    axis.controller.config.vel_gain *= pct
    axis.controller.config.vel_gain += bias
    return None

def update_pos_gain(odrv, axis, pct=1, bias=0):
    """
    Updates pos_gain by multiplying by pct and adding bias.   Logan Daniel lmd328
    """
    pass #code here
    axis.controller.config.pos_gain = axis.controller.config.pos_gain * pct + bias
    return None

def update_vel_integrator_gain(odrv, axis, pct=1, bias=0): #Andrew Byers is doing this
    """
    Updates vel_integrator_gain by multiplying by pct and adding bias.
    """

    axis.controller.config.vel_integrator_gain = axis.controller.config.vel_integrator_gain * pct + bias
    
    return None

def set_vel_integrator_gain(odrv, axis): #Logan and Andrew got this
    """
    Sets vel_integrator_gain based on following equation:
    vel_integrator_gain = 0.5*B*vel_gain
    B is the system bandwidth and is the inverse of the settle time:
    B = 1/t_settle
    Settle time is the time for the system to settle to a position command.
    Must query the user for system settle time.
    Non-numeric/empty responses should rerun the test function.
    """

    while(True):

        test(odrv, axis)
        try:
            t_settle = float(input("Enter system settle time: ")) 
        except:
            print("Nothing entered/invalid character")
        else:
            B = 1/t_settle
            axis.controller.config.vel_integrator_gain = 0.5 * B * axis.controller.config.vel_gain
            break

    
    

    return None

def print_gains(odrv, axis):
    """
    Prints gains. Also returns them.
    """
    axis_config = axis.controller.config  # shorten that
    print("Position:", axis_config.pos_gain )
    print("Velocity:", axis_config.vel_gain)
    print("Velocity Integrator:", axis_config.vel_integrator_gain)
    return axis_config.pos_gain, axis_config.vel_gain, axis_config.vel_integrator_gain

def manual_tweaks(odrv, axis):
    """
    Interactive prompt to change the three gains.
    mia also lives here
    """
    axis_config = axis.controller.config  # shorten that

    while True:  # is there a better way to do this? yes.
        print("1: position 2: velocity 3: velocity integrator")
        while True:
            mod_gain = str(input("Pick which gain to modify: "))
            if mod_gain != str("1") and mod_gain != str("2") and mod_gain != str("3"):
                print("Invalid input")
            else:
                break
        if mod_gain == str("1"):
            gain = "position"
        elif mod_gain == str("2"):
            gain = "velocity"
        else:
            gain = "velocity integrator"
        print("Modifying", gain, "gain")

        ans = yesnoquery("Continue? (Y/N)")

        if ans:
            break
        else:
            continue
    pct = input("Input pct factor")
    bias = input("Input bias")

    if mod_gain == str("1"):
        old_gain = axis_config.pos_gain
        axis_config.pos_gain = axis_config.pos_gain * pct + bias
        new_gain = axis_config.pos_gain
    elif mod_gain == str("2"):
        old_gain = axis_config.vel_gain
        axis_config.vel_gain = axis_config.vel_gain * pct + bias
        new_gain = axis_config.vel_gain
    else:
        old_gain = axis_config.vel_integrator_gain
        axis_config.vel_integrator_gain = axis_config.vel_integrator_gain * pct + bias
        new_gain = axis_config.vel_integrator_gain

    print("Old gain: ", old_gain, "New gain: ", new_gain)
    return None

if __name__ == "__main__":
    odrv, axis = startup()
    if not yesnoquery("Tune axis? (Y/N): "):
        exit()
    initialize(odrv, axis)
    test(odrv, axis)
    while not yesnoquery("Stable? (Y/N): "):
        change_all_gains(odrv, axis, pct=0.5)
        test(odrv, axis)
    while not yesnoquery("Vibrates? (Y/N): "):
        update_vel_gain(odrv, axis, pct=1.3, bias=0)
        test(odrv, axis)
    update_vel_gain(odrv, axis, pct=0.5, bias=0)
    while not yesnoquery("Overshoot? (Y/N): "):
        update_pos_gain(odrv, axis, pct=1.3, bias=0)
        test(odrv, axis)
    while yesnoquery("Still Overshoot? (Y/N): "):
        update_pos_gain(odrv, axis, pct=0.95, bias=0)
        test(odrv, axis)
    while not yesnoquery("Settle Time set? (Y/N): "):
        set_vel_integrator_gain(odrv, axis)
        print_gains(odrv, axis)
        test(odrv, axis)
    while yesnoquery("Manual Tweaking? (Y/N): "):
        manual_tweaks(odrv, axis)
        test(odrv,axis)
        print_gains(odrv, axis)
    exit()
