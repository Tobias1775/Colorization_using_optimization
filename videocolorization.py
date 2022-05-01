from os import path
import cv2
import imageio
import numpy as np
from scipy.linalg import solve
from scipy.sparse.linalg import spsolve
from scipy import sparse
from colorization import colorization,get_neighborhood

def lucas_kanade(gray,last_gray,last_mark):
    m,n = gray.shape[0],gray.shape[1]
    grad_x,grad_y = np.gradient(last_gray[:,:,0])
    output = gray.copy()
    gray = gray[:,:,0]
    last_gray = last_gray[:,:,0]
    for i in range(m):
        for j in range(n):
                A = []
                b = []
                cor = i,j
                neighborhood = get_neighborhood(cor,gray)
                
                for pixel in neighborhood:
                    A.append([ grad_x[ pixel[0],pixel[1] ] , grad_y[ pixel[0],pixel[1] ] ])
                    b.append([ float(last_gray[ pixel[0],pixel[1]]) - float(gray[ pixel[0],pixel[1]]) ])
                
                try:
                    v = solve(np.dot(np.transpose(A),A),np.dot(np.transpose(A),b))
                except:
                    v = [0,0]
                new_i,new_j = int(i+v[0]),int(j+v[1])
                new_i,new_j = max(0,new_i),max(0,new_i)
                new_i,new_j = min(m-1,new_i),min(n-1,new_j)
                
                output[new_i,new_j,1] = last_mark[i,j,1]
                output[new_i,new_j,2] = last_mark[i,j,2]

    return output

def main():
    scr_dir = 'D:\Program\pythonworkspace\colorization_using_optimization\input'
    out_dir = 'D:\Program\pythonworkspace\colorization_using_optimization\output\lake'
    gray,last_gray,result,mark = None,None,None,None
    all_gray = imageio.mimread(path.join(scr_dir,'lake-gray.gif'))
    for i in range(len(all_gray)):
        last_gray = gray
        last_mark = mark
        gray = cv2.imread(path.join(scr_dir,'lake\lake_gray\\frame%d.bmp'%i))
        gray = cv2.cvtColor(gray,cv2.COLOR_BGR2YUV)
        if path.exists(path.join(scr_dir,'lake\lake_mark\\frame%d.bmp'%i)):
            mark = cv2.imread(path.join(scr_dir,'lake\lake_mark\\frame%d.bmp'%i))
            mark = cv2.cvtColor(mark,cv2.COLOR_BGR2YUV)
        else:
            mark = lucas_kanade(gray,last_gray,result)
            cv2.imwrite(path.join(out_dir,'mark%d.bmp'%i),mark)
    
        result = colorization(mark,gray)
        result_image = cv2.cvtColor(result,cv2.COLOR_YUV2BGR)
        cv2.imwrite(path.join(out_dir,'frame%d.bmp'%i),result_image)


main()
            





    
