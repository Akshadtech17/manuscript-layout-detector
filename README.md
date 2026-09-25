# 📜 Manuscript Layout Detector

<div align="center">

### End-to-End Historical Manuscript Layout Region Detection Pipeline

*A modular computer vision pipeline for automatic localization and classification of manuscript layout regions.*

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-Numerical-013243?style=for-the-badge&logo=numpy&logoColor=white)
![CLI](https://img.shields.io/badge/CLI-Batch%20Processing-success?style=for-the-badge)
![JSON](https://img.shields.io/badge/Output-JSON%20%2B%20Annotated%20Images-orange?style=for-the-badge)

</div>

---

## ✨ Overview

Historical manuscripts present unique challenges for automated document analysis, including faded ink, bleed-through, stains, irregular margins, skewed scans, decorative elements, and varying writing styles.

This project implements a **modular end-to-end layout analysis pipeline** that automatically identifies and localizes non-body regions while generating both visual and structured outputs.

### 🎯 Target Layout Classes

| Region | Description |
|---------|-------------|
| **Header** | Top margin text, folio numbers, running headers |
| **Footer** | Bottom margin text, page numbers, catchwords |
| **Main Text** | Primary manuscript content |
| **Side Text** | Marginalia and side annotations |
| **Filler** | Decorative marks, isolated symbols, non-body artifacts |

---

# 🏗️ System Architecture

<AsyncImage query="clean software architecture diagram showing Input Manuscript Image -> Preprocessing -> Text Block Extraction -> Layout Classification -> Annotated Image and JSON Output" aspectRatio="16:9"/>

### Processing Pipeline

text
Input Image
     │
     ▼
Preprocessing
 • Denoising
 • CLAHE Contrast Enhancement
 • Adaptive Thresholding
     │
     ▼
Text Block Extraction
 • Morphological Operations
 • Connected Components
 • Region Merging
     │
     ▼
Layout Classification
 • Header
 • Footer
 • Main Text
 • Side Text
 • Filler
     │
     ▼
Outputs
 ├── Annotated Images
 └── JSON Metadata

# 📂 Project Structure

manuscript-layout-detector/
│
├── inference.py
├── train.py
├── preprocess.py
├── detector.py
├── utils.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── models/
│   └── best.pt
│
├── data/
│   ├── test_images/
│   └── sample_output/
│
└── results/
    ├── images/
    └── predictions/

# 🚀 Features

* Batch processing of manuscript pages

* Automatic layout region detection

* Header/Footer localization

* Marginalia detection

* Main text extraction

* Decorative artifact identification

* Contrast enhancement

* Noise reduction

* Adaptive thresholding

* Structured JSON predictions

* Annotated image generation

* Modular Python architecture

* Relative-path CLI execution

* Page-boundary-safe bounding boxes

# 🧠 Detection Strategy

Unlike a basic contour detector, the pipeline performs multiple processing stages before classification.

## Stage 1 — Image Enhancement

![Computer Vision Based Automatic Margin Computation Model for Digital Document Images | SN Computer Science | Springer Nature Link](https://images.openai.com/static-rsc-4/m8M3IIDlfECNrcEIFhb0OGJxFOmeyIzsnhE60kjh3D0vhm6eh7zrPkcxM45cnn-SSvvGDwCvuSTqYPf1LYwQuww6iWgaPdU-UWG9NmQQIXFkgQzz6L_RoZ-mynQ4JFNZPrjK6MZJUs2Q1NbAF5zSg_Ww88mQzY94ImwNNfJZ7Co?purpose=inline)

The preprocessing module improves degraded manuscript scans using:

* Fast Non-Local Means Denoising

* CLAHE contrast enhancement

* Adaptive thresholding

* Morphological cleanup

This improves robustness against:

* faded ink

* uneven illumination

* stains

* blur

* bleed-through

## Stage 2 — Text Block Extraction

![From Parchment to Pixels: Testing HTR for Medieval Latin Manuscripts at KBLab – The KBLab Blog](https://images.openai.com/static-rsc-4/ehBdmOF7S1TOmW-gRUw4TTLc18wd0H2Pv99hpTl17OAQHr9yLiiT48RRDGFLKxvWiBKZdrqMyWO98jBLw8s_egqglU_bW-GravZGVdAPqLp08q6KUpVAQeKbG2IMNLzX_8W2jE5yXBFRfXFCGYTMJ-KpWCSzyguDm926Gb8K25g?purpose=inline)

The detector merges nearby characters into coherent text blocks using:

* Connected Components

* Morphological Closing

* Region Filtering

* Dynamic Size Thresholds

This prevents character-level fragmentation.

## Stage 3 — Layout Classification

Each detected region is classified using spatial reasoning based on:

* page geometry

* margin proximity

* region size

* aspect ratio

* relative positioning

This enables automatic assignment into:

* Header

* Footer

* Main Text

* Side Text

* Filler

# 📥 Installation

Clone the repository.

Bash

git clone https://github.com/Akshadtech17/manuscript-layout-detector.git
cd manuscript-layout-detector

Create a virtual environment.

Bash

python -m venv venv

Activate it.

Windows

PowerShell


.\venv\Scripts\activate

Install dependencies.

Bash


pip install -r requirements.txt

# ▶️ Usage

### Process an Entire Folder

Bash


python inference.py --input ./data/test_images --output ./results

### Input


data/test_images/
├── page1.jpg
├── page2.jpg
├── page3.jpg
└── ...


### Output


results/
├── images/
│   ├── page1.jpg
│   ├── page2.jpg
│   └── ...
│
└── predictions/
    ├── page1.json
    ├── page2.json
    └── ...


# 📊 Example Output

## Annotated Layout Detection

![From Parchment to Pixels: Testing HTR for Medieval Latin Manuscripts at KBLab – The KBLab Blog](https://images.openai.com/static-rsc-4/ehBdmOF7S1TOmW-gRUw4TTLc18wd0H2Pv99hpTl17OAQHr9yLiiT48RRDGFLKxvWiBKZdrqMyWO98jBLw8s_egqglU_bW-GravZGVdAPqLp08q6KUpVAQeKbG2IMNLzX_8W2jE5yXBFRfXFCGYTMJ-KpWCSzyguDm926Gb8K25g?purpose=inline)

Example visualization:

* Green bounding boxes

* Region labels

* Confidence scores

## JSON Prediction

JSON


{
    "image": "page1.jpg",
    "detections": [
        {
            "label": "header",
            "confidence": 0.93,
            "bbox": [210, 0, 1380, 110]
        },
        {
            "label": "main_text",
            "confidence": 0.98,
            "bbox": [220, 120, 1380, 1220]
        }
    ]
}

# 🛡️ Robustness

The pipeline is designed to handle challenging historical document conditions.

|
Challenge

|

Supported

|
| --- | --- |
|

Faded ink

|

✅

|
|

Uneven lighting

|

✅

|
|

Blur

|

✅

|
|

Noise

|

✅

|
|

Stains

|

✅

|
|

Variable aspect ratios

|

✅

|
|

Margin annotations

|

✅

|
|

Decorative elements

|

✅

|
|

Page boundary preservation

|

✅

|

# ⚙️ Technical Components

|
Module

|

Responsibility

|
| --- | --- |
|

preprocess.py

|

Image enhancement

|
|

detector.py

|

Layout region detection

|
|

utils.py

|

Drawing and JSON export

|
|

inference.py

|

Batch CLI processing

|
|

train.py

|

Training entry point

|

# 📈 Design Decisions

The implementation emphasizes:

* modular architecture

* reproducibility

* readable code

* deterministic processing

* CLI usability

* structured outputs

The detector combines classical computer vision techniques including adaptive thresholding, connected-component analysis, morphology-based region merging, and geometry-aware classification to produce document layout regions while maintaining bounding boxes inside page boundaries.

# 🔄 Future Improvements

Potential future enhancements include:

* YOLO-based manuscript-specific training

* Transformer-based document layout models

* OCR-assisted region refinement

* Automatic skew correction

* Multi-column manuscript optimization

* Confidence calibration

* Rotated bounding boxes

# 📚 Requirements

Core libraries include:

* Python 3.11+

* OpenCV

* NumPy

* Pillow

* tqdm

Install all dependencies with:

Bash

pip install -r requirements.txt

# 👨‍💻 Author

Akshad Aloni

Computer Science & Engineering (Data Science)

GitHub: Akshadtech17



