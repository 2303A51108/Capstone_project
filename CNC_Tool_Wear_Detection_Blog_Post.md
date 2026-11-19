# Transforming Industry 4.0: Explainable AI for Sensorless CNC Tool Wear Detection

### Introduction
In precision computer numerical control (CNC) machining, cutting tools operate under intense mechanical stress and elevated thermal gradients. Over time, cutting edges inevitably degrade through flank wear and micro-chipping. If a worn tool goes unnoticed, it can suddenly fracture mid-cut—ruining high-value aerospace or automotive workpieces, damaging expensive machine spindle bearings, and causing substantial non-productive factory downtime.

Traditional approaches to tool condition monitoring fall into two extremes: either operators rely on conservative, scheduled tool replacements (wasting up to 50% of a tool's remaining useful life), or factories install delicate external sensors like piezoelectric dynamometers and acoustic emission probes that cost tens of thousands of dollars and frequently fail in harsh cutting-fluid environments.

For our final-year B.Tech Capstone Project at the School of Computer Science & Artificial Intelligence, SR University, we set out to answer a pivotal manufacturing question: *Can we accurately detect cutting tool wear using only the internal sensor signals already present in modern CNC machine controllers, without adding a single dollar of external hardware?*

### The Approach: Sensorless Telemetry & 425-Dimensional Feature Engineering
Our project utilizes the University of Michigan SMART Lab machining benchmark, comprising 18 full-length CNC milling experiments across 48 continuous channels sampled at 10 Hz. These channels capture drive currents, commanded and actual multi-axis (X, Y, Z) positions, velocities, and numerical controller execution block numbers.

Because raw machining telemetry consists of thousands of non-stationary temporal data points, we developed a multi-domain statistical feature extraction engine. For every numeric channel, we compute 9 time-domain statistical moments: Mean, Sample Standard Deviation (enforcing Bessel's correction with ddof=1), Median, Minimum, Maximum, Peak-to-Peak Range, RMS, Absolute Mean, and Signal Energy. Combined with operating feed rate and clamping pressure, this yields a rich, aligned 425-dimensional feature matrix.

### Why Leave-One-Out Cross-Validation (LOOCV)?
With 18 complete experimental cuts, standard 80/20 train/test splits introduce massive variance and data leakage. To ensure genuine out-of-sample validity, we implemented Leave-One-Out Cross-Validation (LOOCV). We benchmarked 7 distinct machine learning architectures: Decision Trees, Gradient Boosting, Soft-Voting Ensembles, Two-Tier Stacking Meta-Learners, Random Forests, L2-Regularized Logistic Regression, and RBF Support Vector Machines.

Our structurally-pruned Decision Tree emerged as the champion:
• Accuracy: 77.78%
• F1-Score: 81.82%
• Recall (Sensitivity): 90.00% (catching 9 out of 10 worn tools)

In manufacturing quality control, Recall is paramount. A False Positive results in a brief 2-minute visual check, while a False Negative leads to catastrophic spindle crashes.

### Explainable AI (XAI) & The Physical Reality
Unlike opaque deep learning models, our Decision Tree uncovered two explicit physical rules:
1. Minimum Z-Axis Position (Z1_ActualPosition_min <= 27.60 mm): Sharp tools penetrate cleanly to nominal depth. Worn tools experience severe cutting thrust forces that physically deflect the spindle upward!
2. CNC Controller Block Dwell (M1_sequence_number_abs_mean <= 6.12): Dull cutters trigger controller hesitation and toolpath cycle delays under heavy cutting load.

### Deployment & Live Dashboard
To bridge machine learning with shop-floor operations, we built a production-grade web dashboard using Python and Streamlit (app.py). Operators can explore live multi-axis waveforms, trigger one-click wear diagnostics, view wear probability gauges, and inspect the active Explainable AI rules.

### Conclusion & Team Acknowledgements
This project demonstrates that explainable, regularized machine learning paired with internal CNC controller telemetry delivers a reliable, sensorless paradigm for Industry 4.0 smart manufacturing.

*Project by: Kondapalli Devi Priyanka (2303A51108), Asmaja (2303A51011), and Sarayu (2303A510A6).*
*Under the guidance of Mr. Sallauddin Md, Assistant Professor, School of CS&AI, SR University.*
