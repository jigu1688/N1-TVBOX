import os, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1920, 1080
print("[*] Generating Ultra-Grand Widescreen Cinematic Shutdown Background...")

# Coordinate grids
y_coords, x_coords = np.mgrid[0:H, 0:W].astype(np.float32)

# --- 1. Base Panoramic Sky (Rich, expansive deep-space sapphire to obsidian) ---
# Vertical base gradient
# y=0..300: Deep midnight blue
# y=300..600: Rich celestial cobalt horizon
# y=600..1080: Deep abyss black
v_curve = np.zeros((H, W), dtype=np.float32)
# Top wash
top_mask = y_coords < 470
v_curve[top_mask] = 0.35 + 0.65 * (y_coords[top_mask] / 470.0) ** 1.3
# Bottom wash
bot_mask = y_coords >= 470
v_curve[bot_mask] = np.maximum(0.0, 1.0 - ((y_coords[bot_mask] - 470.0) / 520.0) ** 1.4)

# Wide horizontal sweep: gentle falloff towards the extreme bezel edges
h_falloff = 1.0 - 0.25 * ((np.abs(x_coords - W / 2.0) / (W / 2.0)) ** 2.5)

# Full panoramic atmospheric radiance
radiance = v_curve * h_falloff

# Color mapping: deep indigo (10, 22, 45) -> radiant cobalt (25, 65, 135)
r_chan = 4.0 + 22.0 * radiance
g_chan = 10.0 + 58.0 * radiance
b_chan = 22.0 + 130.0 * radiance

# --- 2. Expansive Horizon Light Curtain (Spanning across x=0..1920) ---
# A soft, broad vertical Gaussian around y=471
horizon_y_dist = np.abs(y_coords - 471.0)
horizon_band = np.exp(-0.5 * (horizon_y_dist / 140.0) ** 2) * (1.0 - 0.35 * ((np.abs(x_coords - W / 2.0) / (W / 2.0)) ** 2.2))

r_chan += 14.0 * horizon_band
g_chan += 48.0 * horizon_band
b_chan += 110.0 * horizon_band

# --- 3. Anamorphic Horizontal Laser Flare (1700px width) ---
# Very tight vertical Gaussian (sigma=8) with wide horizontal stretch (sigma=600)
laser_y_dist = np.abs(y_coords - 471.0)
laser_x_dist = np.abs(x_coords - W / 2.0)
laser_core = np.exp(-0.5 * (laser_y_dist / 3.5) ** 2) * np.maximum(0.0, 1.0 - (laser_x_dist / 860.0) ** 1.6)
laser_glow = np.exp(-0.5 * (laser_y_dist / 22.0) ** 2) * np.maximum(0.0, 1.0 - (laser_x_dist / 780.0) ** 1.4)

r_chan += 60.0 * laser_core + 20.0 * laser_glow
g_chan += 200.0 * laser_core + 75.0 * laser_glow
b_chan += 255.0 * laser_core + 180.0 * laser_glow

# --- 4. Upper Atmospheric Dome Glow (Soft ambient light from top-center) ---
dome_dist = np.sqrt(((x_coords - W / 2.0) / 1.4) ** 2 + ((y_coords - 100.0) / 0.9) ** 2)
dome_glow = np.exp(-0.5 * (dome_dist / 380.0) ** 2)
r_chan += 15.0 * dome_glow
g_chan += 42.0 * dome_glow
b_chan += 95.0 * dome_glow

# --- 5. Add subtle dithering to eliminate 8-bit banding on TV panels ---
np.random.seed(1337)
dither = (np.random.rand(H, W) - 0.5) * 1.2
r_chan = np.clip(r_chan + dither, 0, 255).astype(np.uint8)
g_chan = np.clip(g_chan + dither, 0, 255).astype(np.uint8)
b_chan = np.clip(b_chan + dither, 0, 255).astype(np.uint8)

img_rgb = np.stack([r_chan, g_chan, b_chan], axis=2)
base = Image.fromarray(img_rgb, 'RGB')

# --- 6. Architectural HUD & Geometric Accents ---
hud_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
h_draw = ImageDraw.Draw(hud_layer)

# Thin horizon hairline
for x in range(120, W - 120):
    fade = 1.0 - abs(x - W / 2.0) / float(W / 2.0 - 120)
    fade = max(0.0, fade) ** 1.5
    h_draw.point((x, 471), fill=(56, 189, 248, int(110 * fade)))

# Faint upper and lower guide lines
for gy in [342, 600]:
    for x in range(260, W - 260):
        fade = 1.0 - abs(x - W / 2.0) / float(W / 2.0 - 260)
        fade = max(0.0, fade) ** 2
        h_draw.point((x, gy), fill=(56, 189, 248, int(45 * fade)))

# Horizon tick marks
for tx in range(240, W - 240, 160):
    fade = 1.0 - abs(tx - W / 2.0) / float(W / 2.0 - 240)
    if fade > 0.1:
        h_draw.line([(tx, 467), (tx, 475)], fill=(56, 189, 248, int(120 * fade)), width=1)

base.paste(hud_layer, (0, 0), hud_layer)

# --- 7. Grand Floating Cockpit (950px width, sleek frosted glass) ---
dock_w = 950
dock_h = 236
dock_x = (W - dock_w) // 2
dock_y = 353
dock_r = 38

dock_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
d_draw = ImageDraw.Draw(dock_layer)

# Ambient soft glow behind dock
for expand, alpha in [(18, 25), (10, 45), (4, 80)]:
    d_draw.rounded_rectangle(
        [dock_x - expand, dock_y - expand, dock_x + dock_w + expand, dock_y + dock_h + expand],
        radius=dock_r + expand,
        outline=(56, 189, 248, alpha),
        width=1
    )

# Translucent tinted frosted dark glass fill
d_draw.rounded_rectangle(
    [dock_x, dock_y, dock_x + dock_w, dock_y + dock_h],
    radius=dock_r,
    fill=(8, 18, 34, 185),
    outline=(56, 189, 248, 140),
    width=1
)

# Top edge specular reflection
d_draw.line([(dock_x + dock_r, dock_y), (dock_x + dock_w - dock_r, dock_y)], fill=(255, 255, 255, 175), width=1)

# Precision HUD corner bracket accents on the dock
c_len = 18
c_col = (56, 189, 248, 230)
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

# --- 8. Glowing Power Emblem ---
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

# --- 9. Typography ---
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
out_png = r'C:\Users\jigu\.gemini\antigravity-ide\brain\3a664381-8939-4916-9404-683857cb0b2a\shutdown_bg_ultra_grand.jpg'
out_target = r'tools\re_tools\tvsettings_decompiled\res\drawable-hdpi-v4\shutdown_bg.jpg'
base.save(out_png, quality=96)
base.save(out_target, quality=96)
print(f"[+] Output saved: {out_png}")
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

sim_out = r'C:\Users\jigu\.gemini\antigravity-ide\brain\3a664381-8939-4916-9404-683857cb0b2a\preview_shutdown_ultra_sim.jpg'
sim.save(sim_out, quality=95)
print(f"[+] Simulation preview saved: {sim_out}")
