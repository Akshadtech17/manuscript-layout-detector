from ultralytics import YOLO

def train():

    model=YOLO("yolov8n.pt")

    model.train(
        data="data/dataset.yaml",
        epochs=50,
        imgsz=1024,
        batch=4,
        project="models",
        name="manuscript_detector"
    )

if __name__=="__main__":
    train()