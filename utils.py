import json
import cv2
import os
import numpy as np

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def _convert_numpy(obj):
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, np.floating):
        return float(obj)
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

def save_json(data, path):
    with open(path, "w") as f:
        json.dump(data, f, indent=4, default=_convert_numpy)

def draw_boxes(image, detections):
    for d in detections:
        x1, y1, x2, y2 = map(int, d["bbox"])
        label = d["label"]
        conf = float(d["confidence"])

        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(
            image,
            f"{label}:{conf:.2f}",
            (x1, max(20, y1 - 5)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 0, 0),
            2
        )
    return image