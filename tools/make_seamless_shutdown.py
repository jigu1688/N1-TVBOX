import os, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1920, 1080
print("[*] Generating Seamless High-Integration Shutdown Background & Assets...")

# =========================================================================
# 1. GENERATE SEAMLESS BORDERLESS SHUTDOWN_BG.JPG
# =========================================================================
y_coords, x_coords = np.mgrid[0:H, 0:W].astype(np.float32)

# --- Base Velvet Deep-Space Background (Edge-to-Edge Panoramic) ---
# Vertical master curve (smooth peak around y=480)
v_norm = (y_coords - 480.0) / 440.0
v_factor = np.exp(-0.5 * (v_norm ** 2))

# Wide horizontal sweep: gentle falloff towards the extreme bezel edges
h_norm = np.abs(x_coords - W / 2.0) / (W / 2.0)
h_spread = 1.0 - 0.22 * (h_norm ** 2.2)

ambient = v_factor * h_spread

r_base = 2.0 + 8.0 * ambient
g_base = 5.0 + 22.0 * ambient
b_base = 10.0 + 54.0 * ambient

# --- Celestial Dome Light (Top ambiance) ---
dome_d = np.sqrt(((x_coords - W / 2.0) / 1.6) ** 2 + ((y_coords - 80.0) / 0.8) ** 2)
dome_glow = np.exp(-0.5 * (dome_d / 440.0) ** 2)

r_base += 5.0 * dome_glow
g_base += 16.0 * dome_glow
b_base += 38.0 * dome_glow

# --- Fluid Widescreen Aurora Curtains across 1920px ---
wave1 = np.sin((x_coords / 320.0) + 0.4) * 45.0
y_wave1 = np.abs(y_coords - (460.0 + wave1))
glow_wave1 = np.exp(-0.5 * (y_wave1 / 95.0) ** 2) * (1.0 - 0.2 * (h_norm ** 2.0))

wave2 = np.cos((x_coords / 400.0) - 0.8) * 35.0
y_wave2 = np.abs(y_coords - (500.0 + wave2))
glow_wave2 = np.exp(-0.5 * (y_wave2 / 120.0) ** 2) * (1.0 - 0.25 * (h_norm ** 2.0))

r_base += 4.0 * glow_wave1 + 7.0 * glow_wave2
g_base += 20.0 * glow_wave1 + 18.0 * glow_wave2
b_base += 52.0 * glow_wave1 + 46.0 * glow_wave2

# --- Feather-Soft Organic Ambient Light (Behind buttons, ZERO hard edges!) ---
# Centers around (960, 471) with wide horizontal dispersion (sigma_x=380, sigma_y=110)
btn_x_dist = np.abs(x_coords - W / 2.0) / 380.0
btn_y_dist = np.abs(y_coords - 471.0) / 105.0
btn_ambient = np.exp(-0.5 * (btn_x_dist ** 2 + btn_y_dist ** 2))

r_base += 6.0 * btn_ambient
g_base += 28.0 * btn_ambient
b_base += 68.0 * btn_ambient

# --- Anamorphic Horizon Laser Wings (Positioned below buttons at y=566) ---
# Buttons span y=396 to y=546. Placing horizon line at y=566 anchors the buttons
# like planets floating above a horizon line, completely free of obstructions!
laser_y = np.abs(y_coords - 566.0)
laser_x = np.abs(x_coords - W / 2.0)

laser_mask = np.maximum(0.0, 1.0 - (laser_x / 880.0) ** 1.8)
laser_core = np.exp(-0.5 * (laser_y / 2.2) ** 2) * laser_mask
laser_bloom_mid = np.exp(-0.5 * (laser_y / 12.0) ** 2) * laser_mask
laser_bloom_wide = np.exp(-0.5 * (laser_y / 48.0) ** 2) * (1.0 - 0.3 * (h_norm ** 2))

