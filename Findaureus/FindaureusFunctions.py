#imports
from aicsimageio import AICSImage
import czifile as cf
import webcolors
import cv2
import numpy as np
from tkinter import Tk, filedialog
import json

#functions and class
def ClosestColour(requested_colour):
    """
    

    Parameters
    ----------
    requested_colour : tuple
        DESCRIPTION.
        Sometimes the fluroscence channel color options (HEX code) are not avaliable in the web color package.
        Which throws error when colors names are displayed to the user.
        So this function will give the closest color related to the input image's HEX code

    Returns
    -------
    colours_name : str
        DESCRIPTION.
        color name

    """

    colours_name = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        colours_name[(rd + gd + bd)] = name
    
    return colours_name[min(colours_name.keys())]

class ReadFile():
    
    def ElementToDict(element):
        '''
        
        Parameters
        ----------
        element : etree.ElementTree.Element
            Converts an etree.ElementTree.Element object to a dictionary.

        Returns
        -------
        dictionary : dict
            input image file metadata in form of dictionary

        '''
        
        dictionary = {element.tag: {}}
        if element.attrib:
            dictionary[element.tag].update({'@' + key: value for key, value in element.attrib.items()})
        if element.text:
            dictionary[element.tag]['#text'] = element.text.strip()
        for child_element in element:
            child_dictionary = ReadFile.ElementToDict(child_element)
            if child_element.tag in dictionary[element.tag]:
                if isinstance(dictionary[element.tag][child_element.tag], list):
                    dictionary[element.tag][child_element.tag].append(child_dictionary[child_element.tag])
                else:
                    dictionary[element.tag][child_element.tag] = [dictionary[element.tag][child_element.tag], child_dictionary[child_element.tag]]
            else:
                dictionary[element.tag].update(child_dictionary)

        return dictionary

    def ReadImageFile(image_file_path):
        '''
        
        Parameters
        ----------
        image_file_path : string
            Fluorescence image file path
            
        Returns
        -------
        file_object : aics_image.AICSImage
            input image data and metadata
        file_numpy_array : Array of uint8
            image numpy array consisting image channel, zplanes
        file_metadata : dict
            input image data and metadata

        '''

        file_object = AICSImage(image_file_path)
        file_metadata = file_object.metadata
        
        if image_file_path.endswith(".nd2"):
            file_numpy_array = file_object.get_image_data("CZYX")
        
        else: 
            file_metadata = ReadFile.ElementToDict(file_metadata)
            file_numpy_array = file_object.get_image_data("CZYX")
        
        return (file_object,file_numpy_array,file_metadata)

    def ImageSize (image_file_object):
        '''
        
        Parameters
        ----------
        image_file_object : aics_image.AICSImage
            Image file object which contains basic image information, in this particular case we are exploring the image size

        Returns
        -------
        image_size_x: int
            width of the image in pixel
        image_size_y: int
            height of the image in pixel
            

        '''

        image_size_x = image_file_object.dims.X
        image_size_y = image_file_object.dims.Y
        # image_size_z = image_file_object.dims.Z
        return(image_size_x, image_size_y)

    def No_ChannelsAvaliable(image_file_object):
        '''
        
        Parameters
        ----------
        image_file_object : aics_image.AICSImage
            Image file object which contains basic image information, in this particular case we are exploring the number of channels avaliable

        Returns
        -------
        channel_size : int
            Number of channels (if avaliable)

        '''

        channel_size = int(len(image_file_object.channel_names))
        return (channel_size)

    def ChannelColor (image_file_path):
        '''
        
        Parameters
        ----------
        image_file_path : string
            From the image file path, read and extract channel information 

        Returns
        -------
        channel_colors_name: list
            list of the channels avaliable and there respective color names

        '''
        channel_colours = []
        channel_colours_name = []
        #for nikon extension
        if image_file_path.endswith(".nd2"):
            image_file_object,_,image_metadata = ReadFile.ReadImageFile(image_file_path)
            channel_size = ReadFile.No_ChannelsAvaliable(image_file_object)
            if channel_size == 1:
                channel_colours.append(image_metadata["metadata"].channels.channel.colorRGB)
            if channel_size > 1:
                for ch in range(channel_size):
                    channel_colours.append(image_metadata["metadata"].channels[ch].channel.colorRGB)
            for chclr in range (0, len(channel_colours)):
                rgb_color = webcolors.hex_to_rgb('#{:06x}'.format(channel_colours[chclr]))
                rgb_name = webcolors.rgb_to_name(rgb_color)
                channel_colours_name.append(rgb_name)
        #for zeiss extension
        if image_file_path.endswith(".czi"):
            image_file_object,_,image_metadata = ReadFile.ReadImageFile(image_file_path)
            channel_size = ReadFile.No_ChannelsAvaliable(image_file_object)
            if channel_size == 1:
                channel_colours.append(image_metadata['ImageDocument']['Metadata']['DisplaySetting']['Channels']['Channel']['Color']["#text"])
            if channel_size > 1:
                for ch in range(channel_size):
                    channel_colours.append(image_metadata['ImageDocument']['Metadata']['DisplaySetting']['Channels']['Channel'][ch]['Color']["#text"])
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
        #for leica extension
        if image_file_path.endswith(".lif"):
            image_file_object,_,image_metadata = ReadFile.ReadImageFile(image_file_path)
            channel_size = ReadFile.No_ChannelsAvaliable(image_file_object)
            if channel_size == 1:
                channel_colours.append(image_metadata['LMSDataContainerHeader']['Element']['Children']['Element'][0]['Data']['Image']["ImageDescription"]["Channels"]["ChannelDescription"]["@LUTName"])
            if channel_size > 1:
                for ch in range(channel_size):
                    channel_colours.append(image_metadata['LMSDataContainerHeader']['Element']['Children']['Element'][0]['Data']['Image']["ImageDescription"]["Channels"]["ChannelDescription"][ch]["@LUTName"])
            
            channel_colours_name = channel_colours
        
        return(channel_colours_name)

    def ImageScalingXY(image_file_object):
        '''
        
        Parameters
        ----------
        image_file_object : aics_image.AICSImage
            Image file object which contains basic image information, in this particular case we are exploring the pixel scaling information in the image

        Returns
        -------
        scale_z: float
            pixel scaling information in respect to depth 
        scale_x: float
            pixel scaling information in respect to width 
        scale_z: float
            pixel scaling information in respect to height 

        '''
        
        scale_z = image_file_object.physical_pixel_sizes[0]
        scale_x = image_file_object.physical_pixel_sizes[1]
        scale_y = image_file_object.physical_pixel_sizes[2]
        
        return([scale_z, scale_x, scale_y])

    def ZPlanesAvaliable(image_file_object):
        '''
        
        Parameters
        ----------
        image_file_object : aics_image.AICSImage
            Image file object which contains basic image information, in this particular case we are exploring the avaliable z-planes in the image

        Returns
        -------
        z-planes: int
            No of z-planes avaliable

        '''

        z_planes = image_file_object.dims.Z
        
        return(z_planes)

    def ChooseChannel (channel_colors_name):
        '''
        
        Parameters
        ----------
        channel_colors_name : list
            List of all the channels avaliable in the current image file, for the user to select bacteria specific channel 

        Returns
        -------
        option : int
            User selected bacteria channel

        '''
        for channelcount in range(0, len(channel_colors_name)):
            print(str(channelcount)+': '+str(channel_colors_name[channelcount])+'\n')
        option = int(input('Please provide the channel number to investigate: '))
        
        return(option)

    def ChannelImageList(image_array, user_option):
        '''
        
        Parameters
        ----------
        image_array :  Array of uint8
            numpy array
        user_option : int
            user selected bacteria channel option

        Returns
        -------
        input_image_list: list
            list of all the zplane images in Array of uint8/16/32 based on the channel selected by the user    

        '''

        input_image_list = []
        twod_image_array = image_array
        for z in range (0,twod_image_array.shape[1]):
            img = twod_image_array[[user_option], [z], :, :][0]
            if img.max() > 255:
                img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
            input_image_list.append(img)
        
        return(input_image_list)
    
    def ImageInformation (image_file_object, image_list_numpy_array):
        '''
        
        Parameters
        ----------
        image_file_object : aics_image.AICSImage
            Image file object which contains basic image information, in this particular case we are exploring the imagw size also in micron.
        image_list_numpy_array : list
            list of all the zplane images in Array of uint8/16/32 based on the channel selected by the user

        Returns
        -------
        height: int
            image height in pixels
        width: int
            image width in pixels
        height_um: int
            image height in micron
        width_um: int
            image width in micron
        depth_um: int
            number of z-planes 
        resolution: int
            resolution of the input image, pixel per micron

        '''
        height,width = image_list_numpy_array[0].shape #in pixels
        depth = len(image_list_numpy_array)
        scale_z,scale_x, scale_y = ReadFile.ImageScalingXY(image_file_object)
        height_um, width_um, depth_um  = round(height*scale_x,3), round(width*scale_y,3),round(depth*scale_z,3) #in um
        resolution = round(1/scale_x,3) #pixel per um
        
        return(height, width, height_um, width_um, depth_um,resolution)
    

