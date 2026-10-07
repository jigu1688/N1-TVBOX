import os, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1920, 1080
print("[*] Generating Masterpiece Cinematic Grand Shutdown Background...")

y_coords, x_coords = np.mgrid[0:H, 0:W].astype(np.float32)

# --- 1. Base Velvet Deep-Space Background (Midnight Obsidian & Deep Sapphire) ---
# Vertical master curve:
# Top: deep midnight navy (3, 7, 16)
# Upper-Mid: deep cosmic indigo (8, 18, 38)
# Horizon center (y=471): majestic deep oceanic sapphire (14, 34, 72)
# Lower-Mid: smooth fade (6, 14, 30)
# Bottom: pure deep obsidian (2, 4, 8)
v_norm = (y_coords - 471.0) / 400.0
v_factor = np.exp(-0.5 * (v_norm ** 2)) # peak at y=471

# Smooth edge-to-edge horizontal spread (fills the whole screen, no localized puddle)
h_norm = np.abs(x_coords - W / 2.0) / (W / 2.0)
h_spread = 1.0 - 0.28 * (h_norm ** 2.2)

# Full-bleed ambient wash
ambient = v_factor * h_spread

r_base = 2.0 + 10.0 * ambient
g_base = 5.0 + 26.0 * ambient
b_base = 10.0 + 58.0 * ambient

# --- 2. Top-Down Celestial Dome Light (Gives the upper screen grand breathing space) ---
dome_d = np.sqrt(((x_coords - W / 2.0) / 1.6) ** 2 + ((y_coords - 80.0) / 0.8) ** 2)
dome_glow = np.exp(-0.5 * (dome_d / 440.0) ** 2)

r_base += 6.0 * dome_glow
g_base += 18.0 * dome_glow
b_base += 42.0 * dome_glow

# --- 3. Widescreen Cinematic Aurora Waves (Edge-to-edge flow across 1920px) ---
# Wave 1: Gentle tilted cyan-blue aurora curtain
wave1 = np.sin((x_coords / 320.0) + 0.4) * 45.0
y_wave1 = np.abs(y_coords - (450.0 + wave1))
glow_wave1 = np.exp(-0.5 * (y_wave1 / 95.0) ** 2) * (1.0 - 0.2 * (h_norm ** 2.0))

# Wave 2: Complementary deeper blue horizon wave
wave2 = np.cos((x_coords / 400.0) - 0.8) * 35.0
y_wave2 = np.abs(y_coords - (490.0 + wave2))
glow_wave2 = np.exp(-0.5 * (y_wave2 / 120.0) ** 2) * (1.0 - 0.25 * (h_norm ** 2.0))

r_base += 4.0 * glow_wave1 + 8.0 * glow_wave2
g_base += 24.0 * glow_wave1 + 22.0 * glow_wave2
b_base += 58.0 * glow_wave1 + 52.0 * glow_wave2

# --- 4. Anamorphic Horizontal Horizon Beam (Full 1720px width laser) ---
laser_y = np.abs(y_coords - 471.0)
laser_x = np.abs(x_coords - W / 2.0)

# Ultra-wide razor laser core
laser_mask = np.maximum(0.0, 1.0 - (laser_x / 860.0) ** 1.8)
laser_core = np.exp(-0.5 * (laser_y / 2.8) ** 2) * laser_mask
laser_bloom_mid = np.exp(-0.5 * (laser_y / 14.0) ** 2) * laser_mask
laser_bloom_wide = np.exp(-0.5 * (laser_y / 48.0) ** 2) * (1.0 - 0.35 * (h_norm ** 2))

r_base += 45.0 * laser_core + 14.0 * laser_bloom_mid + 4.0 * laser_bloom_wide
g_base += 165.0 * laser_core + 55.0 * laser_bloom_mid + 18.0 * laser_bloom_wide
b_base += 235.0 * laser_core + 115.0 * laser_bloom_mid + 42.0 * laser_bloom_wide

# --- 5. Dithering (Zero Banding for TV Panels) ---
np.random.seed(2026)
dither = (np.random.rand(H, W) - 0.5) * 1.3
r_final = np.clip(r_base + dither, 0, 255).astype(np.uint8)
g_final = np.clip(g_base + dither, 0, 255).astype(np.uint8)
b_final = np.clip(b_base + dither, 0, 255).astype(np.uint8)

img_rgb = np.stack([r_final, g_final, b_final], axis=2)
base = Image.fromarray(img_rgb, 'RGB')

# --- 6. Deep Space Micro-Cosmos (Faint stars adding cosmic scale) ---
dust_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
d_draw = ImageDraw.Draw(dust_layer)
random.seed(888)
for _ in range(140):
    sx = random.randint(40, W - 40)
    sy = random.randint(30, 800)
    # Higher density in upper hemisphere
    dist_c = math.hypot(sx - W / 2.0, sy - 400)
    alpha = random.randint(25, 110)
    sz = 1 if random.random() < 0.85 else 2
    c = (200, 230, 255, alpha)
    d_draw.ellipse([sx, sy, sx + sz, sy + sz], fill=c)

base.paste(dust_layer, (0, 0), dust_layer)

# --- 7. Architectural Tech Horizon Hairline & Markers ---
hud_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
h_draw = ImageDraw.Draw(hud_layer)

# Horizon hairline across x=100 to 1820
for x in range(100, W - 100):
    f = 1.0 - abs(x - W / 2.0) / float(W / 2.0 - 100)
    f = max(0.0, f) ** 1.4
    a = int(95 * f)
    h_draw.point((x, 471), fill=(56, 189, 248, a))

