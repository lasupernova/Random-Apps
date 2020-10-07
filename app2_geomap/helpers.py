import pandas as pd 
import cv2 

#produces a specific color based on input
def color_by_elevation(elevation):
    if elevation < 2500:
        return 'green'
    elif elevation >= 2500:
        return 'orange'

#checks if filename exists in folder
def check_file_name(filename):
    return f'{filename}.jpg' in os.listdir('pics')

# returns values for proportionally resized dimensions of .jpeg-files
def resize_pic(picname, path, maxsize=200):
    # get current .jpeg-file dimensions
    im = cv2.imread(f'{path}\{picname}.jpg')

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

#class creating an pandas dataframe object containing text info to include html-string passed to folium.Marker() popup argument
class InfoFile():
    # initiate InfoFile object using a file-path and engine (e.g:'odf')
    def __init__(self, path, engine):
        self.file = pd.read_excel(path, engine=engine).set_index('Name')

    # returns info as text-string
    def get_info(self, info_name):
        return self.file.loc[info_name,'Text']