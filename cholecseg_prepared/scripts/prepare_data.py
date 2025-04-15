import os
import shutil
import cv2
import numpy as np
import random

#create and give all necessary i/o paths
def initialize_paths():
    base_input = "CholecSeg8k"# raw directory structure location downladed from kaggle 
    base_output = "cholecseg_prepared" #processed data structure location

    paths = 
    {
        "input": base_input,"output": base_output,
        "raw_images": os.path.join(base_output, 'raw_images'), #raw image folder
        "mask_images": os.path.join(base_output, 'mask_images'), # mask images folder
        "labels": os.path.join(base_output, 'labels'),# folder for all label files
        "train_images": os.path.join(base_output, 'images/train'),
        "val_images": os.path.join(base_output, 'images/val'),
        "test_images": os.path.join(base_output, 'images/test'),
        "train_labels": os.path.join(base_output, 'labels/train'),
        "val_labels": os.path.join(base_output, 'labels/val'),
        "test_labels": os.path.join(base_output, 'labels/test'),
    }
    for key, path in paths.items():# create directory if it doesnt exist
        if key != "input" and not os.path.exists(path):
            os.makedirs(path)
    return paths

#copy raw images and its color masks seperately into seperate folders and rename their filenames
def copy_and_rename_images(paths):
    raw_path = paths["raw_images"]
    mask_path = paths["mask_images"]
    input_path = paths["input"]

    for video_folder in os.listdir(input_path):
        video_path = os.path.join(input_path, video_folder)
        if not os.path.isdir(video_path):
            continue
        for subfolder in os.listdir(video_path):
            sub_path = os.path.join(video_path, subfolder)
            for file in os.listdir(sub_path):
                full_file_path = os.path.join(sub_path, file)
                renamed = f"{video_folder}_{subfolder}_{file}"
                if "color_mask" in file:
                    shutil.copy(full_file_path, os.path.join(mask_path, renamed))
                elif "endo.png" in file and "mask" not in file:
                    shutil.copy(full_file_path, os.path.join(raw_path, renamed))

#color to class mapping according to rgb values
def initialize_mappings():
    color_class_mapping = 
    {
        (127, 127, 127): 0,(210, 140, 140): 1,(255, 114, 114): 2,(231, 70, 156): 3,(186, 183, 75): 4,(170, 255, 0): 5,(255, 85, 0): 6,(255, 0, 0): 7,(255, 255, 0): 8,(169, 255, 184): 9,(255, 160, 165): 10,(0, 50, 128): 11,(111, 74, 0): 12
    }
    return color_class_mapping

#write .txt polygon label files for each object class contour 
def write_polygon_file(class_contour_mapping, height, width, output_path, img_base):
    file_path = os.path.join(output_path, img_base + ".txt")
    with open(file_path, "w") as f:
        for class_id, contours in class_contour_mapping.items():
            for cnt in contours:
                if cv2.contourArea(cnt) < 20:
                    continue
                line = f"{class_id}"
                for point in cnt:
                    x, y = point[0]
                    x_norm = round(x / width, 6)
                    y_norm = round(y / height, 6)
                    line += f" {x_norm} {y_norm}"
                f.write(line + "\n")

#generate polygon label files from mask images using contours
#iterate through each mask image and detect rgb values and for each color find its shape , group the contoursby class id then call write_polygon_file to ave the contours 
def generate_yolov11_annotations(paths, color_class_mapping):
    mask_dir = paths["mask_images"]
    label_dir = paths["labels"]
    os.makedirs(label_dir, exist_ok=True)
    mask_files = sorted(os.listdir(mask_dir))
    for mask_file in mask_files:
        mask_path = os.path.join(mask_dir, mask_file)
        mask_img = cv2.cvtColor(cv2.imread(mask_path), cv2.COLOR_BGR2RGB)
        h, w, _ = mask_img.shape
        base_name = os.path.splitext(mask_file)[0]
        pixels = mask_img.reshape(-1, 3)
        unique_colors = np.unique(pixels, axis=0)
        class_contour_mapping = {}
        for rgb in unique_colors:
            rgb_tuple = tuple(rgb)
            if rgb_tuple not in color_class_mapping:
                continue
            class_id = color_class_mapping[rgb_tuple]
            binary_mask = cv2.inRange(mask_img, np.array(rgb), np.array(rgb))
            contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if contours:
                class_contour_mapping[class_id] = contours
        if class_contour_mapping:
            write_polygon_file(class_contour_mapping, h, w, label_dir, base_name)

#split into train val and test
def split_dataset(paths, train_ratio=0.8, val_ratio=0.1):
    img_dir = paths["raw_images"]
    lbl_dir = paths["labels"]
    all_images = sorted([f for f in os.listdir(img_dir) if f.endswith(".png")])
    def get_base(f): return os.path.splitext(f)[0].replace("_endo", "")
    all_bases = [get_base(f) for f in all_images if os.path.exists(os.path.join(lbl_dir, get_base(f) + ".txt"))]
    random.shuffle(all_bases)
    n_total = len(all_bases)
    n_train = int(n_total * train_ratio)
    n_val = int(n_total * val_ratio)
    train_set = all_bases[:n_train]
    val_set = all_bases[n_train:n_train + n_val]
    test_set = all_bases[n_train + n_val:]
    return train_set, val_set, test_set

# move pairs into their folders
def move_split_files(split_bases, split_type, paths):
    img_src = paths["raw_images"]
    lbl_src = paths["labels"]
    img_dst = paths[f"{split_type}_images"]
    lbl_dst = paths[f"{split_type}_labels"]
    for base in split_bases:
        img_name = base + "_endo.png"
        lbl_name = base + ".txt"
        try:
            shutil.copy(os.path.join(img_src, img_name), os.path.join(img_dst, img_name))
            shutil.copy(os.path.join(lbl_src, lbl_name), os.path.join(lbl_dst, lbl_name))
        except Exception as e:
            continue

#execute all functions 
if __name__ == "__main__":
    paths = initialize_paths()
    copy_and_rename_images(paths)
    color_class_mapping = initialize_mappings()
    generate_yolov11_annotations(paths, color_class_mapping)

    train_set, val_set, test_set = split_dataset(paths)
    move_split_files(train_set, "train", paths)
    move_split_files(val_set, "val", paths)
    move_split_files(test_set, "test", paths)
