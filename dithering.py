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

def addSquare(point):
    return dataset[int(np.round(point))]
    pass

def formLine(row):
    line = addSquare(row[0])
    for i in range(1, row.shape[0]):
        line = np.concatenate((line, addSquare(row[i])), axis=1)
    return line
    pass

def basicDithering(img):
    container = np.array(img, dtype = np.uint16)
    container = np.round(9*container/255)
    aux = formLine(container[0])
    for i in range(1, container.shape[0]):
        aux = np.concatenate((aux, formLine(container[i])))
    aux = np.array(aux, dtype = np.uint8)
    aux = cv2.cvtColor(aux, cv2.COLOR_GRAY2RGB)
    cv2.imwrite("basicDithImage.png", aux)
    pass

def floydSteinbergDithering(img):
    container = np.copy(img)
    for i in range(0, container.shape[0] - 1):
        for j in range(0, container.shape[1] - 1):
            oldp = container[i][j]
            newp = round(oldp / 255) * 255
            container[i][j] = newp
            error = oldp - newp
            container[i + 1][j    ] = min(255, container[i + 1][j    ] + error * 7 / 16)
            container[i - 1][j + 1] = min(255, container[i - 1][j + 1] + error * 3 / 16)
            container[i    ][j + 1] = min(255, container[i    ][j + 1] + error * 5 / 16)
            container[i + 1][j + 1] = min(255, container[i + 1][j + 1] + error * 1 / 16)
    container = cv2.cvtColor(container, cv2.COLOR_GRAY2RGB)
    cv2.imwrite("basicDithImage.png", container)
    plt.imshow(container)
    plt.show()
    pass

img = cv2.cvtColor(cv2.imread("lena.png"), cv2.COLOR_BGR2GRAY)
#basicDithering(img)
floydSteinbergDithering(img)