/**
 * Phenikaa-Flora AI - Real-time Browser Inference with ONNX Runtime Web
 * 10 Flower Classes in Phenikaa University Campus
 */

// 1. Flower Knowledge Base
const FLOWER_DB = [
  {
    id: 0,
    name: "hoa_chieu_tim",
    vietnamese: "Hoa Chiều Tím",
    english: "Mexican Petunia",
    scientific: "Ruellia simplex / Ruellia tuberosa",
    location: "Dọc các bồn hoa lối đi tòa A, ven hàng rào sân bóng và khuôn viên thư viện.",
    description: "Hoa hình loa kèn màu tím đặc trưng, nở rực rỡ vào buổi sáng và chiều, mọc thành từng khóm bụi xanh tươi tốt.",
    color: "#a855f7"
  },
  {
    id: 1,
    name: "hoa_dam_but",
    vietnamese: "Hoa Dâm Bụt (Đỏ)",
    english: "Red Chinese Hibiscus",
    scientific: "Hibiscus rosa-sinensis",
    location: "Hàng rào xanh quanh tòa nhà thí nghiệm và lối đi bộ trung tâm Phenikaa.",
    description: "Cánh hoa to màu đỏ tươi, nhụy hoa dài màu vàng cam nổi bật vươn ra khỏi tâm hoa.",
    color: "#ef4444"
  },
  {
    id: 2,
    name: "hoa_dam_but_cam",
    vietnamese: "Hoa Dâm Bụt Cam",
    english: "Orange Hibiscus",
    scientific: "Hibiscus rosa-sinensis var. orange",
    location: "Khu vườn cảnh quan gần tòa nhà A2 và khu tự học ngoài trời.",
    description: "Hoa dâm bụt có sắc cam hoặc cam viền vàng, cánh hoa mềm mại, nhụy vươn dài thanh thoát.",
    color: "#f97316"
  },
  {
    id: 3,
    name: "hoa_hong",
    vietnamese: "Hoa Hồng",
    english: "Rose",
    scientific: "Rosa spp.",
    location: "Khu vườn hoa hồng trung tâm trước tòa hiệu bộ và bồn hoa tiểu cảnh.",
    description: "Các lớp cánh hoa xếp tầng lớp đan xen, hương thơm dịu nhẹ, lá có răng cưa nhỏ.",
    color: "#f43f5e"
  },
  {
    id: 4,
    name: "hoa_lai_tay",
    vietnamese: "Hoa Lài Tây (Ngọc Bút)",
    english: "Crepe Jasmine",
    scientific: "Tabernaemontana divaricata",
    location: "Các lối đi râm mát dưới tán cây lớn giữa tòa A và giảng đường B.",
    description: "Cánh hoa trắng muốt xòe hình cánh chong chóng 5 cánh hoặc nhiều lớp, lá xanh bóng mượt.",
    color: "#38bdf8"
  },
  {
    id: 5,
    name: "hoa_mau_don_ta",
    vietnamese: "Hoa Mẫu Đơn Ta (Bông Trang Đỏ)",
    english: "Jungle Geranium",
    scientific: "Ixora coccinea",
    location: "Cắt tỉa gọn gàng quanh các bồn cây cảnh lối vào cổng chính Phenikaa.",
    description: "Các chùm hoa hình cầu gồm hàng chục bông hoa nhỏ li ti 4 cánh màu đỏ rực rỡ.",
    color: "#e11d48"
  },
  {
    id: 6,
    name: "hoa_mia_do",
    vietnamese: "Hoa Mía Đỏ (Cát Lồi Đỏ)",
    english: "Red Button Ginger",
    scientific: "Costus woodsonii",
    location: "Khu vực bồn hoa thấp ven hồ cảnh quan và lối dạo quanh công viên sinh viên.",
    description: "Búp hoa hình nón màu đỏ tươi giống bắp ngô nhỏ, hoa con màu cam vàng nhú ra từ các kẽ lá bắc.",
    color: "#dc2626"
  },
  {
    id: 7,
    name: "hoa_mo_ket",
    vietnamese: "Hoa Mỏ Két (Chuối Mỏ Két)",
    english: "Parrot's Beak / False Bird of Paradise",
    scientific: "Heliconia psittacorum",
    location: "Các hàng cây cảnh dọc hành lang tòa nhà A và khu vực sảnh đón tiếp.",
    description: "Cụm hoa mọc đứng gồm các lá bắc màu cam/đỏ cong vút như mỏ chim vẹt, hoa nhỏ màu vàng bên trong.",
    color: "#fb923c"
  },
  {
    id: 8,
    name: "hoa_mo_trang",
    vietnamese: "Hoa Mơ Trắng",
    english: "White Blossom Flower",
    scientific: "Prunus mume / Jasminum",
    location: "Bồn hoa tiểu cảnh đặc biệt tại sảnh chờ và đài phun nước.",
    description: "Cánh hoa trắng tròn trịa thanh khiết, nhụy hoa vàng nhạt, nở rộ thành từng đóa duyên dáng.",
    color: "#94a3b8"
  },
  {
    id: 9,
    name: "huynh_anh_vang",
    vietnamese: "Hoa Huỳnh Anh Vàng",
    english: "Golden Trumpet",
    scientific: "Allamanda cathartica",
    location: "Các giàn hoa leo và hàng rào đón nắng quanh sân thể thao trường.",
    description: "Hoa hình chuông lớn màu vàng rực rỡ như nắng hè, miệng hoa xòe 5 cánh mềm mại.",
    color: "#eab308"
  }
];

