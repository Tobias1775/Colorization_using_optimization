import cv2
from os import path
scr_dir = 'D:\Program\pythonworkspace\colorization_using_optimization\input'
out_dir = 'D:\Program\pythonworkspace\colorization_using_optimization\input'
gray = cv2.imread(path.join(scr_dir,'mark_girl.bmp'),cv2.IMREAD_GRAYSCALE)
cv2.imwrite(path.join(out_dir, "gray_girl.jpg"),gray)