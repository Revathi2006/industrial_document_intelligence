from PIL import Image, ImageDraw, ImageFont
import os

# Create inspection report image
img = Image.new('RGB', (800, 600), color='white')
draw = ImageDraw.Draw(img)

y = 30
lines = [
    ('MAINTENANCE INSPECTION REPORT', 24),
    ('', 16),
    ('Equipment: Centrifugal Pump Model XP-500', 18),
    ('Serial Number: CP-500-2024-001', 18),
    ('Department: Mechanical Maintenance', 18),
    ('Inspector: John Smith', 18),
    ('Date: 15-January-2024', 18),
    ('', 16),
    ('INSPECTION FINDINGS:', 20),
    ('', 16),
    ('1. Pressure Gauge Reading: 6.5 bar (Normal: 5-7 bar)', 16),
    ('2. Bearing Temperature: 45C (Normal: less than 60C)', 16),
    ('3. Oil Level: OK', 16),
    ('4. Vibration Level: 2.1 mm/s (Normal: less than 4.5 mm/s)', 16),
    ('5. Belt Tension: 12mm deflection (Normal: 10-15mm)', 16),
    ('', 16),
    ('ISSUES FOUND:', 20),
    ('', 16),
    ('- Minor oil leak at seal (Replace seal within 2 weeks)', 14),
    ('- Air filter needs cleaning', 14),
    ('', 16),
    ('OVERALL STATUS: PASS WITH RECOMMENDATIONS', 18),
    ('', 16),
    ('Next Scheduled Inspection: 15-February-2024', 16),
]

try:
    font_large = ImageFont.truetype('arial.ttf', 24)
    font_medium = ImageFont.truetype('arial.ttf', 18)
    font_small = ImageFont.truetype('arial.ttf', 14)
except:
    font_large = ImageFont.load_default()
    font_medium = ImageFont.load_default()
    font_small = ImageFont.load_default()

for line, size in lines:
    if size == 24:
        font = font_large
    elif size >= 18:
        font = font_medium
    else:
        font = font_small
    
    if size == 24:
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x = (800 - text_width) / 2
    else:
        x = 50
    
    draw.text((x, y), line, fill='black', font=font)
    y += size + 10

draw.rectangle([10, 10, 790, 590], outline='gray', width=2)
img.save('test_ocr_inspection.png')
print('Created: test_ocr_inspection.png')
print('Size:', os.path.getsize('test_ocr_inspection.png'), 'bytes')
