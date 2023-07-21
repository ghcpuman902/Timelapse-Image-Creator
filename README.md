# Time-Lapse Image Creator

This Python program creates a unique visual art piece - a time-lapse image composed from a series of photographs. The program extracts vertical columns of pixels from each input photo and stitches them together to form a final composite image. This innovative approach allows the depiction of the passage of time in a single image.

## Features

![Features](Feature.jpg)

- **Time-lapse Image Creation**: The program creates a unique visual art piece - a time-lapse image composed from a series of photographs. It extracts vertical columns of pixels from each input photo and stitches them together to form a final composite image. This innovative approach allows the depiction of the passage of time in a single image.

- **Image Rotation**: The program can handle image rotation. If you wish to combine images from top to bottom, you can apply a 90º rotation to the images before processing.

- **Reverse Order**: The program allows you to reverse the order of images. This can be useful in certain scenarios where the time-lapse needs to be depicted in reverse chronological order.

- **Memory Profiling**: The program is equipped with a memory profiler that monitors the maximum memory usage. This is particularly useful when processing large images, as it helps in managing memory resources effectively.

- **Flexible Configuration**: The program comes with a `config.yaml` file that allows you to easily configure the input and output files, as well as additional options like image rotation and reverse order.

- **Supports JPG Format**: The program supports .JPG format for both input and output images. The output format will match the input format.

**Note**: The program does not support reflection.

## Installation and Running the Program

1. Clone the repository.
2. Install the required packages by running `pip install -r requirements.txt`.
3. Update the `config.yaml` file according to your needs. The comments in the file explain how its fields correspond to the program's functionality.
4. Run the program by executing `python main.py`.

**Note**: As this program can be memory intensive due to the processing of large images, it is equipped with a memory profiler that monitors the maximum memory usage. You can take advantage of this by adding `@profile` in front of `process_single_image` then run `python -m memory_profiler main.py`, like this:
```
@profile
def process_single_image(image, slice_index, slice_width, is_horizontal):
# rest of the code
```

## Configuration

The configurations for input and output files as well as additional options are stored in the `config.yaml` file.

```
# Configuration for the time-lapse image creation program

input:
  dir: "./test_imgs/"  # Directory where the input images are stored
  file_prefix: "output_"  # Prefix of the input image files
  file_number_digit_length: 4  # Number of digits in the file number
  file_begin_digit: 1  # Starting number of the image files
  file_end_digit: 360  # Ending number of the image files
  file_suffix: "JPG"  # File extension of the image files

  # the default config will load image ./test_imgs/output_0001.JPG to ./test_imgs/output_0360.JPG 

output:
  dir: "./output/"  # Directory where the output image will be saved

options:
  is_reversed: False  # Option to reverse the order of the images
```

**Note**: output format will match input format, so .JPG will result in a .JPG file

## Example

![Screenshot of list of images](Screenshot.png)
The repository includes test images that correspond to the default YAML configurations. You can run the code directly to generate a time-lapse image. The expected result is shown below:
![Example output](ExampleOutput.JPG)