r_base += 14.0 * laser_core + 8.0 * laser_bloom_mid + 3.0 * laser_bloom_wide
g_base += 115.0 * laser_core + 42.0 * laser_bloom_mid + 16.0 * laser_bloom_wide
b_base += 225.0 * laser_core + 110.0 * laser_bloom_mid + 45.0 * laser_bloom_wide

# --- Dithering (Anti-Banding) ---
np.random.seed(2026)
dither = (np.random.rand(H, W) - 0.5) * 1.3
r_final = np.clip(r_base + dither, 0, 255).astype(np.uint8)
g_final = np.clip(g_base + dither, 0, 255).astype(np.uint8)
b_final = np.clip(b_base + dither, 0, 255).astype(np.uint8)

img_rgb = np.stack([r_final, g_final, b_final], axis=2)
base = Image.fromarray(img_rgb, 'RGB')

# --- Micro-Stars for Infinite Spatial Scale ---
dust_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
d_draw = ImageDraw.Draw(dust_layer)
random.seed(888)
for _ in range(120):
    sx = random.randint(40, W - 40)
    sy = random.randint(30, 800)
    alpha = random.randint(20, 85)
    sz = 1 if random.random() < 0.85 else 2
    c = (200, 230, 255, alpha)
    d_draw.ellipse([sx, sy, sx + sz, sy + sz], fill=c)

base.paste(dust_layer, (0, 0), dust_layer)

# --- Elegant Minimalist Horizon Shelf (y=566, anchors the 3 buttons) ---
shelf_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
sh_draw = ImageDraw.Draw(shelf_layer)

