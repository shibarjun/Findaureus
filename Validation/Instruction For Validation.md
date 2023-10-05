For validation purpose
----------------------------------------------------------
1. Navigate to the Validation directory.
2. Extract the Bacterial Dataset file, which contains bacterial images.
3. If necessary, ensure that the "Bacterial Dataset" path is correctly specified in the `MakeBacterialImagesFunctions.py` file.
4. Open a command prompt or terminal in the Validation directory.
5. Use the following command to install all the dependencies from the `requirements.txt` file:
   ```
   pip install -r requirements.txt
   ```
6. After the dependencies are installed successfully, proceed to the next step.
7. Run the preferred validation technique file, such as `Validate_main_*validation technique*.py`.
9. Select the CZI image file with multiple z planes named "Mandal_etal_ijms_2023_Detail scan_(bacteria channel Lime)" from the Dataset.zip that comes with the release.
10. Uncomment the lines in the script to enable the saving of the validation results.
