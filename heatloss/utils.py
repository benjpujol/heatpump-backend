
# function to calculate the roof area
def calculate_roof_area(roof_shape, roof_type,  roof_perimeter, roof_flat_area, roof_height=4):
    print("calculate roof area")
    print(roof_shape)
    if roof_shape == "flat-roof":

        return  roof_flat_area
    elif roof_shape == "gable-roof":
        print("gable roof")
        print(roof_perimeter)
        print(roof_height)
        print(roof_perimeter*roof_height/2)
        return roof_perimeter * roof_height / 2
    elif roof_shape == "hip-roof":
        return roof_perimeter * roof_height / 2 + roof_flat_area
    return roof_flat_area


# function to calculate the wall area
def calculate_wall_area(number_of_storeys,  roof_perimeter, storey_height=2.8):
    print("calculate wall area")
    return number_of_storeys * storey_height * roof_perimeter
