from ultralytics import YOLO

# Load a pretrained YOLOv8n-pose Pose model
model = YOLO("yolov8n-pose.pt")

# Run inference on an image
results = model.predict(source = "0", show = True)  # results list
