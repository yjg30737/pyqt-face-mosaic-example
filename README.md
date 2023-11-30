# pyqt-face-mosaic-example
Simple PyQt software to de-identification each face in the image

## Requirements
* PyQt5 >= 5.14
* opencv-python

## How to Use
1. git clone ~
2. pip install -r requirements.txt
3. python main.py
4. Here is the GUI:

![image](https://github.com/yjg30737/pyqt-face-mosaic-example/assets/55078043/8b90d5a4-b308-45de-96df-70d4dd9f04b9)

Find the directory that includes images you want to apply mosaic.

Then, select the type of mosaic. There are two types of it. Face and Ped.

**"Face"** is using **"Haar Cascade"** which is specialized in face detection to mosaic the face. This is suitable for application on photos where the face occupies most of the space, such as ID photos.

**"Ped"** is using **"Hog Cascade"** which is specialized in pedestrian detection in street to mosaic the body. This is suitable for application on CCTV or Google Street View where pedestrians are visible.

Either way are suitable for de-identification.

One of the important factor of image dataset for public is de-identification each people in the photo. That's why i've made this !

### Preview

#### Face

![image](https://github.com/yjg30737/pyqt-face-mosaic-example/assets/55078043/2a13912d-40d0-42f0-a6bc-603bbd3ae77f)

#### Ped

![image](https://github.com/yjg30737/pyqt-face-mosaic-example/assets/55078043/cb74dd29-1681-402e-a85f-35eabaee9f3e)

