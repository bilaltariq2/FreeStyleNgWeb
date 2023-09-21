#### Libraries and Import here
from reportlab.lib.pagesizes import landscape, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import PageBreak
import json
import time
import bleach
import textwrap


# Read JSON data from the text file
with open("scan.txt", "r", encoding="utf-8") as readScanTextFile:
    scannedData = readScanTextFile.read()

# Parse the JSON data
data = json.loads(scannedData)

# Define ReportLab styles
styles = getSampleStyleSheet()
attributes_style = ParagraphStyle(name='AttributesStyle', parent=styles['Normal'], spaceAfter=6)


# Generate a timestamp
timestamp = time.strftime("%Y%m%d%H%M%S")  # Format: YYYYMMDDHHMMSS

# Append the timestamp to the filename.You can also change the filename here.
pdf_filename = f"scan_report_{timestamp}.pdf"

# Create a PDF document with landscape orientation and appropriate margins
doc = SimpleDocTemplate(pdf_filename, pagesize=landscape(A4), leftMargin=30, rightMargin=30, topMargin=30, bottomMargin=30)
content = []


# Create a custom ParagraphStyle for the severity and image scan findings title with a different text color
title_style = ParagraphStyle(
    name='TitleStyle',
    parent=styles['Title'],
    textColor=colors.HexColor("#1ae5cd")  # Change the text color here
)

# Add title for Severity Count Information
severity_title = Paragraph("Severity Count Information", title_style)
content.append(severity_title)
content.append(Spacer(1, 12))

# Extract "findingSeverityCounts" data from JSON
severity_counts = data.get('imageScanFindings', {}).get('findingSeverityCounts', {})

# Create a table for severity counts with a "Total" column
severity_table_data = [['Critical', 'High', 'Medium', 'Low', 'Informational', 'Undefined', 'Total']]

# Populate the second row with severity counts or "N/A" if not available
severity_row = [
    severity_counts.get('CRITICAL', '0'),
    severity_counts.get('HIGH', '0'),
    severity_counts.get('MEDIUM', '0'),
    severity_counts.get('LOW', '0'),
    severity_counts.get('INFORMATIONAL', '0'),
    severity_counts.get('UNDEFINED', '0'),
    # Calculate the total count
    sum([int(severity_counts.get('CRITICAL', '0')),
         int(severity_counts.get('HIGH', '0')),
         int(severity_counts.get('MEDIUM', '0')),
         int(severity_counts.get('LOW', '0')),
         int(severity_counts.get('INFORMATIONAL', '0')),
         int(severity_counts.get('UNDEFINED', '0'))])
]

severity_table_data.append(severity_row)

# Create a table for severity counts
severity_table = Table(severity_table_data, colWidths=[111] * 7)
# Changes like changing the color, font alignment, and background color can be done in this section.
severity_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1ae5cd")),  # Change header background color
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#FFFFFF")),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#FFFFFF")),
    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#1ae5cd"))
]))

content.append(severity_table)
content.append(Spacer(1, 12))  # Add space between the severity count table and the image scan findings

# Add a title to the PDF for Image Scan Findings
title = Paragraph("Image Scan Findings", title_style)
content.append(title)
content.append(Spacer(1, 12))

# Extract and format findings
findings = data.get('imageScanFindings', {}).get('findings', [])

table_data = [['Name', 'Description', 'Severity', 'URI', 'Attributes']]

# Calculate the maximum width for each column
max_widths = [95, 230, 95, 160, 200]

for finding in findings:
    name = finding.get('name', 'N/A')
    description = finding.get('description', 'N/A')
    severity = finding.get('severity', 'N/A')
    uri = finding.get('uri', 'N/A')
    attributes = finding.get('attributes', [])

    # Clean and format the description
    description = bleach.clean(description, tags=[], strip=True)  # Remove HTML-like tags
    description = description.replace('<br/>', '\n')  # Replace HTML line breaks with newline characters

    # Clean and format the attributes
    attributes_str = '\n'.join([f"{attr['key']}: {attr['value']}" for attr in attributes])
    attributes_str = bleach.clean(attributes_str, tags=[], strip=True)  # Remove HTML-like tags

    # Wrap the content to limit the cell height
    max_cell_height = 594  # Adjust as needed
    description = '\n'.join(textwrap.wrap(description, width=40))  # Adjust width as needed
    attributes_str = '\n'.join(textwrap.wrap(attributes_str, width=40))  # Adjust width as needed

    # Reduce the font size for large cells
    if len(description) > 100:
        styles['Normal'].fontSize = 8  # Adjust font size as needed
    if len(attributes_str) > 100:
        styles['Normal'].fontSize = 8  # Adjust font size as needed

    table_data.append([Paragraph(name, styles['Normal']),
                       Paragraph(description, styles['Normal']),
                       Paragraph(severity, styles['Normal']),
                       Paragraph(uri, styles['Normal']),
                       Paragraph(attributes_str, attributes_style)])


# Create a table for findings with dynamic row heights
table = Table(table_data, colWidths=max_widths)
# Changes like changing the color, font alignment, and background color can be done in this section.
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1ae5cd")),  # Change header background color
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#FFFFFF")),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#FFFFFF")),
    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#1ae5cd"))
]))

content.append(table)

# Build the PDF document
doc.build(content)
