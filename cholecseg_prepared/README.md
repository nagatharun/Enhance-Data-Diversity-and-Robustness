#Execution Instructions for baseline scores from yolov11

##1. Install dependencies
```python 
pip install -r requirements.txt
```

##2.Prepare the dataset
Run the preprocessing script to extract images, masks, generate labels, and split into train/val/test
```python
python scripts/preprocess_data.py
```

##3.Train the YOLOv11 segmentation model
```python
python scripts/train_yolo.py > results/training_logs.txt #save the training logs to training-logs.txt
```

##4.Evaluate the model on test set
```python 
python scripts/evaluate_test.py > test_results.txt #save the reults to test-results.txt 
```

##5.All training logs and evaluation results will be saved under the results/ folder



