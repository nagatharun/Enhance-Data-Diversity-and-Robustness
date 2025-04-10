# Capstone Project: AI-Based Multi-Organ Prediction in Laparoscopic Videos

## Overview
This capstone project focuses on improving the robustness and generalizability of AI-based multi-organ prediction in Da Vinci-generated laparoscopic videos. The goal is to leverage domain adaptation techniques and generative models (such as GANs or diffusion models) to synthesize new laparoscopic images, thereby expanding and diversifying available datasets. By addressing the variability in patient anatomies, procedures, and lighting conditions, this project aims to produce an AI pipeline that is more resilient to real-world surgical variations and data scarcity.

## Objectives
- Implement domain adaptation techniques to handle variability in laparoscopic imagery across different patients, procedures, and lighting conditions.
- Use generative models (e.g., GANs, diffusion models) to synthesize new laparoscopic images for augmenting real datasets that are limited or imbalanced.
- Integrate synthetic data into a multi-organ prediction workflow to ensure improved model robustness and better generalization to unseen surgical scenarios.
- Validate performance gains through comprehensive testing on existing laparoscopic video datasets and, if possible, real clinical data.
- Document and demonstrate the effectiveness of the synthetic augmentation pipeline and domain adaptation methods through final presentations and code repositories.

## Success Metrics
The success of the project will be measured based on the following criteria:
- **Model Accuracy Improvement**: Demonstrate at least a 10% absolute gain in IOU, Dice score, or relevant metric compared to a baseline model trained on real data only.
- **Generalization to Unseen Data**: Show consistent performance across multiple datasets or different surgical procedures with limited performance degradation.
- **Data Augmentation Efficacy**: Evaluate the quality and diversity of generated images, ensuring that synthetic samples positively impact training without introducing artifacts.
- **Real-time or Near Real-time Processing**: Maintain an inference speed of ≤ 30 ms/frame for organ prediction tasks.
- **Robust Documentation and Code Quality**: Provide thorough documentation enabling future researchers or clinicians to reproduce and extend the work.

## Dataset
We have downloaded the Cholecseg8k dataset from Kaggle for initial testing:
- [Cholecseg8k Dataset](https://www.kaggle.com/datasets/newslab/cholecseg8k)

## GPU Access
Access to the GPU for training and experimentation has been set up using the following guide:
- [Lab GPU Server Setup](https://github.com/SLUVisLab/lab-wiki/wiki/%F0%9F%93%9F-Lab-GPU-Server-Setup)

## Data Upload
1. We have uploaded the dataset(.zip) to the GPU server, use the following generic `rsync` command format:
```bash
rsync -avz --progress <path/to/dataset.zip> <username>@<gpu_server>:<path/to/directory/where/you/want/to/upload>
```
2. After uploading, the dataset can be unzipped on the server using:
```bash
unzip <dataset.zip> -d <directory where you want to unzip>
```
