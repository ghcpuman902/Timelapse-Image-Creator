import os
import time
import gc
import yaml
from itertools import islice
from PIL import Image, ImageOps
from concurrent.futures import ThreadPoolExecutor, as_completed
from memory_profiler import profile
import numpy as np
from datetime import datetime

# Global variable to set the batch size for processing images
BATCH_SIZE = 100

def get_linear_mapping(smaller_num, bigger_num, index):
    """
    This function is used to map a smaller number domain to a bigger number domain linearly.
    """
    if smaller_num == bigger_num:
        return 1
    width_ratio = bigger_num / smaller_num
    return round(width_ratio * (index + 1)) - round(width_ratio * index)

def divide_into_batches(iterable, size):
    """
    This function divides the iterable into batches of a specified size.
    """
    it = iter(iterable)
    return iter(lambda: tuple(islice(it, size)), ())

def get_image_orientation(image):
    """
    Extract image orientation metadata.
    """
    exif = image._getexif()
    if exif is not None:
        orientation = exif.get(274, 1)
        # Map the EXIF orientation to degrees clockwise
        if orientation == 6:
            return 270
        elif orientation == 8:
            return 90
        elif orientation == 3:
            return 180
        else:
            return 0
    else:
        return 0

def process_single_image(image_path, slice_index, slice_width, is_horizontal):
    """
    Process individual image, extracting slices.
    """
    with Image.open(image_path) as image:
        image_np = np.array(image)
        if is_horizontal:
            image_slice = image_np[:, slice_index:slice_index+slice_width]
        else:
            image_slice = image_np[slice_index:slice_index+slice_width, :]
    del image_np
    gc.collect()
    return image_slice

def create_time_lapse(image_paths, is_horizontal):
    """
    Combination of images to create the time-lapse.
    """
    # Initialize blank canvas for final image
    with Image.open(image_paths[0]) as first_image:
        if is_horizontal:
            target_image_side_length = first_image.width
        else:
            target_image_side_length = first_image.height
        combined_image = np.zeros((first_image.height, first_image.width, 3), dtype=np.uint8)
    current_index = 0
    batches = list(divide_into_batches(image_paths, BATCH_SIZE))  # Divide image list into batches
    total_batches = len(batches)  # Get total number of batches
    with ThreadPoolExecutor(max_workers=12) as executor:
        for batch_index, image_batch in enumerate(batches):
            slice_futures = []
            for index, image_path in enumerate(image_batch):
                slice_width = get_linear_mapping(len(image_paths), target_image_side_length, index)
                future = executor.submit(process_single_image, image_path, current_index, slice_width, is_horizontal)
                slice_futures.append((future, current_index, slice_width))
                current_index += slice_width
            for future, start_index, slice_width in slice_futures:
                image_slice = future.result()
                if is_horizontal:
                    combined_image[:, start_index:start_index+slice_width] = image_slice
                else:
                    combined_image[start_index:start_index+slice_width, :] = image_slice
            print(f"Batch {batch_index + 1}/{total_batches} completed")  # Print total number of batches
            gc.collect()

    # Finalize the combined image
    final_image = Image.fromarray(combined_image)
    return final_image

def validate_config(config):
    """
    Validate configuration parameters.
    """
    assert os.path.isdir(config['input']['dir']), "Input directory does not exist."
    assert os.path.isdir(config['output']['dir']), "Output directory does not exist."
    assert isinstance(config['input']['file_number_digit_length'], int), "File number digit length must be an integer."
    assert config['input']['file_number_digit_length'] > 0, "File number digit length must be a positive integer."

@profile
def main():
    """
    Main driver function.
    """
    with open('config.yaml') as config_file:
        config = yaml.safe_load(config_file)

    # Validate configuration
    validate_config(config)

    # Extract configuration params
    input_dir = config['input']['dir']
    output_dir = config['output']['dir']
    file_prefix = config['input']['file_prefix']
    file_number_digit_length = config['input']['file_number_digit_length']
    file_begin_digit = config['input']['file_begin_digit']
    file_end_digit = config['input']['file_end_digit']
    file_suffix = config['input']['file_suffix']
    total_images = file_end_digit - file_begin_digit + 1
    is_reversed = config['options']['is_reversed']

    image_paths = []

    # Load image paths
    start_time = time.time()
    for i in range(file_begin_digit, file_end_digit+1):
        filename = f"{file_prefix}{str(i).zfill(file_number_digit_length)}.{file_suffix}"
        filepath = os.path.join(input_dir, filename)
        if os.path.isfile(filepath):
            image_paths.append(filepath)
        else:
            print(f"File {filename} not found.")

    first_image_file = f"{file_prefix}{str(file_begin_digit).zfill(file_number_digit_length)}.{file_suffix}"
    orientation = get_image_orientation(Image.open(os.path.join(input_dir, first_image_file)))

    if is_reversed ^ (orientation in [270, 180]):
        image_paths.reverse()  # More efficient than image_paths[::-1]

    is_horizontal = (orientation in [0, 180])

    final_image = create_time_lapse(image_paths, is_horizontal)

    if orientation != 0: 
        final_image = final_image.rotate(orientation, expand=True)

    # Get current date and time
    now = datetime.now()
    timestamp = now.strftime("%y%m%d_%H%M%S")
    final_image.save(os.path.join(output_dir, f"_{timestamp}.{file_suffix}"))

    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")

if __name__ == "__main__":
    main()