import os
import glob
import shutil
from collections import defaultdict

def merge_datasets():
    old_dir = "/Users/haiduong/Desktop/PKA_M3/dataset_yolo"
    new_dir = "/Users/haiduong/Desktop/PKA_M3/Data_14"
    out_dir = "/Users/haiduong/Desktop/PKA_M3/dataset_merged_10"

    # Mapping from Data_14 to Unified 10 classes
    data_14_to_unified = {
        0: 0,   # chieu_tim -> hoa_chieu_tim
        4: 1,   # dam_but_vang -> hoa_dam_but
        3: 2,   # dam_but_cam -> hoa_dam_but_cam
        5: 3,   # hong -> hoa_hong
        13: 4,  # ngoc_but -> hoa_lai_tay
        8: 5,   # mau_don_do -> hoa_mau_don_ta
        11: 6,  # mia_do -> hoa_mia_do
        2: 7,   # chuoi_mo_ket -> hoa_mo_ket
        12: 8,  # mo_trang -> hoa_mo_trang
        6: 9    # huynh_anh -> huynh_anh_vang
    }

    unified_classes = [
        "hoa_chieu_tim", "hoa_dam_but", "hoa_dam_but_cam", "hoa_hong",
        "hoa_lai_tay", "hoa_mau_don_ta", "hoa_mia_do", "hoa_mo_ket",
        "hoa_mo_trang", "huynh_anh_vang"
    ]

    # Create target directories
    for split in ["train", "val", "test"]:
        os.makedirs(os.path.join(out_dir, "images", split), exist_ok=True)
        os.makedirs(os.path.join(out_dir, "labels", split), exist_ok=True)

    print("=== BẮT ĐẦU GỘP BỘ DỮ LIỆU ===")
    
    # 1. Copy old dataset (dataset_yolo)
    old_copied = {"train": 0, "val": 0, "test": 0}
    old_boxes = defaultdict(int)

    for split in ["train", "val", "test"]:
        img_files = glob.glob(os.path.join(old_dir, "images", split, "*.*"))
        for img_p in img_files:
            fname = os.path.basename(img_p)
            base_name = os.path.splitext(fname)[0]
            lbl_p = os.path.join(old_dir, "labels", split, f"{base_name}.txt")

            if os.path.exists(lbl_p):
                # Copy image
                dst_img = os.path.join(out_dir, "images", split, fname)
                shutil.copy2(img_p, dst_img)

                # Copy label
                dst_lbl = os.path.join(out_dir, "labels", split, f"{base_name}.txt")
                shutil.copy2(lbl_p, dst_lbl)
                old_copied[split] += 1

                with open(lbl_p, "r") as f:
                    for line in f:
                        parts = line.strip().split()
                        if parts:
                            old_boxes[int(parts[0])] += 1

    print(f"1. Đã copy dữ liệu cũ ({sum(old_copied.values())} ảnh):")
    print(f"   - Train: {old_copied['train']}, Val: {old_copied['val']}, Test: {old_copied['test']}")
    print(f"   - Tổng box cũ: {sum(old_boxes.values())}")

    # 2. Filter and merge new dataset (Data_14)
    new_copied = {"train": 0, "val": 0, "test": 0}
    new_boxes = defaultdict(int)

    split_map = [("train", "train"), ("valid", "val"), ("test", "test")]

    for split_in, split_out in split_map:
        lbl_files = glob.glob(os.path.join(new_dir, split_in, "labels", "*.txt"))
        for lbl_p in lbl_files:
            fname_txt = os.path.basename(lbl_p)
            base_name = os.path.splitext(fname_txt)[0]

            # Find matching image file
            possible_imgs = glob.glob(os.path.join(new_dir, split_in, "images", f"{base_name}.*"))
            if not possible_imgs:
                continue
            img_p = possible_imgs[0]
            img_ext = os.path.splitext(img_p)[1]

            # Read and filter bounding boxes
            filtered_lines = []
            with open(lbl_p, "r") as f:
                for line in f:
                    parts = line.strip().split()
                    if parts:
                        orig_cid = int(parts[0])
                        if orig_cid in data_14_to_unified:
                            new_cid = data_14_to_unified[orig_cid]
                            new_boxes[new_cid] += 1
                            parts[0] = str(new_cid)
                            filtered_lines.append(" ".join(parts) + "\n")

            # Only include image if it has at least one target box
            if filtered_lines:
                dst_img = os.path.join(out_dir, "images", split_out, f"d14_{base_name}{img_ext}")
                dst_lbl = os.path.join(out_dir, "labels", split_out, f"d14_{base_name}.txt")

                shutil.copy2(img_p, dst_img)
                with open(dst_lbl, "w") as f:
                    f.writelines(filtered_lines)

                new_copied[split_out] += 1

    print(f"\n2. Đã lọc và bổ sung từ Data_14 ({sum(new_copied.values())} ảnh mới):")
    print(f"   - Train: {new_copied['train']}, Val: {new_copied['val']}, Test: {new_copied['test']}")
    print(f"   - Tổng box mới bổ sung: {sum(new_boxes.values())}")

    # 3. Create data.yaml
    total_imgs = {s: old_copied[s] + new_copied[s] for s in ["train", "val", "test"]}
    yaml_content = f"""# Phenikaa-Flora Combined 10-Class Flower Dataset for YOLO
path: dataset_merged_10 # dataset root dir
train: images/train
val: images/val
test: images/test

# Number of classes
nc: {len(unified_classes)}

# Class names
names:
"""
    for idx, cname in enumerate(unified_classes):
        yaml_content += f"  {idx}: {cname}\n"

    yaml_path = os.path.join(out_dir, "data.yaml")
    with open(yaml_path, "w", encoding="utf-8") as f:
        f.write(yaml_content)

    print(f"\n3. Đã tạo file cấu hình data.yaml tại: {yaml_path}")
    print("\n=== TỔNG KẾT BỘ DỮ LIỆU GỘP (dataset_merged_10) ===")
    print(f"• Tập Train: {total_imgs['train']} ảnh")
    print(f"• Tập Val:   {total_imgs['val']} ảnh")
    print(f"• Tập Test:  {total_imgs['test']} ảnh")
    print(f"• TỔNG CỘNG: {sum(total_imgs.values())} ảnh")

    print("\nChi tiết phân bố 10 loài hoa sau khi gộp:")
    print(f"{'ID':<3} | {'Tên loài hoa':<20} | {'Box Cũ':<10} | {'Box Mới':<10} | {'Tổng Bounding Boxes'}")
    print("-" * 70)
    total_all_boxes = 0
    for idx, name in enumerate(unified_classes):
        ob = old_boxes[idx]
        nb = new_boxes[idx]
        tb = ob + nb
        total_all_boxes += tb
        print(f"{idx:<3} | {name:<20} | {ob:<10} | {nb:<10} | {tb:<10}")
    print("-" * 70)
    print(f"TỔNG SỐ BOUNDING BOXES: {total_all_boxes} nhãn (gấp {total_all_boxes / sum(old_boxes.values()):.1f} lần bộ cũ)")

if __name__ == "__main__":
    merge_datasets()
