from ultralytics import YOLO

# Load YOLOv11 segmentation model
model = YOLO('yolo11n-seg.pt')

# Train model
model.train(
    data='/student/vcheruku/Enhance-Data-Diversity-and-Robustness/config-yolo-single-class/data.yaml',
    epochs=50,
    imgsz=640,
    batch=8,
    name='yolo-on-single-object-detection',
    project='YOLO11',
    workers=8,
    cache=False,
    device=0
)