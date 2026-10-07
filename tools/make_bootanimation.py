import os, math, zipfile
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def make_bootanimation():
    print("[*] Generating NextGen TV Bootanimation...")
    out_dir = r"tools\bootanim_frames\part1"
    os.makedirs(out_dir, exist_ok=True)

    base_ai_path = r'C:\Users\jigu\.gemini\antigravity-ide\brain\3a664381-8939-4916-9404-683857cb0b2a\nextgen_boot_minimal_1791333677810.jpg'
    base_raw = Image.open(base_ai_path).convert('RGB')
    W, H = 1920, 1080
    base_raw = base_raw.resize((W, H), Image.Resampling.LANCZOS)

    # Clean bottom text on base
    draw_clean = ImageDraw.Draw(base_raw)
    for y in range(880, 1060):
        draw_clean.line([(0, y), (W, y)], fill=(0, 0, 0))

    # Add razor-sharp bottom text
    font_sub = ImageFont.truetype(r'C:\Windows\Fonts\msyh.ttc', 26)
    font_sub_bold = ImageFont.truetype(r'C:\Windows\Fonts\msyhbd.ttc', 26)

    part1 = '恩山无线论坛 '
    part_author = '@jigu'
    part2 = '   •   AMLOGIC S905D 64-BIT   •   NEXTGEN TV OS v19'

    w1 = draw_clean.textbbox((0, 0), part1, font=font_sub)[2] - draw_clean.textbbox((0, 0), part1, font=font_sub)[0]
    wa = draw_clean.textbbox((0, 0), part_author, font=font_sub_bold)[2] - draw_clean.textbbox((0, 0), part_author, font=font_sub_bold)[0]
    w2 = draw_clean.textbbox((0, 0), part2, font=font_sub)[2] - draw_clean.textbbox((0, 0), part2, font=font_sub)[0]

    total_fw = w1 + wa + w2
    fx = (W - total_fw) // 2
    fy = 945

    # Draw bottom text
    draw_clean.text((fx + 1, fy + 1), part1, font=font_sub, fill=(10, 15, 25))
    draw_clean.text((fx + w1 + 1, fy + 1), part_author, font=font_sub_bold, fill=(10, 15, 25))
    draw_clean.text((fx + w1 + wa + 1, fy + 1), part2, font=font_sub, fill=(10, 15, 25))
    draw_clean.text((fx, fy), part1, font=font_sub, fill=(148, 163, 184))
    draw_clean.text((fx + w1, fy), part_author, font=font_sub_bold, fill=(56, 189, 248))  # Cyan highlight
    draw_clean.text((fx + w1 + wa, fy), part2, font=font_sub, fill=(148, 163, 184))

    # Number of frames in breathing cycle
    num_frames = 24
    beam_y = 665
    beam_w = 750

    print(f"[*] Rendering {num_frames} frames of breathing horizon beam...")
    for f_idx in range(num_frames):
        # Sine wave breathing: 0.0 -> 1.0 -> 0.0
        angle = (f_idx / float(num_frames)) * 2 * math.pi
        pulse = (math.sin(angle) + 1.0) / 2.0  # 0.0 to 1.0
        intensity = 0.65 + 0.55 * pulse       # 0.65 to 1.20

        frame = base_raw.copy()

        # Render pulsing laser horizon layer
        pulse_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        p_draw = ImageDraw.Draw(pulse_layer)

        for i in range(-beam_w, beam_w):
            factor = 1.0 - abs(i) / float(beam_w)
            factor = (math.cos((1.0 - factor) * math.pi) + 1.0) / 2.0
            r = int(min(255, (20 + 36 * factor) * intensity))
            g = int(min(255, (80 + 130 * factor) * intensity))
            b = int(min(255, (220 + 35 * factor) * intensity))
            a = int(min(255, 180 * factor * intensity))
            p_draw.line([(W // 2 + i, beam_y), (W // 2 + i, beam_y)], fill=(r, g, b, a), width=2)

        blur_wide = pulse_layer.filter(ImageFilter.GaussianBlur(16))
        blur_mid = pulse_layer.filter(ImageFilter.GaussianBlur(4))

        frame.paste(blur_wide, (0, 0), blur_wide)
        frame.paste(blur_mid, (0, 0), blur_mid)
        frame.paste(pulse_layer, (0, 0), pulse_layer)

        frame_path = os.path.join(out_dir, f"frame_{f_idx:02d}.png")
        frame.save(frame_path, "PNG", optimize=True)

    # Create desc.txt: 1920 1080 20 fps, loop part1 indefinitely
    desc_path = r"tools\bootanim_frames\desc.txt"
    with open(desc_path, "w", newline="\n") as f:
        f.write("1920 1080 20\n")
        f.write("c 0 0 part1\n")

    # Zip with STORED (0 compression) - Android bootanimation requirement!
    zip_path = r"tools\bootanimation_custom.zip"
    print(f"[*] Packaging into uncompressed ZIP: {zip_path}...")
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_STORED) as z:
        z.write(desc_path, "desc.txt")
        for f in sorted(os.listdir(out_dir)):
            if f.endswith(".png"):
                z.write(os.path.join(out_dir, f), f"part1/{f}")

    print(f"[+] SUCCESS! Generated bootanimation.zip ({os.path.getsize(zip_path)} bytes)")

if __name__ == "__main__":
    make_bootanimation()
