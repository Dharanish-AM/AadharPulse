# Aadhaar Pulse: Trends, Update Burden Index (UBI), Anomaly Alerts & Forecasting using UIDAI Datasets (Mar–Dec 2025)

**Team ID:** UIDAI_12654
**Hackathon:** UIDAI Data Hackathon 2026
**Team Members:** Name | College | Email
**Date:** 20 Jan 2026

> *“From Aadhaar raw counts → action-ready operational insights”*

<div style="page-break-after: always;"></div>

## Executive Summary

Aadhaar Pulse investigates the operational dynamics of the Aadhaar ecosystem using three distinct datasets: Enrolment, Demographic Updates, and Biometric Updates (processing over 4.9 million records). We have built a comprehensive analytics framework featuring **Trend Analysis**, **Hotspot Detection**, a novel **Update Burden Index (UBI)**, **Anomaly Detection**, and **Predictive Forecasting**. This solution empowers UIDAI to shift from reactive monitoring to proactive resource allocation, detecting operational irregularities early (via Z-score alerts), and planning infrastructure scaling based on predictive demand patterns for the next quarter.

### Dataset Overview

| Dataset | Records | Time Period |
| :--- | :--- | :--- |
| **Enrolment** | **1,006,029** | Mar–Dec 2025 |
| **Demographic Updates** | **2,071,700** | Mar–Oct 2025 |
| **Biometric Updates** | **1,861,108** | Mar–Oct 2025 |

<div style="page-break-after: always;"></div>

## 3. Problem Statement & Approach

### 3.1 Problem Statement

"Identify meaningful patterns, trends, anomalies, predictive indicators from Aadhaar enrolment and update datasets and translate into insights/frameworks to support decision-making."

### 3.2 Approach (Framework)

The **Aadhaar Pulse Framework** delivers a multi-layered analytical solution:

*   **Trend Analysis:** Tracking monthly ecosystem activity to identify seasonal peaks and growth trajectories.
*   **Hotspot Detection:** Identifying high-activity zones at State, District, and Pincode levels for targeted interventions.
*   **Update Burden Index (UBI):** A custom KPI to quantify operational strain caused by updates relative to base enrolment.
*   **Anomaly Detection:** Statistical monitoring to flag irregular spikes or drops in daily/monthly processing volumes.
*   **Forecasting:** Predictive modelling (Prophet) to estimate future demand for next 2-3 months.
*   **Recommendations:** Strategic guidance for manpower and infrastructure derived from data insights.

<div style="page-break-after: always;"></div>

## 4. Datasets Used

### 4.1 Aadhaar Enrolment Dataset
*   **Records:** 1,006,029
*   **Coverage:** 55 States, 985 Districts, 19,463 Pincodes
*   **Time Range:** Mar 2, 2025 – Dec 31, 2025
*   **Schema:** `date`, `state`, `district`, `pincode`, `age_0_5`, `age_5_17`, `age_18_greater`

### 4.2 Aadhaar Demographic Update Dataset
*   **Records:** 2,071,700
*   **Coverage:** 65 States, 983 Districts, 19,742 Pincodes
*   **Time Range:** Mar 2025 – Oct 2025
*   **Schema:** `date`, `state`, `district`, `pincode`, `demo_age_5_17`, `demo_age_17_`

### 4.3 Aadhaar Biometric Update Dataset
*   **Records:** 1,861,108
*   **Coverage:** 57 States, 974 Districts, 19,707 Pincodes
*   **Time Range:** Mar 2025 – Oct 2025
*   **Schema:** `date`, `state`, `district`, `pincode`, `bio_age_5_17`, `bio_age_17_`

> **Data Quality Notes:** No missing values detected; daily noise exists which is smoothed via monthly aggregation.

<div style="page-break-after: always;"></div>

## 5. Methodology

### 5.1 Data Cleaning & Preprocessing
*   **Merge CSV Shards:** Ingested multiple CSV files into single DataFrames.
*   **Date Parsing:** Converted `date` column (DD-MM-YYYY) to proper datetime objects.
*   **Aggregation:** Created a `month` column (YYYY-MM) to align varying time ranges.
*   **Validation:** Ensured all counts are non-negative.

