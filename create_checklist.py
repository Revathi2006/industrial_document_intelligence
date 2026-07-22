from PIL import Image, ImageDraw, ImageFont

img = Image.new('RGB', (700, 500), color='white')
draw = ImageDraw.Draw(img)

draw.rectangle([20, 20, 680, 80], fill='#e0e0e0')
font = ImageFont.load_default()
draw.text((30, 35), 'DAILY INSPECTION CHECKLIST', fill='black', font=font)

y_positions = [100, 140, 180, 220, 260, 300, 340, 380]
items = [
    'Pressure Gauge Check',
    'Oil Level Check', 
    'Temperature Reading',
    'Vibration Check',
    'Belt Tension',
    'Leak Inspection',
    'Cleanliness',
    'Safety Guards'
]

for y, item in zip(y_positions, items):
    draw.rectangle([30, y, 670, y+35], outline='#ccc')
    draw.text((40, y+8), f'{y_positions.index(y)+1}. {item}', fill='black', font=font)
    draw.text((400, y+8), 'OK / Issue', fill='#666', font=font)

draw.text((30, 420), 'Inspector Name: _______________', fill='black', font=font)
draw.text((400, 420), 'Date: ____/____/2024', fill='black', font=font)
draw.text((30, 450), 'Remarks: ________________________________________', fill='black', font=font)

img.save('test_checklist.png')
print('Created: test_checklist.png')