// 2. DOM Elements
const video = document.getElementById("videoElement");
const canvas = document.getElementById("overlayCanvas");
const ctx = canvas.getContext("2d");
const staticImagePreview = document.getElementById("staticImagePreview");
const toggleCameraBtn = document.getElementById("toggleCameraBtn");
const cameraBtnLabel = document.getElementById("cameraBtnLabel");
const switchCameraBtn = document.getElementById("switchCameraBtn");
const imageFileInput = document.getElementById("imageFileInput");
const confSlider = document.getElementById("confSlider");
const confValue = document.getElementById("confValue");
const iouSlider = document.getElementById("iouSlider");
const iouValue = document.getElementById("iouValue");
const modelStatusBadge = document.getElementById("modelStatusBadge");
const modelStatusText = document.getElementById("modelStatusText");
const statusDot = modelStatusBadge.querySelector(".status-dot");
const fpsBadge = document.getElementById("fpsBadge");
const inferenceTimeEl = document.getElementById("inferenceTime");
const detectedCountEl = document.getElementById("detectedCount");
const viewportLoader = document.getElementById("viewportLoader");
const loaderMessage = document.getElementById("loaderMessage");
const flowerVietnameseName = document.getElementById("flowerVietnameseName");
const flowerConfidenceBadge = document.getElementById("flowerConfidenceBadge");
const flowerEnglishName = document.getElementById("flowerEnglishName");
const flowerSciName = document.getElementById("flowerSciName");
const flowerLocation = document.getElementById("flowerLocation");
const flowerDescription = document.getElementById("flowerDescription");
const flowerTags = document.querySelectorAll("#flowerTagsList li");

// 3. Application State
let session = null;
let isStreaming = false;
let currentFacingMode = "environment"; // mobile rear camera
let animationFrameId = null;
let lastFrameTime = performance.now();
let fpsCounter = 0;
let fpsTimer = performance.now();
let confThreshold = parseFloat(confSlider.value);
let iouThreshold = parseFloat(iouSlider.value);
let isModelReady = false;
let inputShape = [1, 3, 640, 640];
let isProcessingFrame = false;

// 4. Initialize ONNX Runtime Session
async function initSession() {
  viewportLoader.style.display = "flex";
  loaderMessage.innerText = "Đang tải mô hình best.onnx...";
  modelStatusText.innerText = "Đang tải model...";

  try {
    // Check if best.onnx is accessible
    const response = await fetch("best.onnx", { method: "HEAD" });
    if (!response.ok) {
      throw new Error("Chưa tìm thấy file best.onnx");
    }

    // Configure WebAssembly / WebGPU execution provider
    const sessionOptions = {
      executionProviders: ["webgpu", "wasm"],
      graphOptimizationLevel: "all"
    };

    session = await ort.InferenceSession.create("best.onnx", sessionOptions);
    isModelReady = true;
    statusDot.classList.add("active");
    modelStatusText.innerText = "YOLOv8 Sẵn sàng";
    viewportLoader.style.display = "none";
    console.log("ONNX session created successfully!", session.inputNames, session.outputNames);
  } catch (error) {
    console.warn("Không tìm thấy best.onnx, kích hoạt chế độ Demo/Standby:", error);
    isModelReady = false;
    modelStatusText.innerText = "Chế độ Standby (Chờ best.onnx)";
    loaderMessage.innerHTML = "Chưa có file <code>best.onnx</code>.<br><small>Hãy copy file best.onnx sau khi train từ Colab vào thư mục web/ nhé!</small>";
    
    // Auto hide loader after 3.5s so user can test camera UI
    setTimeout(() => {
      viewportLoader.style.display = "none";
    }, 3500);
  }
}

