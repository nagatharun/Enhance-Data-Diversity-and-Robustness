#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CODE RELEASE TO SUPPORT RESEARCH.
COMMERCIAL USE IS NOT PERMITTED.
#==============================================================================
An implementation based on:
***
    C.I. Nwoye, T. Yu, C. Gonzalez, B. Seeliger, P. Mascagni, D. Mutter, J. Marescaux, N. Padoy. 
    Rendezvous: Attention Mechanisms for the Recognition of Surgical Action Triplets in Endoscopic Videos. 
    Medical Image Analysis, 78 (2022) 102433.
***  
Created on Thu Oct 21 15:38:36 2021
#==============================================================================  
Copyright 2021 The Research Group CAMMA Authors All Rights Reserved.
(c) Research Group CAMMA, University of Strasbourg, France
@ Laboratory: CAMMA - ICube
@ Author: Chinedu Innocent Nwoye
@ Website: http://camma.u-strasbg.fr
#==============================================================================
 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
#==============================================================================
"""

import os
import random
import numpy as np
from PIL import Image
import torchvision.transforms as transforms
from torch.utils.data import Dataset, ConcatDataset, DataLoader


class CholecT50():
    def __init__(self, 
                dataset_dir, 
                dataset_variant="cholect45-crossval",
                test_fold=1,
                augmentation_list=['original', 'vflip', 'hflip', 'contrast', 'rot90'],
                image_width=448,
                image_height=256,
                cond_scale=None,
                model_type=None,
                max_rows=None,
                only_train_synthetic=False):
        
        """ Args
                dataset_dir : common path to the dataset (excluding videos, output)
                list_video  : list video IDs, e.g:  ['VID01', 'VID02']
                aug         : data augumentation style
                split       : data split ['train', 'val', 'test']
            Call
                batch_size: int, 
                shuffle: True or False
            Return
                tuple ((image), (tool_label, verb_label, target_label, triplet_label))
        """
        
        # ------- EDIT -------
        self.image_width=image_width
        self.image_height=image_height
        # ------- EDIT -------
        
        self.dataset_dir = dataset_dir
        self.list_dataset_variant = {
            "cholect45-crossval": "for CholecT45 dataset variant with the official cross-validation splits.",
            "cholect50-crossval": "for CholecT50 dataset variant with the official cross-validation splits",
            "cholect50-challenge": "for CholecT50 dataset variant as used in CholecTriplet challenge",
            "cholect50": "for the CholecT50 dataset with original splits used in rendezvous paper",
            "cholect45": "a pointer to cholect45-crossval",
        }
        assert dataset_variant in self.list_dataset_variant.keys(), print(dataset_variant, "is not a valid dataset variant")
        video_split  = self.split_selector(case=dataset_variant, cond_scale=cond_scale, model_type=model_type)
        train_videos = sum([v for k,v in video_split.items() if k!=test_fold], []) if 'crossval' in dataset_variant else video_split['train']
        test_videos  = sum([v for k,v in video_split.items() if k==test_fold], []) if 'crossval' in dataset_variant else video_split['test']
        # ------- EDIT -------
        if only_train_synthetic:
            train_videos = np.array(train_videos)
            train_videos = [79] + train_videos[train_videos>80].tolist()
        # ------- EDIT -------
        if 'crossval' in dataset_variant:
            # ------- EDIT -------
            val_videos   = train_videos[:1] # train_videos[-5:]
            train_videos = train_videos[1:] # train_videos[:-5]
            print(f'TRAIN: {train_videos} | VAL: {val_videos} | TEST: {test_videos}')
            # ------- EDIT -------
        else:
            val_videos   = video_split['val']
        self.train_records = ['VID{}'.format(str(v).zfill(2)) for v in train_videos]
        self.val_records   = ['VID{}'.format(str(v).zfill(2)) for v in val_videos]
        self.test_records  = ['VID{}'.format(str(v).zfill(2)) for v in test_videos]
        self.augmentations = {
            'original': self.no_augumentation,
            'vflip': transforms.RandomVerticalFlip(0.4),
            'hflip': transforms.RandomHorizontalFlip(0.4),
            'contrast': transforms.ColorJitter(brightness=0.1, contrast=0.2, saturation=0, hue=0),
            'rot90': transforms.RandomRotation(90,expand=True),
            'brightness': transforms.RandomAdjustSharpness(sharpness_factor=1.6, p=0.5),
            'contrast': transforms.RandomAutocontrast(p=0.5),
        }
        self.augmentation_list = []
        for aug in augmentation_list:
            self.augmentation_list.append(self.augmentations[aug])
        trainform, testform = self.transform()
        self.build_train_dataset(max_rows=max_rows, transform=trainform)
        self.build_val_dataset(max_rows=max_rows, transform=trainform)
        self.build_test_dataset(max_rows=max_rows, transform=testform)
    
    def list_dataset_variants(self):
        print(self.list_dataset_variant)

    def list_augmentations(self):
        print(self.augmentations.keys())

    def split_selector(self, case='cholect50', cond_scale=None, model_type=None):
        switcher = {
            'cholect50': {
                'train': [1, 15, 26, 40, 52, 65, 79, 2, 18, 27, 43, 56, 66, 92, 4, 22, 31, 47, 57, 68, 96, 5, 23, 35, 48, 60, 70, 103, 13, 25, 36, 49, 62, 75, 110],
                'val'  : [8, 12, 29, 50, 78],
                'test' : [6, 51, 10, 73, 14, 74, 32, 80, 42, 111]
            },
            'cholect50-challenge': {
                'train': [1, 15, 26, 40, 52, 79, 2, 27, 43, 56, 66, 4, 22, 31, 47, 57, 68, 23, 35, 48, 60, 70, 13, 25, 49, 62, 75, 8, 12, 29, 50, 78, 6, 51, 10, 73, 14, 32, 80, 42],
                'val':   [5, 18, 36, 65, 74],
                'test':  [92, 96, 103, 110, 111]
            },
            'cholect45-crossval': {
                1: [79,  2, 51,  6, 25, 14, 66, 23, 50,],
                2: [80, 32,  5, 15, 40, 47, 26, 48, 70,],
                3: [31, 57, 36, 18, 52, 68, 10,  8, 73,],
                4: [42, 29, 60, 27, 65, 75, 22, 49, 12,],
                5: [78, 43, 62, 35, 74,  1, 56,  4, 13,],
            },
            'cholect50-crossval': {
                1: [79,  2, 51,  6, 25, 14, 66, 23, 50, 111],
                2: [80, 32,  5, 15, 40, 47, 26, 48, 70,  96],
                3: [31, 57, 36, 18, 52, 68, 10,  8, 73, 103],
                4: [42, 29, 60, 27, 65, 75, 22, 49, 12, 110],
                5: [78, 43, 62, 35, 74,  1, 56,  4, 13,  92],
            }
        }
        # ------- EDIT -------
        if cond_scale == 3:
            if model_type == 'Imagen':
                switcher['cholect45-crossval']['6']=[81,82,83] # Imagen:           Synthetic images with conditional scale 3
            if model_type == 'ElucidatedImagen':
                switcher['cholect45-crossval']['7']=[84,85,86] # Elucidated Imagen:Synthetic images with conditional scale 3
        if cond_scale == 5:
            if model_type == 'Imagen':            
                switcher['cholect45-crossval']['8']=[87,88,89] # Imagen:           Synthetic images with conditional scale 5
            if model_type == 'ElucidatedImagen':        
                switcher['cholect45-crossval']['9']=[90,91,92]  # Elucidated Imagen:Synthetic images with conditional scale 5
        switcher['cholect45-crossval'] = {int(k):[int(i) for i in v] for k,v in switcher['cholect45-crossval'].items()}
        # ------- EDIT -------
        return switcher.get(case)

    def no_augumentation(self, x):
        return x

    def transform(self):
        normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        op_test   = [transforms.Resize((self.image_height, self.image_width)), transforms.ToTensor(), normalize,]
        # -------
        op_train  = [transforms.Resize((self.image_height, self.image_width))] + self.augmentation_list + [transforms.CenterCrop(self.image_height), transforms.ToTensor(), normalize,]
        # -------
        testform  = transforms.Compose(op_test)
        trainform = transforms.Compose(op_train)
        return trainform, testform

    # ------- EDIT -------
    def build_train_dataset(self, max_rows, transform):
        iterable_dataset = []
        is_synthetic = False
        for video in self.train_records:
            is_synthetic = False
            
            if int(video[-2:]) > 80:
                is_synthetic = True
                print('Synthetic:', is_synthetic)
            
            dataset = T50(img_dir = os.path.join(self.dataset_dir, 'data', video), 
                        triplet_file = os.path.join(self.dataset_dir, 'triplet', '{}.txt'.format(video)), 
                        tool_file = os.path.join(self.dataset_dir, 'instrument', '{}.txt'.format(video)),  
                        verb_file = os.path.join(self.dataset_dir, 'verb', '{}.txt'.format(video)),  
                        target_file = os.path.join(self.dataset_dir, 'target', '{}.txt'.format(video)), 
                        max_rows=max_rows,
                        is_synthetic=is_synthetic,
                        transform=transform)

            iterable_dataset.append(dataset)
        self.train_dataset = ConcatDataset(iterable_dataset)

    def build_val_dataset(self, max_rows, transform):
        iterable_dataset = []
        is_synthetic = False
        for video in self.val_records:
            is_synthetic = False
            
            if int(video[-2:]) > 80:
                is_synthetic = True
                
            dataset = T50(img_dir = os.path.join(self.dataset_dir, 'data', video), 
                        triplet_file = os.path.join(self.dataset_dir, 'triplet', '{}.txt'.format(video)), 
                        tool_file = os.path.join(self.dataset_dir, 'instrument', '{}.txt'.format(video)),  
                        verb_file = os.path.join(self.dataset_dir, 'verb', '{}.txt'.format(video)),  
                        target_file = os.path.join(self.dataset_dir, 'target', '{}.txt'.format(video)), 
                        max_rows=max_rows,
                        is_synthetic=is_synthetic,
                        transform=transform)
            iterable_dataset.append(dataset)
        self.val_dataset = ConcatDataset(iterable_dataset)

    def build_test_dataset(self, max_rows, transform):
        iterable_dataset = []
        is_synthetic = False
        for video in self.test_records:
            is_synthetic = False
            
            if int(video[-2:]) > 80:
                is_synthetic = True
            dataset = T50(img_dir = os.path.join(self.dataset_dir, 'data', video), 
                triplet_file = os.path.join(self.dataset_dir, 'triplet', '{}.txt'.format(video)), 
                tool_file = os.path.join(self.dataset_dir, 'instrument', '{}.txt'.format(video)),  
                verb_file = os.path.join(self.dataset_dir, 'verb', '{}.txt'.format(video)),  
                target_file = os.path.join(self.dataset_dir, 'target', '{}.txt'.format(video)), 
                max_rows=max_rows,
                is_synthetic=is_synthetic,
                transform=transform)
            iterable_dataset.append(dataset)
        self.test_dataset = iterable_dataset
       
    # ------- EDIT -------
        
    def build(self):
        return (self.train_dataset, self.val_dataset, self.test_dataset)

    
class T50(Dataset):
        # ------- EDIT -------
    def __init__(self, img_dir, triplet_file, tool_file, verb_file, target_file, max_rows, is_synthetic, transform=None, target_transform=None):
        if is_synthetic:
            print('Max_rows', max_rows)
            print('triplet_file', triplet_file)
            self.triplet_labels = np.loadtxt(triplet_file, dtype=np.int32, delimiter=',',max_rows=max_rows)
            self.tool_labels = np.loadtxt(tool_file, dtype=np.int32, delimiter=',',max_rows=max_rows)
            self.verb_labels = np.loadtxt(verb_file, dtype=np.int32, delimiter=',',max_rows=max_rows)
            self.target_labels = np.loadtxt(target_file, dtype=np.int32, delimiter=',',max_rows=max_rows)
        else:
            self.triplet_labels = np.loadtxt(triplet_file, dtype=np.int32, delimiter=',')
            self.tool_labels = np.loadtxt(tool_file, dtype=np.int32, delimiter=',')
            self.verb_labels = np.loadtxt(verb_file, dtype=np.int32, delimiter=',')
            self.target_labels = np.loadtxt(target_file, dtype=np.int32, delimiter=',')
        # ------- EDIT -------
        print('SHAPE Labels:', self.triplet_labels.shape)
        self.img_dir = img_dir
        self.transform = transform
        self.target_transform = target_transform
        
    def __len__(self):
        return len(self.triplet_labels)
    
    def __getitem__(self, index):
        triplet_label = self.triplet_labels[index, 1:]
        tool_label = self.tool_labels[index, 1:]
        verb_label = self.verb_labels[index, 1:]
        target_label = self.target_labels[index, 1:]
        # ------- EDIT -------
        if int(self.img_dir[-2:]) > 80:
            if int(self.img_dir[-2:]) in [81,87]:
                basename = "{}-Imagen-grasper retract gallbladder in calot triangle dissection.png".format(str(self.triplet_labels[index, 0]).zfill(5))
            elif int(self.img_dir[-2:]) in [84,90]:
                basename = "{}-ElucidatedImagen-grasper retract gallbladder in calot triangle dissection.png".format(str(self.triplet_labels[index, 0]).zfill(5))
            elif int(self.img_dir[-2:]) in [82,88]:
                basename = "{}-Imagen-grasper retract liver in gallbladder dissection.png".format(str(self.triplet_labels[index, 0]).zfill(5))
            elif int(self.img_dir[-2:]) in [85,91]:
                basename = "{}-ElucidatedImagen-grasper retract liver in gallbladder dissection.png".format(str(self.triplet_labels[index, 0]).zfill(5))
            elif int(self.img_dir[-2:]) in [83,89]:
                basename = "{}-Imagen-hook dissect gallbladder in gallbladder dissection.png".format(str(self.triplet_labels[index, 0]).zfill(5))
            elif int(self.img_dir[-2:]) in [86,92]:
                basename = "{}-ElucidatedImagen-hook dissect gallbladder in gallbladder dissection.png".format(str(self.triplet_labels[index, 0]).zfill(5))
        else:
            basename = "{}.png".format(str(self.triplet_labels[index, 0]).zfill(6))
        # ------- EDIT -------
        img_path = os.path.join(self.img_dir, basename)
        image    = Image.open(img_path)
        if self.transform:
            image = self.transform(image)
        if self.target_transform:
            triplet_label = self.target_transform(triplet_label)
        return image, (tool_label, verb_label, target_label, triplet_label)


if __name__ == "__main__":
    print("Refers to https://github.com/CAMMA-public/cholect45 for the usage guide.")
