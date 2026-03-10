import os
import argparse
from config import *
from utils.dataset_handler import download_dataset, create_subset, update_yaml_for_subset
from utils.yolo_manager import train_yolo

def main():
    parser = argparse.ArgumentParser(description="Litter Detection - Training Script")
    parser.add_argument("--epochs", type=int, default=5, help="Number of training epochs")
    parser.add_argument("--imgsz", type=int, default=640, help="Image size for training")
    parser.add_argument("--train_subset", type=int, default=500, help="Size of the training subset")
    parser.add_argument("--val_subset", type=int, default=200, help="Size of the validation subset")
    args = parser.parse_args()

    print("--- Starting Training Pipeline ---")
    
    # Check for GPU
    import torch
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[INFO] Using device: {device.upper()}")
    if device == "cpu":
        print("[WARNING] No GPU detected. Training on CPU might be slow. Subsetting is recommended.")

    # 1. Dataset Setup
    print(f"[INFO] Downloading dataset: {PROJECT_NAME} v{DATASET_VERSION}")
    dataset_path = download_dataset(ROBOFLOW_API_KEY, WORKSPACE, PROJECT_NAME, DATASET_VERSION, DATASET_FORMAT)
    
    # 2. Create Subsets
    print(f"[INFO] Creating subsets: train={args.train_subset}, val={args.val_subset}")
    train_subset_path = create_subset(dataset_path, split="train", subset_size=args.train_subset)
    val_subset_path = create_subset(dataset_path, split="valid", subset_size=args.val_subset)
    
    # 3. Update YAML
    yaml_path = os.path.join(dataset_path, "data.yaml")
    update_yaml_for_subset(yaml_path, train_subset_path, val_subset_path)
    
    # 4. Training
    print(f"[INFO] Launching YOLOv8 training for {args.epochs} epochs")
    train_yolo(MODEL_TYPE, yaml_path, epochs=args.epochs, imgsz=args.imgsz, project=OUTPUT_DIR, name=OUTPUT_NAME)
    
    print("--- Training Pipeline Complete ---")

if __name__ == "__main__":
    main()
