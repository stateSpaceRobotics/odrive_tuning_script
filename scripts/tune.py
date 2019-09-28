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
    """
    Calibrate ODrive.
    Reset ODrive gains to initial values. Namely, set vel_integrator_gain to 0.
    Sets to closed loop position control mode.
    Also launches the liveplotter.
    """
    pass #code here
    return None

def test(odrv, axis):  #Andrew Byers is trying to work on it :)
    """
    Runs a test function through the ODrive.
    50% duty cycle square wave with a 2-second period and 0,2*pi radian amplitude.
    Runs for 30 seconds.
    NOTE: must convert from radians to encoder counts!
    """
    for i in range 15:
        axis.controller.pos_setpoint = axis.encoder.config.cpr 
        time.sleep(1)
        axis.controller.pos_setpoint = 0
        time.sleep(1)

    return None

def change_all_gains(odrv, axis, pct=0.5):
    """
    Change all odrive gains by pct factor.
    """
    pass #code here
    return None

def update_vel_gain(odrv, axis, pct=1, bias=0):
    """
    Updates vel_gain by multiplying by pct and adding bias.
    """
    pass #code here
    return None

def update_pos_gain(odrv, axis, pct=1, bias=0):
    """
    Updates pos_gain by multiplying by pct and adding bias.   Logan Daniel lmd328
    """
    pass #code here
    odrv.axis.controller.config.pos_gain = odrv.axis.controller.config.pos_gain * pct + bias
    return None

def update_vel_integrator_gain(odrv, axis, pct=1, bias=0): #Andrew Byers is doing this
    """
    Updates vel_integrator_gain by multiplying by pct and adding bias.
    """

     odrv.axis.controller.config.vel_integrator_gain = odrv.axis.controller.config.vel_integrator_gain * pct + bias
    
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
            odrv.axis.controller.config.vel_integrator_gain = 0.5 * B * odrv.axis.controller.config.vel_gain
            break

    
    

    return None

def print_gains(odrv, axis):
    """
    Prints gains. Also returns them.
    """
    pass #code here
    return None,None,None

def manual_tweaks(odrv, axis):
    """
    Interactive prompt to change the three gains.
    """
    pass #code here
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
    set_vel_integrator_gain(odrv, axis)
    print_gains(odrv, axis)
    test(odrv, axis)
    while yesnoquery("Manual Tweaking? (Y/N): "):
        manual_tweaks(odrv, axis)
        test(odrv,axis)
        print_gains(odrv, axis)
    exit()
