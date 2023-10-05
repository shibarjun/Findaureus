from Validation_Functions.MakeBacterialImagesFunctions import *
from Validation_Functions.ValidateFunction_otsu import *
from Validation_Functions.ValidateFunctions import *

no_bac_image, scale, metadata = GetNoBacteriaImages()
fake_images_with_bacteria, fake_images_bacteria_coordinates = MakeFakeBacImage(no_bac_image, scale[0], scale[1])

found_bacteria_in_fake_bacteria_image, found_bacteria_coordinates_in_fake_bacteria_image, found_no_bacteria_in_fake_bacteria_image,pw_bac_coordinates,_,_ = FindBacteriaAndNoBacteria_otsu(fake_images_with_bacteria, metadata)

if found_no_bacteria_in_fake_bacteria_image != "":
    for key, value in found_no_bacteria_in_fake_bacteria_image.items():
        z_no = int(key[5:])
        found_bacteria_coordinates_in_fake_bacteria_image["xy_Z_"+str(z_no)] = []

predicted_bacteria_coordinates = UpdatePredictedCoordinatesList(found_bacteria_coordinates_in_fake_bacteria_image, fake_images_bacteria_coordinates)
true_bacteria_coordinates = fake_images_bacteria_coordinates

#statistical analysis
list_of_ConfusionMatrix = []
list_of_accuracy = []
list_of_precision = []
list_of_recall = []
list_of_f1_score = []


for cm in range(0, len(true_bacteria_coordinates)):
    true_bacteria_set = set(true_bacteria_coordinates[cm])
    predicted_bacteria_set = set(predicted_bacteria_coordinates[cm])
    # background_set = set(true_background_coordinates[cm])
    
    TP = len(true_bacteria_set.intersection(predicted_bacteria_set)) #  Actually positive, predicted as positive
    FP = len(predicted_bacteria_set.difference(true_bacteria_set)) #Actually positive, predicted negative
    FN = len(true_bacteria_set.difference(predicted_bacteria_set)) # Actually negative, predicted as positive
    # TN = TrueNeagtive(fake_images_with_bacteria[cm], pw_bac_coordinates["p_xy_"+str(cm)])- FP #Actually nagative, predicted as negative.
    # TN = int()
    confusion_matrix = np.array([[TP, FN], [FP, np.nan]])
    list_of_ConfusionMatrix.append(confusion_matrix)

    try:
        accuracy = TP / (TP + FP + FN)
    except ZeroDivisionError:
        continue
    list_of_accuracy.append(accuracy)

    precision = TP / (TP + FP) if (TP + FP) > 0 else 0
    list_of_precision.append(precision)

    recall = TP / (TP + FN) if (TP + FN) > 0 else 0
    list_of_recall.append(recall)

    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    list_of_f1_score.append(f1_score)

# overall analysis
final_confusion_matrix = np.zeros_like(list_of_ConfusionMatrix[0])
for matrix in list_of_ConfusionMatrix:
    final_confusion_matrix += matrix
mean_accuracy, mean_precision, mean_recall_sensitivity, mean_f1_score = np.mean(list_of_accuracy), np.mean(list_of_precision), np.mean(list_of_recall), np.mean(list_of_f1_score)
print("\nMean Accuracy:", mean_accuracy, "\nMean Precision:", mean_precision,"\nMean Sensitivity:", mean_recall_sensitivity,"\nMean F1 Score:", mean_f1_score)

#plot the confusion matrix
class_labels_x = ["Bacteria", "Background"]
class_labels_y = ["Bacteria", "Background"]
xticks = np.arange(len(class_labels_x))
yticks = np.arange(len(class_labels_y))
fig, ax = plt.subplots()

cax = ax.matshow(final_confusion_matrix, cmap=plt.cm.Blues)

ax.set_xticks(xticks)
ax.set_yticks(yticks)
ax.set_xticklabels(class_labels_x, rotation=0, ha='center',fontsize=20)
ax.set_yticklabels(class_labels_y, rotation=90, va='center',fontsize=20)

for i in range(len(class_labels_x)):
    for j in range(len(class_labels_y)):
        cell_value = final_confusion_matrix[i, j]
        if not math.isnan(cell_value):  # Check if the value is not NaN
            text = f"${int(cell_value)}$"
        else:
            text = "NaN"
        plt.text(j, i, text, ha='center', va='center', color='red', fontsize=25)
plt.tight_layout()
cbar = fig.colorbar(cax)
#%% For saving the relevant variables and figures
# data = {
#         "Raw Background Images": no_bac_image,
#         "Fake Bacteria Images": fake_images_with_bacteria,
#         "Fake Bacteria Image Coordinates" : fake_images_bacteria_coordinates,
#         "Found Bacteria in Fake Bacteria Images": found_bacteria_in_fake_bacteria_image,
#         "Found Bacteria in Fake Bacteria Image Coordinates": found_bacteria_coordinates_in_fake_bacteria_image,
#         "Updated Found Bacteria in Fake Bacteria Image Coordinates": predicted_bacteria_coordinates,
#         "List of Confusion Matrix": list_of_ConfusionMatrix,
#         "Final Confusion Matrix" : final_confusion_matrix,
#         "List of Accuracy": list_of_accuracy,
#         "Mean Accuracy" : mean_accuracy,
#         "List of recall/sensitivity": list_of_recall,
#         "Mean recall/sensitivity": mean_recall_sensitivity,
#         "List of Precision": list_of_precision,
#         "Mean Precision": mean_precision,
#         "List of F1 Score" : list_of_f1_score,
#         "Mean F1 Score": mean_f1_score,
#         } 
# output_folder = 'path'
# output_name_trialno = "Image name"

# with open(output_folder + 'ObjectVariable_' + output_name_trialno +'.pkl', 'wb') as f:
#     pickle.dump(data, f)
# plt.savefig(output_folder+'Confusion_Matrix_'+output_name_trialno+'.png', dpi=300)

#%% For opening pickle file
# import pandas as pd
# input_folder = r"path"
# obj = pd.read_pickle(input_folder)