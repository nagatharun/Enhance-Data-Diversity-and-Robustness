# Code to check is all the images have corresponding labels

import os

# Paths
root_dir = '/student/vcheruku/Enhance-Data-Diversity-and-Robustness/yolo-for-single-class'
raw_images_dir = os.path.join(root_dir, 'raw_images')
labels_dir = os.path.join(root_dir, 'labels')

# Get all image files
image_files = [f for f in os.listdir(raw_images_dir) if f.lower().endswith('.png')]

# Check for matching labels
missing_labels = []
for image_file in image_files:
    # Derive label file name
    expected_label = image_file.replace('_endo.png', '_endo_color_mask.txt')
    
    # Check if label exists
    label_path = os.path.join(labels_dir, expected_label)
    if not os.path.exists(label_path):
        missing_labels.append((image_file, expected_label))

# Report
if missing_labels:
    print(f"{len(missing_labels)} missing label(s) found!")
    for image_file, expected_label in missing_labels:
        print(f"Image '{image_file}' has no corresponding label '{expected_label}'")
else:
    print("All images have corresponding labels.")
