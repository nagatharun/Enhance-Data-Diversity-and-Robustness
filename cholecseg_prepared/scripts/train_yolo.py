from ultralytics import YOLO

# Load YOLOv11 segmentation model
model = YOLO('yolo11n-seg.pt')

# Train model
model.train(
    data='cholecseg_prepared/data.yaml',
    epochs=50,
    imgsz=640,
    batch=8,
    name='cholecseg_from_script',
    project='YOLO11',
    workers=8,
    cache=False,
    device=0
)
