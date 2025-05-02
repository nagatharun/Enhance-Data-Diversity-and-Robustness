# Code to rename labels to match with the name of image
import os

# Set your directories for images and labels
image_dirs = {
    'train': '/student/vcheruku/Enhance-Data-Diversity-and-Robustness/yolo-for-single-class/images/train',
    'test': '/student/vcheruku/Enhance-Data-Diversity-and-Robustness/yolo-for-single-class/images/test',
    'val': '/student/vcheruku/Enhance-Data-Diversity-and-Robustness/yolo-for-single-class/images/val'
}

label_dirs = {
    'train': '/student/vcheruku/Enhance-Data-Diversity-and-Robustness/yolo-for-single-class/labels/train',
    'test': '/student/vcheruku/Enhance-Data-Diversity-and-Robustness/yolo-for-single-class/labels/test',
    'val': '/student/vcheruku/Enhance-Data-Diversity-and-Robustness/yolo-for-single-class/labels/val'
}

# Iterate over all directories (train, test, val)
for data_split in ['train', 'test', 'val']:
    images_dir = image_dirs[data_split]
    labels_dir = label_dirs[data_split]
    
    # Get all image files in the current set
    image_files = [f for f in os.listdir(images_dir) if f.endswith('.png')]  # Adjust the extension if necessary

    # Iterate through image files and rename corresponding .txt files
    for image_file in image_files:
        image_name = os.path.splitext(image_file)[0]  # Get the name without extension
        label_file = f'{image_name}.txt'  # Create the corresponding .txt file name
        label_file_old = f'{image_name}_color_mask.txt'  # Old .txt file name

        label_path_old = os.path.join(labels_dir, label_file_old)
        label_path_new = os.path.join(labels_dir, label_file)

        # Check if the old label file exists, then rename it
        if os.path.exists(label_path_old):
            os.rename(label_path_old, label_path_new)
        else:
            print(f'Label file not found: {label_path_old}')

print('Renaming completed!')
