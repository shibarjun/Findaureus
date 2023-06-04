import czifile as cf
import webcolors
import cv2
import numpy as np
from tkinter import Tk, filedialog
import json

def ClosestColour(requested_colour):
    """
    Sometimes the fluroscence channel color options (HEX code) are not avaliable in the web color package.
    Which throws error when colors names are displayed to the user.
    So this function will give the closest color related to the input image's HEX code

    Parameters
    ----------
    requested_color: TYPE tuple
        DESCRIPTION.
        RGB value requested when not found in the webcolors package
    
    Returns
    -------
    colour_name: name of the colour
    

    """
    colours_name = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        colours_name[(rd + gd + bd)] = name
    return colours_name[min(colours_name.keys())]

def ReadImageFile(image_file_path):
    '''
    Parameters
    ----------
    image_file_path : TYPE str
        DESCRIPTION.
        Read the image file (.czi in our case) as object and numpy array
        In future more file support will be added

    Returns
    -------
    file_object: object to get the metadata other important information
    file_numpy_array: images as numpy array for processing
    
    

    '''
    file_object = cf.CziFile(image_file_path)
    file_metadata = file_object.metadata(raw=False)
    file_numpy_array = cf.imread(image_file_path)
    # print("Image read succesfully from "+image_file_path)
    
    return (file_metadata, file_numpy_array)

def ImageSize (file_metadatadict_for_imagesize):
    '''
    

    Parameters
    ----------
    file_metadatadict_for_imagesize : dict
        DESCRIPTION.
        extracting the image shape information

    Returns
    -------
    image shape x,y in pixels
    
    

    '''
    image_size_x = int(file_metadatadict_for_imagesize['ImageDocument']['Metadata']['Information']['Image']['SizeX'])
    image_size_y = int(file_metadatadict_for_imagesize['ImageDocument']['Metadata']['Information']['Image']['SizeY'])
    return(image_size_x, image_size_y)

def ChannelsAvaliable(file_metadatadict_for_channel):
    '''

    Parameters
    ----------
    file_metadatadict_for_channel : TYPE dict
        DESCRIPTION.
        From metadata extract channel avaliable and channel colours

    Returns
    -------
    channel_colors_name: list with all the avaliable channel colours
    

    '''
    channel_colours = []
    channel_colours_name = []
    channel_size = int(file_metadatadict_for_channel['ImageDocument']['Metadata']['Information']['Image']['SizeC'])
    
    if channel_size == 1:
        channel_colours.append(file_metadatadict_for_channel['ImageDocument']['Metadata']['DisplaySetting']
                                      ['Channels']['Channel']['Color'])
    if channel_size > 1:
        for ch in range(channel_size):
            channel_colours.append(file_metadatadict_for_channel['ImageDocument']['Metadata']['DisplaySetting']
                                      ['Channels']['Channel'][ch]['Color'])
    
    for chclr in range (0, len(channel_colours)):
        try:
            if len(channel_colours[chclr])>7:
                color_new = str('#')+channel_colours[chclr][3:]
                rgb = webcolors.hex_to_rgb(color_new)
            else:
                rgb = webcolors.hex_to_rgb(channel_colours[chclr][:7])
            closest_name = actual_name = webcolors.rgb_to_name(rgb)
            channel_colours_name.append(actual_name)
        except ValueError:
            closest_name = ClosestColour(rgb)
            channel_colours_name.append(closest_name)
    
    # print ('There are ' + str(len(channel_colours_name)) + ' avaliable channels: ', channel_colours_name)
    
    return(channel_colours_name)

def ImageScalingXY(file_metadatadict_for_scaling):
    '''
    

    Parameters
    ----------
    file_metadatadict_for_scaling : TYPE dict
        DESCRIPTION.
        From image metadata extract x and y pixle scaling

    Returns
    -------
    scale_x,scale_y: scaling per pixle in x, y direction
    

    '''
    scale_x = file_metadatadict_for_scaling['ImageDocument']['Metadata']['Scaling']['Items']['Distance'][0]['Value']
    scale_y = file_metadatadict_for_scaling['ImageDocument']['Metadata']['Scaling']['Items']['Distance'][1]['Value']
    return([scale_x, scale_y])