class ReadFileException:
    
    def ReadImageFile(image_file_path):
        '''
        
        Parameters
        ----------
        image_file_path : string
            Fluorescence image file path

        Returns
        -------
        file_metadata : dict
            input image data and metadata
        file_numpy_array : Array of uint8
            image numpy array consisting image channel, zplanes

        '''
        file_object = cf.CziFile(image_file_path)
        file_metadata = file_object.metadata(raw=False)
        file_numpy_array = cf.imread(image_file_path)
        
        return (file_metadata, file_numpy_array)

    def ImageSize (file_metadatadict_for_imagesize):
        '''
        
        Parameters
        ----------
        file_metadatadict_for_imagesize : dict
            Image file object which contains basic image information, in this particular case we are exploring the image size

        Returns
        -------
        image_size_x: int
            width of the image in pixel
        image_size_y: int
            height of the image in pixel
            

        '''
        image_size_x = int(file_metadatadict_for_imagesize['ImageDocument']['Metadata']['Information']['Image']['SizeX'])
        image_size_y = int(file_metadatadict_for_imagesize['ImageDocument']['Metadata']['Information']['Image']['SizeY'])
        return(image_size_x, image_size_y)

    def No_ChannelsAvaliable(file_metadatadict_for_channel):
        '''
        
        Parameters
        ----------
        file_metadatadict_for_channel : dict
            Image file object which contains basic image information, in this particular case we are exploring the number of channels avaliable

        Returns
        -------
        channel_colours_name : list
            Number of channels and there colors name (if avaliable)

        '''
        channel_colours = []
        channel_colours_name = []
        channel_size = int(file_metadatadict_for_channel['ImageDocument']['Metadata']['Information']['Image']['SizeC'])
        
        if channel_size == 1:
            channel_colours.append(file_metadatadict_for_channel['ImageDocument']['Metadata']['DisplaySetting']['Channels']['Channel']['Color'])
        if channel_size > 1:
            for ch in range(channel_size):
                channel_colours.append(file_metadatadict_for_channel['ImageDocument']['Metadata']['DisplaySetting']['Channels']['Channel'][ch]['Color'])
        
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
        
        return(channel_colours_name)

    def ImageScalingXY(file_metadatadict_for_scaling):
        '''
        
        Parameters
        ----------
        file_metadatadict_for_scaling : dict
            Image file object which contains basic image information, in this particular case we are exploring the pixel scaling information in the image

        Returns
        -------
        scale_z: float
            pixel scaling information in respect to depth 
        scale_x: float
            pixel scaling information in respect to width 
        scale_z: float
            pixel scaling information in respect to height 

        '''
        scale_x = file_metadatadict_for_scaling['ImageDocument']['Metadata']['Scaling']['Items']['Distance'][0]['Value']
        scale_x = scale_x*10**6
        scale_y = file_metadatadict_for_scaling['ImageDocument']['Metadata']['Scaling']['Items']['Distance'][1]['Value']
        scale_y = scale_y*10**6
        try:
            scale_z = file_metadatadict_for_scaling['ImageDocument']['Metadata']['Scaling']['Items']['Distance'][2]['Value']
            scale_z = scale_z*10**6
        except IndexError:
            scale_z = 1
        return([scale_z, scale_x, scale_y])

    def ZPlanesAvaliable(file_metadatadict_for_z_planes):
        '''
        
        Parameters
        ----------
        file_metadatadict_for_z_planes : dict
            Image file metadata dictionary which contains basic image information, in this particular case we are exploring the avaliable z-planes in the image

        Returns
        -------
        z-planes: int
            No of z-planes avaliable

        '''
        if "SizeZ" in file_metadatadict_for_z_planes['ImageDocument']['Metadata']['Information']['Image']:
            z_planes = int(file_metadatadict_for_z_planes['ImageDocument']['Metadata']['Information']['Image']['SizeZ'])
        else:
            z_planes = ()
        
        return(z_planes)

    def ChooseChannel (channel_colors_name):
        '''
        
        Parameters
        ----------
        channel_colors_name : list
            List of all the channels avaliable in the current image file, for the user to select bacteria specific channel 

        Returns
        -------
        option : int
            User selected bacteria channel

        '''
        for channelcount in range(0, len(channel_colors_name)):
            print(str(channelcount)+': '+str(channel_colors_name[channelcount])+'\n')
        option = int(input('Please provide the channel number to investigate: '))
        return(option)

    def ChannelImageList(image_file_numpy_array, user_option):
        '''
        
        Parameters
        ----------
        image_file_numpy_array :  Array of uint8
            numpy array
        user_option : int
            user selected bacteria channel option

        Returns
        -------
        input_image_list: list
            list of all the zplane images in Array of uint8/16/32 based on the channel selected by the user    

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
        file_metadata : dict
            Image file metadata which contains basic image information, in this particular case we are exploring the imagw size also in micron.
        image_list_numpy_array : list
            list of all the zplane images in Array of uint8/16/32 based on the channel selected by the user

        Returns
        -------
        height: int
            image height in pixels
        width: int
            image width in pixels
        height_um: int
            image height in micron
        width_um: int
            image width in micron
        depth_um: int
            number of z-planes 
        resolution: int
            resolution of the input image, pixel per micron

        '''
        height,width = image_list_numpy_array[0].shape #in pixels
        depth = len(image_list_numpy_array)
        scale_z, scale_x, scale_y = ReadFileException.ImageScalingXY(file_metadata)
        height_um, width_um, depth_um  = round(height*scale_x,3), round(width*scale_y,3),round(depth*scale_z,3) #in um
        resolution = round(1/scale_x,3) #pixel per um
        return(height, width, height_um, width_um, depth_um, resolution)
        

