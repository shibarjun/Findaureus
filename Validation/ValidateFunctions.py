import numpy as np
import re

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


def BinaryResult(one_fake_image_coordinates, one_processed_fake_image_coordinates):
    '''
    

    Parameters
    ----------
    one_fake_image_coordinates : TYPE list
        DESCRIPTION.
        list of planned bacteria coordinates in one fake image
    one_processed_fake_image_coordinates : TYPE list
        DESCRIPTION.
        list of bacteria coordinates found by the alogorithm in one fake image

    Returns
    -------
    Binary_result_list : TYPE list
        DESCRIPTION.
        if 1 cooridnates are found accurately,
        if 0 coordinates are found inaccurately

    '''

    Binary_result_list = []
    for count_p in range(0, len(one_processed_fake_image_coordinates)):
        x_p_coord, y_p_coord = one_processed_fake_image_coordinates[count_p]
        for count_f in range(0,len(one_fake_image_coordinates)):
            x_f_coord, y_f_coord = one_fake_image_coordinates[count_f]
            if x_p_coord in range((x_f_coord-5), (x_f_coord+5),1) and y_p_coord in range((y_f_coord-5),(y_f_coord+5) ,1):
                Binary_result_list.append(1)
            else:
                continue
    for cnt in range(0,abs((len(one_fake_image_coordinates)-len(one_processed_fake_image_coordinates)))):
        Binary_result_list.append(0)
    return (Binary_result_list)

def Accuracy(Binary_result_list):
    '''
    

    Parameters
    ----------
    Binary_result_list : TYPE list
        DESCRIPTION.
        based on the 1 and 0 count make the accuracy

    Returns
    -------
    accu: accuracy
    

    '''
    correct_prediction = Binary_result_list.count(1)
    total_prediction = len(Binary_result_list)
    try:
        
        Accu = correct_prediction/total_prediction
    except ZeroDivisionError:
        Accu = 0
    
    return(Accu)

def List2Ignore (false_no_bacteria_image_dict):
    '''
    

    Parameters
    ----------
    false_no_bacteria_image_dict : TYPE dict
        DESCRIPTION.
        When image found with no bacteria (False negative)
        get the z_plane number, which will be ignored from acutual fake image when comparing with processed fake image for accuracy

    Returns
    -------
    list of the z_planes number to ignore for accuracy
    

    '''
    ignore_z_no = []
    for no_b_c in range(0,len(false_no_bacteria_image_dict)):
        key = list(false_no_bacteria_image_dict.keys())[no_b_c]
        key_no = re.split('(\d+)',key)
        ignore_z_no.append(int(key_no[1]))
    return(ignore_z_no)
    
    
def FindAccuracy(fake_bacteria_coordinate, find_fake_bacteria_coordinates, false__no_bacteria_images):
    '''
    

    Parameters
    ----------
    fake_bacteria_coordinate : TYPE list
        DESCRIPTION.
        list of all the fake-image wise coordinates
    find_fake_bacteria_coordinates : TYPE
        DESCRIPTION.
        list of all the fake-image wise coordinates after finding bacteria location
    false__no_bacteria_images : TYPE dict
        DESCRIPTION.
        z-plane number with images when there is false negative

    Returns
    -------
    acc_list: based on the binary count, accuracy got determined and appended on this list for each image
    acc: float- average of all the accuracy found by suming all the image wise acccuracy
    None.

    '''
    acc_list = []
    total_fake_image = len(fake_bacteria_coordinate)
    z_ignore = List2Ignore(false__no_bacteria_images)
    
    for cnt_img in range(0,len(fake_bacteria_coordinate)):
        if cnt_img in z_ignore:
            continue
        one_fake_image_coord = fake_bacteria_coordinate[cnt_img]
        one_proc_fake_image_coord = find_fake_bacteria_coordinates['xy_Z_'+str(cnt_img)]
        bin_list = BinaryResult(one_fake_image_coord, one_proc_fake_image_coord)
        acc = Accuracy(bin_list)
        acc_list.append(acc)
    acc = sum(acc_list)/total_fake_image*100
    print('Accuracy:'+str(acc))
    return(acc_list, acc)
