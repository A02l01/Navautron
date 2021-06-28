# Navautron
Some tools to design your own **Navautron**
(as in 1. A. Barbacci, O. Navaud, M. Mbengue, M. Barascud, L. Godiard, M. Khafif, A. Lacaze, S. Raffaele, 
Rapid identification of an Arabidopsis NLR gene as a candidate conferring susceptibility to Sclerotinia 
sclerotiorum using time‐resolved automated phenotyping . Plant J., 1–15 (2020).)

- **taking_picture** directory contains the python script we used to take picture without autofocus. 
 **NB: this script take a picture per camera plug to the computer. The time between pictures is counted 
 by the cron daemon. In other words, the cron daemon executes this script every n seconds**
 
 - **making_box** directory contains svg file for laser cut. **Do not forget to draw a hole on the top of the box for the camera**. 
 Great online can used to draw a Navautron box e.g. https://fr.makercase.com/#/basicbox
 
 - **calibration** directory contains material for fish-eye camera calibration. 
      - In a first step distortion and intrinsics camera matrix must be computed on the basis of ~15 pictures of a grid (grille_calibration.svg). 
 The script to_calibrate_a_cam.py can be modify (an alternative is using calibration software such as https://github.com/Abhijit-2592/camera_calibration_API). 
      - In second step, pictures must be undistorded on the basis on the latter matrix using image_calibration.py script (or other script available on internet).
  
  Good luck
