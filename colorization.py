from types import AsyncGeneratorType
import cv2
import numpy as np
from scipy.sparse import lil_matrix as lil_matrix
from scipy.sparse import linalg as linalg
from os import path
import mpmath

def get_points(gray):
    row,col = gray.shape[0],gray.shape[1]
    pt = []
    for i in range(row):
        for j in range(col):
            pt.append((i,j))
    return pt

def get_neighborhood(cor,gray):
    i,j = cor
    neighborhood = []
    x_upperbound,y_upperbound = gray.shape[0],gray.shape[1]
    for x in range(i-1,i+2):
        if x >= 0 and x < x_upperbound:
            for y in range(j-1,j+2):
                if y >= 0 and y < y_upperbound:
                    neighborhood.append((x,y))
    neighborhood.remove((i,j))
    return neighborhood

def get_sigma(gray,neighborhood):
    return np.std([gray[x] for x in neighborhood])

def get_weight(r,s,sigma):
    if sigma != 0: 
        weight = np.exp( -1*(r-s)**2 / (2*sigma**2) ) ** 5
    else: 
        weight = 1
    return weight

def colorization(mark,unmark):
    gray = unmark[:,:,0]
    n = gray.size
    pt = get_points(gray)
    b1 = np.zeros(n)
    b2 = np.zeros(n)
    weight_matrix = lil_matrix((n,n),dtype=float)
    row,col = gray.shape[0],gray.shape[1]
    for i,cor in enumerate(pt):
        x,y = cor
        weight_matrix[i,i] = 1.
        
        if abs(float(mark[x,y,0])-float(unmark[x,y,0])) > 0 or abs(float(mark[x,y,1]) - float(unmark[x,y,1])) > 0 or abs(float(mark[x,y,2]) - float(unmark[x,y,2])) > 0:
            b1[i] = mark[x,y,1]
            b2[i] = mark[x,y,2]
            continue
        
        neighborhood = get_neighborhood(cor,gray)
        sigma = get_sigma(gray,neighborhood)
        weights = []
        sum = 0
        for k in range(len(neighborhood)):
                if sigma>0:
                    r = gray[cor]
                    s_cor = neighborhood[k]
                    s = gray[s_cor]
                    w = get_weight(float(r),float(s),sigma)
                    weights.append(w)
                    sum += w
                else:
                    weights.append(1)
                    sum += 1.
        for k in range(len(neighborhood)):
                weights[k] /= sum
                x,y = neighborhood[k]
                weight_matrix[i,x*col+y] = -1*weights[k]

    weight_matrix = weight_matrix.tocsc()
    
    x1 = linalg.spsolve(weight_matrix,b1)
    x2 = linalg.spsolve(weight_matrix,b2)
    
    composite = np.copy(unmark)
    
    for i,cor in enumerate(pt):
        x,y = cor
        composite[x,y,1],composite[x,y,2] = x1[i],x2[i]
    
    return composite
    

def main():
    scr_dir = 'D:\Program\pythonworkspace\colorization_using_optimization\input'
    out_dir = 'D:\Program\pythonworkspace\colorization_using_optimization\output'
    rgb_mark = cv2.imread(path.join(scr_dir,'example4_new.png'))
    rgb_gray = cv2.imread(path.join(scr_dir,'example4.png'))
    mark = cv2.cvtColor(rgb_mark,cv2.COLOR_BGR2YUV)
    gray = cv2.cvtColor(rgb_gray,cv2.COLOR_BGR2YUV)
    result = colorization(mark,gray)
    result = cv2.cvtColor(result,cv2.COLOR_YUV2BGR)
    cv2.imwrite(path.join(out_dir, "example4_new.png"), result)

if __name__ == '__main__':
    main()