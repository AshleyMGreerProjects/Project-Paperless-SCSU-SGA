# Project Paperless

## Overview of the Project

The **Tech Fee Committee Attendance/Weekly Report Generator** is a robust Python application built to streamline and automate the process of logging committee attendance and generating weekly reports. The system eliminates the manual, paper-based tracking methods, transitioning six committees (each with 30-50 members) to a fully digital, paperless system. By reducing the time needed for manual reporting by **80%**, the tool enhances accuracy and efficiency, ensuring that attendance data is easily accessible in CSV or PDF formats.

This system was iteratively refined based on user feedback to ensure it met the specific needs of the committees using it, including real-time quorum verification and customizable report outputs. The application is designed to be user-friendly, with a Graphical User Interface (GUI) that supports seamless data entry, exporting capabilities, and attendance management.

## Features of the Tool

1. **Attendance Tracking**:
   - Users can log and edit member attendance during meetings.
   - Attendance records are stored for future reference.
   - Custom fields for **in-person** or **virtual** attendance modes are supported.

2. **Quorum Verification**:
   - The system automatically checks if quorum is met, ensuring that meetings can proceed with official decision-making.

3. **Automated Export to CSV and PDF**:
   - Attendance data can be exported as **CSV** or **PDF** files, simplifying record-keeping and formal documentation.
   - Weekly reports summarizing meeting outcomes can also be generated in **PDF** format for formal use.

4. **User-Friendly GUI**:
   - The tool provides a clean and intuitive GUI where users can input attendance data, generate reports, and manage members. All actions are simple, requiring no programming knowledge.

5. **Customization**:
   - The system allows users to pre-load members, dynamically add or remove members, and easily adjust attendance data during a meeting.

## Prerequisites

Before you begin, ensure that the following are installed on your machine:
- **Python 3.8+**
- Required Python libraries (`pandas`, `PyQt6`, `reportlab`, etc.).

### Required Python Libraries:
- `PyQt6`: For creating the graphical user interface.
- `pandas`: For data handling and CSV export.
- `reportlab`: For generating PDF files.
- `tkinter`: An optional dependency for file dialogs.

## Installation Instructions

To install and run the **Tech Fee Committee Attendance/Weekly Report Generator**, follow these steps:

### Step 1: Clone or Download the Repository

If the project is hosted on a platform like GitHub, you can clone it using:

```bash
git clone https://github.com/username/attendance-weekly-report-generator.git
```

If you've downloaded a `.zip` file:
1. Extract the files to your preferred location.
2. Navigate to the project folder.

### Step 2: Install the Required Python Libraries

You can install the necessary libraries by running:

```bash
pip install -r requirements.txt
```

Alternatively, if a `requirements.txt` file is not included, install the libraries manually:

```bash
pip install PyQt6 pandas reportlab
```

### Step 3: Running the Program

Once dependencies are installed, navigate to the project directory and run the program:

```bash
python attendance_report_generator.py
```

This will launch the GUI where you can begin tracking attendance and generating reports.

## User Guide: Step-by-Step Usage

### Step 1: Entering Attendance

- **Date Selector**: Select the meeting date using the calendar widget.
- **Member Information**: Input the member's name, position, and attendance status (in-person or virtual).
- **Attendance**: Mark whether each member is present or absent.

### Step 2: Managing Members

- Use the **Add Member** button to add new attendees to the list dynamically.
- The **Delete Member** button allows you to remove members from the list.

### Step 3: Verifying Quorum

- The system automatically checks if the number of attendees meets the quorum requirement and alerts the user if it is not met.

### Step 4: Exporting Data

- **Save Attendance**: Save the attendance data for the current meeting.
- **Export to CSV**: Export the data to a CSV file.
- **Export Attendance to PDF**: Generate a formal attendance report in PDF format.

### Step 5: Generating Weekly Reports

- The tool also includes a **Weekly Report** section where you can summarize the meeting outcomes.
- Export the report as a **PDF** for official use.

### Step 6: Customizing the Watermark and Headers

- The tool adds the **SCSU logo** as a watermark on the PDFs, along with headers that align with your organization's branding.
  
## Example Outputs

1. **Attendance Record (PDF)**: A formal attendance report listing each member’s name, position, attendance method (in-person or virtual), and their status (present or absent).
   
2. **Weekly Report (PDF)**: A summarized report that includes the date, attendance record, and a detailed summary of the meeting's discussions.

## How I Made Committees Follow These Instructions

To ensure that the six committees effectively adopted this system, I provided clear, step-by-step instructions for both installation and usage. I held training sessions with committee members to walk them through the installation process and show them how to use the tool for both attendance tracking and report generation.

Through these sessions, I gathered feedback, which helped in iterating the tool to make it more user-friendly. Features such as quorum checking and report generation were refined based on real-world usage, ensuring that the tool met the needs of committee members. 

Each committee had approximately **10 to 15 members,** tracking 60-75 members in total, and the tool was designed to handle all of them efficiently. Over a two-month period, I implemented their feedback, streamlining processes and customizing the tool for each committee’s needs. This resulted in an 80% reduction in the time spent on manual attendance tracking and reporting.