# Upper and lower subtle architectural divider lines
for hy in [336, 606]:
    for x in range(220, W - 220):
        f = 1.0 - abs(x - W / 2.0) / float(W / 2.0 - 220)
        a = int(35 * (max(0.0, f) ** 2))
        h_draw.point((x, hy), fill=(56, 189, 248, a))

# Precision tick marks
for tx in range(200, W - 200, 140):
    f = 1.0 - abs(tx - W / 2.0) / float(W / 2.0 - 200)
    if f > 0.08:
        h_draw.line([(tx, 467), (tx, 475)], fill=(56, 189, 248, int(105 * f)), width=1)

base.paste(hud_layer, (0, 0), hud_layer)

# --- 8. Grand Floating Glass Dock (Wide 960px, Luxurious Smoked Glass) ---
dock_w = 960
dock_h = 236
dock_x = (W - dock_w) // 2
dock_y = 353
dock_r = 38

dock_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
d_draw = ImageDraw.Draw(dock_layer)

# Outer soft cyan atmospheric halo
for expand, alpha in [(20, 18), (10, 38), (4, 70)]:
    d_draw.rounded_rectangle(
        [dock_x - expand, dock_y - expand, dock_x + dock_w + expand, dock_y + dock_h + expand],
        radius=dock_r + expand,
        outline=(56, 189, 248, alpha),
        width=1
    )

# Translucent smoked glass fill (dark midnight glass with subtle cyan tint)
d_draw.rounded_rectangle(
    [dock_x, dock_y, dock_x + dock_w, dock_y + dock_h],
    radius=dock_r,
    fill=(6, 14, 26, 190),
    outline=(56, 189, 248, 130),
    width=1
)

# Top edge specular rim
d_draw.line([(dock_x + dock_r, dock_y), (dock_x + dock_w - dock_r, dock_y)], fill=(255, 255, 255, 170), width=1)

# Precision HUD corner bracket accents on the dock
c_len = 18
c_col = (56, 189, 248, 220)
# Top-Left
d_draw.line([(dock_x + 12, dock_y + 12), (dock_x + 12 + c_len, dock_y + 12)], fill=c_col, width=2)
d_draw.line([(dock_x + 12, dock_y + 12), (dock_x + 12, dock_y + 12 + c_len)], fill=c_col, width=2)
# Top-Right
d_draw.line([(dock_x + dock_w - 12 - c_len, dock_y + 12), (dock_x + dock_w - 12, dock_y + 12)], fill=c_col, width=2)
d_draw.line([(dock_x + dock_w - 12, dock_y + 12), (dock_x + dock_w - 12, dock_y + 12 + c_len)], fill=c_col, width=2)
# Bottom-Left
d_draw.line([(dock_x + 12, dock_y + dock_h - 12), (dock_x + 12 + c_len, dock_y + dock_h - 12)], fill=c_col, width=2)
d_draw.line([(dock_x + 12, dock_y + dock_h - 12 - c_len), (dock_x + 12, dock_y + dock_h - 12)], fill=c_col, width=2)
# Bottom-Right
d_draw.line([(dock_x + dock_w - 12 - c_len, dock_y + dock_h - 12), (dock_x + dock_w - 12, dock_y + dock_h - 12)], fill=c_col, width=2)
d_draw.line([(dock_x + dock_w - 12, dock_y + dock_h - 12 - c_len), (dock_x + dock_w - 12, dock_y + dock_h - 12)], fill=c_col, width=2)

base.paste(dock_layer, (0, 0), dock_layer)

# --- 9. Glowing Top Power Emblem ---
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

# --- 10. Typography ---
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

# Save outputs
out_png = r'C:\Users\jigu\.gemini\antigravity-ide\brain\3a664381-8939-4916-9404-683857cb0b2a\shutdown_bg_masterpiece.jpg'
out_target = r'tools\re_tools\tvsettings_decompiled\res\drawable-hdpi-v4\shutdown_bg.jpg'
base.save(out_png, quality=96)
base.save(out_target, quality=96)
print(f"[+] Masterpiece output saved: {out_png}")
print(f"[+] Target replaced: {out_target}")

# Simulation with real buttons
sim = base.copy()
s_draw = ImageDraw.Draw(sim)
for bx, label, is_focused in [(642, "关机", True), (882, "重启", False), (1122, "U盘启动", False)]:
    bg_col = (14, 116, 144, 230) if is_focused else (15, 23, 42, 210)
    border_col = (56, 189, 248, 255) if is_focused else (71, 85, 105, 180)
    s_draw.ellipse([bx, 396, bx + 150, 546], fill=bg_col, outline=border_col, width=3 if is_focused else 2)
    font_btn = ImageFont.truetype(r'C:\Windows\Fonts\msyhbd.ttc', 26)
    b_bb = s_draw.textbbox((0, 0), label, font=font_btn)
    bw = b_bb[2] - b_bb[0]
    bh = b_bb[3] - b_bb[1]
    s_draw.text((bx + (150 - bw)//2, 396 + (150 - bh)//2), label, font=font_btn, fill=(255, 255, 255) if is_focused else (203, 213, 225))

sim_out = r'C:\Users\jigu\.gemini\antigravity-ide\brain\3a664381-8939-4916-9404-683857cb0b2a\preview_shutdown_masterpiece_sim.jpg'
sim.save(sim_out, quality=95)
print(f"[+] Masterpiece simulation preview saved: {sim_out}")
