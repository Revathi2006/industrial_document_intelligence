from PIL import Image, ImageDraw, ImageFont

img = Image.new('RGB', (600, 400), color='#f5f5f0')
draw = ImageDraw.Draw(img)

draw.rectangle([20, 20, 580, 380], outline='#888', width=3)
draw.rectangle([25, 25, 575, 375], outline='#aaa', width=1)

lines = [
    ('MOTOR NAMEPLATE', 22),
    ('', 12),
    ('Manufacturer: Siemens', 18),
    ('Model: 1LE1503-1CB23-4AA4', 18),
    ('Power: 15 kW (20 HP)', 18),
    ('Speed: 1460 RPM', 18),
    ('Voltage: 415V +/- 10%', 18),
    ('Current: 28.5 A', 18),
    ('Frequency: 50 Hz', 18),
    ('Protection: IP55', 18),
    ('Insulation Class: F', 18),
    ('', 12),
    ('Serial No: S-2024-784512', 16),
    ('Year: 2024', 16),
]

y = 35
for line, size in lines:
    try:
        font = ImageFont.truetype('arial.ttf', size)
    except:
        font = ImageFont.load_default()
    
    if size == 22:
        bbox = draw.textbbox((0, 0), line, font=font)
        x = (600 - (bbox[2] - bbox[0])) / 2
    else:
        x = 50
    
    draw.text((x, y), line, fill='#1a1a1a', font=font)
    y += size + 8

img.save('test_nameplate.png')
print('Created: test_nameplate.png')
