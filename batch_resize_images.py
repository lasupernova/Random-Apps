# import libraries
import cv2
import os

class ToResize():
    def __init__(self,path_to_folder):
        self.path = path_to_folder
        self.files = self.find_images()
        self.output_dir = f"{self.path}/resized_img_output"

    def find_images(self):
        # create list
        files= []
        # iterate over files in folder
        for file in os.listdir(f"{self.path}"):
            # check if file is an image
            if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".bmp") or file.endswith(".png") or file.endswith(".tiff"):
                files.append(file)
        return files


    def resize_all(self, output_size=(100,100)):
        # create output-directory if it does not already exist
        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)
        for file in self.files:
         #load image and save in variable
            img = cv2.imread(f"{self.path}/{file}", 1) 

            # resize image
            resized_img = cv2.resize(img,output_size)

            # get filename enad extension
            filename, file_extension = os.path.splitext(f'{file}')
            #modify filename
            filename += f"_resized"

            #save resized image into file using filename and extension
            cv2.imwrite(f"{self.path}/resized_img_output/{filename}{file_extension}",resized_img) 
        print(f"{len(self.files)} images successfully resized! :)")
        return 1

if __name__ == "__main__":
    ToResize("media").resize_all()
