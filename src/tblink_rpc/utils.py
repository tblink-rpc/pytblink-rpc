'''
Created on Dec 28, 2021

@author: mballance
'''

def scale_time(time, time_units, target_units):
    if time_units == target_units:
        return time
    else:
        unscaled = time
        
        if target_units > time_units:
            # Desired units are coarser than target
            unscaled *= (10 ** (target_units-time_units))
        else:
            # Desired units are finter than default
            unscaled /= (10 ** (time_units-target_units))
        
        return int(unscaled)
        