def ZPlanesAvaliable(file_metadatadict_for_z_planes):
    '''
    

    Parameters
    ----------
    file_metadatadict_for_z_planes : TYPE dict
        DESCRIPTION.
       From image metadata dictionary extract no of z planes avaliable

    Returns
    -------
    z_palnes: no of z planes avaliable
    

    '''
    if "SizeZ" in file_metadatadict_for_z_planes['ImageDocument']['Metadata']['Information']['Image']:
        z_planes = int(file_metadatadict_for_z_planes['ImageDocument']['Metadata']['Information']['Image']['SizeZ'])
        # print("No of Z layers avaliable :", z_planes)
    else:
        z_planes = ()
        # print("No avaliable Z layers")
    
    return(z_planes)

def ChooseChannel (channel_colors_name):
    '''
    

    Parameters
    ----------
    channel_color_name : TYPE list
        DESCRIPTION.
        list of all the avaliable channel colors and ask the user to input

    Returns
    -------
    option: channel number based on the user input
    

    '''
    for channelcount in range(0, len(channel_colors_name)):
        print(str(channelcount)+': '+str(channel_colors_name[channelcount])+'\n')
    option = int(input('Please provide the channel number to investigate: '))
    # print('You have choosen the channel: ', channel_colors_name[option])
    
    return(option)

def ChannelImageList(image_file_numpy_array, user_option):
    '''
    

    Parameters
    ----------
    image_file_numpy_array : TYPE array of uint8/uint16
        DESCRIPTION.
    user_option : TYPE int
        DESCRIPTION.
        Read the image file and extract the nump arrays ReadImageFile fucntion (if input array is more than 8bit, nomalize it to 8bit)
        Take the user slected channel option for returning the list of images as numpy array from that particular channel

    Returns
    -------
    image_list: list of images from the choosen particula channel in 8bit
    

    '''
    if len(image_file_numpy_array.shape) == 8:
        try:
            two_d_image = image_file_numpy_array[0, 0, :, 0, :, :, :, 0]
            img_check = two_d_image[[1], [0], :, :][0]
        except IndexError:
            two_d_image = image_file_numpy_array[0, 0, 0, :, :, :, :, 0]
            
    elif len(image_file_numpy_array.shape) == 7:
        two_d_image = image_file_numpy_array[0,0,:,:,:,:,0]
    else:
        print('Something is very wrong with the file,please check the file and try again')
    input_image_list = []
    for z in range (0,two_d_image.shape[1]):
        img = two_d_image[[user_option], [z], :, :][0]
        if img.max() > 255:
            img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        input_image_list.append(img)
    return(input_image_list)

def ImageInformation (file_metadata, image_list_numpy_array):
    '''
    

    Parameters
    ----------
    file_metadata : dictionary
        extracting information from metadata like width, height in micron and resolution (pixels per micron)
    image_list_numpy_array : list
        extract height and width in pixels of the image, not avaliable in metadata

    Returns
    -------
    height and width in pixels and micron. resolution

    '''
    height,width = image_list_numpy_array[0].shape #in pixels
    scale_x, scale_y = ImageScalingXY(file_metadata)
    height_um, width_um  = round(height*scale_x*10**6,3), round(width*scale_y*10**6,3)#in um
    resolution = round(10**-6/scale_x,3) #pixel per um
    return(height, width, height_um, width_um,resolution)
    

def LowerValue_exp_theshold(input_image):
    '''
    

    Parameters
    ----------
    input_image : numpy array
        export value using quantile from exponential distribution

    Returns
    -------
    lower bound value for masking

    '''
    lower = -np.log(0.001)*np.median(input_image) / np.log(2)
    return(lower)

def ValueForMask(input_image):
    '''
    

    Parameters
    ----------
    input_image: TYPE Numpy array, Array of uint8
        DESCRIPTION.

    Returns
    -------
    upper, lower: upper and lower value for mask bacteria
    None.

    '''
    
    upper = int(np.max(input_image))
    try:
        lower = LowerValue_exp_theshold(input_image)
    except ZeroDivisionError:
        lower=()
    
    return(lower, upper)

def CreateBacteriaMask(input_image, lower, upper):
    '''
    

    Parameters
    ----------
    input_image : TYPE Numpy array, Array of uint8
        DESCRIPTION.
        image where the bacteria mask will be applied
    lower : TYPE int
        DESCRIPTION.
        lower value for creating a bacteria mask
    upper : TYPE int
        DESCRIPTION.
        upper value for creating a bacteria mask

    Returns
    -------
    image with bacteria mask


    '''
    bacteria_mask = cv2.inRange(input_image, lower, upper)
    return(bacteria_mask)

