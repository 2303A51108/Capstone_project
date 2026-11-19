import sys
from pathlib import Path
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def create_report():
    doc = Document()

    # Set 1-inch margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Palette
    COLOR_PRIMARY = RGBColor(15, 23, 42)    # Deep Navy
    COLOR_SECONDARY = RGBColor(37, 99, 235) # Accent Blue
    COLOR_TEXT = RGBColor(51, 65, 85)       # Slate Gray
    COLOR_MUTED = RGBColor(100, 116, 139)   # Muted Gray

    # Style Helpers
    def set_font(p, text, size=11, bold=False, italic=False, color=COLOR_TEXT, align=WD_ALIGN_PARAGRAPH.LEFT, space_after=6):
        p.alignment = align
        p.paragraph_format.space_after = Pt(space_after)
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.italic = italic
        run.font.color.rgb = color
        return run

    def add_h1(title):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.keep_with_next = True
        set_font(p, title, size=18, bold=True, color=COLOR_PRIMARY)

    def add_h2(title):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        set_font(p, title, size=14, bold=True, color=COLOR_SECONDARY)

    def add_h3(title):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        set_font(p, title, size=12, bold=True, color=COLOR_PRIMARY)

    def add_p(text, bold_prefix=None, space_after=6):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.name = "Calibri"
            r_pre.font.size = Pt(11)
            r_pre.font.bold = True
            r_pre.font.color.rgb = COLOR_PRIMARY
        r_txt = p.add_run(text)
        r_txt.font.name = "Calibri"
        r_txt.font.size = Pt(11)
        r_txt.font.color.rgb = COLOR_TEXT
        return p

    def add_bullet(text, bold_prefix=None):
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.name = "Calibri"
            r_pre.font.size = Pt(11)
            r_pre.font.bold = True
            r_pre.font.color.rgb = COLOR_PRIMARY
        r_txt = p.add_run(text)
        r_txt.font.name = "Calibri"
        r_txt.font.size = Pt(11)
        r_txt.font.color.rgb = COLOR_TEXT

    def format_table(table, header_bg="0F172A", alt_bg="F8FAFC"):
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        for idx, row in enumerate(table.rows):
            for cell in row.cells:
                cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                tcPr = cell._tc.get_or_add_tcPr()
                # Borders
                tcBorders = parse_xml(r'''
                    <w:tcBorders {} >
                        <w:top w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
                        <w:left w:val="none"/>
                        <w:bottom w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
                        <w:right w:val="none"/>
                    </w:tcBorders>
                '''.format(nsdecls('w')))
                tcPr.append(tcBorders)

                if idx == 0:
                    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{header_bg}"/>')
                    tcPr.append(shading)
                    for paragraph in cell.paragraphs:
                        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                        for run in paragraph.runs:
                            run.font.bold = True
                            run.font.color.rgb = RGBColor(255, 255, 255)
                elif idx % 2 == 1:
                    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{alt_bg}"/>')
                    tcPr.append(shading)

    # ==============================================================
    # COVER PAGE
    # ==============================================================
    p_pre = doc.add_paragraph()
    set_font(p_pre, "FINAL YEAR B.TECH CAPSTONE PROJECT REPORT", size=12, bold=True, color=COLOR_SECONDARY, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=24)

    p_title = doc.add_paragraph()
    set_font(p_title, "CNC TOOL WEAR DETECTION IN CNC MILLING OPERATIONS", size=24, bold=True, color=COLOR_PRIMARY, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)

    p_sub = doc.add_paragraph()
    set_font(p_sub, "In-Process Multi-Sensor Condition Monitoring Using Time-Domain Statistical Feature Engineering and Explainable Machine Learning", size=13, italic=True, color=COLOR_MUTED, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=36)

    p_div = doc.add_paragraph()
    set_font(p_div, "______________________________________________________", size=11, color=COLOR_MUTED, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=36)

    p_submitted = doc.add_paragraph()
    set_font(p_submitted, "Submitted in partial fulfillment of the requirements for the degree of\nBACHELOR OF TECHNOLOGY", size=12, bold=True, color=COLOR_PRIMARY, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=36)

    # Info Table
    t_info = doc.add_table(rows=3, cols=2)
    t_info.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell_w = Inches(3.2)
    for row in t_info.rows:
        row.cells[0].width = cell_w
        row.cells[1].width = cell_w

    t_info.rows[0].cells[0].paragraphs[0].text = "Candidate Name:"
    t_info.rows[0].cells[0].paragraphs[0].runs[0].font.bold = True
    t_info.rows[0].cells[1].paragraphs[0].text = "Final Year B.Tech Student"

    t_info.rows[1].cells[0].paragraphs[0].text = "Department / Discipline:"
    t_info.rows[1].cells[0].paragraphs[0].runs[0].font.bold = True
    t_info.rows[1].cells[1].paragraphs[0].text = "Mechanical / Mechatronics / Computer Science"

    t_info.rows[2].cells[0].paragraphs[0].text = "Project Domain:"
    t_info.rows[2].cells[0].paragraphs[0].runs[0].font.bold = True
    t_info.rows[2].cells[1].paragraphs[0].text = "Industry 4.0 | Smart Manufacturing | Machine Learning"

    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(48)
    set_font(p_sp, "Academic Year 2025 - 2026", size=12, bold=True, color=COLOR_PRIMARY, align=WD_ALIGN_PARAGRAPH.CENTER)

    doc.add_page_break()

    # ==============================================================
    # CERTIFICATE & DECLARATION
    # ==============================================================
    add_h1("BONAFIDE CERTIFICATE")
    add_p("This is to certify that the project report titled \"CNC TOOL WEAR DETECTION IN CNC MILLING OPERATIONS\" is the bonafide work carried out by the candidate under our supervision and guidance in partial fulfillment of the requirements for the award of the degree of Bachelor of Technology.")
    
    p_sig = doc.add_paragraph()
    p_sig.paragraph_format.space_before = Pt(48)
    p_sig.paragraph_format.space_after = Pt(24)
    r_sig = p_sig.add_run("______________________________                                  ______________________________\nProject Supervisor / Guide                                                    Head of the Department")
    r_sig.font.name = "Calibri"
    r_sig.font.size = Pt(11)
    r_sig.font.bold = True
    r_sig.font.color.rgb = COLOR_PRIMARY

    add_h1("CANDIDATE DECLARATION")
    add_p("I hereby declare that the project work presented in this report entitled \"CNC Tool Wear Detection in CNC Milling Operations\" submitted to the Department is an authentic record of our own research and software development carried out under the supervision of our guide. The work reported herein does not duplicate any previously submitted dissertation or degree.")

    doc.add_page_break()

    # ==============================================================
    # EXECUTIVE SUMMARY / ABSTRACT
    # ==============================================================
    add_h1("ABSTRACT")
    add_p("In automated high-precision manufacturing, milling cutter degradation represents one of the primary catalysts for dimensional deviations, surface roughness deterioration, and catastrophic spindle failures. Conventional tool condition monitoring (TCM) approaches rely heavily on offline manual inspection, which introduces costly machine downtime, or conservative timer-based replacement schedules, which discard up to 30% of useful tool life prematurely.")
    add_p("This capstone project presents an end-to-end, sensor-based, in-process tool condition monitoring system leveraging the University of Michigan SMART Lab CNC Milling Dataset. The system captures high-frequency 48-channel multi-axis telemetry (100 ms sampling rate) from linear drives (X, Y, Z), main spindle motor (S), and CNC controller registers across 18 full-part machining experiments producing complex 'S' shape wax workpieces.")
    add_p("A rigorous multi-domain feature engineering pipeline was developed to aggregate massive continuous time-series streams into a deterministic 425-dimensional feature matrix. This formulation extracts 9 statistical operators (Mean, Sample Standard Deviation with N-1 degrees of freedom, Median, Min, Max, Range, RMS Energy, Absolute Mean, and Total Energy) across 47 numeric channels, fused with machine operating parameters (Feed Rate and Clamping Pressure).")
    add_p("To benchmark classification performance, seven distinct machine learning architectures were trained and evaluated under Leave-One-Experiment-Out Cross-Validation (LOOCV), including Decision Trees, Gradient Boosting, Random Forests, Support Vector Machines, Logistic Regression, a Soft-Voting Ensemble, and a custom Two-Tier Hybrid Stacking Architecture. The structurally pruned Decision Tree classifier (max_depth=2, min_samples_leaf=2) emerged as the superior production model, achieving 77.78% LOOCV Accuracy, 81.82% F1-Score, and a vital 90.00% Recall (catching 9 out of 10 worn tools), while demonstrating 100% resubstitution accuracy on full training runs.")
    add_p("Crucially, the trained Decision Tree provides complete Explainable AI (XAI) transparency by discovering two physical thresholds: vertical Z-axis thrust deflection (Z1_ActualPosition_min <= 27.60 mm) and G-code execution delay (M1_sequence_number_abs_mean <= 6.12). The entire pipeline is deployed in a responsive Streamlit web dashboard featuring 5-tab multi-signal visualizers, parameter safety validation, automated experiment identification, and historical benchmark profile comparisons.")
    add_p("Keywords: CNC Milling, Tool Wear Detection, Industry 4.0, Predictive Maintenance, Machine Learning, Feature Engineering, Explainable AI, Streamlit.", bold_prefix="Index Terms / ")

    doc.add_page_break()

    # ==============================================================
    # CHAPTER 1: INTRODUCTION
    # ==============================================================
    add_h1("CHAPTER 1: INTRODUCTION & INDUSTRIAL MOTIVATION")
    
    add_h2("1.1 Background of CNC Machining")
    add_p("Computer Numerical Control (CNC) milling represents the backbone of modern discrete component manufacturing, enabling rapid, high-precision subtractive shaping of complex structural geometries. In high-speed milling operations, cutting inserts and end-mills are subjected to severe thermomechanical stresses, abrasive contact friction, and cyclic dynamic shock loading. Over extended machining cycles, cutting edges suffer flank wear, rake cratering, micro-chipping, and thermal cracking.")

    add_h2("1.2 The Problem of Cutting Tool Wear")
    add_p("The progressive degradation of cutting tools produces cascading industrial failures:")
    add_bullet("Degraded Part Surface Quality: Worn tools burnish rather than shear material, causing high surface roughness, burr formation, and out-of-spec dimensions.", "1. Dimensional Inaccuracy: ")
    add_bullet("Workpiece Scrapping: Critical aerospace and automotive components are frequently scrapped late in the machining process when a worn tool exceeds tolerances.", "2. Expensive Scrap: ")
    add_bullet("Catastrophic Tool Breakage: Continued operation of dull cutters leads to mechanical binding, excessive cutting torque, and tool snapping, risking spindle bearing destruction costing upwards of $10,000 to $50,000.", "3. Machine Damage: ")

    add_h2("1.3 Limitations of Conventional Approaches")
    add_p("Historically, machine shops have managed tool condition through two primitive methods:")
    add_bullet("Requires halting the machine tool, clearing chips, and using an optical magnifier or touch probe. This destroys Overall Equipment Effectiveness (OEE).", "Offline Manual Inspection: ")
    add_bullet("Operators change inserts after a predetermined number of parts or cutting hours. Because tool wear is highly stochastic and varies with workpiece hardness and feed rate, conservative timers discard expensive carbide inserts with 20% to 35% of remaining useful life (RUL).", "Scheduled Replacement: ")

    add_h2("1.4 Objectives of This Project")
    add_bullet("Ingest and analyze comprehensive multi-sensor time-series telemetry from a modern CNC milling center.", "Objective 1: ")
    add_bullet("Engineer a deterministic 425-dimensional feature pipeline converting raw 100 ms time-series into statistical representations.", "Objective 2: ")
    add_bullet("Design, evaluate, and benchmark multiple machine learning classifiers, including a custom Two-Tier Hybrid Stacking Architecture.", "Objective 3: ")
    add_bullet("Validate model generalization using rigorous Leave-One-Experiment-Out Cross-Validation (LOOCV), prioritizing Recall over mere accuracy.", "Objective 4: ")
    add_bullet("Extract explainable, physics-informed decision rules for manufacturing engineering transparency.", "Objective 5: ")
    add_bullet("Deliver a production-ready interactive web application with multi-axis sensor exploration and live wear diagnosis.", "Objective 6: ")

    # ==============================================================
    # CHAPTER 2: LITERATURE REVIEW
    # ==============================================================
    add_h1("CHAPTER 2: LITERATURE REVIEW & SENSING TECHNIQUES")
    add_h2("2.1 Direct vs Indirect Sensing Methods")
    add_p("Tool condition monitoring (TCM) methodologies are classified into direct and indirect sensing techniques:")
    add_bullet("Direct measurement of tool flank wear using optical cameras, vision systems, or radioactive tracers. While accurate, direct methods are impractical in industrial production due to opaque coolant sprays, flying chips, and optical occlusion.", "Direct Methods: ")
    add_bullet("Measurement of secondary operational signals correlated with cutting forces, including spindle motor current, drive power, vibration, acoustic emission (AE), and tool displacement. Indirect methods are non-intrusive and ideally suited for in-process automation.", "Indirect Methods: ")

    add_h2("2.2 Sensorless Monitoring via Servo Telemetry")
    add_p("A key breakthrough in Industry 4.0 smart manufacturing is 'sensorless' monitoring. Rather than mounting expensive, delicate external dynamometers (cutting force sensors) to the workpiece table, modern CNC digital servo drives continuously record internal feedback currents, DC bus voltages, and commanded velocities. Because motor current is directly proportional to cutting torque (T = Kt * I), internal drive currents serve as built-in dynamometers at zero additional sensor hardware cost.")

    # ==============================================================
    # CHAPTER 3: DATASET & TELEMETRY
    # ==============================================================
    add_h1("CHAPTER 3: EXPERIMENTAL TESTBED & DATASET")
    add_h2("3.1 University of Michigan SMART Lab Testbed")
    add_p("The dataset used in this study was collected at the System-level Manufacturing and Automation Research Testbed (SMART) at the University of Michigan. Machining trials were conducted on a 3-axis CNC vertical milling center. Workpieces consisted of 2\" x 2\" x 1.5\" machinable wax blocks, chosen for experimental repeatability. Each experiment carved an 'S' shape contour into the top face of the block across multiple vertical Z-axis depths (Layer 1, Layer 2, Layer 3).")

    add_h2("3.2 Experimental Cohort & Operating Parameters")
    add_p("A total of 18 distinct machining experiments were run under varied operating regimes:")
    add_bullet("Experiments 1, 2, 3, 4, 5, 11, 12, and 17 (8 Experiments).", "UNWORN Tools (Class 0): ")
    add_bullet("Experiments 6, 7, 8, 9, 10, 13, 14, 15, 16, and 18 (10 Experiments).", "WORN Tools (Class 1): ")
    add_bullet("Varied across 3, 6, 12, 15, and 20 mm/s.", "Feed Rates: ")
    add_bullet("Varied across 2.5, 3.0, and 4.0 bar.", "Pneumatic Vise Clamping Pressures: ")

    add_h2("3.3 48-Channel Telemetry Architecture")
    add_p("Every 100 milliseconds, the CNC data logger sampled 48 channels across four physical motors and the controller:")
    
    # Sensor Table
    table = doc.add_table(rows=7, cols=3)
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = "Signal Category"
    hdr_cells[1].text = "Channels"
    hdr_cells[2].text = "Physical Description & Engineering Significance"

    sensor_rows = [
        ("Current Signals (8)", "X1/Y1/Z1/S1 OutputCurrent & CurrentFeedback", "Drive current (A). Spindle current reflects cutting torque friction; linear currents reflect axis feed resistance."),
        ("Power Signals (3)", "S1, X1, Y1 OutputPower", "Electrical motor power (kW). Note: Z1 axis drive does not possess a power sensor in this setup."),
        ("Feed Rate & Velocities (7)", "M1_CURRENT_FEEDRATE, Actual & Command Velocities", "Instantaneous spindle feed rate and linear velocities (mm/s). Tracks tool hesitation and feed rate override."),
        ("Acceleration Signals (8)", "X1/Y1/Z1/S1 Actual & Command Acceleration", "Tool and drive acceleration (mm/s², deg/s²). Serves as high-frequency vibration and chatter indicator."),
        ("Position Signals (8)", "X1/Y1/Z1/S1 Actual & Command Position", "Actual vs reference trajectory (mm). Tracks vertical Z-axis deflection under cutting thrust loads."),
        ("Voltage & Controller (14)", "DCBusVoltage, OutputVoltage, Program No, Sequence No", "Drive voltages (V), G-code execution line counter, and spindle torque inertia (kg*m²).")
    ]
    for idx, (cat, ch, desc) in enumerate(sensor_rows, start=1):
        row_cells = table.rows[idx].cells
        row_cells[0].text = cat
        row_cells[1].text = ch
        row_cells[2].text = desc

    format_table(table)

    # ==============================================================
    # CHAPTER 4: FEATURE ENGINEERING
    # ==============================================================
    add_h1("CHAPTER 4: TIME-DOMAIN FEATURE ENGINEERING")
    add_h2("4.1 Mathematical Formulation of Statistical Features")
    add_p("Each raw experiment CSV contains between 1,000 and 10,500 continuous rows. Direct row-by-row classification is impossible due to variable run lengths and air-cutting repositioning. Therefore, a comprehensive feature extraction engine aggregates every numeric sensor stream into 9 statistical operators:")
    add_bullet("Calculates the central operational level of current, power, and velocity.", "1. Arithmetic Mean: ")
    add_bullet("Computed using Bessel's sample correction with N-1 degrees of freedom (ddof=1) to ensure unbiased variance estimation and strict parity with training records.", "2. Sample Standard Deviation: ")
    add_bullet("Outlier-resistant measure of baseline operating dynamics.", "3. Median: ")
    add_bullet("Captures peak instantaneous compressive or negative shock dynamics.", "4. Minimum Value: ")
    add_bullet("Captures peak positive power surge or dynamic acceleration spike.", "5. Maximum Value: ")
    add_bullet("Max - Min amplitude span, measuring overall fluctuation band.", "6. Peak-to-Peak Range: ")
    add_bullet("Root Mean Square represents the true effective energy and vibration power content of the waveform.", "7. RMS Energy: ")
    add_bullet("Mean of absolute amplitudes, indicating rectified energy magnitude.", "8. Absolute Mean: ")
    add_bullet("Sum of squared samples, reflecting cumulative energy expenditure over the machining trial.", "9. Total Energy: ")

    add_h2("4.2 Dimension Composition & Parameter Safety")
    add_p("Multiplying 47 numeric channels by 9 statistical operators yields 423 features. Fusing the 2 machine operating settings (Feed Rate and Clamping Pressure) creates exactly 425 features in strict training sequence.")
    add_p("Crucially, our pipeline enforces strict parameter safety: if an external CSV is processed, the system requires explicit user entry and prohibits silent zero-substitution.")

    # ==============================================================
    # CHAPTER 5: AI ARCHITECTURES & HYBRID MODEL
    # ==============================================================
    add_h1("CHAPTER 5: MACHINE LEARNING MODEL ARCHITECTURES")
    add_h2("5.1 Individual Supervised Classifiers")
    add_p("We evaluated five diverse individual classifiers:")
    add_bullet("CART induction with hyperparameter pruning (max_depth=2, min_samples_leaf=2, balanced class weights).", "Decision Tree Classifier: ")
    add_bullet("Sequential boosting ensemble of 50 shallow decision stumps (learning_rate=0.05).", "Gradient Boosting Classifier: ")
    add_bullet("Bagging ensemble of 200 randomized decision trees (max_depth=3).", "Random Forest Classifier: ")
    add_bullet("RBF kernel margin classifier with SelectKBest (k=20) feature selection.", "Support Vector Machine (SVM): ")
    add_bullet("L2-regularized linear probabilistic model with median imputation and standard scaling.", "Logistic Regression: ")

    add_h2("5.2 Custom Two-Tier Hybrid Stacking Architecture")
    add_p("Beyond standard models, we engineered a custom Two-Tier Stacking Meta-Classifier:")
    add_bullet("Level-0 consists of four heterogeneous base learners: Decision Tree, Gradient Boosting, SVM, and Random Forest. Each generates out-of-fold class probability vectors.", "Tier 1 (Base Experts): ")
    add_bullet("A balanced Logistic Regression meta-learner trains on Tier 1 probability predictions, learning the optimal blend weights for the final wear diagnosis.", "Tier 2 (Meta-Learner): ")

    # ==============================================================
    # CHAPTER 6: SOFTWARE & WEB DASHBOARD
    # ==============================================================
    add_h1("CHAPTER 6: SOFTWARE IMPLEMENTATION & WEB DASHBOARD")
    add_p("The production monitoring platform was developed using Streamlit (Python). Key features include:")
    add_bullet("Extracts experiment IDs from file headers and queries train.csv for verified operating settings.", "1. Automated Experiment Identification: ")
    add_bullet("Organized into 5 interactive tabs: Current (8 channels), Power (3 channels), Feed & Velocity, Acceleration (8 channels), and Position/Voltage.", "2. Multi-Axis Sensor Dashboard: ")
    add_bullet("Extracts the 425-feature vector and re-indexes columns in strict alignment with model metadata.", "3. Feature Alignment Pipeline: ")
    add_bullet("Renders clear Green UNWORN (0) or Red WORN (1) alerts with leaf probability bars and replacement guidance.", "4. Diagnostic Engine: ")
    add_bullet("Compares the uploaded run against historical UNWORN vs WORN benchmark averages across decisive features.", "5. Physical Benchmark Profile: ")

    # ==============================================================
    # CHAPTER 7: RESULTS & DISCUSSION
    # ==============================================================
    add_h1("CHAPTER 7: RESULTS, EVALUATION & DISCUSSION")
    add_h2("7.1 Cross-Validation Benchmarking (LOOCV)")
    add_p("Due to the 18-experiment cohort, Leave-One-Experiment-Out Cross-Validation (LOOCV) was enforced to measure true out-of-sample generalization. Table 7.1 details the verified benchmark results:")

    # Results Table
    res_table = doc.add_table(rows=8, cols=5)
    r_hdr = res_table.rows[0].cells
    r_hdr[0].text = "AI Model Architecture"
    r_hdr[1].text = "LOOCV Accuracy"
    r_hdr[2].text = "Precision"
    r_hdr[3].text = "Recall"
    r_hdr[4].text = "F1-Score"

    results_data = [
        ("Decision Tree Classifier (Selected)", "77.78%", "75.00%", "90.00%", "81.82%"),
        ("Gradient Boosting Classifier", "66.67%", "64.29%", "90.00%", "75.00%"),
        ("Soft-Voting Ensemble", "66.67%", "64.29%", "90.00%", "75.00%"),
        ("Two-Tier Stacking Hybrid", "72.22%", "77.78%", "70.00%", "73.68%"),
        ("Random Forest Classifier", "44.44%", "50.00%", "60.00%", "54.55%"),
        ("Logistic Regression", "38.89%", "45.45%", "50.00%", "47.62%"),
        ("Support Vector Machine (SVM)", "0.00%", "0.00%", "0.00%", "0.00%")
    ]
    for idx, row in enumerate(results_data, start=1):
        rc = res_table.rows[idx].cells
        rc[0].text = row[0]
        rc[1].text = row[1]
        rc[2].text = row[2]
        rc[3].text = row[3]
        rc[4].text = row[4]

    format_table(res_table)

    add_h2("7.2 Academic Rigor: Resubstitution vs LOOCV")
    add_p("When evaluated against the 18 training experiments upon full-fit, the Decision Tree achieves 100% resubstitution accuracy. However, in our report and defense, we strictly emphasize the 77.78% LOOCV accuracy and 90.00% recall as the authentic measure of generalized performance on unseen workpieces.")

    add_h2("7.3 Explainable AI (XAI) Physical Decision Rules")
    add_p("The trained Decision Tree discovered two deterministic physical boundaries:")
    add_bullet("Z1_ActualPosition_min <= 27.60 mm -> Tool is sharp, penetrates cleanly without excessive thrust deflection -> Classified as UNWORN (Class 0).", "Primary Decision Rule: ")
    add_bullet("If Z1_min > 27.60 mm, the tree checks G-code progression dynamics. If M1_sequence_number_abs_mean <= 6.12 -> UNWORN (Class 0); else -> Tool exhibits cycle hesitation and dynamic delay -> Classified as WORN (Class 1).", "Secondary Decision Rule: ")

    # ==============================================================
    # CHAPTER 8: CONCLUSION
    # ==============================================================
    add_h1("CHAPTER 8: CONCLUSION & FUTURE SCOPE")
    add_h2("8.1 Summary of Contributions")
    add_p("This project successfully demonstrated that multi-sensor CNC telemetry can accurately diagnose cutting tool wear in-process. Key contributions include the 425-dimensional statistical feature pipeline, the Two-Tier Hybrid Stacking model, the 90% recall Decision Tree with physical explainability, and the production-ready Streamlit web platform.")

    add_h2("8.2 Future Scope")
    add_bullet("Extend trials to hardened tool steels and titanium alloys.", "Multi-Material Adaptation: ")
    add_bullet("Fuse high-frequency acoustic emission (100 kHz - 1 MHz) for micro-crack detection.", "Acoustic Emission Integration: ")
    add_bullet("Investigate Temporal Convolutional Networks (TCN) and LSTMs for sub-layer segment classification.", "Deep Sequence Modeling: ")
    add_bullet("Deploy on edge IPCs communicating via OPC-UA/MTConnect for automated tool changer (ATC) triggering.", "Edge Gateway Deployment: ")

    # References
    add_h1("REFERENCES")
    refs = [
        "[1] University of Michigan SMART Lab, 'CNC Milling Dataset,' System-level Manufacturing and Automation Research Testbed, 2018.",
        "[2] Byrne, G., Dornfeld, D., et al., 'Advancing Cutting Technology of Machine Tools,' CIRP Annals, Vol. 44, No. 2, pp. 241-267.",
        "[3] Teti, R., Jemielniak, K., et al., 'Advanced Monitoring of Machining Operations,' CIRP Annals, Vol. 59, No. 2, pp. 717-739.",
        "[4] Breiman, L., 'Random Forests,' Machine Learning, Vol. 45, No. 1, pp. 5-32.",
        "[5] Wolpert, D. H., 'Stacked Generalization,' Neural Networks, Vol. 5, No. 2, pp. 241-259.",
        "[6] Pedregosa, F., et al., 'Scikit-learn: Machine Learning in Python,' JMLR, Vol. 12, pp. 2825-2830."
    ]
    for r in refs:
        add_p(r, space_after=4)

    # Save Word document
    output_path = Path("CNC_Tool_Wear_Detection_Final_Report.docx")
    doc.save(str(output_path))
    print(f"Successfully generated Final Report: {output_path.resolve()}, size: {output_path.stat().st_size} bytes")

if __name__ == "__main__":
    create_report()
