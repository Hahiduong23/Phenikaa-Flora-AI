import os
import glob
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict

def generate_merged_eda():
    merged_dir = "/Users/haiduong/Desktop/PKA_M3/dataset_merged_10"
    out_dir = "/Users/haiduong/Desktop/PKA_M3/eda_reports"
    os.makedirs(out_dir, exist_ok=True)

    class_names = [
        "hoa_chieu_tim", "hoa_dam_but", "hoa_dam_but_cam", "hoa_hong",
        "hoa_lai_tay", "hoa_mau_don_ta", "hoa_mia_do", "hoa_mo_ket",
        "hoa_mo_trang", "huynh_anh_vang"
    ]

    split_class_counts = {"train": defaultdict(int), "val": defaultdict(int), "test": defaultdict(int)}
    box_w = []
    box_h = []

    for split in ["train", "val", "test"]:
        lbl_files = glob.glob(os.path.join(merged_dir, "labels", split, "*.txt"))
        for lf in lbl_files:
            with open(lf) as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) >= 5:
                        cid = int(parts[0])
                        w = float(parts[3])
                        h = float(parts[4])
                        split_class_counts[split][cid] += 1
                        box_w.append(w)
                        box_h.append(h)

    # 1. Bar chart across Train, Val, Test for merged dataset
    plt.figure(figsize=(13, 6))
    x_indices = list(range(len(class_names)))
    bar_width = 0.25

    train_vals = [split_class_counts["train"][i] for i in x_indices]
    val_vals = [split_class_counts["val"][i] for i in x_indices]
    test_vals = [split_class_counts["test"][i] for i in x_indices]

    plt.bar([x - bar_width for x in x_indices], train_vals, width=bar_width, label=f"Train ({sum(train_vals)})", color="#3b82f6")
    plt.bar(x_indices, val_vals, width=bar_width, label=f"Val ({sum(val_vals)})", color="#10b981")
    plt.bar([x + bar_width for x in x_indices], test_vals, width=bar_width, label=f"Test ({sum(test_vals)})", color="#f59e0b")

    plt.xticks(x_indices, class_names, rotation=35, ha="right", fontsize=10, fontweight="bold")
    plt.ylabel("Số lượng Bounding Boxes", fontsize=12)
    plt.title("Phenikaa-Flora: Phân Bố 10 Loài Hoa Trên Bộ Dữ Liệu Lớn Đã Gộp (10.926 Boxes)", fontsize=14, fontweight="bold")
    plt.legend(fontsize=11)
    plt.grid(axis="y", linestyle="--", alpha=0.6)
    plt.tight_layout()
    chart1 = os.path.join(out_dir, "class_distribution_merged.png")
    plt.savefig(chart1, dpi=200)
    plt.close()
    print(f"Saved {chart1}")

    # 2. Growth comparison chart (Old vs Merged)
    plt.figure(figsize=(10, 5))
    metrics = ["Số lượng ảnh (Images)", "Số lượng nhãn (Bounding Boxes)"]
    old_vals = [788, 1290]
    merged_vals = [4227, 10926]

    x = range(len(metrics))
    width = 0.35

    bars1 = plt.bar([p - width/2 for p in x], old_vals, width, label="Bộ Dữ Liệu Cũ", color="#94a3b8")
    bars2 = plt.bar([p + width/2 for p in x], merged_vals, width, label="Bộ Dữ Liệu Mới Đã Gộp", color="#6366f1")

    # Add data labels on bars
    for b in bars1:
        yval = b.get_height()
        plt.text(b.get_x() + b.get_width()/2, yval + 150, f"{yval:,}", ha="center", va="bottom", fontweight="bold")
    for b in bars2:
        yval = b.get_height()
        multiplier = yval / old_vals[int(b.get_x() > 0.5)]
        plt.text(b.get_x() + b.get_width()/2, yval + 150, f"{yval:,} (x{multiplier:.1f})", ha="center", va="bottom", fontweight="bold", color="#4338ca")

    plt.xticks(x, metrics, fontsize=12, fontweight="bold")
    plt.ylabel("Quy mô dữ liệu", fontsize=12)
    plt.title("So Sánh Quy Mô Bộ Dữ Liệu Trước & Sau Khi Mở Rộng Gộp Data_14", fontsize=14, fontweight="bold")
    plt.legend(fontsize=11)
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.ylim(0, 13000)
    plt.tight_layout()
    chart2 = os.path.join(out_dir, "dataset_growth_comparison.png")
    plt.savefig(chart2, dpi=200)
    plt.close()
    print(f"Saved {chart2}")

if __name__ == "__main__":
    generate_merged_eda()
