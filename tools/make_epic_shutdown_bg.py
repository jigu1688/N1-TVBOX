import math, random, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1920, 1080
print("[*] Generating Epic Widescreen Grand Shutdown Background...")

# Base image
base = Image.new('RGB', (W, H), (2, 5, 10))
draw = ImageDraw.Draw(base)

# 1. Full-screen Cinematic Sky & Deep Gradient (Edge-to-edge, NO oval puddle)
# We calculate a smooth full-bleed backdrop across all 1920x1080 pixels
sky = Image.new('RGB', (W, H), (0, 0, 0))
s_draw = ImageDraw.Draw(sky)

for y in range(H):
    # Vertical progression:
    # y=0: deep dark navy (8, 16, 32)
    # y=200~520: rich deep cobalt (16, 36, 75)
    # y=520~800: smooth descent (10, 22, 45)
    # y=800~1080: deep black (2, 4, 8)
    if y < 460:
        factor = (y / 460.0) ** 1.2
        r = int(6 + 12 * factor)
        g = int(14 + 26 * factor)
        b = int(28 + 52 * factor)
    else:
        factor = ((y - 460) / float(H - 460)) ** 1.5
        r = int(18 * (1.0 - factor) + 2 * factor)
        g = int(40 * (1.0 - factor) + 4 * factor)
        b = int(80 * (1.0 - factor) + 8 * factor)
    
    s_draw.line([(0, y), (W, y)], fill=(r, g, b))

# 2. Wide Horizontal Atmospheric Horizon (Sweeps across entire width x=0~1920)
horizon_layer = Image.new('RGB', (W, H), (0, 0, 0))
h_draw = ImageDraw.Draw(horizon_layer)