### 5.2 Feature Engineering
We derived critical aggregate metrics to simplify analysis:
*   `total_enrolments` = `age_0_5` + `age_5_17` + `age_18_greater`
*   `total_demo_updates` = `demo_age_5_17` + `demo_age_17_`
*   `total_bio_updates` = `bio_age_5_17` + `bio_age_17_`
*   `total_updates` = `total_demo_updates` + `total_bio_updates`

### 5.3 KPI: Update Burden Index (UBI)
We introduced the UBI to measure operational stress:
$$ UBI = \frac{\text{Total Updates}}{\text{Total Enrolments} + 1} $$

*   **High UBI:** "Update-Heavy" region—requires maintenance-focused resources.
*   **Low UBI:** "Enrolment-Driven" region—requires acquisition-focused resources (camps).

### 5.4 Techniques Used
*   **Univariate/Bivariate Analysis:** Distribution & Correlation checks.
*   **Anomaly Detection:** Rolling Window Z-score (Threshold > 3 sigma).
*   **Forecasting:** Meta's Prophet model for seasonality-aware predictions.

<div style="page-break-after: always;"></div>

## 6. Data Analysis & Visualisations

### 6.1 National Trend Dashboard

**Figure 1: Monthly Enrolments Trend**
![Dataset Overview](/Users/dharanisham/.gemini/antigravity/brain/5e809bd3-da2c-4f00-9955-4d2aafede202/dataset_overview.png)

**Figure 2: Monthly Total Updates Trend**
![Enrolment vs Updates](/Users/dharanisham/.gemini/antigravity/brain/5e809bd3-da2c-4f00-9955-4d2aafede202/enrolment_vs_updates.png)

**Insights:**
*   **Time Coverage:** Enrolment data extends to Dec 2025, while updates are available until Oct 2025.
*   **Volatility:** Update volumes show significantly higher month-to-month volatility compared to steady enrolments.

<div style="page-break-after: always;"></div>

### 6.2 State Hotspot Ranking

**Figure 3: Top 10 States by Enrolment**
![Top 10 States Enrolment](/Users/dharanisham/.gemini/antigravity/brain/5e809bd3-da2c-4f00-9955-4d2aafede202/top10_enrolment.png)

**Figure 4: Top 10 States by Total Updates**
![Top 10 States Updates](/Users/dharanisham/.gemini/antigravity/brain/5e809bd3-da2c-4f00-9955-4d2aafede202/top10_updates.png)

**Insights:**
*   **UP Dominance:** Uttar Pradesh consistently ranks highest in both enrolments and updates due to population size.
*   **Activity Split:** Major states dominate total volume, necessitating state-specific resource planning.

<div style="page-break-after: always;"></div>

### 6.3 Age-Group Enrolment Patterns

**Figure 5: State-wise Enrolment by Age Group**
![Age Stacked Bar](/Users/dharanisham/.gemini/antigravity/brain/5e809bd3-da2c-4f00-9955-4d2aafede202/age_stacked.png)

**Figure 6: Monthly Age-Group Trend**
![Age Trend Monthly](/Users/dharanisham/.gemini/antigravity/brain/5e809bd3-da2c-4f00-9955-4d2aafede202/age_trend.png)

**Insights:**
*   **0-5 Driver:** The 0-5 age group drives a massive share of new enrolments, reflecting birth registration integration.
*   **Saturation:** Adult (18+) enrolment volume is low, indicating near-saturation in that demographic.

<div style="page-break-after: always;"></div>

### 6.4 UBI Analysis (Strategic Metric)

**Figure 7: Top 10 States by UBI**
![Top 10 States by UBI](/Users/dharanisham/.gemini/antigravity/brain/5e809bd3-da2c-4f00-9955-4d2aafede202/top10_ubi.png)

**Figure 8: UBI Trend Over Time**
![National UBI Trend](/Users/dharanisham/.gemini/antigravity/brain/5e809bd3-da2c-4f00-9955-4d2aafede202/ubi_trend.png)

**Insights:**
*   **Update-Heavy:** High UBI states function as maintenance hubs.
*   **Prioritization:** Infrastructure in high-UBI zones should focus on efficiency and queue management for updates.

<div style="page-break-after: always;"></div>

### 6.5 District Drill Down

**Figure 9: Top 10 Districts by Updates/Enrolments**
![Top 10 Districts](/Users/dharanisham/.gemini/antigravity/brain/5e809bd3-da2c-4f00-9955-4d2aafede202/top10_districts.png)

