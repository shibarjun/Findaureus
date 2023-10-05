import numpy as np
import matplotlib.pyplot as plt
import pickle
import math

def FindBacOverlap (actual_fake_bac_coord_list, processed_fake_bac_coord_dict):
    '''
    Not so relevant right now

    Parameters
    ----------
    actual_fake_bac_coord_list : TYPE
        DESCRIPTION.
    processed_fake_bac_coord_dict : TYPE
        DESCRIPTION.

    Returns
    -------
    actual_FakeBacImageCoor : TYPE
        DESCRIPTION.
    processed_FakeBacImageCoor : TYPE
        DESCRIPTION.
    ObtainedBactCoord : TYPE
        DESCRIPTION.
    ActualBactCoord : TYPE
        DESCRIPTION.

    '''
    
    processed_fake_bac_coord_list = list(processed_fake_bac_coord_dict.values())
    actual_FakeBacImageCoor = []
    processed_FakeBacImageCoor  = []
    
    for aBacCount in range(0,len(actual_fake_bac_coord_list)):
        for aInBacCount in range (0, len(actual_fake_bac_coord_list[aBacCount])):
            actual_FakeBacImageCoor.append(actual_fake_bac_coord_list[aBacCount][aInBacCount])
            
    for pBacCount in range(0,len(processed_fake_bac_coord_list)):
        for pInBacCount in range (0, len(processed_fake_bac_coord_list[pBacCount])):
            processed_FakeBacImageCoor.append(processed_fake_bac_coord_list[pBacCount][pInBacCount])
        
    ObtainedBactCoord = []
    for count_a in range(0,len(processed_FakeBacImageCoor)):
        x_valcoor, y_valcoor = processed_FakeBacImageCoor[count_a]
        for count_b in range(0,len(actual_FakeBacImageCoor)):
            x_baccoor, y_baccoor = actual_FakeBacImageCoor[count_b]
            if x_valcoor in range((x_baccoor-5), (x_baccoor+5),1) and y_valcoor in range((y_baccoor-5),(y_baccoor+5) ,1):
                ObtainedBactCoord.append(1)
            else:
                continue
                
    for cnt in range(0,(len(actual_FakeBacImageCoor)-len(ObtainedBactCoord))):
        ObtainedBactCoord.append(0)
    
    ActualBactCoord = np.ones(len(actual_FakeBacImageCoor))
    return (actual_FakeBacImageCoor,processed_FakeBacImageCoor, ObtainedBactCoord, ActualBactCoord)


def update_predicted_coordinates(predicted_coordinates, actual_coordinates, range_threshold=7):
    updated_predicted = []

    for pred_x, pred_y in predicted_coordinates:
        is_actual = False
        updated_coord = (pred_x, pred_y)

        for actual_x, actual_y in actual_coordinates:
            if abs(pred_x - actual_x) <= range_threshold and abs(pred_y - actual_y) <= range_threshold:
                is_actual = True
                updated_coord = (actual_x, actual_y)
                break

        updated_predicted.append(updated_coord)

    return updated_predicted

def UpdatePredictedCoordinatesList(predicted_coordinates_dict, actual_bacteria_coordinates_list):
    
    updated_predicted_list = []
    
    for zplane_no in range(0, len(actual_bacteria_coordinates_list)):
        
        predicted_coordinates = predicted_coordinates_dict["xy_Z_"+str(zplane_no)]
        # background_coordinates = background_coordinates_list[zplane_no]
        actual_bacteria_coordinates = actual_bacteria_coordinates_list[zplane_no]
        updated_predicted = update_predicted_coordinates(predicted_coordinates, actual_bacteria_coordinates)
        updated_predicted_list.append(updated_predicted)
        
    return(updated_predicted_list)