// 5. Camera Management
async function startCamera() {
  if (video.srcObject) {
    video.srcObject.getTracks().forEach(track => track.stop());
  }

  const constraints = {
    audio: false,
    video: {
      facingMode: currentFacingMode,
      width: { ideal: 1280 },
      height: { ideal: 720 }
    }
  };

  try {
    const stream = await navigator.mediaDevices.getUserMedia(constraints);
    video.srcObject = stream;
    staticImagePreview.style.display = "none";
    video.style.display = "block";

    video.onloadedmetadata = () => {
      video.play();
      isStreaming = true;
      cameraBtnLabel.innerText = "Dừng Camera";
      resizeCanvas();
      detectLoop();
    };
  } catch (err) {
    console.error("Lỗi truy cập camera:", err);
    alert("Không thể mở camera. Vui lòng cấp quyền truy cập camera trên trình duyệt!");
  }
}

function stopCamera() {
  if (video.srcObject) {
    video.srcObject.getTracks().forEach(track => track.stop());
    video.srcObject = null;
  }
  isStreaming = false;
  cameraBtnLabel.innerText = "Bật Camera";
  if (animationFrameId) {
    cancelAnimationFrame(animationFrameId);
  }
  ctx.clearRect(0, 0, canvas.width, canvas.height);
}

function switchCamera() {
  currentFacingMode = currentFacingMode === "environment" ? "user" : "environment";
  if (isStreaming) {
    startCamera();
  }
}

// 6. Preprocessing (Resize & Letterbox to 640x640)
function preprocess(sourceElement) {
  const modelW = 640;
  const modelH = 640;

  const tempCanvas = document.createElement("canvas");
  tempCanvas.width = modelW;
  tempCanvas.height = modelH;
  const tempCtx = tempCanvas.getContext("2d");

  // Fill black padding
  tempCtx.fillStyle = "#000000";
  tempCtx.fillRect(0, 0, modelW, modelH);

  const srcW = sourceElement.videoWidth || sourceElement.naturalWidth || sourceElement.width;
  const srcH = sourceElement.videoHeight || sourceElement.naturalHeight || sourceElement.height;

  // Scale ratio
  const scale = Math.min(modelW / srcW, modelH / srcH);
  const nw = srcW * scale;
  const nh = srcH * scale;
  const dx = (modelW - nw) / 2;
  const dy = (modelH - nh) / 2;

  tempCtx.drawImage(sourceElement, dx, dy, nw, nh);

  const imageData = tempCtx.getImageData(0, 0, modelW, modelH);
  const data = imageData.data;

  // Convert RGBA to planar CHW float32 tensor normalized to [0, 1]
  const float32Data = new Float32Array(3 * modelW * modelH);
  const planeSize = modelW * modelH;

  for (let i = 0; i < planeSize; i++) {
    float32Data[i] = data[i * 4] / 255.0; // R
    float32Data[planeSize + i] = data[i * 4 + 1] / 255.0; // G
    float32Data[2 * planeSize + i] = data[i * 4 + 2] / 255.0; // B
  }

  const tensor = new ort.Tensor("float32", float32Data, inputShape);
  return { tensor, scale, dx, dy, srcW, srcH };
}