shelf_w = 480
for x in range(-shelf_w, shelf_w):
    f = 1.0 - abs(x) / float(shelf_w)
    f = (math.cos((1.0 - f) * math.pi) + 1.0) / 2.0
    alpha = int(105 * (f ** 1.6))
    sh_draw.point((W // 2 + x, 566), fill=(56, 189, 248, alpha))
    alpha_soft = int(45 * (f ** 2.0))
    sh_draw.point((W // 2 + x, 567), fill=(56, 189, 248, alpha_soft))

# Micro-anchor indicators below each button center (x=717, 957, 1197)
for bx in [717, 957, 1197]:
    sh_draw.ellipse([bx - 3, 564, bx + 3, 568], fill=(56, 189, 248, 160))

base.paste(shelf_layer, (0, 0), shelf_layer)

# --- Top Power Emblem ---
power_cx, power_cy = W // 2, 192
pr = 34

p_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
p_draw = ImageDraw.Draw(p_layer)

for gr in range(46, 28, -2):
    ga = int(85 * (1.0 - (gr - 28) / 18.0))
    p_draw.ellipse([power_cx - gr, power_cy - gr, power_cx + gr, power_cy + gr], outline=(56, 189, 248, ga), width=2)

p_draw.arc([power_cx - pr, power_cy - pr, power_cx + pr, power_cy + pr], start=125, end=415, fill=(56, 189, 248, 250), width=5)
p_draw.line([(power_cx, power_cy - pr - 6), (power_cx, power_cy - 4)], fill=(56, 189, 248, 255), width=5)

p_glow = p_layer.filter(ImageFilter.GaussianBlur(10))
base.paste(p_glow, (0, 0), p_glow)
base.paste(p_layer, (0, 0), p_layer)

# --- Typography ---
draw = ImageDraw.Draw(base)
font_title = ImageFont.truetype(r'C:\Windows\Fonts\msyhbd.ttc', 38)
font_eng = ImageFont.truetype(r'C:\Windows\Fonts\arialbd.ttf', 18)
font_tip = ImageFont.truetype(r'C:\Windows\Fonts\msyh.ttc', 21)
font_sub = ImageFont.truetype(r'C:\Windows\Fonts\msyh.ttc', 21)
font_sub_bold = ImageFont.truetype(r'C:\Windows\Fonts\msyhbd.ttc', 21)

t1 = "电  源  选  项"
t2 = "S Y S T E M   P O W E R   C O N T R O L"

bb1 = draw.textbbox((0, 0), t1, font=font_title)
tw1 = bb1[2] - bb1[0]
draw.text(((W - tw1) // 2, 252), t1, font=font_title, fill=(248, 250, 252))

bb2 = draw.textbbox((0, 0), t2, font=font_eng)
tw2 = bb2[2] - bb2[0]
draw.text(((W - tw2) // 2, 305), t2, font=font_eng, fill=(56, 189, 248))

# Interactive Hint (y=642)
hint_text = "按遥控器方向键选择   •   按 OK 键确认   •   倒计时结束将自动睡眠"
bb_h = draw.textbbox((0, 0), hint_text, font=font_tip)
hw = bb_h[2] - bb_h[0]
draw.text(((W - hw) // 2, 642), hint_text, font=font_tip, fill=(148, 163, 184))

# Footer (y=960)
part1 = "PHICOMM N1   •   NEXTGEN TV OS   •   "
part_author = "恩山无线论坛 @jigu"

w1 = draw.textbbox((0, 0), part1, font=font_sub)[2] - draw.textbbox((0, 0), part1, font=font_sub)[0]
wa = draw.textbbox((0, 0), part_author, font=font_sub_bold)[2] - draw.textbbox((0, 0), part_author, font=font_sub_bold)[0]
total_fw = w1 + wa
fx = (W - total_fw) // 2
fy = 960

draw.text((fx, fy), part1, font=font_sub, fill=(100, 116, 139))
draw.text((fx + w1, fy), part_author, font=font_sub_bold, fill=(56, 189, 248))

# Save shutdown_bg.jpg
bg_target = r'tools\re_tools\tvsettings_decompiled\res\drawable-hdpi-v4\shutdown_bg.jpg'
base.save(bg_target, quality=96)
print(f"[+] Saved seamless shutdown_bg: {bg_target}")

# =========================================================================
# 2. UPGRADE BUTTON ASSETS (SELECT_NOT_BG & SELECTED_BG) FOR ULTIMATE INTEGRATION
# =========================================================================
# select_not_bg.png: 150x150, unfocused button
# Replace dull gray solid disc with a sleek, translucent dark-glass disc with subtle cyan border
btn_not = Image.new('RGBA', (150, 150), (0, 0, 0, 0))
bn_draw = ImageDraw.Draw(btn_not)
# Translucent tinted dark disc
bn_draw.ellipse([4, 4, 146, 146], fill=(15, 23, 42, 175), outline=(56, 189, 248, 65), width=2)
# Top subtle highlight shimmer
bn_draw.arc([10, 10, 140, 140], start=210, end=330, fill=(255, 255, 255, 90), width=2)
btn_not.save(r'tools\re_tools\tvsettings_decompiled\res\drawable-hdpi-v4\select_not_bg.png')
print("[+] Upgraded select_not_bg.png (sleek translucent glass)")

# selected_bg.png: 152x152, focused button
# Glowing electric cyan ring
btn_sel = Image.new('RGBA', (152, 152), (0, 0, 0, 0))
bs_draw = ImageDraw.Draw(btn_sel)
# Soft glow
for gr, ga in [(12, 35), (8, 65), (4, 120)]:
    bs_draw.ellipse([gr, gr, 152 - gr, 152 - gr], outline=(56, 189, 248, ga), width=2)
# Crisp bright ring
bs_draw.ellipse([14, 14, 138, 138], fill=(14, 116, 144, 185), outline=(56, 189, 248, 255), width=3)
# Inner highlight
bs_draw.arc([20, 20, 132, 132], start=200, end=340, fill=(255, 255, 255, 180), width=2)
btn_sel.save(r'tools\re_tools\tvsettings_decompiled\res\drawable-hdpi-v4\selected_bg.png')
print("[+] Upgraded selected_bg.png (electric cyan glowing focus ring)")

print("[+] All assets updated successfully!")