def LowerValue_exp_theshold(input_image):
    '''
    

    Parameters
    ----------
    input_image : numpy array
        export value using quantile from exponential distribution

    Returns
    -------
    lower : int
        lower bound value for masking

    '''
    lower = -np.log(0.001)*np.median(input_image) / np.log(2)
    return(lower)

def ValueForMask(input_image):
    '''
    

    Parameters
    ----------
    input_image: Numpy array, Array of uint8
        Input image calculate the lower and upper threshold value for masking bacterial region

    Returns
    -------
    upper, lower: int
        upper and lower value for mask bacteria

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
    input_image : Array of uint8
        DESCRIPTION.
        image where the bacteria mask will be applied
    lower : TYPE int
        DESCRIPTION.
        lower value for creating a bacteria mask
    upper : TYPE int
        upper value for creating a bacteria mask

    Returns
    -------
    bacteria_mask : Array of uint8
    image with bacteria mask


    '''
    
    bacteria_mask = cv2.inRange(input_image, lower, upper)
    return(bacteria_mask)

def MorphologicalOperations(bacteria_mask):
    '''
    

    Parameters
    ----------
    bacteria_mask : Array of uint8
        Takes the masked bacteria image for morphological operations

    Returns
    -------
    morphed_image : Array of uint8
        morphological operated image
    

    '''
    kernel = np.ones((3,3),np.uint8)
    opening_bacteria_mask = cv2.morphologyEx(bacteria_mask, cv2.MORPH_OPEN, kernel)
    numLabels, labeled_image = cv2.connectedComponents(opening_bacteria_mask)
    labeled_image = np.uint8(labeled_image)
    morphed_image = cv2.medianBlur(labeled_image,5)
    
    return(morphed_image)

