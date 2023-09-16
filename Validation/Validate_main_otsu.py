from Validation_Functions.MakeBacterialImagesFunctions import *
from Validation_Functions.ValidateFunction_otsu import *
from Validation_Functions.ValidateFunctions import *
import pickle


no_bac_image, scale, metadata = GetNoBacteriaImages()
fake_images_with_bacteria, fake_images_bacteria_coordinates = MakeFakeBacImage(no_bac_image, scale[0], scale[1])

found_bacteria_in_fake_bacteria_image, found_bacteria_coordinates_in_fake_bacteria_image, found_no_bacteria_in_fake_bacteria_image,pw_bac_coordinates,_,_ = FindBacteriaAndNoBacteria_otsu(fake_images_with_bacteria, metadata)

if found_no_bacteria_in_fake_bacteria_image != "":
    for key, value in found_no_bacteria_in_fake_bacteria_image.items():
        z_no = int(key[5:])
        found_bacteria_coordinates_in_fake_bacteria_image["xy_Z_"+str(z_no)] = []

predicted_bacteria_coordinates = UpdatePredictedCoordinatesList(found_bacteria_coordinates_in_fake_bacteria_image, fake_images_bacteria_coordinates)
true_bacteria_coordinates = fake_images_bacteria_coordinates
#%%
list_of_ConfusionMatrix = []
list_of_accuracy = []
list_of_precision = []
list_of_recall = []
list_of_f1_score = []


for cm in range(0, len(true_bacteria_coordinates)):
    true_bacteria_set = set(true_bacteria_coordinates[cm])
    predicted_bacteria_set = set(predicted_bacteria_coordinates[cm])
    # background_set = set(true_background_coordinates[cm])
    
    TP = len(true_bacteria_set.intersection(predicted_bacteria_set)) #  belonging to the positive class being classified correctly
    FP = len(predicted_bacteria_set.difference(true_bacteria_set)) #belonging to the negative class but being classified wrongly as belonging to the positive class
    FN = len(true_bacteria_set.difference(predicted_bacteria_set)) # belonging to the positive class but being classified wrongly as belonging to the negative class
    # TN = TrueNeagtive(fake_images_with_bacteria[cm], pw_bac_coordinates["p_xy_"+str(cm)])- FP #belonging to the negative class being classified correctly.
    TN = 0
    confusion_matrix = np.array([[TP, FN], [FP, TN]])
    list_of_ConfusionMatrix.append(confusion_matrix)

    accuracy = (TP + TN) / (TP + TN + FP + FN)
    list_of_accuracy.append(accuracy)

    precision = TP / (TP + FP) if (TP + FP) > 0 else 0
    list_of_precision.append(precision)

    recall = TP / (TP + FN) if (TP + FN) > 0 else 0
    list_of_recall.append(recall)

    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    list_of_f1_score.append(f1_score)

final_confusion_matrix = np.zeros_like(list_of_ConfusionMatrix[0])
for matrix in list_of_ConfusionMatrix:
    final_confusion_matrix += matrix

print("Accuracy :", np.mean(list_of_accuracy))

#output_folder = AskOutputFolder('Export')
#with open(output_folder+'\Object_Variable_Otsu_T.pkl', 'wb') as f: 
#    pickle.dump([acc, fake_images_bacteria_coordinates,fake_images_with_bacteria,  found_bacteria_coordinates_in_fake_bacteria_image,found_bacteria_in_fake_bacteria_image, no_bac_image], f)

#%% For opening pickle file
# import pandas as pd
# input_folder = 'path'
# obj = pd.read_pickle(input_folder+'\Object_Variable_otsu_T1.pkl')
