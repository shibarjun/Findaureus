from Validation.MakeBacterialImagesFunctions import *
from FindAureusFunctions_tri import *
from Validation.ValidateFunctions import *
import pickle
accuracy = []

no_bac_image, scale, metadata = GetNoBacteriaImages()
fake_images_with_bacteria, fake_images_bacteria_coordinates = MakeFakeBacImage(no_bac_image, scale[0], scale[1])

found_bacteria_in_fake_bacteria_image, found_bacteria_coordinates_in_fake_bacteria_image, found_no_bacteria_in_fake_bacteria_image,_,_,_ = FindBacteriaAndNoBacteria_tri(fake_images_with_bacteria, metadata)

acc = FindAccuracy(fake_images_bacteria_coordinates, found_bacteria_coordinates_in_fake_bacteria_image, found_no_bacteria_in_fake_bacteria_image)
accuracy.append(acc[1])
    
#output_folder = AskOutputFolder('Export')
#with open(output_folder+'\Object_Variable_tri_T.pkl', 'wb') as f: 
#    pickle.dump([acc, fake_images_bacteria_coordinates,fake_images_with_bacteria,  found_bacteria_coordinates_in_fake_bacteria_image,found_bacteria_in_fake_bacteria_image, no_bac_image], f)

#%% For opening pickle file
# import pandas as pd
# input_folder = 'path'
# obj = pd.read_pickle(input_folder+'\Object_Variable_tri_T1.pkl')
