import os
import json
import shutil
from collections import defaultdict

def prepare_yolo_dataset():
    src_dir = "/Users/haiduong/Desktop/PKA_M3/Phenikaa-FL/train"
    coco_json_path = os.path.join(src_dir, "_annotations.coco.json")
    out_dir = "/Users/haiduong/Desktop/PKA_M3/dataset_yolo"
    
    with open(coco_json_path, "r", encoding="utf-8") as f:
        coco = json.load(f)

    # Filter out category id 0 ('Phenikaa-FL') and build 0-indexed class map
    valid_categories = [c for c in coco["categories"] if c["id"] != 0]
    valid_categories.sort(key=lambda x: x["id"])
    
    coco_to_yolo_id = {}
    class_names = []
    for new_id, cat in enumerate(valid_categories):
        coco_to_yolo_id[cat["id"]] = new_id
        class_names.append(cat["name"])

    print("Class mapping (0 to 9):")
    for new_id, name in enumerate(class_names):
        print(f"  {new_id}: {name}")

    # Map annotations to image_id
    img_annotations = defaultdict(list)
    for ann in coco["annotations"]:
        cid = ann["category_id"]
        if cid in coco_to_yolo_id:
            img_annotations[ann["image_id"]].append(ann)

    # Group images by video sequence
    # Filenames: IMG_1302_MOV-0000_jpg.rf.xxx.jpg
    images = coco["images"]
    video_groups = defaultdict(list)
    for img in images:
        fname = img["file_name"]
        prefix = fname.split("-")[0] if "-" in fname else "misc"
        video_groups[prefix].append(img)

    for pfx in video_groups:
        # Sort by filename so frames are ordered 0000, 0001, 0002...
        video_groups[pfx].sort(key=lambda x: x["file_name"])

    # Prepare directories
    for split in ["train", "val", "test"]:
        os.makedirs(os.path.join(out_dir, "images", split), exist_ok=True)
        os.makedirs(os.path.join(out_dir, "labels", split), exist_ok=True)

    split_counts = defaultdict(int)
    class_split_counts = defaultdict(lambda: defaultdict(int))

    for pfx, img_list in sorted(video_groups.items()):
        n = len(img_list)
        # Split: 75% train, 15% val, 10% test
        n_train = int(n * 0.75)
        n_val = int(n * 0.15)
        # rest is test (at least 1 if n >= 10)
        n_test = n - n_train - n_val

        train_imgs = img_list[:n_train]
        val_imgs = img_list[n_train:n_train + n_val]
        test_imgs = img_list[n_train + n_val:]

        splits = [("train", train_imgs), ("val", val_imgs), ("test", test_imgs)]
        print(f"Prefix {pfx} ({n} images) -> Train: {len(train_imgs)}, Val: {len(val_imgs)}, Test: {len(test_imgs)}")

        for split_name, s_imgs in splits:
            for img in s_imgs:
                split_counts[split_name] += 1
                fname = img["file_name"]
                img_w = img["width"]
                img_h = img["height"]

                # Copy image
                src_img_path = os.path.join(src_dir, fname)
                dst_img_path = os.path.join(out_dir, "images", split_name, fname)
                shutil.copy2(src_img_path, dst_img_path)

                # Write YOLO format label
                base_name = os.path.splitext(fname)[0]
                label_path = os.path.join(out_dir, "labels", split_name, f"{base_name}.txt")

                anns = img_annotations.get(img["id"], [])
                lines = []
                for ann in anns:
                    yolo_cid = coco_to_yolo_id[ann["category_id"]]
                    class_split_counts[split_name][yolo_cid] += 1
                    x, y, w, h = ann["bbox"]
                    
                    # Convert to normalized xywh
                    x_c = (x + w / 2.0) / img_w
                    y_c = (y + h / 2.0) / img_h
                    w_norm = w / img_w
                    h_norm = h / img_h

                    # Clip to [0, 1] for safety
                    x_c = min(max(x_c, 0.0), 1.0)
                    y_c = min(max(y_c, 0.0), 1.0)
                    w_norm = min(max(w_norm, 0.0), 1.0)
                    h_norm = min(max(h_norm, 0.0), 1.0)

                    lines.append(f"{yolo_cid} {x_c:.6f} {y_c:.6f} {w_norm:.6f} {h_norm:.6f}\n")

                with open(label_path, "w", encoding="utf-8") as lf:
                    lf.writelines(lines)

    print("\n--- Summary ---")
    print(f"Total Train images: {split_counts['train']}")
    print(f"Total Val images:   {split_counts['val']}")
    print(f"Total Test images:  {split_counts['test']}")

    # Write data.yaml
    yaml_content = f"""# Phenikaa-Flora 10-Class Flower Dataset for YOLO
path: dataset_yolo # dataset root dir
train: images/train
val: images/val
test: images/test

# Number of classes
nc: {len(class_names)}

# Class names
names:
"""
    for idx, cname in enumerate(class_names):
        yaml_content += f"  {idx}: {cname}\n"

    yaml_path = os.path.join(out_dir, "data.yaml")
    with open(yaml_path, "w", encoding="utf-8") as yf:
        yf.write(yaml_content)

    print(f"\nCreated data.yaml at {yaml_path}")

if __name__ == "__main__":
    prepare_yolo_dataset()
