import math
import numpy as np
from PIL import Image

def getMappingWidth(smaller_num, bigger_num, i_in_smaller_num):
    ## this is for when the number of image provided doesnt match the width of the image
    ## example use:
    # a = 14
    # b = 20
    # for i in range(a):
    #     for j in range(getMappingWidth(a,b,i)):
    #         print("{:02d}".format(i)+"|",end="")
    # print()
    # for i in range(b):
    #     print("{:02d}".format(i)+"|",end="")
    ## it does this:
    ## 00|01|02|02|03|04|04|05|06|06|07|08|09|09|10|11|11|12|13|13|
    ## 00|01|02|03|04|05|06|07|08|09|10|11|12|13|14|15|16|17|18|19|
    if smaller_num == bigger_num:
        return 1
    return math.floor((bigger_num/smaller_num)*(i_in_smaller_num+1)) - math.floor((bigger_num/smaller_num)*(i_in_smaller_num))


def combine_vertical_columns(image_list):
    # get the height and width of the images in the list
    height = image_list[0].size[1]
    width = image_list[0].size[0]

    # create an empty image with the combined height and width of the images
    combined_image = Image.new('RGB', (width, height))

    # loop through each image in the list
    current_y = 0
    
    for i, image in enumerate(image_list):
        # convert the image to numpy array
        image_np = np.asarray(image)
        # print progress
        print(f"{i/len(image_list)*100}%")
        
        slotWidth = getMappingWidth(2592,2592,i)
        # get a slot with calculated width
        column = []
        for j in range(slotWidth):
            column.append(image_np[i+j])
        # combine the pixel values from each image into the combined image
        column_image = Image.fromarray(np.uint8(column))
        # paste the combined image into the final image
        combined_image.paste(column_image, (0, current_y))
        # move the y position for next pasting
        current_y += slotWidth
        if(i%200 == 0):
            # output a temp image every 200 image for minitoring
            combined_image.save("/output/Output_Temp.JPG")

    return combined_image


image_list = []

for i in range(2592):
    image_list.append(Image.open("/images/DSC0" + "{:04d}".format(2190+i) + ".JPG"))



combined_image = combine_vertical_columns(image_list)
combined_image.save("/output/Output.JPG")


