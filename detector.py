import cv2
import numpy as np


class ManuscriptDetector:

    def __init__(self):
        pass

    def predict(self, image):

        h, w = image.shape[:2]

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        gray = cv2.fastNlMeansDenoising(gray)

        clahe = cv2.createCLAHE(2.5, (8, 8))
        gray = clahe.apply(gray)

        binary = cv2.adaptiveThreshold(
            gray,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            35,
            15
        )

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

        horizontal_kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT,
            (max(25, w // 60), 5)
        )

        merged = cv2.morphologyEx(
            binary,
            cv2.MORPH_CLOSE,
            horizontal_kernel
        )

        contours, _ = cv2.findContours(
            merged,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        detections = []

        for cnt in contours:

            x, y, bw, bh = cv2.boundingRect(cnt)

            area = bw * bh

            if area < 1500:
                continue

            if bw > w * 0.98 and bh > h * 0.98:
                continue

            label = self.classify_region(
                x, y, bw, bh,
                w, h,
                area
            )

            confidence = self.compute_confidence(
                bw,
                bh,
                area,
                w,
                h
            )

            detections.append({
                "label": label,
                "confidence": confidence,
                "bbox": [
                    int(x),
                    int(y),
                    int(x + bw),
                    int(y + bh)
                ]
            })

        detections = self.merge_regions(detections)

        detections = self.add_missing_regions(
            detections,
            w,
            h
        )

        detections.sort(
            key=lambda d: (
                d["bbox"][1],
                d["bbox"][0]
            )
        )

        return detections

    def classify_region(
        self,
        x,
        y,
        bw,
        bh,
        page_w,
        page_h,
        area
    ):

        aspect = bw / max(bh, 1)

        if y < page_h * 0.12:
            return "header"

        if y + bh > page_h * 0.90:
            return "footer"

        if x < page_w * 0.12 or x + bw > page_w * 0.88:
            return "side_text"

        if area < 12000 or aspect < 0.45:
            return "filler"

        return "main_text"

    def compute_confidence(
        self,
        bw,
        bh,
        area,
        page_w,
        page_h
    ):

        size_score = min(area / (page_w * page_h * 0.20), 1.0)

        aspect = bw / max(bh, 1)

        shape_score = min(aspect / 4.0, 1.0)

        confidence = 0.60 + 0.25 * size_score + 0.15 * shape_score

        return round(min(confidence, 0.99), 2)

    def merge_regions(self, detections):

        if not detections:
            return []

        merged = []

        detections = sorted(
            detections,
            key=lambda d: (
                d["label"],
                d["bbox"][1]
            )
        )

        for d in detections:

            if not merged:
                merged.append(d)
                continue

            last = merged[-1]

            if last["label"] != d["label"]:
                merged.append(d)
                continue

            x1, y1, x2, y2 = last["bbox"]
            a1, b1, a2, b2 = d["bbox"]

            overlap = not (
                a1 > x2 + 40 or
                a2 < x1 - 40 or
                b1 > y2 + 40 or
                b2 < y1 - 40
            )

            if overlap:

                last["bbox"] = [
                    min(x1, a1),
                    min(y1, b1),
                    max(x2, a2),
                    max(y2, b2)
                ]

                last["confidence"] = max(
                    last["confidence"],
                    d["confidence"]
                )

            else:
                merged.append(d)

        return merged

    def add_missing_regions(
        self,
        detections,
        w,
        h
    ):

        labels = [d["label"] for d in detections]

        main = next(
            (d for d in detections if d["label"] == "main_text"),
            None
        )

        if main is None:

            detections.append({
                "label": "main_text",
                "confidence": 0.65,
                "bbox": [
                    int(w * 0.15),
                    int(h * 0.12),
                    int(w * 0.85),
                    int(h * 0.88)
                ]
            })

            return detections

        x1, y1, x2, y2 = main["bbox"]

        if "header" not in labels and y1 > h * 0.08:

            detections.append({
                "label": "header",
                "confidence": 0.70,
                "bbox": [
                    x1,
                    0,
                    x2,
                    y1
                ]
            })

        if "footer" not in labels and y2 < h * 0.92:

            detections.append({
                "label": "footer",
                "confidence": 0.70,
                "bbox": [
                    x1,
                    y2,
                    x2,
                    h
                ]
            })

        return detections