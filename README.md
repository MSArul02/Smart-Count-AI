# Smart Count AI — Object Detection & Counting (Classical Computer Vision)

**Smart Count AI** is a lightweight object detection and counting system built using **Flask**, **OpenCV**, and **Classical Image Processing** (segmentation + watershed + contour analysis).  
It is designed for counting small hardware components such as **nuts, bolts, screws, and washers** in controlled conditions.

This project showcases practical computer-vision engineering skills without using any trained deep-learning models.

---

## 🧪 Example Output

<img width="1919" height="768" alt="image" src="https://github.com/user-attachments/assets/2509bd7a-da53-496e-8a66-bfd6b7370d49" />
<img width="1919" height="764" alt="image" src="https://github.com/user-attachments/assets/f3590893-a809-4f62-81ed-00f54e04a954" />
<img width="1919" height="769" alt="image" src="https://github.com/user-attachments/assets/c942946a-7d2e-4fd6-93d9-73b432d01045" />
<img width="1919" height="772" alt="image" src="https://github.com/user-attachments/assets/1950bd22-287e-437f-a4b5-dcd3587896d4" />

---

## 🚀 Features

### ✔ Classical CV Object Detection  
No machine learning, no training required. The system uses a custom pipeline built from:
- CLAHE illumination normalization  
- Morphological operations  
- Adaptive thresholding  
- Distance transform  
- **Watershed segmentation** for separating touching objects  
- Contour analysis  
- Shape-based heuristics (circularity, aspect ratio, extent)

### ✔ Web App Interface  
- **Live camera feed** (browser-based)  
- **Image upload**  
- **Adjustable confidence threshold**  
- **Instant annotated results**  
- **Download annotated image**  
- **Session statistics** (counts, average, range, time)

### ✔ Stability (Vibration Method)  
A rolling window computes:
- Most frequent count across recent frames  
- Consistency score  
- Recommendation to stabilize counting  

---

## 🎯 Purpose of the Project

Modern factories often need rapid counting of mixed hardware items.  
Smart Count AI demonstrates how **classical CV techniques** can be used to rapidly prototype such a counting system with:

- No training  
- No GPU  
- No datasets  
- Fully offline  
- Easy demonstration locally  

---

## 🧠 How the Algorithm Works

### 1️⃣ Preprocessing  
- Convert to grayscale  
- Apply **CLAHE** for contrast enhancement  
- Smooth using bilateral/Gaussian filters

### 2️⃣ Segmentation  
- Morphological top-hat operations  
- Adaptive thresholding  
- Distance transform  
- **Watershed segmentation** to split touching objects

### 3️⃣ Contour Filtering  
Contours are filtered based on:
- Area  
- Circularity  
- Extent ratio  
- Aspect ratio  
- Boundary proximity  

### 4️⃣ Type Classification (Heuristic-based)  
Based on shape features:
- Nuts  
- Bolts  
- Screws  
- Washers  

### 5️⃣ Stabilization  
Rolling window count → most common count → consistency score.

---

## 📂 Project Structure

```
Object_counter/
│
├── simple_working_app.py           # Flask backend
├── simple_working_detector.py      # Core classical CV detector
├── requirements.txt                # Dependencies
│
├── templates/
│   └── simple_factory_index.html   # Main UI page
│
├── static/
│   ├── simple_factory_style.css    # Styling
│   ├── simple_factory_script.js    # Frontend logic
│   ├── uploads/                    # Uploaded images
│   ├── results/                    # Annotated outputs
│   └── debug/                      # Optional debug outputs
│
└── README.md
```

---

## 🛠 Installation

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/Object_counter.git
cd Object_counter
```

### 2. Create a virtual environment  
**Windows PowerShell:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application

```bash
python simple_working_app.py
```

Open in browser:

```
http://127.0.0.1:5000
```

---

## 🎛 UI Overview

### **Left Panel**
- Camera feed  
- Upload button  
- Capture button  
- Confidence slider  

### **Center Panel**
- Annotated detection result  
- Count + confidence  
- Vibration-based count consistency  

### **Right Panel**
- Classification breakdown  
- Session statistics (images, average, range, duration)

---

## 📊 Strengths

- Works offline  
- No dataset or GPU required  
- Simple UI  
- Good results in controlled lighting  
- Excellent for demonstrating **classical CV thinking**  

---

## 🔮 Future Improvements

1. Replace heuristics with a trained detector (YOLO, SSD, RT-DETR)  
2. Add camera calibration for consistent size filtering  
3. Real-time inference mode  
4. Dataset creation + annotation pipeline  
5. Docker container for deployment  
6. Batch processing + CSV/JSON export  


