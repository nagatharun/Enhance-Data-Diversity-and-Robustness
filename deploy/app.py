import streamlit as st
import cv2
import tempfile
import time
import os
from ultralytics import YOLO
import numpy as np
from PIL import Image

st.sidebar.header("controls")
model_choice = st.sidebar.radio("Choose your model:", ("Multi-object", "Liver only"))
if model_choice == "Multi-object":
    model_path = "C://Users//karth//OneDrive//Desktop//model_Deploy_streamlit//best.pt"
else:
    model_path = "C://Users//karth//OneDrive//Desktop//model_Deploy_streamlit//single.pt"
model = YOLO(model_path)
model.fuse()
model.verbose = False
speed = st.sidebar.slider("FPS", min_value=1, max_value=50, value=10)
pause = st.sidebar.checkbox("Pause")
st.title("Laparoscopic Segmentation Demo using YOLOv11")
st.markdown("### Image Segmentation")
image = st.file_uploader("Upload an image i.e a laprsocopic surgery frame", type=["jpg", "jpeg", "png"])
if image is not None:
    img = Image.open(image).convert("RGB")
    img_np = np.array(img)
    results = model(img_np)[0]
    annotated_img = results.plot()
    annotated_img = cv2.cvtColor(annotated_img, cv2.COLOR_BGR2RGB)
    st.image(annotated_img, caption="Segmented Image", use_column_width=True)
st.markdown("### Video Segmentation")
video = st.file_uploader("Upload a DaVinci generated laproscopic surgery video", type=["mp4", "avi", "mov", "mkv"])
if video is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(video.read())
    video_path = tfile.name
    cap = cv2.VideoCapture(video_path)
    stframe = st.empty()
    sttext = st.empty()
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps_actual = int(cap.get(cv2.CAP_PROP_FPS))
    delay = 1 / speed
    frame_number = 0
    output_frames = []
    st.markdown("Playing video")
    while cap.isOpened():
        if pause:
            time.sleep(0.1)
            continue
        ret, frame = cap.read()
        if not ret:
            break
        results = model(frame)[0]
        annotated_frame = results.plot()
        annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
        output_frames.append(cv2.cvtColor(annotated_frame, cv2.COLOR_RGB2BGR))
        if results.boxes is not None and results.boxes.conf is not None:
            avg_conf = results.boxes.conf.cpu().numpy().mean()
            sttext.markdown(f"**Frame {frame_number + 1}/{frame_count} – Avg Confidence: {avg_conf:.2f}**")
        else:
            sttext.markdown(f"**Frame {frame_number + 1}/{frame_count} – No detections**")
        stframe.image(annotated_frame, caption=f"Frame {frame_number + 1}/{frame_count}", use_column_width=True)
        frame_number += 1
        time.sleep(delay)
    cap.release()
    st.success("video ended!!")
    output_path = "segmented.mp4"
    h, w, _ = output_frames[0].shape
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), 20, (w, h))
    for f in output_frames:
        out.write(f)
    out.release()
    with open(output_path, "rb") as file:
        st.download_button("Download Segmented Video", file, file_name="segmented_output.mp4")