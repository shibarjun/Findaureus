<p align="center">
<img src = "https://github.com/shibarjun/Findaureus/blob/main/Images/Findaureus_icon_readme.gif" />
</p>

<h1 align="center" style="margin-top: 0px;">Find bacteria across confocal laser scanning microscopy (CLSM) obtained infected bone tissue images.</h1>


## Running the application

1. Go to the latest release or click on this [link](https://github.com/shibarjun/Findaureus/releases/download/untagged-9eee0dd3fb29d6cdb9d4/Findaureus.zip) to download the Findaureus.zip file.
2. Use your preferred extraction tool, such as WinRAR or 7-Zip, to extract the ZIP file's contents.
3. Double-click on the "Findaureus" shortcut in the extracted folder to open the application.
4. Now you can use the software as intended.

Findaureus is currently undergoing testing on an infected mouse bone dataset with CZI file extensions. This choice was made due to the limited variety of datasets available for testing purposes. However, it's worth noting that the software has been designed to support other image file extensions, specifically ND2 (Nikon) and LIF (Leica). Users are encouraged to report any bugs they encounter via the Issues page on GitHub or through the contact information provided below. As the application gains wider usage, we will have the opportunity to engage with various file extensions, diverse tissue types, and bacteria. This will allow us to improve the application through future updates, ensuring it continues to enhance its functionality.

Contact: shibarjunmandal@gmail.com / shibarjun.mandal@leibniz.ipht.de

## Summary

Osteomyelitis is a serious bone infection where fluorescence imaging provides a detailed visualization of bone cells, structure, and bacteria from infected bone tissues. However, the resulting images can be complex and challenging to analyze, particularly when it comes to locating bacteria. 

Findaureus is an open-source Python-based application that helps researchers and clinicians quickly and accurately locate bacteria or bacterial regions in fluorescence images of infected bone tissue. This application provides easy-to-use tools and extracts relevant information, making it a powerful tool for researchers and clinicians alike. Findaureus has been compared to state-of-the-art algorithms and validated by real users from various research and clinical institutions, demonstrating its effectiveness in helping to identify and locate bacteria in infected bone tissue. 

## Screenshots

<p align="center">
<img src = "https://github.com/shibarjun/Findaureus/blob/main/Images/Screenshot_1.png" width="550" height="400" /><img src = "https://github.com/shibarjun/Findaureus/blob/main/Images/Screenshot_2.png" width="350" height="400" />   
</p>

## Demo

To facilitate application testing, we offer two types of CZI extension image files: a tissue overview scan (3788 x 3788 x 3 x 6) and a detailed scan (1316 x 1316 x 120 x 4). These files are currently available to the public and can be found at the latest release or [here](https://github.com/shibarjun/Findaureus/releases/download/v1.0.0/Dataset.zip). If you use this data for scientific publication or any other purpose, please cite this [article](https://www.mdpi.com/1422-0067/24/11/9762). Please note that all image files belong to the referenced research article. Upon request, we can provide demonstrations with additional image files that are not included in the repository.

<p align="center">
<img src = "https://github.com/shibarjun/FindAureus/blob/main/Images/Findaureus_Demo.gif" width="600" height="550" />   
</p>

We kindly request users to utilize the application with their own datasets, if available, and share any encountered error messages or feedback during usage. Your valuable input will greatly help us improve the functionality of the application and address any issues that may arise. Thank you for your cooperation and support!

## Citation
If you utilize any image file from the dataset for scientific publication or any other purpose, please remember to cite the below article.

Mandal S, Tannert A, Ebert C, Guliev RR, Ozegowski Y, Carvalho L, Wildemann B, Eiserloh S, Coldewey SM, Löffler B, Bastião Silva L, Hoerr V, Tuchscherr L, Neugebauer U. Insights into S. aureus-Induced Bone Deformation in a Mouse Model of Chronic Osteomyelitis Using Fluorescence and Raman Imaging. International Journal of Molecular Sciences. 2023; 24(11):9762. https://doi.org/10.3390/ijms24119762

## Acknowledgements

This project is a part of the European Union's Horizon 2020 research and innovation program under grant agreement No 861122 (ITN IMAGE-IN). We acknowledge support from the Jena Biophotonics and Imaging Laboratory (JBIL), from the European Union via EFRE funds within the Thüringer Innovationszentrum für Medizintechnik-Lösungen (ThIMEDOP, FKZ IZN 2018 0002), the BMBF via the funding program Photonics Research Germany (LPI, FKZ: 13N15713) and via the CSCC (FKZ 01EO1502) and the Institute of Anatomical and Molecular Pathology, University Coimbra, Portugal.
