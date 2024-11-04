# Tech Fee Committee Attendance/Weekly Report Generator Documentation

## Table of Contents

1. [Introduction](#introduction)
2. [Project Overview](#project-overview)
3. [Features](#features)
4. [Technical Specifications](#technical-specifications)
5. [Architecture and Design](#architecture-and-design)
6. [Detailed Code Explanation](#detailed-code-explanation)
   - [Imports and Dependencies](#imports-and-dependencies)
   - [AttendanceApp Class](#attendanceapp-class)
     - [Initialization](#initialization)
     - [User Interface Setup](#user-interface-setup)
     - [Attendance Tab](#attendance-tab)
     - [Weekly Report Tab](#weekly-report-tab)
     - [Announcements/Agenda Tab](#announcementsagenda-tab)
     - [Technical Document Tab](#technical-document-tab)
     - [Member Management](#member-management)
     - [Export Functionality](#export-functionality)
     - [Watermark Integration](#watermark-integration)
     - [Error Handling and Notifications](#error-handling-and-notifications)
7. [Installation and Setup](#installation-and-setup)
8. [Usage Guide](#usage-guide)
9. [Testing and Validation](#testing-and-validation)
10. [Future Enhancements](#future-enhancements)
11. [Conclusion](#conclusion)
12. [Appendix](#appendix)
    - [Dependencies](#dependencies)
    - [License](#license)
    - [Repository Links](#repository-links)

---

## Introduction

The **Tech Fee Committee Attendance/Weekly Report Generator** is a Python-based desktop application developed to automate and streamline the process of logging committee attendance and generating weekly reports. Designed to transition six committees (each comprising 10-15 members) from manual, paper-based tracking to a fully digital, paperless system, this tool significantly enhances accuracy, efficiency, and accessibility of attendance data.

---

## Project Overview

The **Tech Fee Committee Attendance/Weekly Report Generator** is crafted using Python's PyQt6 framework for the graphical user interface and ReportLab for PDF generation. The application automates the attendance logging process, verifies quorum in real-time, and facilitates the generation of comprehensive reports in both CSV and PDF formats. By reducing the time required for manual reporting by **80%**, the tool ensures that attendance data is meticulously recorded and easily retrievable.

Key functionalities include:

- **Attendance Tracking:** Log and manage member attendance seamlessly.
- **Quorum Verification:** Automatically verify if quorum requirements are met during meetings.
- **Report Generation:** Export attendance records and weekly summaries in CSV and PDF formats.
- **User-Friendly Interface:** Intuitive GUI for effortless data entry and management.
- **Customization:** Dynamic member management and customizable report outputs.

---

## Features

1. **Attendance Tracking**:
   - Log and edit member attendance during meetings.
   - Store attendance records for future reference.
   - Support for **in-person** and **virtual** attendance modes.

2. **Quorum Verification**:
   - Automatic verification of quorum to ensure official decision-making capabilities.

3. **Automated Export to CSV and PDF**:
   - Export attendance data and weekly reports in **CSV** or **PDF** formats.
   - Simplify record-keeping and formal documentation processes.

4. **User-Friendly GUI**:
   - Clean and intuitive interface for data entry, report generation, and member management.
   - No programming knowledge required for operation.

5. **Customization**:
   - Pre-load members, dynamically add or remove members, and adjust attendance data as needed.

6. **Enhanced Reporting Features**:
   - Additional tabs for **Announcements/Agenda** and **Technical Documents** with export capabilities.

7. **Watermark Integration**:
   - All exported PDFs include a full-page watermark featuring the SCSU logo for branding consistency and security.

8. **Status Bar Integration**:
   - Real-time feedback and notifications to guide users through various actions.

---

## Technical Specifications

- **Programming Language:** Python 3.8+
- **Framework:** PyQt6
- **Libraries:**
  - `pandas`: Data handling and CSV export.
  - `reportlab`: PDF generation.
  - `tkinter`: Optional dependency for file dialogs.
  - `PIL (Pillow)`: Image manipulation for electronic signatures.
- **Operating Systems:** Windows, macOS, Linux

---

## Architecture and Design

The application follows a modular architecture, ensuring maintainability and scalability. The primary components include:

1. **Graphical User Interface (GUI):**
   - Built using PyQt6, providing a responsive and intuitive interface.
   - Organized into multiple tabs for distinct functionalities: Attendance, Weekly Report, Announcements/Agenda, and Technical Document.

2. **Backend Logic:**
   - Manages data handling, report generation, and member management.
   - Utilizes pandas for efficient data processing and storage.

3. **Export Functionality:**
   - Leverages ReportLab for creating well-formatted PDF documents with watermark integration.
   - Supports CSV exports for versatile data utilization.

4. **Customization and Persistence:**
   - Stores member information in a JSON file (`members.json`) for data persistence across sessions.
   - Allows dynamic addition and deletion of members to accommodate changing committee structures.

5. **Security and Branding:**
   - Incorporates watermarks in exported PDFs to align with organizational branding and enhance document security.

---

## Detailed Code Explanation

The **Tech Fee Committee Attendance/Weekly Report Generator** is meticulously designed to ensure robust functionality, user-friendly interactions, and secure data management. This section delves into the intricacies of the application's codebase, elucidating the purpose and functionality of each component.

### Imports and Dependencies

```python
import sys
import os
import csv
import json
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QFileDialog, QComboBox, QScrollArea, QTextEdit,
    QDateEdit, QGridLayout, QSizePolicy, QTabWidget, QTimeEdit, QFrame, QStatusBar
)
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt, QDate, QTime, QTimer
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer, Image as RLImage
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader

# Import PIL for image manipulation
from PIL import Image, ImageDraw, ImageFont  # Needed for signature image generation
```

- **Standard Libraries:**
  - `sys`, `os`, `csv`, `json`, `datetime`: Handle system operations, file management, data serialization, and time-related functions.
  
- **PyQt6 Modules:**
  - `QtWidgets`, `QtGui`, `QtCore`: Facilitate the creation of the graphical user interface and manage events and timers.
  
- **ReportLab Modules:**
  - `platypus`, `lib.pagesizes`, `lib.styles`, `lib.units`, `lib.colors`, `lib.utils`: Enable the generation of PDF documents with tables, styling, and images.
  
- **PIL (Pillow):**
  - `Image`, `ImageDraw`, `ImageFont`: Handle image creation and manipulation for generating electronic signatures.

### AttendanceApp Class

The `AttendanceApp` class serves as the core of the application, managing the user interface, data handling, and export functionalities.

#### Initialization

```python
class AttendanceApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tech Fee Committee Attendance/Weekly Report Generator")
        self.setMinimumSize(1200, 800)
        self.attendance_options = ["Attending", "Absent"]
        self.attending_as_options = ["In-Person", "Virtual"]
        self.entries = []

        # Load preloaded names and positions
        self.load_preloaded_members()

        self.init_ui()
```

- **Window Configuration:**
  - Sets the application window title and minimum size for optimal display.
  
- **Options Initialization:**
  - Defines attendance status options and attendance modes for in-person or virtual meetings.
  
- **Data Loading:**
  - Loads pre-existing member information from `members.json` to populate the attendance records.

#### User Interface Setup

```python
def init_ui(self):
    main_layout = QVBoxLayout()
    self.setLayout(main_layout)

    # Header with Clock
    header_layout = QHBoxLayout()
    main_layout.addLayout(header_layout)

    title_label = QLabel("Tech Fee Committee Attendance/Weekly Report Generator")
    title_font = QFont("Arial", 20, QFont.Weight.Bold)
    title_label.setFont(title_font)
    title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    header_layout.addWidget(title_label)

    # Spacer between title and clock
    header_layout.addStretch()

    # Clock Label
    self.clock_label = QLabel()
    clock_font = QFont("Arial", 14, QFont.Weight.Bold)
    self.clock_label.setFont(clock_font)
    self.clock_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
    header_layout.addWidget(self.clock_label)

    # Initialize Timer for Clock
    self.timer = QTimer()
    self.timer.timeout.connect(self.update_clock)
    self.timer.start(1000)  # Update every second
    self.update_clock()  # Initial call to set the clock

    # Tab Widget
    self.tabs = QTabWidget()
    main_layout.addWidget(self.tabs)

    # Attendance Tab
    self.attendance_tab = QWidget()
    self.tabs.addTab(self.attendance_tab, "Attendance")
    self.init_attendance_tab()

    # Weekly Report Tab
    self.report_tab = QWidget()
    self.tabs.addTab(self.report_tab, "Weekly Report")
    self.init_report_tab()

    # Announcement/Agenda Tab
    self.announcement_tab = QWidget()
    self.tabs.addTab(self.announcement_tab, "Announcements/Agenda")
    self.init_announcement_tab()

    # Technical Document Tab
    self.technical_document_tab = QWidget()
    self.tabs.addTab(self.technical_document_tab, "Technical Document")
    self.init_technical_document_tab()

    # Status Bar
    self.status_bar = QStatusBar()
    main_layout.addWidget(self.status_bar)
```

- **Header Section:**
  - Displays the application title and a real-time clock for enhanced user awareness during meetings.
  
- **Tab Integration:**
  - Organizes functionalities into distinct tabs: Attendance, Weekly Report, Announcements/Agenda, and Technical Document for streamlined navigation.
  
- **Status Bar:**
  - Provides real-time feedback and notifications to users, enhancing the interactive experience.

#### Attendance Tab

```python
def init_attendance_tab(self):
    layout = QVBoxLayout()
    self.attendance_tab.setLayout(layout)

    # Date Input
    date_layout = QHBoxLayout()
    layout.addLayout(date_layout)

    date_label = QLabel("Date:")
    date_label.setFont(QFont("Arial", 12))
    date_layout.addWidget(date_label)

    self.date_edit_attendance = QDateEdit()
    self.date_edit_attendance.setCalendarPopup(True)
    self.date_edit_attendance.setDate(QDate.currentDate())
    self.date_edit_attendance.setDisplayFormat("MM/dd/yyyy")
    date_layout.addWidget(self.date_edit_attendance)

    # Spacer
    date_layout.addStretch()

    # Scroll Area for Form
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    layout.addWidget(scroll)

    form_widget = QWidget()
    scroll.setWidget(form_widget)
    form_layout = QVBoxLayout()
    form_widget.setLayout(form_layout)

    # Grid for Attendance Records
    grid_layout = QGridLayout()
    form_layout.addLayout(grid_layout)

    # Headers
    headers = ["Member Name", "Position", "Virtual/In-Person", "Attendance", "Time In", "Time Out"]
    for col, header in enumerate(headers):
        label = QLabel(header)
        label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("background-color: red; color: white; padding: 5px;")
        grid_layout.addWidget(label, 0, col)

    # Set column stretch factors for even distribution and wider Time In/Out
    for col in range(6):
        if col in [4, 5]:  # Time In and Time Out columns
            grid_layout.setColumnStretch(col, 2)
        else:
            grid_layout.setColumnStretch(col, 1)

    # Add member rows
    for i, member in enumerate(self.preloaded_members, start=1):
        self.add_member_row(grid_layout, i, member['name'], member['position'])
    # If there are less than 20 members, fill the rest
    for i in range(len(self.preloaded_members)+1, 21):
        self.add_member_row(grid_layout, i)

    # Buttons Layout
    button_layout = QHBoxLayout()
    form_layout.addLayout(button_layout)

    save_button = QPushButton("Save Attendance")
    save_button.setStyleSheet("background-color: #007BFF; color: white; padding: 10px;")
    save_button.clicked.connect(self.save_data_attendance)
    save_button.setToolTip("Save the current attendance records")
    button_layout.addWidget(save_button)

    export_csv_button = QPushButton("Export to CSV")
    export_csv_button.setStyleSheet("background-color: #28A745; color: white; padding: 10px;")
    export_csv_button.clicked.connect(self.export_to_csv)
    export_csv_button.setToolTip("Export attendance records to a CSV file")
    button_layout.addWidget(export_csv_button)

    export_attendance_pdf_button = QPushButton("Export Attendance to PDF")
    export_attendance_pdf_button.setStyleSheet("background-color: #17A2B8; color: white; padding: 10px;")
    export_attendance_pdf_button.clicked.connect(self.export_to_pdf)
    export_attendance_pdf_button.setToolTip("Export attendance records to a PDF file")
    button_layout.addWidget(export_attendance_pdf_button)

    # Spacer
    button_layout.addStretch()

    # Add and Delete Member Buttons
    manage_layout = QHBoxLayout()
    form_layout.addLayout(manage_layout)

    add_member_button = QPushButton("Add Member")
    add_member_button.setStyleSheet("background-color: #17A2B8; color: white; padding: 10px;")
    add_member_button.clicked.connect(self.add_member)
    add_member_button.setToolTip("Add a new member to the attendance list")
    manage_layout.addWidget(add_member_button)

    delete_member_button = QPushButton("Delete Member")
    delete_member_button.setStyleSheet("background-color: #DC3545; color: white; padding: 10px;")
    delete_member_button.clicked.connect(self.delete_member)
    delete_member_button.setToolTip("Delete the last member from the attendance list")
    manage_layout.addWidget(delete_member_button)
```

- **Date Selection:**
  - Allows users to select the meeting date using a calendar widget.
  
- **Attendance Records Grid:**
  - Displays a table with columns for Member Name, Position, Attendance Mode, Attendance Status, Time In, and Time Out.
  - Preloads existing members and provides up to 20 rows for attendance tracking.
  
- **Member Management:**
  - **Add Member:** Dynamically adds a new member row for attendance tracking.
  - **Delete Member:** Removes the last member row from the attendance list.
  
- **Export and Save Functionality:**
  - **Save Attendance:** Saves the current attendance records to persistent storage.
  - **Export to CSV:** Allows exporting attendance data to a CSV file for external use.
  - **Export to PDF:** Generates a well-formatted PDF report of the attendance records with watermark integration.

#### Weekly Report Tab

```python
def init_report_tab(self):
    layout = QVBoxLayout()
    self.report_tab.setLayout(layout)

    # Create a central frame to center the content
    central_frame = QFrame()
    central_layout = QVBoxLayout()
    central_frame.setLayout(central_layout)
    central_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(central_frame, alignment=Qt.AlignmentFlag.AlignCenter)

    # Container layout with fixed width for better aesthetics
    container_layout = QVBoxLayout()
    container_layout.setContentsMargins(50, 20, 50, 20)  # Add margins
    container_layout.setSpacing(20)  # Add spacing between widgets
    central_layout.addLayout(container_layout)

    # Date Input
    date_layout = QHBoxLayout()
    container_layout.addLayout(date_layout)

    date_label = QLabel("Date:")
    date_label.setFont(QFont("Arial", 12))
    date_layout.addWidget(date_label)

    self.date_edit_report = QDateEdit()
    self.date_edit_report.setCalendarPopup(True)
    self.date_edit_report.setDate(QDate.currentDate())
    self.date_edit_report.setDisplayFormat("MM/dd/yyyy")
    self.date_edit_report.setFixedWidth(150)
    date_layout.addWidget(self.date_edit_report)

    # Spacer to push date input to the left
    date_layout.addStretch()

    # Weekly Report Input
    report_layout = QVBoxLayout()
    container_layout.addLayout(report_layout)

    report_label = QLabel("Weekly Report:")
    report_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
    report_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    report_layout.addWidget(report_label)

    self.report_text = QTextEdit()
    self.report_text.setMinimumHeight(500)  # Increased height for better input
    self.report_text.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    report_layout.addWidget(self.report_text)

    # Buttons Layout for Report Tab
    report_button_layout = QHBoxLayout()
    container_layout.addLayout(report_button_layout)

    export_report_pdf_button = QPushButton("Export Report to PDF")
    export_report_pdf_button.setStyleSheet("background-color: #FFC107; color: white; padding: 10px;")
    export_report_pdf_button.clicked.connect(self.export_weekly_report_pdf)
    export_report_pdf_button.setToolTip("Export the weekly report to a PDF file")
    report_button_layout.addWidget(export_report_pdf_button)

    clear_report_button = QPushButton("Clear Report")
    clear_report_button.setStyleSheet("background-color: #6C757D; color: white; padding: 10px;")
    clear_report_button.clicked.connect(self.clear_weekly_report)
    clear_report_button.setToolTip("Clear the weekly report text")
    report_button_layout.addWidget(clear_report_button)

    # Spacer to center the buttons
    report_button_layout.addStretch()
```

- **Date Selection:**
  - Allows users to specify the date for the weekly report.
  
- **Report Input:**
  - Provides a large text area for users to input the weekly report summary.
  
- **Export and Clear Functionality:**
  - **Export to PDF:** Generates a PDF version of the weekly report with watermark integration.
  - **Clear Report:** Clears the input text area after user confirmation.

#### Announcements/Agenda Tab

```python
def init_announcement_tab(self):
    layout = QVBoxLayout()
    self.announcement_tab.setLayout(layout)

    # Create a central frame to center the content
    central_frame = QFrame()
    central_layout = QVBoxLayout()
    central_frame.setLayout(central_layout)
    central_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(central_frame, alignment=Qt.AlignmentFlag.AlignCenter)

    # Container layout with fixed width for better aesthetics
    container_layout = QVBoxLayout()
    container_layout.setContentsMargins(50, 20, 50, 20)  # Add margins
    container_layout.setSpacing(20)  # Add spacing between widgets
    central_layout.addLayout(container_layout)

    # Date Input
    date_layout = QHBoxLayout()
    container_layout.addLayout(date_layout)

    date_label = QLabel("Date:")
    date_label.setFont(QFont("Arial", 12))
    date_layout.addWidget(date_label)

    self.date_edit_announcement = QDateEdit()
    self.date_edit_announcement.setCalendarPopup(True)
    self.date_edit_announcement.setDate(QDate.currentDate())
    self.date_edit_announcement.setDisplayFormat("MM/dd/yyyy")
    self.date_edit_announcement.setFixedWidth(150)
    date_layout.addWidget(self.date_edit_announcement)

    # Spacer to push date input to the left
    date_layout.addStretch()

    # Announcement Input
    announcement_layout = QVBoxLayout()
    container_layout.addLayout(announcement_layout)

    announcement_label = QLabel("Announcements/Agenda:")
    announcement_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
    announcement_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    announcement_layout.addWidget(announcement_label)

    self.announcement_text = QTextEdit()
    self.announcement_text.setMinimumHeight(500)  # Increased height for better input
    self.announcement_text.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    announcement_layout.addWidget(self.announcement_text)

    # Buttons Layout for Announcement Tab
    announcement_button_layout = QHBoxLayout()
    container_layout.addLayout(announcement_button_layout)

    export_announcement_pdf_button = QPushButton("Export Announcements/Agenda to PDF")
    export_announcement_pdf_button.setStyleSheet("background-color: #FFC107; color: white; padding: 10px;")
    export_announcement_pdf_button.clicked.connect(self.export_announcement_pdf)
    export_announcement_pdf_button.setToolTip("Export the announcements/agenda to a PDF file")
    announcement_button_layout.addWidget(export_announcement_pdf_button)

    clear_announcement_button = QPushButton("Clear Announcements/Agenda")
    clear_announcement_button.setStyleSheet("background-color: #6C757D; color: white; padding: 10px;")
    clear_announcement_button.clicked.connect(self.clear_announcements)
    clear_announcement_button.setToolTip("Clear the announcements/agenda text")
    announcement_button_layout.addWidget(clear_announcement_button)

    # Spacer to center the buttons
    announcement_button_layout.addStretch()
```

- **Date Selection:**
  - Allows users to specify the date for the announcements or agenda.
  
- **Announcements/Agenda Input:**
  - Provides a large text area for users to input meeting announcements or agendas.
  
- **Export and Clear Functionality:**
  - **Export to PDF:** Generates a PDF version of the announcements or agenda with watermark integration.
  - **Clear Announcements/Agenda:** Clears the input text area after user confirmation.

#### Technical Document Tab

```python
def init_technical_document_tab(self):
    layout = QVBoxLayout()
    self.technical_document_tab.setLayout(layout)

    # Create a central frame to center the content
    central_frame = QFrame()
    central_layout = QVBoxLayout()
    central_frame.setLayout(central_layout)
    central_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(central_frame, alignment=Qt.AlignmentFlag.AlignCenter)

    # Container layout with fixed width for better aesthetics
    container_layout = QVBoxLayout()
    container_layout.setContentsMargins(50, 20, 50, 20)  # Add margins
    container_layout.setSpacing(20)  # Add spacing between widgets
    central_layout.addLayout(container_layout)

    # Date and Document Name Input
    date_doc_layout = QHBoxLayout()
    container_layout.addLayout(date_doc_layout)

    date_label = QLabel("Date:")
    date_label.setFont(QFont("Arial", 12))
    date_doc_layout.addWidget(date_label)

    self.date_edit_technical_document = QDateEdit()
    self.date_edit_technical_document.setCalendarPopup(True)
    self.date_edit_technical_document.setDate(QDate.currentDate())
    self.date_edit_technical_document.setDisplayFormat("MM/dd/yyyy")
    self.date_edit_technical_document.setFixedWidth(150)
    date_doc_layout.addWidget(self.date_edit_technical_document)

    # Document Name Input
    doc_name_label = QLabel("Document Name:")
    doc_name_label.setFont(QFont("Arial", 12))
    date_doc_layout.addWidget(doc_name_label)

    self.doc_name_edit = QLineEdit()
    self.doc_name_edit.setPlaceholderText("Enter document name")
    self.doc_name_edit.setFixedWidth(300)
    date_doc_layout.addWidget(self.doc_name_edit)

    # Spacer to push date input to the left
    date_doc_layout.addStretch()

    # Technical Document Input
    tech_doc_layout = QVBoxLayout()
    container_layout.addLayout(tech_doc_layout)

    tech_doc_label = QLabel("Technical Document:")
    tech_doc_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
    tech_doc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    tech_doc_layout.addWidget(tech_doc_label)

    self.tech_doc_text = QTextEdit()
    self.tech_doc_text.setMinimumHeight(400)  # Adjusted height
    self.tech_doc_text.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    tech_doc_layout.addWidget(self.tech_doc_text)

    # Electronic Signature Input
    signature_layout = QHBoxLayout()
    container_layout.addLayout(signature_layout)

    signature_label = QLabel("Electronic Signature:")
    signature_label.setFont(QFont("Arial", 12))
    signature_layout.addWidget(signature_label)

    self.signature_edit = QLineEdit()
    self.signature_edit.setPlaceholderText("Enter electronic signature")
    self.signature_edit.setFixedWidth(300)
    signature_layout.addWidget(self.signature_edit)

    # Spacer to push signature input to the left
    signature_layout.addStretch()

    # Buttons Layout for Technical Document Tab
    tech_doc_button_layout = QHBoxLayout()
    container_layout.addLayout(tech_doc_button_layout)

    export_tech_doc_pdf_button = QPushButton("Export Technical Document to PDF")
    export_tech_doc_pdf_button.setStyleSheet("background-color: #FFC107; color: white; padding: 10px;")
    export_tech_doc_pdf_button.clicked.connect(self.export_technical_document_pdf)
    export_tech_doc_pdf_button.setToolTip("Export the technical document to a PDF file")
    tech_doc_button_layout.addWidget(export_tech_doc_pdf_button)

    clear_tech_doc_button = QPushButton("Clear Technical Document")
    clear_tech_doc_button.setStyleSheet("background-color: #6C757D; color: white; padding: 10px;")
    clear_tech_doc_button.clicked.connect(self.clear_technical_document)
    clear_tech_doc_button.setToolTip("Clear the technical document text")
    tech_doc_button_layout.addWidget(clear_tech_doc_button)

    # Spacer to center the buttons
    tech_doc_button_layout.addStretch()
```

- **Date and Document Name:**
  - Allows users to specify the date and name of the technical document.
  
- **Technical Document Input:**
  - Provides a sizable text area for users to compose detailed technical documents.
  
- **Electronic Signature:**
  - Enables users to input an electronic signature, which can be embedded as an image in the PDF.
  
- **Export and Clear Functionality:**
  - **Export Technical Document to PDF:** Generates a PDF version of the technical document with an electronic signature and watermark.
  - **Clear Technical Document:** Clears the input fields after user confirmation.

#### Member Management

```python
def add_member_row(self, layout, row_number, name='', position=''):
    row_entries = []
    name_entry = QLineEdit()
    name_entry.setPlaceholderText("Enter name")
    name_entry.setText(name)
    name_entry.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
    layout.addWidget(name_entry, row_number, 0)
    row_entries.append(name_entry)

    position_entry = QLineEdit()
    position_entry.setPlaceholderText("Enter position")
    position_entry.setText(position)
    position_entry.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
    layout.addWidget(position_entry, row_number, 1)
    row_entries.append(position_entry)

    attending_as_combo = QComboBox()
    attending_as_combo.addItems(self.attending_as_options)
    attending_as_combo.setCurrentIndex(0)
    attending_as_combo.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
    layout.addWidget(attending_as_combo, row_number, 2)
    row_entries.append(attending_as_combo)

    attendance_combo = QComboBox()
    attendance_combo.addItems(self.attendance_options)
    attendance_combo.setCurrentIndex(0)
    attendance_combo.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
    layout.addWidget(attendance_combo, row_number, 3)
    row_entries.append(attendance_combo)

    # Add Time In and Time Out fields
    time_in_edit = QTimeEdit()
    time_in_edit.setDisplayFormat("hh:mm AP")
    time_in_edit.setTime(QTime.currentTime())
    time_in_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
    layout.addWidget(time_in_edit, row_number, 4)
    row_entries.append(time_in_edit)

    time_out_edit = QTimeEdit()
    time_out_edit.setDisplayFormat("hh:mm AP")
    time_out_edit.setTime(QTime.currentTime())
    time_out_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
    layout.addWidget(time_out_edit, row_number, 5)
    row_entries.append(time_out_edit)

    self.entries.append(row_entries)
```

- **Functionality:**
  - Dynamically adds a new row in the attendance grid for a committee member.
  - Each row includes fields for Member Name, Position, Attendance Mode, Attendance Status, Time In, and Time Out.
  
- **User Interaction:**
  - Users can input or edit member details directly within the grid.
  
- **Data Management:**
  - Maintains a list of entries to facilitate saving and exporting attendance data.

#### Export Functionality

##### Export to CSV

```python
def export_to_csv(self):
    try:
        default_filename = f"Tech_Fee_Committee_Attendance_{datetime.now().strftime('%m-%d-%Y')}.csv"
        file_path, _ = QFileDialog.getSaveFileName(self, "Save CSV", default_filename, "CSV Files (*.csv)")

        if file_path:
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([f"Tech Fee Committee Attendance Record ({self.date_edit_attendance.date().toString('MM/dd/yyyy')})"])
                writer.writerow(["Member Name", "Position", "Virtual/In-Person", "Attendance", "Time In", "Time Out"])

                for row in self.entries:
                    member_name = row[0].text()
                    position = row[1].text()
                    virtual_in_person = row[2].currentText()
                    attendance = row[3].currentText()
                    time_in = row[4].time().toString("hh:mm AP")
                    time_out = row[5].time().toString("hh:mm AP")
                    writer.writerow([member_name, position, virtual_in_person, attendance, time_in, time_out])

            self.status_bar.showMessage(f"Attendance data exported to {file_path}", 5000)  # Display for 5 seconds
        else:
            QMessageBox.warning(self, "No File Selected", "Please choose a file path.")
    except Exception as e:
        QMessageBox.critical(self, "Error", f"Error exporting data: {e}")
```

- **Purpose:** Allows users to export attendance records to a CSV file for external analysis, reporting, or archival purposes.
  
- **Process:**
  - Prompts the user to select a save location and filename.
  - Writes attendance data with headers to the specified CSV file.
  - Provides real-time feedback via the status bar upon successful export or error notifications if issues arise.

##### Export to PDF

```python
def export_to_pdf(self):
    try:
        default_filename = f"Tech_Fee_Committee_Attendance_{datetime.now().strftime('%m-%d-%Y')}.pdf"
        file_path, _ = QFileDialog.getSaveFileName(self, "Save PDF", default_filename, "PDF Files (*.pdf)")

        if file_path:
            # Create a PDF document with margins
            doc = SimpleDocTemplate(file_path, pagesize=letter,
                                    rightMargin=72, leftMargin=72,
                                    topMargin=72, bottomMargin=72)
            elements = []

            # Styles
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'TitleStyle',
                parent=styles['Title'],
                fontName='Helvetica-Bold',
                fontSize=24,
                textColor=colors.red,
                alignment=1,  # Center
                spaceAfter=12
            )
            subtitle_style = ParagraphStyle(
                'SubtitleStyle',
                parent=styles['Normal'],
                fontName='Helvetica',
                fontSize=14,
                textColor=colors.black,
                alignment=1,  # Center
                spaceAfter=24
            )
            normal_style = ParagraphStyle(
                'NormalCentered',
                parent=styles['Normal'],
                alignment=1,  # Center
                spaceAfter=12
            )

            # Title
            title = Paragraph("Tech Fee Committee Attendance Record", title_style)
            elements.append(title)

            # Date as Subtitle
            date_paragraph = Paragraph(f"Date: {self.date_edit_attendance.date().toString('MM/dd/yyyy')}", subtitle_style)
            elements.append(date_paragraph)

            # Table Data
            data = [["Member Name", "Position", "Virtual/In-Person", "Attendance", "Time In", "Time Out"]]
            for row in self.entries:
                member_name = row[0].text()
                position = row[1].text()
                virtual_in_person = row[2].currentText()
                attendance = row[3].currentText()
                time_in = row[4].time().toString("hh:mm AP")
                time_out = row[5].time().toString("hh:mm AP")
                data.append([member_name, position, virtual_in_person, attendance, time_in, time_out])

            # Table Style with Red Headers and Alternating Row Colors
            table = Table(data, colWidths=[1.5 * inch] * 6)
            table_style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.red),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ])

            # Add alternating row colors
            for i in range(1, len(data)):
                if i % 2 == 0:
                    bg_color = colors.lightgrey
                else:
                    bg_color = colors.whitesmoke
                table_style.add('BACKGROUND', (0, i), (-1, i), bg_color)

            table.setStyle(table_style)

            # Center the table
            table.hAlign = 'CENTER'

            elements.append(table)
            elements.append(Spacer(1, 0.2 * inch))

            # Build PDF with full-page watermark
            doc.build(elements, onFirstPage=self.add_watermark, onLaterPages=self.add_watermark)

            self.status_bar.showMessage(f"Attendance data exported to {file_path}", 5000)  # Display for 5 seconds
        else:
            QMessageBox.warning(self, "No File Selected", "Please choose a file path.")
    except Exception as e:
        QMessageBox.critical(self, "Error", f"Error exporting data: {e}")
```

- **Purpose:** Enables users to generate a professional PDF report of attendance records, complete with organizational branding via watermark integration.
  
- **Process:**
  - Prompts the user to select a save location and filename.
  - Constructs a PDF document with a title, date, and a well-formatted table of attendance records.
  - Applies styling for headers and alternating row colors for enhanced readability.
  - Integrates a full-page watermark featuring the SCSU logo to maintain branding consistency and document security.
  - Provides real-time feedback via the status bar upon successful export or error notifications if issues arise.

#### Watermark Integration

```python
def add_watermark(self, canvas_obj, doc):
    """Adds a full-page watermark using the sga.jpg image."""
    canvas_obj.saveState()
    # Draw the watermark image
    watermark_path = r"C:\scsuimage\sga.jpg"  # Ensure this path is correct or make it configurable
    if os.path.exists(watermark_path):
        try:
            # Read the image
            watermark = ImageReader(watermark_path)
            # Get the dimensions of the page
            page_width, page_height = letter
            # Calculate scale to cover the entire page
            img_width, img_height = watermark.getSize()
            scale_x = page_width / img_width
            scale_y = page_height / img_height
            scale = max(scale_x, scale_y)
            # Calculate position to center the image
            x = (page_width - img_width * scale) / 2
            y = (page_height - img_height * scale) / 2
            # Set transparency
            canvas_obj.setFillAlpha(0.1)  # Adjust transparency as needed
            # Draw the image
            canvas_obj.drawImage(
                watermark,
                x,
                y,
                width=img_width * scale,
                height=img_height * scale,
                mask='auto'
            )
            # Reset transparency
            canvas_obj.setFillAlpha(1)
        except Exception as img_e:
            QMessageBox.warning(self, "Watermark Error", f"Failed to add watermark image: {img_e}")
    else:
        QMessageBox.warning(self, "Watermark Image Not Found", f"Watermark image not found at {watermark_path}.")
    canvas_obj.restoreState()
```

- **Purpose:** Ensures that all exported PDF documents include a full-page watermark featuring the SCSU logo (`sga.jpg`) for branding and security.
  
- **Process:**
  - Verifies the existence of the watermark image at the specified path.
  - Calculates the appropriate scaling to cover the entire page without distortion.
  - Applies transparency to the watermark to prevent it from overpowering the document content.
  - Handles errors gracefully by notifying users if the watermark image is missing or fails to load.

**Note:** Ensure that the `watermark_path` is correctly set to the location of the `sga.jpg` image on your system or make it configurable within the application settings.

#### Error Handling and Notifications

- **Status Bar Messages:**
  - Provides users with real-time feedback on actions such as saving data or exporting files.
  
- **Message Boxes:**
  - Alerts users to critical issues, such as incomplete data entries or file export errors, ensuring that they are informed of necessary corrective actions.
  
- **Tooltips:**
  - Offers brief explanations for buttons and input fields to guide users through the application's functionalities.

---

## Installation and Setup

To install and run the **Tech Fee Committee Attendance/Weekly Report Generator**, follow these steps:

### 1. Clone or Download the Repository

If the project is hosted on a platform like GitHub, you can clone it using:

```bash
git clone https://github.com/AshleyMGreerProjects/Project-Paperless-SCSU-SGA.git
```

If you've downloaded a `.zip` file:

1. Extract the files to your preferred location.
2. Navigate to the project folder.

### 2. Create a Virtual Environment (Recommended)

It's advisable to create a virtual environment to manage dependencies without affecting system-wide packages.

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install the Required Python Libraries

You can install the necessary libraries by running:

```bash
pip install -r requirements.txt
```

**`requirements.txt` Content:**

```
PyQt6==6.5.2
pandas==2.1.1
reportlab==3.6.12
Pillow==9.5.0
```

*Note:* Including specific version numbers ensures compatibility and stability. Adjust the versions as needed based on your development environment.

If a `requirements.txt` file is not included, install the libraries manually:

```bash
pip install PyQt6==6.5.2 pandas==2.1.1 reportlab==3.6.12 Pillow==9.5.0
```

### 4. Run the Program

Once dependencies are installed, navigate to the project directory and run the program:

```bash
python attendance_report_generator.py
```

This will launch the GUI where you can begin tracking attendance and generating reports.

### 5. Setting Up the Watermark Image

Ensure that the watermark image (`sga.jpg`) is placed at the specified path (`C:\scsuimage\sga.jpg`) or update the `watermark_path` in the code to reflect its actual location on your system.

---

## Usage Guide

Upon launching the **Tech Fee Committee Attendance/Weekly Report Generator**, users are greeted with an intuitive interface divided into four primary tabs: Attendance, Weekly Report, Announcements/Agenda, and Technical Document. Below is a step-by-step guide to utilizing each feature effectively.

### 1. **Attendance Tab**

#### Step 1: Entering Attendance

- **Date Selector:** Select the meeting date using the calendar widget.
- **Member Information:** Input the member's name, position, and attendance mode (In-Person or Virtual).
- **Attendance Status:** Mark each member as **Attending** or **Absent**.
- **Time In/Out:** Record the exact times members join and leave the meeting.

#### Step 2: Managing Members

- **Add Member:** Click the **Add Member** button to dynamically add a new member row for attendance tracking.
- **Delete Member:** Click the **Delete Member** button to remove the last member row from the attendance list.

#### Step 3: Saving and Exporting Attendance Data

- **Save Attendance:** Click **Save Attendance** to save the current attendance records.
- **Export to CSV:** Click **Export to CSV** to save attendance data in CSV format.
- **Export Attendance to PDF:** Click **Export Attendance to PDF** to generate a PDF report with a watermark.

### 2. **Weekly Report Tab**

#### Step 1: Creating a Weekly Report

- **Date Selector:** Choose the date for the weekly report.
- **Report Input:** Enter the summary of the week's meetings, discussions, and outcomes in the provided text area.

#### Step 2: Exporting the Report

- **Export Report to PDF:** Click to generate a PDF version of the weekly report with a watermark.
- **Clear Report:** Click to clear the report text area after confirmation.

### 3. **Announcements/Agenda Tab**

#### Step 1: Inputting Announcements or Agenda

- **Date Selector:** Select the date for the announcements or agenda.
- **Announcements/Agenda Input:** Enter the relevant information in the text area.

#### Step 2: Exporting Announcements/Agenda

- **Export Announcements/Agenda to PDF:** Click to generate a PDF document of the announcements or agenda with a watermark.
- **Clear Announcements/Agenda:** Click to clear the input area after confirmation.

### 4. **Technical Document Tab**

#### Step 1: Creating a Technical Document

- **Date Selector:** Choose the date for the technical document.
- **Document Name:** Enter the name/title of the document.
- **Technical Document Input:** Compose the technical document in the provided text area.
- **Electronic Signature:** Input an electronic signature, which will be embedded as an image in the PDF.

#### Step 2: Exporting the Technical Document

- **Export Technical Document to PDF:** Click to generate a PDF version of the technical document with an embedded signature and watermark.
- **Clear Technical Document:** Click to clear the document text area and signature field after confirmation.

---

## Testing and Validation

Throughout a meticulous development process, the **Tech Fee Committee Attendance/Weekly Report Generator** underwent extensive testing to ensure reliability, security, and user satisfaction.

### 1. **Unit Testing**

- **Attendance Logging:** Verified that attendance records are accurately captured and stored.
- **Export Functions:** Ensured that CSV and PDF exports contain correct and complete data.
- **GUI Components:** Tested all buttons, inputs, and interactive elements for responsiveness and correctness.

### 2. **Integration Testing**

- **Data Flow:** Confirmed seamless data flow between different tabs and functionalities.
- **Watermark Integration:** Validated that all exported PDFs correctly display the watermark without affecting document readability.
- **Member Management:** Tested dynamic addition and deletion of members to ensure the attendance grid updates appropriately.

### 3. **User Acceptance Testing (UAT)**

- **Usability:** Conducted sessions with committee members to gather feedback on the application's ease of use and functionality.
- **Feedback Incorporation:** Iteratively refined features based on user feedback to enhance user experience and address specific needs.

### 4. **Security Testing**

- **Data Protection:** Ensured that all data exports, especially PDFs with sensitive attendance information, are securely handled.
- **Error Handling:** Tested the application's resilience against potential errors, such as missing watermark images or invalid data entries, ensuring graceful degradation and informative alerts.

---

## Future Enhancements

While the current version of the **Tech Fee Committee Attendance/Weekly Report Generator** offers robust features, several enhancements are planned to further elevate its utility and performance:

1. **User Authentication:** Implement secure login mechanisms to restrict access to authorized committee members only.
2. **Cloud Integration:** Enable cloud-based storage for attendance records and reports for easier access and backup.
3. **Mobile Compatibility:** Develop a mobile version or responsive design to allow attendance tracking on-the-go.
4. **Advanced Reporting:** Introduce more detailed analytics and visualizations for attendance trends and member participation.
5. **Customization Options:** Allow users to customize report templates and watermark images to better align with organizational branding.
6. **Automated Notifications:** Implement email or in-app notifications for upcoming meetings, report generation reminders, or quorum alerts.
7. **Multi-Language Support:** Expand accessibility by supporting multiple languages within the user interface.

---

## Conclusion

The **Tech Fee Committee Attendance/Weekly Report Generator** stands as a testament to efficient software design and user-centric development. By automating attendance logging and report generation, it significantly reduces manual effort, enhances data accuracy, and ensures that committee operations are both streamlined and transparent. The application's thoughtful integration of features like real-time quorum verification, customizable exports, and secure data handling underscores its commitment to meeting the specific needs of committee members.

Through continuous feedback and iterative refinements, the tool not only meets but exceeds the initial project objectives, fostering a fully digital and paperless environment for the six committees involved. As future enhancements are planned, the application is poised to become an indispensable asset in committee management and reporting.

---

## Appendix

### Dependencies

Ensure that the following Python packages are installed:

- **PyQt6:** For building the graphical user interface.
- **pandas:** For data handling and CSV export.
- **reportlab:** For generating PDF files.
- **Pillow (PIL):** For image manipulation, particularly for generating electronic signatures.

**Installation via pip:**

```bash
pip install PyQt6==6.5.2 pandas==2.1.1 reportlab==3.6.12 Pillow==9.5.0
```

Alternatively, if a `requirements.txt` file is provided, install all dependencies at once:

```bash
pip install -r requirements.txt
```

**`requirements.txt` Content:**

```
PyQt6==6.5.2
pandas==2.1.1
reportlab==3.6.12
Pillow==9.5.0
```

*Note:* Including specific version numbers ensures compatibility and stability. Adjust the versions as needed based on your development environment.

### License

The **Tech Fee Committee Attendance/Weekly Report Generator** application is licensed under the [MIT License](https://opensource.org/licenses/MIT).

**MIT License**

```
MIT License

Copyright (c) 2024 

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### Repository Links

- **Tech Fee Committee Attendance/Weekly Report Generator:**
  
  [https://github.com/AshleyMGreerProjects/attendance-weekly-report-generator](https://github.com/AshleyMGreerProjects/attendance-weekly-report-generator)

- **Project-Paperless-SCSU-SGA:**
  
  [https://github.com/AshleyMGreerProjects/Project-Paperless-SCSU-SGA](https://github.com/AshleyMGreerProjects/Project-Paperless-SCSU-SGA)

---

**Repository Links:**  
- [Tech Fee Committee Attendance/Weekly Report Generator](https://github.com/AshleyMGreerProjects/attendance-weekly-report-generator)  
- [Project-Paperless-SCSU-SGA](https://github.com/AshleyMGreerProjects/Project-Paperless-SCSU-SGA)

For any additional information, updates, or contributions, please visit the [GitHub repositories](https://github.com/AshleyMGreerProjects).

---

**Notes for Further Integration:**

If you intend to include more detailed information from the **Project-Paperless-SCSU-SGA** repository into this documentation, consider adding a new section or subsection within the **Project Overview** or **Features** sections. Here's an example of how you might incorporate it:

### 2. **Project-Paperless-SCSU-SGA Overview**

The **Project-Paperless-SCSU-SGA** is an initiative aimed at transitioning the SCSU Student Government Association (SGA) to a fully digital, paperless system. This project complements the **Tech Fee Committee Attendance/Weekly Report Generator** by providing additional tools and functionalities to enhance administrative efficiency and data management across various SGA committees.

**Key Features:**

- **Digital Document Management:** Centralized storage and retrieval of all SGA documents.
- **Automated Workflow Processes:** Streamlining approvals and submissions through digital workflows.
- **Real-Time Collaboration:** Facilitating seamless collaboration among SGA members with version control and access management.
- **Security Enhancements:** Implementing robust security measures to protect sensitive SGA data.

For more details, visit the [Project-Paperless-SCSU-SGA repository](https://github.com/AshleyMGreerProjects/Project-Paperless-SCSU-SGA).
