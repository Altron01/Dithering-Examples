#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 11:07:01 2017

@author: altron01
"""


dataset = [[[1  , 1  , 1  ],
            [1  , 1  , 1  ], 
            [1  , 1  , 1  ]],

           [[1  , 1  , 1  ],
            [1  , 255, 1  ], 
            [1  , 1  , 1  ]],
            
           [[1  , 1  , 1  ],
            [255, 255, 1  ], 
            [1  , 1  , 1  ]],
            
           [[1  , 1  , 1  ],
            [255, 255, 1  ], 
            [1  , 255, 1  ]],
            
           [[1  , 1  , 1  ],
            [255, 255, 255], 
            [1  , 255, 1  ]],
            
           [[1  , 1  , 255],
            [255, 255, 255], 
            [1  , 255, 1  ]],
            
           [[1  , 1  , 255],
            [255, 255, 255], 
            [255, 255, 1  ]],
            
           [[255, 1  , 255],
            [255, 255, 255], 
            [255, 255, 1  ]],
            
           [[255, 1  , 255],
            [255, 255, 255], 
            [255, 255, 255]],
            
           [[255, 255, 255],
            [255, 255, 255], 
                [255, 255, 255]]]
import numpy as np
from matplotlib import pyplot as plt
import cv2
import time

def normalized_values():
    val = []
    for i in range(0, 256):
        val.append(int(9*i/255))
    return val
    pass

def addSquare(point, nvalues):
    return dataset[nvalues[point]]
    pass

def formLine(row, nvalues):
    line = addSquare(row[0], nvalues)
    for i in range(1, row.shape[0]):
        line = np.concatenate((line, addSquare(row[i], nvalues)), axis=1)
    return line
    pass

#Pattern Dither
def basicDithering(img):
    stime = time.time()
    nvalues = normalized_values()
    container = formLine(img[0], nvalues)
    for i in range(1, img.shape[0]):
        container = np.concatenate((container, formLine(img[i], nvalues)))
    container = np.array(container, dtype = np.uint8)
    container = cv2.cvtColor(container, cv2.COLOR_GRAY2RGB)
    cv2.imwrite("BasicDithImage.png", container)
    ftime = time.time() - stime
    print(ftime)
    pass

#Raster Scan
def floydSteinbergRasterDithering(img):
    stime = time.time()
    container = np.copy(img)
    for i in range(0, container.shape[0] - 1):
        for j in range(0, container.shape[1] - 1):
            oldp = container[i][j]
            newp = round(oldp / 255) * 255
            container[i][j] = newp
            error = oldp - newp
            container[i + 1][j    ] += error * 7 / 16
            container[i - 1][j + 1] += error * 3 / 16
            container[i    ][j + 1] += error * 5 / 16
            container[i + 1][j + 1] += error * 1 / 16
    container = cv2.cvtColor(container, cv2.COLOR_GRAY2RGB)
    cv2.imwrite("RasterDithering.png", container)
    ftime = time.time() - stime
    print(ftime)
    pass

#Serpentine Scan
def floydSteinbergSerpentineDithering(img):
    stime = time.time()
    container = np.copy(img)
    d = [container.shape[1] - 1, 0]
    dire = -1
    for i in range(0, container.shape[0] - 1):
        dire = -dire
        aux = d[0]
        d[0] = d[1]
        d[1] = aux
        for j in range(d[0], d[1]):
            oldp = container[i][j]
            newp = round(oldp / 255) * 255
            container[i][j] = newp
            error = oldp - newp
            container[i + 1][j       ] += error * 7 / 16
            container[i - 1][j + dire] += error * 3 / 16
            container[i    ][j + dire] += error * 5 / 16
            container[i + 1][j + dire] += error * 1 / 16
    container = cv2.cvtColor(container, cv2.COLOR_GRAY2RGB)
    cv2.imwrite("SnakeDithering.png", container)
    ftime = time.time() - stime
    print(ftime)
    pass
img = cv2.cvtColor(cv2.imread("lena.png"), cv2.COLOR_BGR2GRAY)
basicDithering(img)
floydSteinbergRasterDithering(img)
floydSteinbergSerpentineDithering(img)