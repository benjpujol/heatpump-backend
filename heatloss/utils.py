import math


# function to calculate the roof area
def calculate_roof_area(roof_shape, roof_type,  roof_perimeter, roof_flat_area, roof_height=2.5):
    print("calculate roof area")
    if (roof_type == "lost-attic" or roof_shape == "flat-roof"):
        return roof_flat_area
    elif roof_shape == "gable-roof":
        return gable_roof_area(roof_flat_area, roof_perimeter, 0.5, roof_height)
    elif roof_shape == "hip-roof":
        return hip_roof_area(roof_flat_area, roof_perimeter, 0.5,  roof_height)
    return roof_flat_area



# function to calculate the wall area
def calculate_wall_area(number_of_storeys,  roof_perimeter, storey_height=2.8):
    print("calculate wall area")
    return number_of_storeys * storey_height * roof_perimeter





def hip_roof_area(flat_roof_area, roof_perimeter, roof_overhang=0.5, roof_height=2.5):
    print("calculate hip roof area")
    ratio_length_to_width=1.66
   
    return 1.2*flat_roof_area



def gable_roof_area(flat_roof_area, roof_perimeter, roof_overhang, roof_height):
    print("calculate gable roof area")
  
    return 1.1*flat_roof_area


def get_default_insulation_roof(year_built=1975):
    if year_built <= 1974:
        return 2.5
    elif (year_built >= 1975) and  (year_built <= 1977):
        return 0.5
    elif (year_built >= 1978) and  (year_built <= 1982):
        return 0.5
    elif (year_built >= 1983) and  (year_built <= 1988):
        return 0.3
    elif (year_built >= 1989) and  (year_built <= 2000):
        return 0.25
    elif (year_built >= 2001) and  (year_built <= 2005):
        return 0.23
    elif (year_built >= 2006) and  (year_built <= 2012):
        return 0.2
    elif (year_built >= 2013) and  (year_built <= 2005):
        return 0.14
    

def get_default_insulation_wall(year_built=1975):
    if year_built <= 1974:
        return 2.5
    elif (year_built >= 1975) and  (year_built <= 1977):
        return 1
    elif (year_built >= 1978) and  (year_built <= 1982):
        return 1 
    elif (year_built >= 1983) and  (year_built <= 1988):
        return 0.8
    elif (year_built >= 1989) and  (year_built <= 2000):
        return 0.5
    elif (year_built >= 2001) and  (year_built <= 2005):
        return 0.4
    elif (year_built >= 2006) and  (year_built <= 2012):
        return 0.36
    elif (year_built >= 2013) and  (year_built <= 2005):
        return 0.23

    
def get_default_insulation_floor(year_built=1975, floor_type="cellar"):
    if year_built <= 1974:
        return 2
    elif (year_built >= 1975) and  (year_built <= 1977):
        return 0.9
    elif (year_built >= 1978) and  (year_built <= 1982):
        return 0.9
    elif (year_built >= 1983) and  (year_built <= 1988):
        return 0.8
    elif (year_built >= 1989) and  (year_built <= 2000):
        return 0.5
    elif (year_built >= 2001) and  (year_built <= 2005):
        return 0.3
    elif (year_built >= 2006) and  (year_built <= 2012):
        return 0.27
    elif (year_built >= 2013) and  (year_built <= 2005):
        return 0.23