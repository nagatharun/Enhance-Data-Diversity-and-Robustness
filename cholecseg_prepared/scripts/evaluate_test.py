#put evaluation code here or the testing code here
from ultralytics import YOLO
#imporrt model with best weight s
model = YOLO("YOLO11/cholecseg_from_script3/weights/best.pt")

metrics = model.val(
    data="cholecseg_prepared/data.yaml",
    split="test",
    imgsz=640,
    batch=8,
    verbose=True
)

print(metrics)
