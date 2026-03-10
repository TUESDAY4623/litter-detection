import os
import argparse
from config import *
from utils.dataset_handler import download_dataset, create_subset, update_yaml_for_subset
from utils.video_downloader import download_video
from utils.yolo_manager import train_yolo, run_prediction, get_latest_model

def main():
    parser = argparse.ArgumentParser(description="Litter Detection Project")
    parser.add_argument("--mode", choices=["train", "predict", "full"], default="full", help="Process mode")
    parser.add_argument("--url", help="Video URL for prediction")
    args = parser.parse_args()

    # 1. Dataset Setup & Training
    if args.mode in ["train", "full"]:
        print("--- Step 1: Dataset Setup & Training ---")
        
        # Check for GPU
        import torch
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"[INFO] Using device: {device.upper()}")

        dataset_path = download_dataset(ROBOFLOW_API_KEY, WORKSPACE, PROJECT_NAME, DATASET_VERSION, DATASET_FORMAT)
        
        # Use smaller subsets for main logic unless specified
        train_subset_path = create_subset(dataset_path, split="train", subset_size=500)
        val_subset_path = create_subset(dataset_path, split="valid", subset_size=200)
        

        yaml_path = os.path.join(dataset_path, "data.yaml")
        update_yaml_for_subset(yaml_path, train_subset_path, val_subset_path)
        
        train_yolo(MODEL_TYPE, yaml_path, epochs=12, project=OUTPUT_DIR, name=OUTPUT_NAME) # 1 epoch for quick demonstration

    # 2. Prediction
    if args.mode in ["predict", "full"]:
        print("\n--- Step 2: Prediction ---")
        video_url = args.url if args.url else "https://www.youtube.com/watch?v=LNus-1OF5iQ"
        video_path = download_video(video_url)
        
        if video_path:
            model_path = get_latest_model()
            if not model_path:
                print("No trained model found, using base model.")
                model_path = MODEL_TYPE
            
            run_prediction(model_path, video_path, conf=CONFIDENCE_THRESHOLD)

if __name__ == "__main__":
    main()