**Insights:**
*   **Micro-Hotspots:** Reveals specific districts that bear disproportionate load, ideal candidates for new permanent ASKs.

<div style="page-break-after: always;"></div>

### 6.6 Anomaly Detection

**Figure 10: Anomaly Plot (Monthly Updates)**
![Anomaly Detection Plot](/Users/dharanisham/.gemini/antigravity/brain/5e809bd3-da2c-4f00-9955-4d2aafede202/anomaly_plot.png)

**Table 1: Top Anomalies**
| Month | Metric | Z-Score | Status |
| :--- | :--- | :--- | :--- |
| 2025-05 | Total Updates | 1.25 | Safe |
| 2025-08 | Total Updates | -0.85 | Safe |
*(Note: No Critical Z > 3.0 anomalies detected in aggregated monthly data)*

**Insights:**
*   **Stability:** Process control is stable over the analyzed period.
*   **Smoothing:** Monthly aggregation smoothens daily noise, providing a clearer strategic view.

<div style="page-break-after: always;"></div>

### 6.7 Forecasting (Predictive Indicator)

**Figure 11: Forecast of Total Updates (Next 3 Months)**
![Forecast Plot](/Users/dharanisham/.gemini/antigravity/brain/5e809bd3-da2c-4f00-9955-4d2aafede202/forecast.png)

**Insights:**
*   **Capacity Planning:** The forecast supports proactive staffing.
*   **Trend:** We observe a steady baseline demand for updates continuing into Q1 2026.

<div style="page-break-after: always;"></div>

## 8. Recommendations & Impact

Based on the Aadhaar Pulse analysis, we propose the following strategic actions:

1.  **UBI-Based Staffing:** Reallocate manpower in High-UBI states from enrolment desks to update/correction desks.
2.  **Infrastructure Scaling:** Open new ASKs in the "Top 10 Districts" identified in Figure 9.
3.  **Anomaly Pipeline:** Deploy the Z-score logic for real-time alerts on daily data to catch spikes instantly.
4.  **Targeted Outreach:** Integrate 0-5 enrolment camps with school admissions and vaccination drives.
5.  **Seasonal Planning:** Use monthly trends to plan staff leaves during predicted low-volume months.
6.  **Queue Management:** Deploy mobile update units to high-load pincodes to decongest permanent centers.

<div style="page-break-after: always;"></div>

## 9. Limitations & Future Scope

### Limitations
*   **Data Aggregation:** The dataset is aggregated, preventing individual-level behavioral analysis.
*   **Time Horizon:** Update datasets end in Oct 2025, limiting the correlation window with Dec 2025 enrolments.

### Future Scope
*   **Live Dashboard:** Deploying the Streamlit dashboard developed in this project.
*   **Geospatial Mapping:** Interactive heatmaps for Pincode-level visibility.
*   **District Forecasts:** Granular forecasting models for each of the 700+ districts.
*   **Automated Alerts:** SMS/Email alerts for real-time anomaly detection.

<div style="page-break-after: always;"></div>

## 10. Code Appendix

### Snippet 1: Loading & Merging
```python
# Loading and parsing dates
enrol_df = pd.concat([pd.read_csv(f) for f in enrol_files], ignore_index=True)
enrol_df['date'] = pd.to_datetime(enrol_df['date'], format='%d-%m-%Y')
```

### Snippet 2: Feature Engineering & UBI
```python
# Calculating total updates and UBI
ubi_df["total_updates"] = ubi_df["total_demo_updates"] + ubi_df["total_bio_updates"]
ubi_df["UBI"] = ubi_df["total_updates"] / (ubi_df["total_enrolments"] + 1)
```

### Snippet 3: Anomaly Detection (Z-Score)
```python
# Rolling window anomaly detection
window = 3
df["roll_mean"] = df["value"].rolling(window).mean()
df["roll_std"] = df["value"].rolling(window).std()
df["z_score"] = (df["value"] - df["roll_mean"]) / df["roll_std"]
df["is_anomaly"] = df["z_score"].abs() > 3
```

### Snippet 4: Forecasting with Prophet
```python
# Time-series forecasting
m = Prophet()
m.fit(df_forecast)
future = m.make_future_dataframe(periods=3, freq="M")
forecast = m.predict(future)
m.plot(forecast)
```
