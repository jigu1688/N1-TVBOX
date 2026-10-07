import os
from PIL import Image, ImageDraw, ImageFont

res_drawable = "tools/tvwidget_project/res/drawable"
os.makedirs(res_drawable, exist_ok=True)

def create_preview(filename, title, subtitle, badges, bg_color=(15, 23, 42)):
    # 540x300 preview image
    img = Image.new('RGBA', (540, 300), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw rounded panel
    draw.rounded_rectangle([10, 10, 530, 290], radius=24, fill=bg_color, outline=(255, 255, 255, 60), width=2)

    # Try standard font
    try:
        font_large = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 68)
        font_med = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 22)
        font_small = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 18)
    except:
        font_large = font_med = font_small = ImageFont.load_default()

    # Draw big title / time
    draw.text((40, 50), title, font=font_large, fill=(255, 255, 255, 255))
    draw.text((44, 150), subtitle, font=font_med, fill=(186, 230, 253, 255))

    # Draw badges
    bx = 44
    by = 205
    for badge, bcol in badges:
        # Measure text
        bbox = draw.textbbox((0, 0), badge, font=font_small)
        bw = bbox[2] - bbox[0] + 24
        bh = 40
        draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=10, fill=bcol, outline=(255, 255, 255, 40), width=1)
        draw.text((bx + 12, by + 8), badge, font=font_small, fill=(255, 255, 255, 255))
        bx += bw + 12

    p = os.path.join(res_drawable, filename)
    img.save(p, "PNG")
    print(f"[+] Generated {p}")

create_preview(
    "preview_dashboard.png",
    "10:08",
    "8月30日 星期日 · 农历七月十八",
    [("🌤️ 晴 26°C", (2, 132, 199, 180)), ("🌡️ 48°C", (217, 119, 6, 180)), ("⚡ RAM 38%", (30, 41, 59, 220)), ("🌐 192.168.31.114", (30, 41, 59, 220))]
)

create_preview(
    "preview_clock_weather.png",
    "10:08",
    "8月30日 星期日 · 农历七月十八",
    [("🌤️ 晴 26°C · 深圳", (2, 132, 199, 200)), ("空气质量: 优", (16, 185, 129, 180))]
)

create_preview(
    "preview_system_monitor.png",
    "斐讯 N1 极速版",
    "硬件实时监视 · 千兆网络",
    [("🌡️ CPU 48°C", (217, 119, 6, 200)), ("⚡ RAM 38%", (16, 185, 129, 200)), ("📦 闪存 4.3G", (30, 41, 59, 220)), ("🌐 192.168.31.114", (2, 132, 199, 200))]
)
