import os
import glob
import cv2
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict

def generate_eda():
    yolo_dir = "/Users/haiduong/Desktop/PKA_M3/dataset_yolo"
    output_dir = "/Users/haiduong/Desktop/PKA_M3/eda_reports"
    os.makedirs(output_dir, exist_ok=True)

    class_names = [
        "hoa_chieu_tim", "hoa_dam_but", "hoa_dam_but_cam", "hoa_hong",
        "hoa_lai_tay", "hoa_mau_don_ta", "hoa_mia_do", "hoa_mo_ket",
        "hoa_mo_trang", "huynh_anh_vang"
    ]

    # Collect stats
    split_class_counts = {"train": defaultdict(int), "val": defaultdict(int), "test": defaultdict(int)}
    box_widths = []
    box_heights = []

    for split in ["train", "val", "test"]:
        label_files = glob.glob(os.path.join(yolo_dir, "labels", split, "*.txt"))
        for lf in label_files:
            with open(lf, "r") as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) >= 5:
                        cls_id = int(parts[0])
                        w = float(parts[3])
                        h = float(parts[4])
                        split_class_counts[split][cls_id] += 1
                        box_widths.append(w * 1080)
                        box_heights.append(h * 1920)

    # 1. Plot Class Distribution across splits
    plt.figure(figsize=(12, 6))
    x_indices = list(range(len(class_names)))
    bar_width = 0.25

    train_vals = [split_class_counts["train"][i] for i in x_indices]
    val_vals = [split_class_counts["val"][i] for i in x_indices]
    test_vals = [split_class_counts["test"][i] for i in x_indices]

    plt.bar([x - bar_width for x in x_indices], train_vals, width=bar_width, label="Train", color="#3b82f6")
    plt.bar(x_indices, val_vals, width=bar_width, label="Val", color="#10b981")
    plt.bar([x + bar_width for x in x_indices], test_vals, width=bar_width, label="Test", color="#f59e0b")

    plt.xticks(x_indices, class_names, rotation=35, ha="right", fontsize=10)
    plt.ylabel("Number of Bounding Boxes", fontsize=12)
    plt.title("Phenikaa-Flora: Class Distribution Across Train/Val/Test Splits", fontsize=14, fontweight="bold")
    plt.legend(fontsize=11)
    plt.grid(axis="y", linestyle="--", alpha=0.6)
    plt.tight_layout()
    chart1_path = os.path.join(output_dir, "class_distribution.png")
    plt.savefig(chart1_path, dpi=200)
    plt.close()
    print(f"Saved {chart1_path}")

    # 2. Bounding Box Dimensions Scatter Plot
    plt.figure(figsize=(8, 7))
    sns.scatterplot(x=box_widths, y=box_heights, alpha=0.4, color="#6366f1")
    plt.xlabel("Bounding Box Width (pixels)", fontsize=12)
    plt.ylabel("Bounding Box Height (pixels)", fontsize=12)
    plt.title("Bounding Box Dimensions Distribution (1080x1920 canvas)", fontsize=13, fontweight="bold")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    chart2_path = os.path.join(output_dir, "bbox_dimensions.png")
    plt.savefig(chart2_path, dpi=200)
    plt.close()
    print(f"Saved {chart2_path}")

    # 3. Sample labeled images collage
    sample_images = glob.glob(os.path.join(yolo_dir, "images", "val", "*.jpg"))[:4]
    plt.figure(figsize=(14, 12))
    colors = [
        (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
        (255, 0, 255), (0, 255, 255), (255, 128, 0), (128, 0, 255),
        (0, 128, 255), (255, 0, 128)
    ]

    for idx, img_path in enumerate(sample_images):
        img = cv2.imread(img_path)
        img_h, img_w = img.shape[:2]
        base_name = os.path.splitext(os.path.basename(img_path))[0]
        label_path = os.path.join(yolo_dir, "labels", "val", f"{base_name}.txt")

        if os.path.exists(label_path):
            with open(label_path, "r") as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) >= 5:
                        cls_id = int(parts[0])
                        xc, yc, bw, bh = map(float, parts[1:5])
                        x1 = int((xc - bw / 2) * img_w)
                        y1 = int((yc - bh / 2) * img_h)
                        x2 = int((xc + bw / 2) * img_w)
                        y2 = int((yc + bh / 2) * img_h)

                        c = colors[cls_id % len(colors)]
                        cv2.rectangle(img, (x1, y1), (x2, y2), c, 6)
                        label_txt = f"{class_names[cls_id]}"
                        cv2.putText(img, label_txt, (x1, max(35, y1 - 10)),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3, cv2.LINE_AA)

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        plt.subplot(2, 2, idx + 1)
        plt.imshow(img_rgb)
        plt.title(f"Sample {idx + 1}: {base_name[:20]}...", fontsize=11)
        plt.axis("off")

    plt.tight_layout()
    chart3_path = os.path.join(output_dir, "sample_labels_preview.png")
    plt.savefig(chart3_path, dpi=200)
    plt.close()
    print(f"Saved {chart3_path}")

if __name__ == "__main__":
    generate_eda()
