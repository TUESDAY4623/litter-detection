from ultralytics import YOLO
import os

def train_yolo(model_type, data_yaml, epochs=5, imgsz=640, project="runs", name="detects"):
    model = YOLO(model_type)
    print(f"Starting training for {epochs} epochs...")
    # Use absolute path for project to avoid defaults to home directory
    abs_project = os.path.abspath(project)
    results = model.train(data=data_yaml, epochs=epochs, imgsz=imgsz, project=abs_project, name=name)
    return results

def run_prediction(model_path, source, conf=0.25, save=True):
    model = YOLO(model_path)
    print(f"Running prediction on: {source}")
    results = model.predict(source=source, conf=conf, save=save)
    return results

def get_latest_model(runs_dir=None):
    if runs_dir is None:
        runs_dir = os.path.join(os.getcwd(), "runs", "detects")
    import glob
    models = glob.glob(os.path.join(runs_dir, "train*/weights/best.pt"))
    if not models:
        return None
    latest_model = max(models, key=os.path.getmtime)
    return latest_model
