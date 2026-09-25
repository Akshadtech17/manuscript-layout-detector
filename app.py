import streamlit as st
import cv2
import numpy as np
import tempfile
import json

from detector import ManuscriptDetector
from preprocess import preprocess_image
from utils import draw_boxes

st.set_page_config(
    page_title="Manuscript Layout Detector",
    page_icon="📜",
    layout="wide"
)

st.title("📜 Manuscript Layout Detector")

st.write(
    "Upload a historical manuscript image and automatically detect layout regions."
)

uploaded = st.file_uploader(
    "Upload Image",
    type=["jpg","jpeg","png","tif","tiff"]
)

if uploaded:

    with tempfile.NamedTemporaryFile(delete=False,suffix=".jpg") as tmp:

        tmp.write(uploaded.read())

        temp_path=tmp.name

    img=preprocess_image(temp_path)

    detector=ManuscriptDetector()

    detections=detector.predict(img)

    annotated=draw_boxes(img.copy(),detections)

    st.subheader("Annotated Output")

    st.image(
        cv2.cvtColor(annotated,cv2.COLOR_BGR2RGB),
        use_container_width=True
    )

    st.subheader("JSON Prediction")

    st.json({
        "image":uploaded.name,
        "detections":detections
    })

    _,buffer=cv2.imencode(".jpg",annotated)

    st.download_button(
        "Download Annotated Image",
        buffer.tobytes(),
        file_name="annotated.jpg",
        mime="image/jpeg"
    )

    st.download_button(
        "Download JSON",
        json.dumps(
            {"image":uploaded.name,"detections":detections},
            indent=4
        ),
        file_name="prediction.json",
        mime="application/json"
    )