def ContourSelection (input_image,avaliable_contours):
    '''
    
    Parameters
    ----------
    input_image : Array of uint8
        input image to select the contour region
    avaliable_contours : tuple
        contours found by opencv for selection based on conditions

    Returns
    -------
    contours : tuple
        selected contours, based on the average pixel intensity of each contoutr

    '''
    contours = []
    image = input_image.copy()
    for no_contour in range(len(avaliable_contours)):
        contour = avaliable_contours[no_contour]
        mask = np.zeros_like(image)
        cv2.drawContours(mask, [contour], 0, 255, thickness=cv2.FILLED)
        coordinates = np.where(mask == 255)
        values = image[coordinates]
        value_avg = np.average(values)
        if value_avg >20:
            contours.append(contour)
    contours = tuple(contours)
        
    return(contours)

def FindingContours(input_morphed_image):
    '''
    

    Parameters
    ----------
    input_morphed_image : Array of uint8
        Find the avaliable contours for creating bouinding box
        Selection of contours based on criteria is also avaliable. Takes longer time to implement in case of huge image

    Returns
    -------
    contours: tuples 
        Avaliable contours
    

    '''
    contours, hierarchy = cv2.findContours(input_morphed_image, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    # selected_contours = ContourSelection(input_image,contours)
    return(contours)

def GetPixelWiseBacteriaCoordinates(input_morphed_image):
    '''
    

    Parameters
    ----------
    input_morphed_image : Array of uint8
        Get the pixle coordinates from the bacteria masked-- morphed image
    
    Returns
    -------
    xy_pixelwise_coords : list
        list of all the pixle coordinates belongs to input morphed bacterial image
    

    '''
    bac_pixel_coords = np.argwhere(input_morphed_image)
    xy_pixelwise_coords = []
    for p in bac_pixel_coords:
        pxy = p[0], p[1]
        xy_pixelwise_coords.append(pxy)
    
    return(xy_pixelwise_coords)

def NonMaxSuppression(boxes, overlap_thresh):
    '''
    
    Parameters
    ----------
    boxes : list
        list of the selected boxes
    overlap_thresh : int
        threshold to ignore the overlapping of the bounding box

    Returns
    -------
    boxes[pick] : list
        list of all the selected box

    '''
    if len(boxes) == 0:
        return []

    if isinstance(boxes, list):
        boxes = np.array(boxes)
    pick = []
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 0] + boxes[:, 2]
    y2 = boxes[:, 1] + boxes[:, 3]
    area = boxes[:, 2] * boxes[:, 3]
    idxs = np.argsort(y2)


    while len(idxs) > 0:

        last = len(idxs) - 1
        i = idxs[last]
        pick.append(i)

        xx1 = np.maximum(x1[i], x1[idxs[:last]])
        yy1 = np.maximum(y1[i], y1[idxs[:last]])
        xx2 = np.minimum(x2[i], x2[idxs[:last]])
        yy2 = np.minimum(y2[i], y2[idxs[:last]])


        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)


        overlap = (w * h) / area[idxs[:last]]


        idxs = np.delete(idxs, np.concatenate(([last], np.where(overlap > overlap_thresh)[0])))


    return boxes[pick]

