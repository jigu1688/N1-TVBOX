import math, random, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1920, 1080

print("[*] Rendering Grand Panoramic Cinematic Shutdown Background...")
img = Image.new('RGB', (W, H), (0, 0, 0))

# 1. Full-bleed Panoramic Atmospheric Sky (Edge-to-edge smooth gradient, no circle puddle!)
# We use a mathematical 2D function for smooth, vast cosmic wash
sky = Image.new('RGB', (W, H), (0, 0, 0))
s_draw = ImageDraw.Draw(sky)

# Vertical panoramic wash: peak around y=440
for y in range(H):
    # Vertical curve
    y_dist = abs(y - 440) / 460.0
    v_factor = max(0.0, math.cos(min(1.0, y_dist) * (math.pi / 2.0))) ** 1.3
    
    # Horizontal curve: broad, gentle falloff at edges
    # We draw line segments across x to calculate 2D atmospheric falloff
    r_val = int(8 * v_factor)
    g_val = int(28 * v_factor)
    b_val = int(75 * v_factor)
    s_draw.line([(0, y), (W, y)], fill=(r_val, g_val, b_val))

# Add horizontal wide-angle ambient band (stretching from x=0 to x=1920)
for i in range(0, W, 4):
    x_dist = abs(i - W//2) / float(W // 2)
    x_factor = max(0.0, math.cos(x_dist * (math.pi / 2.0))) ** 0.8
    for y in range(150, 750, 10):
        y_dist = abs(y - 450) / 300.0
        y_factor = max(0.0, math.cos(min(1.0, y_dist) * (math.pi / 2.0)))
        total = x_factor * y_factor
        if total > 0.02:
            r = int(14 * total)
            g = int(48 * total)
            b = int(110 * total)
            cur = sky.getpixel((i, y))
            sky.putpixel((i, y), (min(255, cur[0] + r), min(255, cur[1] + g), min(255, cur[2] + b)))

# Super smooth 60px Gaussian blur for zero banding on TV screens
sky = sky.filter(ImageFilter.GaussianBlur(55))
img = Image.blend(img, sky, 0.95)

# 2. Add subtle cosmic stardust / micro-particles for deep-space vastness
random.seed(42)
dust_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
d_draw = ImageDraw.Draw(dust_layer)
for _ in range(160):
    sx = random.randint(40, W - 40)
    sy = random.randint(40, 750)
    # Brightness higher in middle
    dist_center = math.hypot(sx - W//2, sy - 440)
    if dist_center < 700:
        sz = random.choice([1, 1, 2])
        alpha = random.randint(40, 160)
        c = random.choice([(147, 197, 253, alpha), (186, 230, 253, alpha), (241, 245, 249, alpha)])
        d_draw.ellipse([sx, sy, sx + sz, sy + sz], fill=c)

img.paste(dust_layer, (0, 0), dust_layer)
draw = ImageDraw.Draw(img)

# Fonts
font_title = ImageFont.truetype(r'C:\Windows\Fonts\msyhbd.ttc', 38)
font_eng = ImageFont.truetype(r'C:\Windows\Fonts\arialbd.ttf', 20)
font_tip = ImageFont.truetype(r'C:\Windows\Fonts\msyh.ttc', 22)
font_sub = ImageFont.truetype(r'C:\Windows\Fonts\msyh.ttc', 22)
font_sub_bold = ImageFont.truetype(r'C:\Windows\Fonts\msyhbd.ttc', 22)

# 3. Majestic Anamorphic Horizon Laser Beam (Full 1700px width, matching boot screen language!)
beam_y = 471
beam_img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
bm_draw = ImageDraw.Draw(beam_img)

beam_w = 850
for i in range(-beam_w, beam_w):
    factor = 1.0 - abs(i) / float(beam_w)
    factor = (math.cos((1.0 - factor) * math.pi) + 1.0) / 2.0
    r = int(25 * (1 - factor) + 56 * factor)
    g = int(85 * (1 - factor) + 210 * factor)
    b = int(235 * (1 - factor) + 255 * factor)
    a = int(255 * (factor ** 1.3))
    bm_draw.line([(W // 2 + i, beam_y), (W // 2 + i, beam_y)], fill=(r, g, b, a), width=3)

# Multi-stage anamorphic glow
beam_glow_wide = beam_img.filter(ImageFilter.GaussianBlur(28))
beam_glow_mid = beam_img.filter(ImageFilter.GaussianBlur(8))
img.paste(beam_glow_wide, (0, 0), beam_glow_wide)
img.paste(beam_glow_mid, (0, 0), beam_glow_mid)
img.paste(beam_img, (0, 0), beam_img)

# 4. Refined Floating Glass Dock (Wider 880px, framing the 3 buttons gracefully)
dock_w = 880
dock_h = 224
dock_x = (W - dock_w) // 2
dock_y = 359
dock_r = 38

glass_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
g_draw = ImageDraw.Draw(glass_layer)

# Translucent tinted dark glass
g_draw.rounded_rectangle([dock_x, dock_y, dock_x + dock_w, dock_y + dock_h], radius=dock_r, fill=(8, 16, 28, 195), outline=(56, 189, 248, 110), width=1)
# Top rim specular highlight
g_draw.line([(dock_x + dock_r, dock_y), (dock_x + dock_w - dock_r, dock_y)], fill=(255, 255, 255, 130), width=1)

img.paste(glass_layer, (0, 0), glass_layer)

# 5. Top Power Emblem (y=160~260)
power_cx, power_cy = W // 2, 195
pr = 34

p_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
p_draw = ImageDraw.Draw(p_layer)

for gr in range(48, 28, -2):
    ga = int(70 * (1.0 - (gr - 28) / 20.0))
    p_draw.ellipse([power_cx - gr, power_cy - gr, power_cx + gr, power_cy + gr], outline=(56, 189, 248, ga), width=2)

p_draw.arc([power_cx - pr, power_cy - pr, power_cx + pr, power_cy + pr], start=125, end=415, fill=(56, 189, 248, 240), width=5)
p_draw.line([(power_cx, power_cy - pr - 6), (power_cx, power_cy - 4)], fill=(56, 189, 248, 255), width=5)

p_glow = p_layer.filter(ImageFilter.GaussianBlur(10))
img.paste(p_glow, (0, 0), p_glow)
img.paste(p_layer, (0, 0), p_layer)

# Title: 电源选项 / POWER OPTIONS
t1 = '电源选项'
t2 = 'POWER OPTIONS'
bbox1 = draw.textbbox((0, 0), t1, font=font_title)
tw1 = bbox1[2] - bbox1[0]
draw.text(((W - tw1) // 2, 260), t1, font=font_title, fill=(248, 250, 252))

bbox2 = draw.textbbox((0, 0), t2, font=font_eng)
tw2 = bbox2[2] - bbox2[0]
draw.text(((W - tw2) // 2, 312), t2, font=font_eng, fill=(56, 189, 248))

# 6. Clean Interactive Hint (y=635)
hint_text = '按遥控器方向键选择   •   按 OK 键确认   •   倒计时结束将自动睡眠'
bbox_h = draw.textbbox((0, 0), hint_text, font=font_tip)
hw = bbox_h[2] - bbox_h[0]
draw.text(((W - hw) // 2, 638), hint_text, font=font_tip, fill=(148, 163, 184))

# 7. Bottom developer & brand signature (y=960)
part1 = 'PHICOMM N1   •   NEXTGEN TV OS   •   '
part_author = '恩山无线论坛 @jigu'

w1 = draw.textbbox((0, 0), part1, font=font_sub)[2] - draw.textbbox((0, 0), part1, font=font_sub)[0]
wa = draw.textbbox((0, 0), part_author, font=font_sub_bold)[2] - draw.textbbox((0, 0), part_author, font=font_sub_bold)[0]
total_fw = w1 + wa
fx = (W - total_fw) // 2
fy = 960

draw.text((fx, fy), part1, font=font_sub, fill=(100, 116, 139))
draw.text((fx + w1, fy), part_author, font=font_sub_bold, fill=(56, 189, 248))

# Save outputs
out_png = r'C:\Users\jigu\.gemini\antigravity-ide\brain\3a664381-8939-4916-9404-683857cb0b2a\shutdown_bg_grand_panoramic.jpg'
out_target = r'tools\re_tools\tvsettings_decompiled\res\drawable-hdpi-v4\shutdown_bg.jpg'
img.save(out_png, quality=96)
img.save(out_target, quality=96)
print(f"[+] Successfully generated grand background: {out_png}")
print(f"[+] Replaced target in tvsettings_decompiled: {out_target}")