def MorphologicalOperations(bacteria_mask):
    '''
    

    Parameters
    ----------
    bacteria_mask : TYPE Array of uint8
        DESCRIPTION.
        Takes the masked bacteria image for morphological operations

    Returns
    -------
    morphed_image: morphological operated image
    

    '''
    kernel = np.ones((2,2),np.uint8)
    opening_bacteria_mask = cv2.morphologyEx(bacteria_mask, cv2.MORPH_OPEN, kernel)
    numLabels, labeled_image = cv2.connectedComponents(opening_bacteria_mask)
    labeled_image = np.uint8(labeled_image)
    morphed_image = cv2.medianBlur(labeled_image,5)
    
    return(morphed_image)

def FindingContours(input_morphed_image):
    '''
    

    Parameters
    ----------
    input_morphed_image : TYPE Array of uint8
        DESCRIPTION.
        Find the avaliable contours for creating bouinding box

    Returns
    -------
    contours: in tuples for the contours
    

    '''
    contours, hierarchy = cv2.findContours(input_morphed_image, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    return(contours)

def GetPixelWiseBacteriaCoordinates(input_morphed_image):
    '''
    

    Parameters
    ----------
    input_morphed_image : TYPE Array of uint8
        DESCRIPTION.
        Get the pixle coordinates from the bacteria masked-- morphed image
    
    Returns
    -------
    list of all the pixle coordinates
    

    '''
    bac_pixel_coords = np.argwhere(input_morphed_image)
    xy_pixelwise_coords = []
    for p in bac_pixel_coords:
        pxy = p[0], p[1]
        xy_pixelwise_coords.append(pxy)
    
    return(xy_pixelwise_coords)

def MakeBoundingBoxWithCentroid(input_image, found_contour, scaling_info_metadata):
    '''
    

    Parameters
    ----------
    input_image : TYPE Array uint8
        DESCRIPTION.
    found_contour : TYPE tuple
        DESCRIPTION.
        
    scaling_info_metadata : TYPE str
        DESCRIPTION.
        needed for getting the scaling information
    Returns
    -------
    Image with bacteria region boxed and the centroids of the boxed bacteria
    

    '''
    centroid = []
    area_list_um2 = []
    bound_boxed_image = input_image.copy()
    for cnt in found_contour:
        scalex,scaley = ImageScalingXY(scaling_info_metadata)
        bac_dia = 0.5 # considering bac size 0.5 um in diameter
        contour_area = cv2.contourArea(cnt)
        contour_area_um = ((scalex*10**6)*(scaley*10**6))*(contour_area)
        area_bac_um = np.pi*(bac_dia/2)**2
        
        if contour_area_um<=area_bac_um: 
            continue
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(bound_boxed_image,(x,y),(x+w,y+h),(255,0,0),1)
        cx = int(x + 0.5 * w)
        cy = int(y + 0.5 * h)
        cxy = (cx,cy)
        area_list_um2.append(contour_area_um)
        centroid.append(cxy)
    
    coord_area_um2 = dict(zip(centroid,area_list_um2))
    
    return(bound_boxed_image, centroid, coord_area_um2)

def FindBacteriaAndNoBacteria(input_image_list, file_metadata):
    '''
    

    Parameters
    ----------
    input_image_list : TYPE list
        DESCRIPTION.
        All images in list from the bacteria channel 
file_metadata : TYPE dict
    DESCRIPTION.
    scaling information from the metadata for localizing bacteria
    Returns
    -------
    bac_image_list = z planes with bacteria boxed
    bac_centroid_xy_coordinates: dict- coordinates of the box with bacteria
    no_bact_dict: dict- z planes and with z plane numbers with no bacteria
    bac_pixelwise_xy_coordinates: all pixle coordinates with suspected bacteria
    

    '''
    
    bac_image_list = []
    no_bac_image_list = []
    no_bac_image_name_list = []
    bac_pixelwise_xy_coordinates = {}
    bac_centroid_xy_coordinates = {}
    bacteria_area = {}
    for imageno in range(0,len(input_image_list)):
        locals()["xy_Z_"+format(imageno)] = []
        locals()["p_xy_"+format(imageno)] = []
        input_image = input_image_list[imageno]
        maskvalue_lower, maskvalue_upper = ValueForMask(input_image)
        if maskvalue_lower == ():
            no_bac_image_list.append(input_image)
            no_bac_image_name_list.append('z'+str(imageno))
            continue
        mask_image = CreateBacteriaMask(input_image, maskvalue_lower, maskvalue_upper)
        morph_image = MorphologicalOperations(mask_image)
        contours_avaliable = FindingContours(morph_image)
        
        bac_pixel_coordinates = GetPixelWiseBacteriaCoordinates(morph_image)
        locals()["p_xy_"+format(imageno)].append(bac_pixel_coordinates)
        bac_pixelwise_xy_coordinates["p_xy_"+format(imageno)]=bac_pixel_coordinates
        
        bac_image,bac_centroid_coordinates,bact_area = MakeBoundingBoxWithCentroid(input_image, contours_avaliable, file_metadata)
        if bac_centroid_coordinates == []:
            no_bac_image_list.append(bac_image)
            no_bac_image_name_list.append('z'+str(imageno))
        else:
            bac_image_list.append(bac_image)
            locals()["xy_Z_"+format(imageno)].append(bac_centroid_coordinates)
            bac_centroid_xy_coordinates["xy_Z_"+format(imageno)]= bac_centroid_coordinates
            bacteria_area["xy_Z_"+format(imageno)]=bact_area
    no_bac_dict = dict(zip(no_bac_image_name_list, no_bac_image_list))
    
    # print('\nNo of z planes with bacteria is/are : '+str(len(bac_image_list)))
    # print('\nNo of z planes with no bacteria is/are : '+str(len(no_bac_dict)))
    
    
    return(bac_image_list, bac_centroid_xy_coordinates, no_bac_dict, bac_pixelwise_xy_coordinates, bacteria_area,file_metadata)

def AskOutputFolder (foldertitle):
    '''
    

    Parameters
    ----------
    foldertitle : TYPE str
        DESCRIPTION.
        title of the folder

    Returns
    -------
    output_folder : TYPE str
        DESCRIPTION.
        directory of the folder choosen

    '''
    output_folder = filedialog.askdirectory(title=str(foldertitle))
    return (output_folder)

def ExportBacteria(bacteria_boxed_image_list=False, centroids=False, scaling_info_metadata=False, zproject=False):
    '''
    

    Parameters
    ----------
    bacteria_boxed_image : TYPE list of array of uint8
        images with bacteria in bounding box
    centroids : TYPE dict
        bacteria coordinates
    scaling_info_metadata : TYPE list
        scaling information to create a scale bar on the z project image
    zproject : TYPE Array of uint8
        zproject image of the all the bacteria z planes

    Returns
    -------
    

    '''
    output_folder = AskOutputFolder('Export folder')
    if bacteria_boxed_image_list and centroids:
        
        for listsize in range(0, len(bacteria_boxed_image_list)):
            bacteria_boxed = bacteria_boxed_image_list[listsize]
            cv2.imwrite(output_folder+'/Z_%i.png'%listsize, bacteria_boxed)
            with open(output_folder+'/BacteriaCoordinates.json', 'w') as fp:
                fp.write(json.dumps(centroids))
    # print('\nBacteria image/images and coordinates exported at' + output_folder)
    
    
    return(output_folder)

def FindAureus():
    '''
    

    Returns
    -------
    bac_image_list = z planes with bacteria boxed
    bac_centroid_xy_coordinates: dict- coordinates of the box with bacteria
    no_bact_dict: dict- z planes and with z plane numbers with no bacteria
    bac_pixelwise_xy_coordinates: all pixle coordinates with suspected bacteria

    '''
    root = Tk()
    root.withdraw()
    filename = filedialog.askopenfilename(filetypes = [("czi files","*.czi")])
    inputimagefilemetadata, inputimagefilenumpyarray = ReadImageFile(filename)
    channels = ChannelsAvaliable(inputimagefilemetadata)
    choosechannel = ChooseChannel(channels)
    channelimagelist = ChannelImageList(inputimagefilenumpyarray, choosechannel)
    faureus = FindBacteriaAndNoBacteria(channelimagelist, inputimagefilemetadata)
    if faureus[0] != []:
        asktoexport = input("Do you want to export the images and the bacterial coordinates? Y/N :")
        if asktoexport=='Y' or asktoexport=='yes' or asktoexport=='y':
            out_directory = ExportBacteria(faureus[0], faureus[1])
        else:
            pass
    else:
        print('No images with bacteria to export, please do not ask for it')
        pass
    
    return(faureus)