import os
import shutil
import random

# Paths
root_dir = '/student/vcheruku/Enhance-Data-Diversity-and-Robustness/yolo-for-single-class'
raw_images_dir = os.path.join(root_dir, 'raw_images')
images_dir = os.path.join(root_dir, 'images')
labels_dir = os.path.join(root_dir, 'labels')

# Destination splits
splits = ['train', 'test', 'val']

# Create necessary folders if they don't exist
for split in splits:
    os.makedirs(os.path.join(images_dir, split), exist_ok=True)
    os.makedirs(os.path.join(labels_dir, split), exist_ok=True)

# Get all images
all_images = [f for f in os.listdir(raw_images_dir) if f.lower().endswith('.png')]
random.shuffle(all_images)

# Calculate split sizes based on ratios
n = len(all_images)
n_train = int(n * 0.8)
n_test = int(n * 0.1)
n_val = n - n_train - n_test  # Remaining go to val

# Split the list
train_images = all_images[:n_train]
test_images = all_images[n_train:n_train + n_test]
val_images = all_images[n_train + n_test:]

# Helper function to move files
def move_files(file_list, split):
    for image_file in file_list:
        # Move image
        src_image_path = os.path.join(raw_images_dir, image_file)
        dst_image_path = os.path.join(images_dir, split, image_file)
        shutil.move(src_image_path, dst_image_path)

        # Move corresponding label
        if image_file.endswith('_endo.png'):
            label_file = image_file.replace('_endo.png', '_endo_color_mask.txt')
            src_label_path = os.path.join(labels_dir, label_file)
            dst_label_path = os.path.join(labels_dir, split, label_file)

            if os.path.exists(src_label_path):
                shutil.move(src_label_path, dst_label_path)
            else:
                print(f"Warning: Label file {label_file} not found for image {image_file}")

# Move files
move_files(train_images, 'train')
move_files(test_images, 'test')
move_files(val_images, 'val')

print("Successfully split images and labels into train (80%), test (10%), and val (10%).")
