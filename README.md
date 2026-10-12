# 🌸 Phenikaa-Flora: Real-time 10-Class Flower Detection & xAI

Dự án ứng dụng Trí tuệ Nhân tạo nhận diện thời gian thực 10 loài hoa tại khuôn viên Đại học Phenikaa (Phenikaa Campus), tích hợp giải thích mô hình (Explainable AI - xAI) và triển khai Web Realtime trên GitHub Pages (chạy trên cả PC & Mobile).

---

## 📁 Cấu Trúc Thư Mục

```
PKA_M3/
├── Phenikaa-FL-YOLO.zip               # File nén dataset chuẩn YOLO (Tải lên Google Colab)
├── Phenikaa_Flowers_Training_and_xAI.ipynb  # Notebook Colab huấn luyện & chạy xAI trọn gói
├── dataset_yolo/                      # Bộ dữ liệu đã chuyển đổi & chia Train/Val/Test
│   ├── data.yaml                      # Cấu hình 10 classes
│   ├── images/ {train, val, test}
│   └── labels/ {train, val, test}
├── eda_reports/                       # Biểu đồ phân tích dữ liệu phục vụ báo cáo
│   ├── class_distribution.png
│   ├── bbox_dimensions.png
│   └── sample_labels_preview.png
├── web/                               # Mã nguồn Web App Realtime (Deploy GitHub Pages)
│   ├── index.html                     # Giao diện chính (Camera, Slider, Info card)
│   ├── style.css                      # Giao diện Dark mode + Glassmorphism
│   ├── app.js                         # Suy luận ONNX Runtime Web phía trình duyệt
│   └── best.onnx                      # File mô hình (copy từ kết quả Colab vào đây)
└── prepare_yolo_dataset.py            # Script xử lý dữ liệu
```

---

## 🚀 Hướng Dẫn Các Bước Thực Hiện

### Bước 1: Huấn luyện trên Google Colab (GPU NVIDIA T4)
1. Truy cập [Google Colab](https://colab.research.google.com/) và chọn **Upload notebook**.
2. Tải lên file [`Phenikaa_Flowers_Training_and_xAI.ipynb`](Phenikaa_Flowers_Training_and_xAI.ipynb).
3. Bật GPU: Vào **Runtime > Change runtime type > T4 GPU**.
4. Kéo thả file [`Phenikaa-FL-YOLO.zip`](Phenikaa-FL-YOLO.zip) vào thư mục Files (`/content/`) của Colab.
5. Chọn **Runtime > Run all** (Chạy toàn bộ).
6. Sau khoảng 8–10 phút, Colab sẽ:
   - Huấn luyện xong mô hình YOLOv8n.
   - Xuất ma trận nhầm lẫn (Confusion Matrix) và kết quả mAP trên tập Test.
   - Chạy 3 kỹ thuật xAI: **Feature Maps Activation**, **Eigen-CAM / Grad-CAM++**, **t-SNE Feature Embedding**.
   - Xuất mô hình sang định dạng **`best.onnx`**.
   - Tự động nén và tải về máy file `Phenikaa_Flora_Trained_Results.zip`.

---

### Bước 2: Đưa mô hình vào Web và Kiểm thử Local
1. Giải nén file kết quả từ Colab, copy file `best.onnx` vào thư mục `web/`.
2. Mở terminal và chạy thử web tại local:
   ```bash
   cd web
   python3 -m http.server 8000
   ```
3. Mở trình duyệt truy cập `http://localhost:8000` để bật camera máy tính hoặc test tải ảnh.

---

### Bước 3: Triển khai Web Miễn Phí Lên GitHub Pages (Chạy trên Điện thoại & PC)
1. Tạo một repository mới trên GitHub (ví dụ: `phenikaa-flora-ai`).
2. Đẩy toàn bộ nội dung thư mục `web/` lên nhánh `main`:
   ```bash
   cd web
   git init
   git add .
   git commit -m "Deploy Phenikaa-Flora Web App"
   git remote add origin https://github.com/<username>/phenikaa-flora-ai.git
   git branch -M main
   git push -u origin main
   ```
3. Trên GitHub, vào **Settings > Pages**:
   - Tại mục **Build and deployment > Branch**: Chọn nhánh `main` và thư mục `/(root)`.
   - Nhấn **Save**.
4. Sau 1 phút, GitHub Pages sẽ cấp đường link HTTPS miễn phí trọn đời (ví dụ: `https://<username>.github.io/phenikaa-flora-ai/`).
5. **Mở link trên điện thoại:** Trình duyệt di động sẽ yêu cầu quyền Camera, có thể bấm "Đổi Camera" để dùng camera sau quét hoa trực tiếp trong trường Phenikaa!