// 7. Postprocessing (YOLOv8 Output Parser & NMS)
function postprocess(outputTensor, scale, dx, dy, srcW, srcH) {
  // YOLOv8 output shape: [1, 14, 8400]
  const data = outputTensor.data;
  const dims = outputTensor.dims; // [1, 14, 8400]
  const numChannels = dims[1]; // 14: 4 coords + 10 classes
  const numBoxes = dims[2]; // 8400 candidates
  const numClasses = numChannels - 4; // 10

  const boxes = [];

  for (let i = 0; i < numBoxes; i++) {
    // Find class with max confidence
    let maxScore = 0;
    let maxClass = -1;

    for (let c = 0; c < numClasses; c++) {
      const score = data[(4 + c) * numBoxes + i];
      if (score > maxScore) {
        maxScore = score;
        maxClass = c;
      }
    }

    if (maxScore >= confThreshold) {
      const xc = data[0 * numBoxes + i];
      const yc = data[1 * numBoxes + i];
      const w = data[2 * numBoxes + i];
      const h = data[3 * numBoxes + i];

      // Convert from letterbox 640x640 back to original source coords
      const x1 = (xc - w / 2 - dx) / scale;
      const y1 = (yc - h / 2 - dy) / scale;
      const x2 = (xc + w / 2 - dx) / scale;
      const y2 = (yc + h / 2 - dy) / scale;

      boxes.push({
        x1: Math.max(0, x1),
        y1: Math.max(0, y1),
        x2: Math.min(srcW, x2),
        y2: Math.min(srcH, y2),
        score: maxScore,
        classId: maxClass
      });
    }
  }

  // Non-Maximum Suppression (NMS)
  return applyNMS(boxes, iouThreshold);
}

function applyNMS(boxes, iouThresh) {
  boxes.sort((a, b) => b.score - a.score);
  const selected = [];

  for (const box of boxes) {
    let keep = true;
    for (const prior of selected) {
      if (box.classId === prior.classId) {
        const iou = calculateIoU(box, prior);
        if (iou > iouThresh) {
          keep = false;
          break;
        }
      }
    }
    if (keep) {
      selected.push(box);
    }
  }

  return selected;
}

function calculateIoU(b1, b2) {
  const xx1 = Math.max(b1.x1, b2.x1);
  const yy1 = Math.max(b1.y1, b2.y1);
  const xx2 = Math.min(b1.x2, b2.x2);
  const yy2 = Math.min(b1.y2, b2.y2);

  const w = Math.max(0, xx2 - xx1);
  const h = Math.max(0, yy2 - yy1);
  const inter = w * h;

  const area1 = (b1.x2 - b1.x1) * (b1.y2 - b1.y1);
  const area2 = (b2.x2 - b2.x1) * (b2.y2 - b2.y1);
  const union = area1 + area2 - inter;

  return union <= 0 ? 0 : inter / union;
}

// 8. Canvas Rendering
function renderDetections(detections, srcW, srcH) {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  const scaleX = canvas.width / srcW;
  const scaleY = canvas.height / srcH;

  detectedCountEl.innerText = detections.length;

  // Reset tag highlight
  flowerTags.forEach(tag => tag.classList.remove("active"));

  if (detections.length === 0) {
    flowerConfidenceBadge.innerText = "Chờ nhận diện";
    return;
  }

  // Find most confident detection to update info card
  const topDetection = detections[0];
  const flower = FLOWER_DB[topDetection.classId];
  if (flower) {
    flowerVietnameseName.innerText = `🌸 ${flower.vietnamese}`;
    flowerConfidenceBadge.innerText = `${Math.round(topDetection.score * 100)}% Tin cậy`;
    flowerEnglishName.innerText = flower.english;
    flowerSciName.innerText = flower.scientific;
    flowerLocation.innerText = flower.location;
    flowerDescription.innerText = flower.description;

    // Highlight tag in list
    const tag = document.querySelector(`#flowerTagsList li[data-class="${flower.id}"]`);
    if (tag) tag.classList.add("active");
  }

  // Draw each box
  for (const det of detections) {
    const fInfo = FLOWER_DB[det.classId] || { vietnamese: "Hoa", color: "#6366f1" };
    const x = det.x1 * scaleX;
    const y = det.y1 * scaleY;
    const w = (det.x2 - det.x1) * scaleX;
    const h = (det.y2 - det.y1) * scaleY;

    // Bounding box glow
    ctx.shadowColor = fInfo.color;
    ctx.shadowBlur = 12;

    // Box stroke
    ctx.strokeStyle = fInfo.color;
    ctx.lineWidth = 3.5;
    ctx.strokeRect(x, y, w, h);

    // Label tag
    ctx.shadowBlur = 0;
    const labelText = `${fInfo.vietnamese} (${Math.round(det.score * 100)}%)`;
    ctx.font = "bold 13px 'Plus Jakarta Sans', sans-serif";
    const textWidth = ctx.measureText(labelText).width;

    ctx.fillStyle = fInfo.color;
    ctx.fillRect(x - 1, Math.max(0, y - 24), textWidth + 14, 24);

    ctx.fillStyle = "#ffffff";
    ctx.fillText(labelText, x + 7, Math.max(16, y - 7));
  }
}

