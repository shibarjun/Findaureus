<p align="center">
<img src = "https://github.com/shibarjun/Findaureus/blob/main/Images/Findaureus_icon_readme.gif" />
</p>

<h1 align="center" style="margin-top: 0px;">Find bacteria across confocal laser scanning microscopy (CLSM) obtained infected bone tissue images.</h1>

## Installation

For running the application
----------------------------------------------------------
1. Access the following link and click on the "Download Findaureus" button.
2. Choose the option to download the software as a ZIP file.
3. Once the download is complete, locate the downloaded ZIP file on your computer.
4. Extract the contents of the ZIP file using your preferred extraction tool, such as WinRAR or 7-Zip.
5. After extraction, a folder containing the extracted files will be created.
6. Open the extracted folder and locate the executable (EXE) file named "Findaureus".
7. Double-click on the EXE file to launch the software application.
8. You can now utilize the software as intended.

[Download Findaureus](https://github.com/shibarjun/Findaureus/releases/download/untagged-535b007f3400e6311660/Findaureus.zip)

Findaureus, currently under testing, is being evaluated using CZI (Carl Zeiss) file extensions infected mouse bone dataset. This choice is driven by the limited variety of datasets available for testing purposes. However, it's worth noting that the software is designed to accommodate other image file extensions as well, specifically ND2 (Nikon) and LIF (Leica). Users are encouraged to report any bugs via the Issues page on GitHub or via below contact. As the application gains wider usage, we will have the opportunity to engage with various file extensions, diverse tissue types, and bacteria. This will allow us to enhance the application through future updates, ensuring its continual improvement.

Contact: shibarjunmandal@gmail.com / shibarjun.mandal@leibniz.ipht.de

## Summary

Osteomyelitis is a serious bone infection where fluorescence imaging provides a detailed visualization of bone cells, structure, and bacteria from infected bone tissues. However, the resulting images can be complex and challenging to analyze, particularly when it comes to locating bacteria. 

Findaureus is an open-source Python-based application that helps researchers and clinicians quickly and accurately locate bacteria or bacterial regions in fluorescence images of infected bone tissue. This application provides easy-to-use tools and extracts relevant information, making it a powerful tool for researchers and clinicians alike. Findaureus has been compared to state-of-the-art algorithms and validated by real users from various research and clinical institutions, demonstrating its effectiveness in helping to identify and locate bacteria in infected bone tissue. 

## Screenshots

<p align="center">
<img src = "https://github.com/shibarjun/Findaureus/blob/main/Images/Screenshot_1.png" width="550" height="400" /><img src = "https://github.com/shibarjun/Findaureus/blob/main/Images/Screenshot_2.png" width="350" height="400" />   
</p>

## Demo

For the convenience of application testing, we provide two types of CZI extension image files: a tissue overview scan (3788 pixels (x) × 3788 pixels (y) × 3 (z) × 6 (channel)) and a detail scan (1316 pixels (x) × 1316 pixels (y) × 120 (z) × 4 (channel)). These files are currently publicly accessible and can be found in [here](https://github.com/shibarjun/Findaureus/releases/download/v1.0.0/Dataset.zip). Please ensure to [cite the article](https://www.mdpi.com/1422-0067/24/11/9762) if you utilize this data. It is important to note that all the image files belong to the referenced research article. However, hands-on demonstrations are available upon request. While waiting, you can enjoy the application demo video below.

<p align="center">
<img src = "https://github.com/shibarjun/FindAureus/blob/main/Images/Findaureus_Demo.gif" width="600" height="550" />   
</p>

We kindly request users to utilize the application with their own datasets, if available, and share any encountered error messages or feedback during usage. Your valuable input will greatly help us improve the functionality of the application and address any issues that may arise. Thank you for your cooperation and support!

## Citation
If you utilize any image file from the dataset for scientific publication or any other purpose, please remember to cite the below article.

Mandal S, Tannert A, Ebert C, Guliev RR, Ozegowski Y, Carvalho L, Wildemann B, Eiserloh S, Coldewey SM, Löffler B, Bastião Silva L, Hoerr V, Tuchscherr L, Neugebauer U. Insights into S. aureus-Induced Bone Deformation in a Mouse Model of Chronic Osteomyelitis Using Fluorescence and Raman Imaging. International Journal of Molecular Sciences. 2023; 24(11):9762. https://doi.org/10.3390/ijms24119762

## Acknowledgements

This project is a part of the European Union's Horizon 2020 research and innovation program under grant agreement No 861122 (ITN IMAGE-IN). We acknowledge support from the Jena Biophotonics and Imaging Laboratory (JBIL), from the European Union via EFRE funds within the Thüringer Innovationszentrum für Medizintechnik-Lösungen (ThIMEDOP, FKZ IZN 2018 0002), the BMBF via the funding program Photonics Research Germany (LPI, FKZ: 13N15713) and via the CSCC (FKZ 01EO1502) and the Institute of Anatomical and Molecular Pathology, University Coimbra, Portugal.
