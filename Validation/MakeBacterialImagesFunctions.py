import glob
import random
import cv2
import numpy as np
from FindAureus.FindAureusFunctions import *

def GetNoBacteriaImages():
    '''
    Ask for input image (.czi file) and then present only z plane images with no bacteria

    Returns
    -------
    z-plane images with no bacteria
    

    '''
    root = Tk()
    root.withdraw()
    print('Please select the .czi image file')
    filename = filedialog.askopenfilename(filetypes = [("czi files","*.czi")])
    inputimagefilemetadata, inputimagefilenumpyarray = ReadImageFile(filename)
    channels = ChannelsAvaliable(inputimagefilemetadata)
    scaleinfo = ImageScalingXY(inputimagefilemetadata)
    zplanes = ZPlanesAvaliable(inputimagefilemetadata)
    choosechannel = ChooseChannel(channels)
    channelimagelist = ChannelImageList(inputimagefilenumpyarray, choosechannel)
    _,_,no_bac_images,_,_,_ = FindBacteriaAndNoBacteria(channelimagelist, inputimagefilemetadata)
    if len(no_bac_images)==0:
        print('\nPlease try some other file\n good luck!')
    else:
        ()
    return(no_bac_images, scaleinfo, inputimagefilemetadata)

def ResizeBacteria (bacteria_folder_path, scale_x, scale_y):
    '''
    

    Parameters
    ----------
    bacteria_folder_path : TYPE
        DESCRIPTION.
        directory with cropped bacteria
    scale_x: TYPE
        DESCRIPTION.
        resize the bacteria based on the image scaling x
    scale_y : TYPE
        DESCRIPTION.
        resize the bacteria based on the image scaling y

    Returns
    -------
    

    '''
    bac_image_List = glob.glob(bacteria_folder_path +'/*.png')
    random_bac_img = random.choice(bac_image_List)
    img_read = cv2.imread(random_bac_img,0)
    Bac_min = round(10**-6/scale_x)*1
    Bac_max = round(10**-6/scale_x)*3
    Bac_rand_dia = random.randrange(Bac_min, Bac_max)
    dim = Bac_rand_dia, Bac_rand_dia
    Resized_Bac = cv2.resize(img_read, dim)
    
    return (Resized_Bac)

def RetrieveNoBacteriaImages (no_bac_image_dict):
    '''
    

    Parameters
    ----------
    no_bac_image_dict : TYPE dict
        DESCRIPTION.
        extract the numpy arrays with no bacteria found by the algorithm

    Returns
    -------
    no_bac_image_list : TYPE list
        DESCRIPTION.
        list of all the images with no bacteria found by the algorithm

    '''
    no_bac_image_list = list(no_bac_image_dict.values())
    return (no_bac_image_list)

def MakeFakeBacImage (nobac_image_dict, img_scale_x, img_scale_y):
    '''
    

    Parameters
    ----------
    nobac_image_dict : TYPE dict
        DESCRIPTION.
        extract the numpy arrays with no bacteria found by the algorithm
    img_scale_x : TYPE float
        DESCRIPTION.
        image scaling needed for resizing the bacteria
    img_scale_y : TYPE
        DESCRIPTION.
        image scaling needed for resizing the bacteria

    Returns
    -------
    new_fake_bac_img_list: list of the images with planned bacteria
    randCoord: image wise coordinates of all the bacteria
    

    '''
    randCoord = []
    new_fake_bac_img_list = []
    bacteria_folder_path = r"Validation\Bacteria Images For Validation"
    no_bac_image_list = RetrieveNoBacteriaImages(nobac_image_dict)
    for NoBacImageNo in range(0,len(no_bac_image_list)):
        qty = random.randrange(1,20)
        NoBacImage = no_bac_image_list[NoBacImageNo]
        rangeX = (0,NoBacImage.shape[0])
        rangeY = (0,NoBacImage.shape[1])
        tempRandCoord = []
        
        for bac_coor in range(0,qty):
            Bac = ResizeBacteria(bacteria_folder_path, img_scale_x, img_scale_y)
            xBacShape,yBacShape = Bac.shape
            x = random.randrange(*rangeX)
            xcen = round(x+0.5*xBacShape)
            y= random.randrange(*rangeY)
            ycen = round(y+0.5*yBacShape)
            
            
            roi = NoBacImage[x:x+xBacShape, y:y+yBacShape]
            ret, maskk = cv2.threshold(Bac, 10, 255, cv2.THRESH_BINARY)
            mask_inv = cv2.bitwise_not(maskk)
            
            try:
                
                NoBacImage_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)
                Bac_fg = cv2.bitwise_and(Bac,Bac,mask = maskk)
                dst = cv2.add(NoBacImage_bg,Bac_fg)
                NoBacImage[x:x+xBacShape, y:y+yBacShape] = dst
                tempRandCoord.append((ycen,xcen))
            except Exception:
                continue
        randCoord.append(tempRandCoord)
        new_fake_bac_img_list.append(NoBacImage)
    
    return(new_fake_bac_img_list, randCoord)
