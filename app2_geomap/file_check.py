import os 

# return f'{picname}.jpg' in os.listdir('pics')

import cv2

# for pic in os.listdir('pics'):
#     im = cv2.imread(f'pics\{pic}')
#     print(f'{pic}:')
#     print(type(im))
#     # <class 'numpy.ndarray'>

#     if im.shape[0] > im.shape[1]:
#         height = 200
#         shrink_factor = 200/im.shape[0]
#         width = im.shape[1]*shrink_factor
#     else:
#         width = 200
#         shrink_factor = 200/im.shape[1]
#         height = im.shape[0]*shrink_factor
#     print(f'shape before: width={im.shape[1]} height={im.shape[0]}\nshape after: width={width} height={height}')
#     # (225, 400, 3)
    # <class 'tuple'>

# returns values for proportionally resized dimensions of .jpeg-files
def resize_pic(picname, path, maxsize=200):
    # get current .jpeg-file dimensions
    im = cv2.imread(f'{path}\{picname}.jpg')
    print(im)
    #get modified dimensions
    if im.shape[0] > im.shape[1]: #if picture is vertical
        height = maxsize
        shrink_factor = maxsize/im.shape[0]
        width = im.shape[1]*shrink_factor
    else: #if picture is horizontal
        width = maxsize
        shrink_factor = maxsize/im.shape[1]
        height = im.shape[0]*shrink_factor

    # return modified dimensions
    return height, width

print(resize_pic('Unisphere', 'monkey_pics'))