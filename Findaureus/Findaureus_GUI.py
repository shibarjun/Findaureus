#Necessary packages
from FindaureusFunctions import *
from io import BytesIO
import os
import time
import sys
import PySimpleGUI as sg
from PIL import Image
import matplotlib.pyplot as plt

if getattr(sys, 'frozen', False):
    import pyi_splash

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
        
    return os.path.join(base_path, relative_path)

#set theme, font, colors
sg.theme("Material2")
font = ('Helvetica', 10, 'bold')
sg.set_options(font=font)
colors = (sg.theme_background_color(), sg.theme_background_color())

#specify file types
file_types = [('Zeiss, NIkon, Leica','*.czi;*.nd2;*.lif'),("All files (*.*)", "*.*")]

#funtions required
def array_to_data(array):
    im = Image.fromarray(array)
    im.thumbnail((500,500))
    with BytesIO() as output:
        im.save(output, format="PNG")
        data = output.getvalue()
    return data

#reset all the features
def reset():
    for key in values:
        window['-IMAGE-'].update('',size=(500,500))
        window['Explore'].update('Explore', visible=False)
        window['-TEXT-'].update('',visible = False)
        for chnl_key in range(0,6):
            window.Element(format(chnl_key)).update(False, visible=False)
        window['Ok'].update('Ok',visible = False)
        window['-ZTEXT-'].update('',visible = False)
        window['BacteriaRegionFound'].update('',visible = False)
        window['-SLIDER-'].update(False,visible = False)
        window['Find Bacteria'].update(disabled=True)
        window['-ZNo-'].update('',visible = False)
        window['-TEXTBACTERIA-'].update('',visible = False)
        window['-TEXTNOBACTERIA-'].update('',visible = False)
        window['-BACZTEXT-'].update('',visible = False)
        window['Export results'].update(visible=False)
        window['-BACBOX-'].update('',visible = False)
        window['-TEXTNOBACTERIA-'].update('',visible = False)
        window['-SBAR-'].update('')
        window['ImageInfo'].update('',visible = False)
        window.refresh()
    return None

#default matplotlib window for exploring the selected image in an interactively manner
def explore(value):
    plt.imshow(value, cmap='binary_r')
    plt.show(block=False)

#features on the left column

left_column = [[sg.Text("Image file:"), sg.Input(key="-FILE-"),
                sg.FileBrowse(file_types=file_types),sg.Button("Load Image", enable_events = True, expand_x=True),sg.Button(key ='Clear', enable_events = True, button_color=colors, image_filename=resource_path(r'delete.png'),tooltip='Clear all' )],
               [sg.Image(key ='-IMAGE-', visible=True,size=(500, 500), enable_events = True,expand_x=True, expand_y=True)],
               [sg.Button('', visible=False, enable_events = True, button_color=colors, image_filename=resource_path(r'find_search_locate.png'),key ='Explore',tooltip='Explore selected image')],
               [sg.Text('\n\nChannels avaliable:', key = '-TEXT-', visible = False, enable_events = True, expand_x=True, justification='left')],
               [sg.Radio(None, 1, key = '0', visible=False, enable_events = True, expand_x=True),
                    sg.Radio(None, 1, key = '1', visible=False, enable_events = True, expand_x=True),
                    sg.Radio(None, 1, key = '2', visible=False, enable_events = True, expand_x=True),
                    sg.Radio(None, 1, key = '3', visible=False, enable_events = True, expand_x=True),
                    sg.Radio(None, 1, key = '4', visible=False, enable_events = True, expand_x=True),
                    sg.Radio(None, 1, key = '5', visible=False, enable_events = True, expand_x=True),
                    sg.Radio(None, 1, key = '6', visible=False, enable_events = True, expand_x=True),
                    sg.Button(key ='Ok', visible = False, expand_x=True,button_color=colors, image_filename=resource_path(r'things.png'))],
               [sg.Text('', key = '-ZTEXT-', visible = False, enable_events = True)],
               [sg.Slider(range=(None, None),orientation='h',disable_number_display=True, key='-SLIDER-', enable_events = True, visible=False, expand_x=True), 
                sg.Text('', key = '-ZNo-', visible = False, enable_events = True)],
               [sg.StatusBar('Welcome!', size=(40,2), key='-SBAR-', visible=True, expand_x=True)],
                             ]

#features on the right column

