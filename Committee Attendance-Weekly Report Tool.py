import sys
import os
import csv
import json
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QFileDialog, QComboBox, QScrollArea, QTextEdit,
    QDateEdit, QGridLayout, QSizePolicy, QSpacerItem, QTabWidget
)
from PyQt6.QtGui import QFont, QPixmap, QColor
from PyQt6.QtCore import Qt, QDate
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader

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

    def load_preloaded_members(self):
        self.preloaded_members = []
        if os.path.exists('members.json'):
            with open('members.json', 'r') as f:
                self.preloaded_members = json.load(f)
        else:
            # If the file doesn't exist, create an empty list
            self.preloaded_members = []

    def save_preloaded_members(self):
        with open('members.json', 'w') as f:
            json.dump(self.preloaded_members, f, indent=4)

    def init_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Header without Image
        header_layout = QHBoxLayout()
        main_layout.addLayout(header_layout)

        title_label = QLabel("Tech Fee Committee Attendance/Weekly Report Generator")
        title_font = QFont("Arial", 20, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(title_label)

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
        headers = ["Member Name", "Position", "Virtual/In-Person", "Attendance"]
        for col, header in enumerate(headers):
            label = QLabel(header)
            label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet("background-color: red; color: white; padding: 5px;")
            grid_layout.addWidget(label, 0, col)

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
        button_layout.addWidget(save_button)

        export_csv_button = QPushButton("Export to CSV")
        export_csv_button.setStyleSheet("background-color: #28A745; color: white; padding: 10px;")
        export_csv_button.clicked.connect(self.export_to_csv)
        button_layout.addWidget(export_csv_button)

        export_attendance_pdf_button = QPushButton("Export Attendance to PDF")
        export_attendance_pdf_button.setStyleSheet("background-color: #17A2B8; color: white; padding: 10px;")
        export_attendance_pdf_button.clicked.connect(self.export_to_pdf)
        button_layout.addWidget(export_attendance_pdf_button)

        # Spacer
        button_layout.addStretch()

        # Add and Delete Member Buttons
        manage_layout = QHBoxLayout()
        form_layout.addLayout(manage_layout)

        add_member_button = QPushButton("Add Member")
        add_member_button.setStyleSheet("background-color: #17A2B8; color: white; padding: 10px;")
        add_member_button.clicked.connect(self.add_member)
        manage_layout.addWidget(add_member_button)

        delete_member_button = QPushButton("Delete Member")
        delete_member_button.setStyleSheet("background-color: #DC3545; color: white; padding: 10px;")
        delete_member_button.clicked.connect(self.delete_member)
        manage_layout.addWidget(delete_member_button)

    def init_report_tab(self):
        layout = QVBoxLayout()
        self.report_tab.setLayout(layout)

        # Date Input
        date_layout = QHBoxLayout()
        layout.addLayout(date_layout)

        date_label = QLabel("Date:")
        date_label.setFont(QFont("Arial", 12))
        date_layout.addWidget(date_label)

        self.date_edit_report = QDateEdit()
        self.date_edit_report.setCalendarPopup(True)
        self.date_edit_report.setDate(QDate.currentDate())
        self.date_edit_report.setDisplayFormat("MM/dd/yyyy")
        date_layout.addWidget(self.date_edit_report)

        # Spacer
        date_layout.addStretch()

        # Weekly Report Input
        report_layout = QVBoxLayout()
        layout.addLayout(report_layout)

        report_label = QLabel("Weekly Report:")
        report_label.setFont(QFont("Arial", 12))
        report_layout.addWidget(report_label)

        self.report_text = QTextEdit()
        self.report_text.setFixedHeight(400)  # Increased height for better input
        report_layout.addWidget(self.report_text)

        # Export Button
        export_layout = QHBoxLayout()
        layout.addLayout(export_layout)

        export_report_pdf_button = QPushButton("Export Report to PDF")
        export_report_pdf_button.setStyleSheet("background-color: #FFC107; color: white; padding: 10px;")
        export_report_pdf_button.clicked.connect(self.export_weekly_report_pdf)
        export_layout.addWidget(export_report_pdf_button)

        # Spacer
        export_layout.addStretch()

    def add_member_row(self, layout, row_number, name='', position=''):
        row_entries = []
        name_entry = QLineEdit()
        name_entry.setPlaceholderText("Enter name")
        name_entry.setText(name)
        layout.addWidget(name_entry, row_number, 0)
        row_entries.append(name_entry)

        position_entry = QLineEdit()
        position_entry.setPlaceholderText("Enter position")
        position_entry.setText(position)
        layout.addWidget(position_entry, row_number, 1)
        row_entries.append(position_entry)

        attending_as_combo = QComboBox()
        attending_as_combo.addItems(self.attending_as_options)
        attending_as_combo.setCurrentIndex(0)
        layout.addWidget(attending_as_combo, row_number, 2)
        row_entries.append(attending_as_combo)

        attendance_combo = QComboBox()
        attendance_combo.addItems(self.attendance_options)
        attendance_combo.setCurrentIndex(0)
        layout.addWidget(attendance_combo, row_number, 3)
        row_entries.append(attendance_combo)

        self.entries.append(row_entries)

    def save_data_attendance(self):
        self.saved_data = []
        new_preloaded_members = []
        for row in self.entries:
            name = row[0].text().strip()
            position = row[1].text().strip()
            attending_as = row[2].currentText()
            attendance = row[3].currentText()
            if name or position:
                if not name:
                    QMessageBox.warning(self, "Incomplete Data", "Member name cannot be empty.")
                    return
                self.saved_data.append([name, position, attending_as, attendance])
                new_preloaded_members.append({'name': name, 'position': position})
        # Save preloaded members
        self.preloaded_members = new_preloaded_members
        self.save_preloaded_members()
        QMessageBox.information(self, "Data Saved", "Attendance data saved successfully!")

    def export_to_csv(self):
        try:
            default_filename = f"Tech_Fee_Committee_Attendance_{datetime.now().strftime('%m-%d-%Y')}.csv"
            file_path, _ = QFileDialog.getSaveFileName(self, "Save CSV", default_filename, "CSV Files (*.csv)")

            if file_path:
                with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow([f"Tech Fee Committee Attendance Record ({self.date_edit_attendance.date().toString('MM/dd/yyyy')})"])
                    writer.writerow(["Member Name", "Position", "Virtual/In-Person", "Attendance"])

                    for row in self.entries:
                        member_name = row[0].text()
                        position = row[1].text()
                        virtual_in_person = row[2].currentText()
                        attendance = row[3].currentText()
                        writer.writerow([member_name, position, virtual_in_person, attendance])

                QMessageBox.information(self, "CSV Exported", f"Attendance data exported to {file_path}")
            else:
                QMessageBox.warning(self, "No File Selected", "Please choose a file path.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error exporting data: {e}")

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
                data = [["Member Name", "Position", "Virtual/In-Person", "Attendance"]]
                for row in self.entries:
                    member_name = row[0].text()
                    position = row[1].text()
                    virtual_in_person = row[2].currentText()
                    attendance = row[3].currentText()
                    data.append([member_name, position, virtual_in_person, attendance])

                # Table Style with Red Headers and Alternating Row Colors
                table = Table(data, colWidths=[2 * inch, 2 * inch, 1.5 * inch, 1.5 * inch])
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

                QMessageBox.information(self, "PDF Exported", f"Attendance data exported to {file_path}")
            else:
                QMessageBox.warning(self, "No File Selected", "Please choose a file path.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error exporting data: {e}")

    def export_weekly_report_pdf(self):
        try:
            default_filename = f"Tech_Fee_Committee_Weekly_Report_{datetime.now().strftime('%m-%d-%Y')}.pdf"
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Weekly Report PDF", default_filename, "PDF Files (*.pdf)")

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
                body_style = ParagraphStyle(
                    'BodyStyle',
                    parent=styles['Normal'],
                    fontName='Helvetica',
                    fontSize=12,
                    textColor=colors.black,
                    leading=15,
                    alignment=0,  # Left align
                    spaceAfter=12
                )

                # Title
                title = Paragraph("Tech Fee Committee Weekly Report", title_style)
                elements.append(title)

                # Date as Subtitle
                date_paragraph = Paragraph(f"Date: {self.date_edit_report.date().toString('MM/dd/yyyy')}", subtitle_style)
                elements.append(date_paragraph)

                # Weekly Report Content
                report_content = self.report_text.toPlainText().strip()
                if report_content:
                    # Split the report into paragraphs based on double newlines
                    paragraphs = report_content.split('\n\n')
                    for para in paragraphs:
                        # Replace single newlines with <br/> to preserve line breaks
                        formatted_para = para.replace('\n', '<br/>')
                        p = Paragraph(formatted_para, body_style)
                        elements.append(p)
                        elements.append(Spacer(1, 0.1 * inch))
                else:
                    p = Paragraph("No weekly report content provided.", body_style)
                    elements.append(p)
                    elements.append(Spacer(1, 0.1 * inch))

                # Build PDF with full-page watermark
                doc.build(elements, onFirstPage=self.add_watermark, onLaterPages=self.add_watermark)

                QMessageBox.information(self, "PDF Exported", f"Weekly report exported to {file_path}")
            else:
                QMessageBox.warning(self, "No File Selected", "Please choose a file path.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error exporting weekly report: {e}")

    def add_watermark(self, canvas_obj, doc):
        """Adds a full-page watermark using the sga.jpg image."""
        canvas_obj.saveState()
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
            except Exception as img_e:
                QMessageBox.warning(self, "Watermark Error", f"Failed to add watermark image: {img_e}")
        else:
            QMessageBox.warning(self, "Watermark Image Not Found", f"Watermark image not found at {watermark_path}.")
        canvas_obj.restoreState()

    def add_member(self):
        # Add a new member row at the end
        row_number = len(self.entries) + 1
        grid_layout = self.find_child_layout_attendance()
        if grid_layout:
            self.add_member_row(grid_layout, row_number)
            self.on_frame_configure()
            QMessageBox.information(self, "Member Added", f"Added a new member row ({row_number}).")
        else:
            QMessageBox.warning(self, "Error", "Unable to add member row.")

    def delete_member(self):
        if self.entries:
            row_entries = self.entries.pop()
            for widget in row_entries:
                widget.deleteLater()
            self.on_frame_configure()
            QMessageBox.information(self, "Member Deleted", "Last member row has been deleted.")
        else:
            QMessageBox.warning(self, "No Members", "There are no members to delete.")

    def find_child_layout_attendance(self):
        """Finds the grid layout inside the attendance tab."""
        for child in self.attendance_tab.findChildren(QGridLayout):
            return child
        return None

    def on_frame_configure(self, event=None):
        """Reset the scroll region to encompass the inner frame"""
        # In PyQt6, QScrollArea automatically handles the scroll region
        pass

# Initialize the application
def main():
    app = QApplication(sys.argv)
    window = AttendanceApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
