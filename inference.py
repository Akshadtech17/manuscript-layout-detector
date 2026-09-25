import argparse
import os
import cv2
from tqdm import tqdm

from detector import ManuscriptDetector
from preprocess import preprocess_image
from utils import draw_boxes, save_json, ensure_dir

SUPPORTED = (".jpg", ".jpeg", ".png", ".tif", ".tiff")

def main():
    parser = argparse.ArgumentParser(
        description="Manuscript Layout Region Detection"
    )

    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)

    args = parser.parse_args()

    image_out = os.path.join(args.output, "images")
    json_out = os.path.join(args.output, "predictions")

    ensure_dir(image_out)
    ensure_dir(json_out)

    detector = ManuscriptDetector()

    if os.path.isfile(args.input):
        images = [os.path.basename(args.input)]
        input_dir = os.path.dirname(args.input)
    else:
        input_dir = args.input
        images = [
            f for f in os.listdir(input_dir)
            if f.lower().endswith(SUPPORTED)
        ]

    for name in tqdm(images, desc="Processing"):
        path = os.path.join(input_dir, name)

        img = preprocess_image(path)

        detections = detector.predict(img)

        annotated = draw_boxes(img.copy(), detections)

        cv2.imwrite(os.path.join(image_out, name), annotated)

        save_json(
            {"image": name, "detections": detections},
            os.path.join(json_out, os.path.splitext(name)[0] + ".json")
        )

    print("Inference completed.")
    print(f"Annotated images: {image_out}")
    print(f"JSON predictions: {json_out}")

if __name__ == "__main__":
    main()