right_column = [[sg.Button('Find Bacteria', disabled=True, expand_x=True, tooltip='Click to find bacteria')],
                [sg.Text('', key = '-TEXTBACTERIA-', visible = False, expand_x=True)],
                [sg.Text('', key = '-TEXTNOBACTERIA-', visible = False, expand_x=True)],
                [sg.Text('', key = '-BACZTEXT-', visible = False, expand_x=True)],
                [sg.Text('View image with bacteria location', key = 'ViewText', enable_events=True,visible=False, expand_x=True)],
                [sg.CB('View image with bacteria location', enable_events=True, size=(30,2), key='-BACBOX-', visible=False, expand_x=True)],
                [sg.Text('', key = 'BacteriaRegionFound', visible=False, expand_x=True)],
                [sg.Button('Export Results',key='Export results',visible=False, expand_x=True, tooltip = 'Export bacteria boxed images and coordinates')],
                [sg.Text('', key = 'ImageInfo', visible=False, expand_x=True)]]
                

#window layout

window_layout = [
    [sg.Column(left_column, vertical_alignment='top', expand_x=True, expand_y=True,element_justification='center'),sg.VSeparator(pad=(20,0)), sg.Column(right_column, vertical_alignment='top',expand_x=True, expand_y=True,element_justification='center')],
]

window = sg.Window("Findaureus", window_layout,finalize=True,use_ttk_buttons=True, resizable=False, element_justification='center', icon=resource_path(r'application_icon.ico'))

