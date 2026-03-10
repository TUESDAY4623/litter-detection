import os
import shutil
import random
from roboflow import Roboflow
import yaml

def download_dataset(api_key, workspace, project_name, version, format):
    rf = Roboflow(api_key=api_key)
    project = rf.workspace(workspace).project(project_name)
    dataset = project.version(version).download(format)
    return dataset.location

def create_subset(dataset_path, split="train", subset_size=3000):
    images_src = os.path.join(dataset_path, split, "images")
    labels_src = os.path.join(dataset_path, split, "labels")
    
    if not os.path.exists(images_src):
        print(f"[WARNING] Split {split} not found in {dataset_path}")
        return None

    subset_dir = f"{split}_subset"
    subset_path = os.path.join(dataset_path, subset_dir)
    subset_images = os.path.join(subset_path, "images")
    subset_labels = os.path.join(subset_path, "labels")
    
    os.makedirs(subset_images, exist_ok=True)
    os.makedirs(subset_labels, exist_ok=True)
    
    images = [f for f in os.listdir(images_src) if f.lower().endswith((".jpg", ".png"))]
    actual_subset_size = min(subset_size, len(images))
    
    random.seed(42)
    selected = random.sample(images, actual_subset_size)
    
    for img in selected:
        shutil.copy(os.path.join(images_src, img), subset_images)
        # Check for matching label (assuming same filename with .txt)
        label = os.path.splitext(img)[0] + ".txt"
        label_file_src = os.path.join(labels_src, label)
        if os.path.exists(label_file_src):
            shutil.copy(label_file_src, subset_labels)
    
    print(f"Subset created for {split} with {actual_subset_size} images")
    return subset_path

def update_yaml_for_subset(yaml_path, train_subset_path, val_subset_path=None):
    dataset_path = os.path.dirname(yaml_path)
    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f)
    
    # Set relative paths for all sets
    data['train'] = os.path.join(".", os.path.relpath(train_subset_path, dataset_path), "images").replace("\\", "/")
    
    if val_subset_path:
        data['val'] = os.path.join(".", os.path.relpath(val_subset_path, dataset_path), "images").replace("\\", "/")
    else:
        # Fallback to full validation set if no subset created
        val_path = os.path.join(dataset_path, "valid/images")
        if os.path.exists(val_path):
            data['val'] = "./valid/images"
    
    # Optional test path
    test_path = os.path.join(dataset_path, "test/images")
    if os.path.exists(test_path):
        data['test'] = "./test/images"
        
    # Ensure 'val' is present
    if 'val' not in data:
        for folder in ["valid", "val", "validation"]:
            candidate = os.path.join(dataset_path, folder, "images")
            if os.path.exists(candidate):
                data['val'] = f"./{folder}/images"
                break

    with open(yaml_path, 'w') as f:
        yaml.dump(data, f)
    
    print(f"data.yaml updated with relative paths")