def MakeBoundingBoxWithCentroid(input_image, found_contour, image_file_object):
    '''
    

    Parameters
    ----------
    input_image : Array uint8
        create bounding box on the input image
    found_contour : tuple
        contours for making bounding boxes around after checking bacteria area
        
    image_file_object : TYPE 
        needed for getting the scaling information for calculate bacteria area
        
    Returns
    -------
    bound_boxed_image : Array of uint8
        Image with bacteria region boxed
    centroid : list
        centroids of the boxed bacteria
    coord_area_um2 : dict
        area of the bacterial region mentioned by each bacterial region centroid
    

    '''
    centroid = []
    area_list_um2 = []
    boxes = []
    bound_boxed_image = input_image.copy()
    for cnt in found_contour:
        try:
            _,scalex,scaley = ReadFile.ImageScalingXY(image_file_object)
        except:
            _,scalex,scaley = ReadFileException.ImageScalingXY(image_file_object)
        bac_dia = 0.5 # considering bac size 0.5 um in diameter
        contour_area = cv2.contourArea(cnt)
        contour_area_um = (scalex*scaley)*(contour_area)
        area_bac_um = np.pi*(bac_dia/2)**2
        
        if contour_area_um<=area_bac_um: 
            continue
        x, y, w, h = cv2.boundingRect(cnt)
        
        if w and h >= input_image.shape[0] and input_image.shape[1]:
            break
        boxes.append((x,y,w,h))
   
    selected_boxes = NonMaxSuppression(boxes, overlap_thresh=0.3)
        
    for box in selected_boxes:
        x,y,w,h = box
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
    input_image_list : list
        Input images from the bacteria channel 
    file_metadata :dict
    scaling information from the metadata for localizing bacteria
    
    Returns
    -------
    bac_image_list : list 
        z planes with bacteria boxed
    bac_centroid_xy_coordinates: dict 
        coordinates of the box with bacteria
    no_bact_dict: dict
        z planes and with z plane numbers with no bacteria
    bac_pixelwise_xy_coordinates: dict
        all pixle coordinates with suspected bacteria
    bacteria_area:
        
    file_metadata: dict
    

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
    filename = filedialog.askopenfilename(title="Select file",filetypes = [("czi, nd2, lif","*.czi;*.nd2;*.lif")])
    try:
        inputimagefileobject, inputimagefilenumpyarray, inputimagefilemetadata = ReadFile.ReadImageFile(filename)
        channels = ReadFile.ChannelColor(filename)
    except:
        inputimagefilemetadata, inputimagefilenumpyarray = ReadFileException.ReadImageFile(filename)
        channels = ReadFileException.No_ChannelsAvaliable(inputimagefilemetadata)
        choosechannel = ReadFileException.ChooseChannel(channels)
        channelimagelist = ReadFileException.ChannelImageList(inputimagefilenumpyarray, choosechannel)
        faureus = FindBacteriaAndNoBacteria(channelimagelist, inputimagefilemetadata)
    else:
        choosechannel = ReadFile.ChooseChannel(channels)
        channelimagelist = ReadFile.ChannelImageList(inputimagefilenumpyarray, choosechannel)
        faureus = FindBacteriaAndNoBacteria(channelimagelist, inputimagefileobject)
        
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
