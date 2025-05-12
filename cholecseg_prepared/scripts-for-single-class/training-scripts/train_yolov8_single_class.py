from ultralytics import YOLO

# Load YOLOv8 segmentation model (nano version as an example)
model = YOLO('yolov8n-seg.pt')  # You can use yolov8s-seg.pt, yolov8m-seg.pt, etc., based on your needs

# Train model
model.train(
    data='/student/vcheruku/Enhance-Data-Diversity-and-Robustness/config-yolo-single-class/data.yaml',
    epochs=50,
    imgsz=640,
    batch=8,
    name='yolov8-single-object-detection',  # Name of the experiment folder
    project='/student/vcheruku/Enhance-Data-Diversity-and-Robustness/yolo-for-single-class/YOLOv8',  # Full path to the directory where results will be stored
    workers=8,
    cache=False,
    device=0
)