ok_image_list = [] 
try:
    if getattr(sys, 'frozen', False):
        pyi_splash.close()
    while True:
        event, values = window.read()
        
    #if close or exit
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
    # button load image : load the image and display brightfiled image as default image as ask to select the channel
        if event == "Load Image":
            reset()
            window['-SBAR-'].update('Loading.....')
            window.refresh()
            ok_image_list = []
            filename = values["-FILE-"]
            if os.path.exists(filename):
                try:
                    file = ReadFile.ReadImageFile(filename)
                    size_x, size_y = ReadFile.ImageSize(file[0])
                    zplane = ReadFile.ZPlanesAvaliable(file[0])
                    channels = ReadFile.ChannelColor(filename)
                    take_defaut_image = ReadFile.ChannelImageList(file[1], (len(channels)-1))
                    image_height, image_width,image_height_um, image_width_um, depth_um, resolution  = ReadFile.ImageInformation(file[0], take_defaut_image)
                except: #exception
                    
                    file = ReadFileException.ReadImageFile(filename)
                    size_x, size_y = ReadFileException.ImageSize(file[0])
                    zplane = ReadFileException.ZPlanesAvaliable(file[0])
                    channels = ReadFileException.No_ChannelsAvaliable(file[0])
                    take_defaut_image = ReadFileException.ChannelImageList(file[1], (len(channels)-1))
                    image_height, image_width,image_height_um, image_width_um, depth_um, resolution  = ReadFileException.ImageInformation(file[0], take_defaut_image)
                
                default_image = array_to_data(take_defaut_image[0])
                window['-IMAGE-'].update(data = default_image)
                for chnl_no in range(0, len(channels)):
                        window.Element(format(chnl_no)).update(text = channels[chnl_no], visible=True)
                window['-TEXT-'].update(visible=True)
                window['ImageInfo'].update('\nImage height: '+str(image_height_um)+' microns '+'('+str(image_height)+')\nImage width: '+str(image_width_um)+' microns '+'('+str(image_width)+')\nImage resolution: '+str(resolution)+' pixels per micron',visible=True)
                window['Ok'].update(visible = True)
            window['-SBAR-'].update('Image loaded succesfully \nPlease select the channel for bacteria investigation')
            
    #button ok: lets you select the channel and display the slider if any zplanes avaliable
        if event == 'Ok':
            window['Find Bacteria'].update(disabled=False)
            
            window['Explore'].update(visible= True)
            key_value = int(list(values.keys())[list(values.values()).index(True)])
            window['-IMAGE-'].update( visible=True )
            try:
                ok_image_list = ReadFile.ChannelImageList(file[1], key_value)
                ok_image = array_to_data(ok_image_list[0])
            except:
                ok_image_list = ReadFileException.ChannelImageList(file[1], key_value)
                ok_image = array_to_data(ok_image_list[0])
            window['-IMAGE-'].update(data = ok_image)
            if zplane == ():
                window['-SLIDER-'].update(visible=True)
                window['-ZTEXT-'].update('\nNo of Z planes avaliable : 0', visible=True)
                
            else:
                window['-SLIDER-'].update(range=(0,zplane-1), visible=True)
                window['-ZNo-'].update(str(int(values['-SLIDER-'])), visible=True)
                window['-ZTEXT-'].update('\nNo of Z planes avaliable : '+str(zplane), visible=True)
            window['-SBAR-'].update('Channel selected: '+str(channels[key_value]))
    #button explore: lets you explore the slider selectd image in details, giving options for zoom , pan save one particular image
        if event == 'Explore':
            
            if values ['-BACBOX-']:
                if len(zplanes_with_bacteria) ==1:
                    N_bac_val = zplanes_with_bacteria[0]
                    explore(N_bac_val)
                else:
                    bac_val = zplanes_with_bacteria[int(values['-SLIDER-'])]
                    explore(bac_val)
            else:
                if len(ok_image_list) ==1:
                    Nval = ok_image_list[0]
                    explore(Nval)
                else:
                    val = ok_image_list[int(values['-SLIDER-'])]
                    explore(val)
    
        if event == '-SLIDER-':
    
            imgdata = array_to_data(ok_image_list[int(values['-SLIDER-'])])
            window['-IMAGE-'].update(data = imgdata)
            window['-ZNo-'].update(str(int(values['-SLIDER-'])), visible=True)
    
    # button find bacteria: find bacteria across avlaibale zplanes
        if event == 'Find Bacteria':
            window['-SBAR-'].update('Finding bacteria....')
            window.refresh()
            zplanes_with_bacteria, bacteria_coordinate, zplanes_with_no_bacteria, pixlewise_bacteria_coordinate, bacteria_area, metadata = FindBacteriaAndNoBacteria(ok_image_list, file[0])
            
            list_bacteria_coordinate = list(bacteria_coordinate.keys())
            z_plane_numbers_list = []
            for zno in range(0,len(list_bacteria_coordinate)):
                znum = list_bacteria_coordinate[zno].split('_',2)[2]
                z_plane_numbers_list.append(znum)
            window['-SBAR-'].update('Finished')
            if zplanes_with_bacteria == []:
                window['-BACBOX-'].update(visible=False)
                window['-SBAR-'].update('No bacteria found')
                window['Export results'].update(disabled=True)
            else:
                window['-BACBOX-'].update(visible=True)
                window['Export results'].update(visible=True, disabled=False)
            window['-TEXTBACTERIA-'].update('\nNo of Z planes with bacteria : '+str(len(zplanes_with_bacteria)), visible=True)
            window['-TEXTNOBACTERIA-'].update('\nNo of Z planes without bacteria : '+str(len(zplanes_with_no_bacteria)), visible=True)
    
    
        elif values ['-BACBOX-']:
            
            window['-ZTEXT-'].update('\nNo of Z planes with bacteria : '+str(len(zplanes_with_bacteria)))
            if len(zplanes_with_bacteria) ==1:
                window['-SLIDER-'].update(visible = False)
                bac_imgdata = array_to_data(zplanes_with_bacteria[0])
                window['-IMAGE-'].update(data = bac_imgdata)
                window['BacteriaRegionFound'].update('\nBacterial region found : '+str(len(bacteria_coordinate['xy_Z_'+znum])), visible=True)
                
    
            else:
                window['-SLIDER-'].update(range=(0,len(zplanes_with_bacteria)-1), visible = True)
                try:
                    z_plane_number = z_plane_numbers_list[int(values['-SLIDER-'])]
                    window['-ZNo-'].update(str(z_plane_number), visible=True)
                    bac_imgdata = array_to_data(zplanes_with_bacteria[int(values['-SLIDER-'])])
                except Exception:
                    continue
                window['-IMAGE-'].update(data = bac_imgdata)
                window['BacteriaRegionFound'].update('\nBacterial region found : '+str(len(bacteria_coordinate['xy_Z_'+(str(z_plane_number))])), visible=True)
    
    
            
        elif values ['-BACBOX-'] == False and ok_image_list != []:
            
            window['-ZTEXT-'].update('\nNo of Z planes avaliable : '+str(len(ok_image_list)))
            if len(ok_image_list)==1 :
                slider_imgdata = array_to_data(ok_image_list[0])
                window['-IMAGE-'].update(data = slider_imgdata)
                window['-SLIDER-'].update(visible = False)
                window['BacteriaRegionFound'].update(visible=False)
            else:
                window['-SLIDER-'].update(range=(0,(len(ok_image_list)-1)), visible = True)
                slider_imgdata = array_to_data(ok_image_list[int(values['-SLIDER-'])])
                window['-IMAGE-'].update(data = slider_imgdata)
                window['BacteriaRegionFound'].update(visible=False)
    
        if event =='Export results':
            try: 
                window['-SBAR-'].update('Results exporting......')
                export_folder_name = ExportBacteria(zplanes_with_bacteria, bacteria_coordinate)
                window['-SBAR-'].update('Results exported at: '+str(export_folder_name))
            except:
                window['-SBAR-'].update('Result export cancelled by the user')
        if event == 'Clear':
                reset()
                
    
    
        # print(event, values)
            
    
    window.close()
except Exception as e:
    sg.popup_error_with_traceback('AN ERROR OCCURRED!', str(e)+' Please inform to the owner Thank you')