// 9. Real-time Detection Loop
async function detectLoop() {
  if (!isStreaming) return;

  if (isModelReady && session && !isProcessingFrame && video.readyState === 4) {
    isProcessingFrame = true;
    const t0 = performance.now();

    try {
      const { tensor, scale, dx, dy, srcW, srcH } = preprocess(video);
      const feeds = {};
      feeds[session.inputNames[0]] = tensor;

      const results = await session.run(feeds);
      const output = results[session.outputNames[0]];

      const detections = postprocess(output, scale, dx, dy, srcW, srcH);
      renderDetections(detections, srcW, srcH);

      const t1 = performance.now();
      inferenceTimeEl.innerText = `${Math.round(t1 - t0)} ms`;
    } catch (err) {
      console.error("Lỗi suy luận:", err);
    } finally {
      isProcessingFrame = false;
    }
  }

  // FPS calculation
  fpsCounter++;
  const now = performance.now();
  if (now - fpsTimer >= 1000) {
    const currentFps = Math.round((fpsCounter * 1000) / (now - fpsTimer));
    fpsBadge.innerText = `${currentFps} FPS`;
    fpsCounter = 0;
    fpsTimer = now;
  }

  animationFrameId = requestAnimationFrame(detectLoop);
}

// 10. Process Static Uploaded Image
async function processStaticImage(imgElement) {
  if (!isModelReady || !session) {
    alert("Vui lòng đợi mô hình ONNX tải xong trước khi phân tích ảnh!");
    return;
  }

  viewportLoader.style.display = "flex";
  loaderMessage.innerText = "Đang nhận diện loài hoa...";

  setTimeout(async () => {
    const t0 = performance.now();
    try {
      const { tensor, scale, dx, dy, srcW, srcH } = preprocess(imgElement);
      const feeds = {};
      feeds[session.inputNames[0]] = tensor;

      const results = await session.run(feeds);
      const output = results[session.outputNames[0]];

      const detections = postprocess(output, scale, dx, dy, srcW, srcH);
      renderDetections(detections, srcW, srcH);

      const t1 = performance.now();
      inferenceTimeEl.innerText = `${Math.round(t1 - t0)} ms`;
    } catch (err) {
      console.error("Lỗi phân tích ảnh:", err);
    } finally {
      viewportLoader.style.display = "none";
    }
  }, 50);
}

// 11. Canvas resizing
function resizeCanvas() {
  const rect = canvas.getBoundingClientRect();
  canvas.width = rect.width;
  canvas.height = rect.height;
}

// 12. Event Listeners
window.addEventListener("resize", resizeCanvas);

toggleCameraBtn.addEventListener("click", () => {
  if (isStreaming) {
    stopCamera();
  } else {
    startCamera();
  }
});

switchCameraBtn.addEventListener("click", switchCamera);

imageFileInput.addEventListener("change", (e) => {
  const file = e.target.files[0];
  if (!file) return;

  stopCamera();
  const reader = new FileReader();
  reader.onload = (event) => {
    staticImagePreview.src = event.target.result;
    staticImagePreview.style.display = "block";
    video.style.display = "none";
    staticImagePreview.onload = () => {
      resizeCanvas();
      processStaticImage(staticImagePreview);
    };
  };
  reader.readAsDataURL(file);
});

confSlider.addEventListener("input", (e) => {
  confThreshold = parseFloat(e.target.value);
  confValue.innerText = confThreshold.toFixed(2);
});

iouSlider.addEventListener("input", (e) => {
  iouThreshold = parseFloat(e.target.value);
  iouValue.innerText = iouThreshold.toFixed(2);
});

// Click flower tag to show information
flowerTags.forEach((tag, idx) => {
  tag.addEventListener("click", () => {
    flowerTags.forEach(t => t.classList.remove("active"));
    tag.classList.add("active");
    const flower = FLOWER_DB[idx];
    if (flower) {
      flowerVietnameseName.innerText = `🌸 ${flower.vietnamese}`;
      flowerConfidenceBadge.innerText = "Thông tin tra cứu";
      flowerEnglishName.innerText = flower.english;
      flowerSciName.innerText = flower.scientific;
      flowerLocation.innerText = flower.location;
      flowerDescription.innerText = flower.description;
    }
  });
});

// Start initialization on page load
document.addEventListener("DOMContentLoaded", () => {
  resizeCanvas();
  initSession();
});
