#put evaluation code here or the testing code here
from ultralytics import YOLO
#imporrt model with best weight s
model = YOLO("/student/vcheruku/Enhance-Data-Diversity-and-Robustness/yolo-for-single-class/YOLO11/yolo-on-single-object-detection/weights/best.pt")

metrics = model.val(
    data="/student/vcheruku/Enhance-Data-Diversity-and-Robustness/config-yolo-single-class/data.yaml",
    split="test",
    imgsz=640,
    batch=8,
    verbose=True
)

print(metrics)
