# Aadhaar Pulse 📊

**Team ID:** UIDAI_12654 | **Hackathon:** UIDAI Data Hackathon 2026

**Aadhaar Pulse** is a data analytics framework designed to unlock actionable insights from Aadhaar enrolment and update datasets. By processing over **4.9 million records**, this solution provides a comprehensive view of the ecosystem's health, identifies operational bottlenecks, and forecasts future demand.

---

## 🚀 Key Features

*   **Trend Analysis**: Monthly tracking of Enrolments vs. Updates (Demographic & Biometric).
*   **Update Burden Index (UBI)**: A custom KPI to identify "Update-Heavy" states that require specialized maintenance centers.
*   **Hotspot Detection**: Identification of high-volume Districts and States to guide infrastructure planning.
*   **Anomaly Detection**: Statistical monitoring (Z-score) to flag operational irregularities.
*   **Forecasting**: Predictive modelling using **Prophet** to estimate update volume for the next quarter.

---

## 📂 Project Structure

```bash
Aadhaar Pulse/
├── aadhaar_pulse.ipynb       # Main Analysis Notebook (Run this!)
├── PROJECT_REPORT.md         # Full detailed report for submission
├── requirements.txt          # Python dependencies
├── data/                     # Raw datasets (Enrolment, Demo, Bio)
└── README.md                 # This file
```

---

## 🛠️ Installation & Usage

1.  **Prerequisites**: Python 3.8+ installed.

2.  **Setup Environment**:
    ```bash
    # Create virtual environment
    python3 -m venv venv
    source venv/bin/activate
    
    # Install dependencies
    pip install -r requirements.txt
    ```

3.  **Run Analysis**:
    launch Jupyter Notebook:
    ```bash
    jupyter notebook aadhaar_pulse.ipynb
    ```
    *Run all cells to generate visuals and analysis.*

---

## 📄 Project Report

For a deep dive into the methodology, detailed findings, and strategic recommendations, please refer to the **[PROJECT_REPORT.md](PROJECT_REPORT.md)** file. This document is formatted for export to PDF for your final hackathon submission.

---
*Generated for UIDAI Data Hackathon 2026*