for y in range(160, 780):
    # Gaussian bell curve around y=440
    y_norm = abs(y - 440) / 280.0
    y_glow = max(0.0, math.exp(-3.2 * (y_norm ** 2)))
    
    for x in range(0, W, 4):
        # Broad horizontal spread from edge to edge with subtle cinema falloff at extreme sides
        x_norm = abs(x - W//2) / float(W//2)
        x_glow = max(0.0, 1.0 - 0.45 * (x_norm ** 2.2))
        
        lum = y_glow * x_glow
        if lum > 0.01:
            cr = int(16 * lum)
            cg = int(58 * lum)
            cb = int(135 * lum)
            cur = horizon_layer.getpixel((x, y))
            horizon_layer.putpixel((x, y), (min(255, cur[0] + cr), min(255, cur[1] + cg), min(255, cur[2] + cb)))

horizon_blur = horizon_layer.filter(ImageFilter.GaussianBlur(65))
sky = Image.blend(sky, horizon_blur, 0.85)

# 3. Subtle Technical Floor & Perspective Lines (Adds immense architectural depth)
grid_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
g_draw = ImageDraw.Draw(grid_layer)

# Horizon divider line at y=471 (the buttons' vertical center)
for x in range(60, W - 60):
    fade = 1.0 - abs(x - W//2) / float(W//2 - 60)
    fade = max(0.0, fade) ** 1.8
    alpha = int(90 * fade)
    g_draw.point((x, 471), fill=(56, 189, 248, alpha))

# Fine horizontal accent lines below and above
for hy in [335, 605]:
    for x in range(180, W - 180):
        fade = 1.0 - abs(x - W//2) / float(W//2 - 180)
        alpha = int(35 * (max(0.0, fade) ** 2))
        g_draw.point((x, hy), fill=(56, 189, 248, alpha))

# Combine background layers
base.paste(sky, (0, 0))
base.paste(grid_layer, (0, 0), grid_layer)

# 4. Anamorphic Cinematic Light Streaks (Horizontal cyan glow)
streak_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
st_draw = ImageDraw.Draw(streak_layer)

for hw in [780, 520, 260]:
    for x in range(-hw, hw):
        f = 1.0 - abs(x) / float(hw)
        f = (math.cos((1.0 - f) * math.pi) + 1.0) / 2.0
        a = int(60 * (f ** 1.5))
        st_draw.line([(W//2 + x, 471), (W//2 + x, 471)], fill=(56, 189, 248, a), width=2)

streak_blur = streak_layer.filter(ImageFilter.GaussianBlur(12))
streak_blur_wide = streak_layer.filter(ImageFilter.GaussianBlur(28))
base.paste(streak_blur_wide, (0, 0), streak_blur_wide)
base.paste(streak_blur, (0, 0), streak_blur)

# 5. Grand Floating Glass Dock (Wide 960px, perfectly balanced)
dock_w = 940
dock_h = 236
dock_x = (W - dock_w) // 2
dock_y = 353
dock_r = 36

dock_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
d_draw = ImageDraw.Draw(dock_layer)

# Outer soft ambient shadow/glow
for glow_expand, glow_alpha in [(16, 25), (8, 45), (4, 70)]:
    d_draw.rounded_rectangle(
        [dock_x - glow_expand, dock_y - glow_expand, dock_x + dock_w + glow_expand, dock_y + dock_h + glow_expand],
        radius=dock_r + glow_expand,
        outline=(56, 189, 248, glow_alpha),
        width=1
    )

# Translucent dark frosted glass fill (smooth glass gradient)
d_draw.rounded_rectangle(
    [dock_x, dock_y, dock_x + dock_w, dock_y + dock_h],
    radius=dock_r,
    fill=(10, 20, 36, 190),
    outline=(56, 189, 248, 120),
    width=1
)

# Top edge specular rim
d_draw.line([(dock_x + dock_r, dock_y), (dock_x + dock_w - dock_r, dock_y)], fill=(255, 255, 255, 160), width=1)

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

# 6. Top Power Emblem (y=175~245)
power_cx, power_cy = W // 2, 192
pr = 34

p_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
p_draw = ImageDraw.Draw(p_layer)

for gr in range(46, 28, -2):
    ga = int(80 * (1.0 - (gr - 28) / 18.0))
    p_draw.ellipse([power_cx - gr, power_cy - gr, power_cx + gr, power_cy + gr], outline=(56, 189, 248, ga), width=2)

p_draw.arc([power_cx - pr, power_cy - pr, power_cx + pr, power_cy + pr], start=125, end=415, fill=(56, 189, 248, 250), width=5)
p_draw.line([(power_cx, power_cy - pr - 6), (power_cx, power_cy - 4)], fill=(56, 189, 248, 255), width=5)

p_glow = p_layer.filter(ImageFilter.GaussianBlur(10))
base.paste(p_glow, (0, 0), p_glow)
base.paste(p_layer, (0, 0), p_layer)

# 7. Typography (Grand, letter-spaced, authoritative)
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

# Interactive Hint (y=640)
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

# Save epic outputs
out_png = r'C:\Users\jigu\.gemini\antigravity-ide\brain\3a664381-8939-4916-9404-683857cb0b2a\shutdown_bg_epic_grand.jpg'
out_target = r'tools\re_tools\tvsettings_decompiled\res\drawable-hdpi-v4\shutdown_bg.jpg'
base.save(out_png, quality=96)
base.save(out_target, quality=96)
print(f"[+] Output saved: {out_png}")
print(f"[+] Output updated in apktool: {out_target}")

# Also generate a simulation with the 3 buttons drawn on it
sim = base.copy()
s_draw = ImageDraw.Draw(sim)
# FrameLayout / arcView & shutdown: [642, 396, 792, 546]
# Reboot: [882, 396, 1032, 546]
# Sleep: [1122, 396, 1272, 546]
for bx, label in [(642, "关机"), (882, "重启"), (1122, "U盘启动")]:
    s_draw.ellipse([bx, 396, bx + 150, 546], fill=(15, 23, 42, 230), outline=(56, 189, 248, 220), width=3)
    font_btn = ImageFont.truetype(r'C:\Windows\Fonts\msyhbd.ttc', 26)
    b_bb = s_draw.textbbox((0, 0), label, font=font_btn)
    bw = b_bb[2] - b_bb[0]
    bh = b_bb[3] - b_bb[1]
    s_draw.text((bx + (150 - bw)//2, 396 + (150 - bh)//2), label, font=font_btn, fill=(241, 245, 249))

sim_out = r'C:\Users\jigu\.gemini\antigravity-ide\brain\3a664381-8939-4916-9404-683857cb0b2a\preview_shutdown_epic_sim.jpg'
sim.save(sim_out, quality=95)
print(f"[+] Simulation preview saved: {sim_out}")
