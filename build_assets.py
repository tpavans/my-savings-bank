import os, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

src_path = r'C:/Users/pavan/.gemini/antigravity/brain/004100bd-c715-473f-97cb-689bdad17047/.user_uploaded/media_1793352396001_173808a8.png'
dest_dir = r'D:\my saving bank\savings-app-1'
os.makedirs(dest_dir, exist_ok=True)

# 1. Load source image and isolate subject cleanly
src = Image.open(src_path).convert('RGBA')
arr = np.array(src, dtype=float)

# Distance from pure white
diff = np.sqrt(np.sum((arr[:, :, :3] - 255.0)**2, axis=2))
color_dev = np.maximum(np.abs(arr[:,:,0] - arr[:,:,2]), np.abs(arr[:,:,1] - arr[:,:,2]))

# Alpha mask with smooth anti-aliased edge
alpha = np.clip((diff - 12.0) / 28.0, 0.0, 1.0)
alpha[color_dev < 15] = 0.0

# Un-premultiply white to prevent fringe
clean_rgb = np.zeros_like(arr[:, :, :3])
for c in range(3):
    ch = (arr[:, :, c] - (1.0 - alpha) * 255.0) / np.maximum(alpha, 0.001)
    clean_rgb[:, :, c] = np.clip(ch, 0.0, 255.0)

cutout_arr = np.dstack([clean_rgb, alpha * 255.0]).astype(np.uint8)
cutout = Image.fromarray(cutout_arr)

# Crop exactly to the content bounds
bbox = cutout.getbbox()
subject = cutout.crop(bbox)
print(f"Isolated subject bbox: {bbox}, size: {subject.size}")

# Save the clean transparent subject logo
isolated_logo_path = os.path.join(dest_dir, 'app-logo.png')
subject.save(isolated_logo_path, format='PNG')
print(f"Saved transparent logo to {isolated_logo_path}")

def make_deep_blue_icon(size=512, is_maskable=False, rounded_squircle=True):
    # Create coordinate grid
    y, x = np.mgrid[0:size, 0:size].astype(float)
    # Center coords normalized (-1 to 1)
    cx = (x - size / 2.0) / (size / 2.0)
    cy = (y - size / 2.0) / (size / 2.0)
    r_dist = np.sqrt(cx**2 + cy**2)

    # Deep blue base gradient:
    # Center: Rich royal sapphire (#123078 / (18, 48, 120))
    # Mid: Deep oceanic navy (#0b1c48 / (11, 28, 72))
    # Edge: Midnight deep blue base (#040a1c / (4, 10, 28))
    # Subtle diagonal lighting from top-left (-0.3, -0.3)
    lx = (cx + 0.3)
    ly = (cy + 0.3)
    light_dist = np.sqrt(lx**2 + ly**2)
    center_glow = np.clip(1.0 - r_dist * 0.75, 0.0, 1.0)
    top_light = np.clip(1.0 - light_dist * 0.65, 0.0, 1.0)

    # Blend deep blue base
    r_chan = 4 + 10 * center_glow + 8 * top_light
    g_chan = 10 + 26 * center_glow + 18 * top_light
    b_chan = 28 + 72 * center_glow + 45 * top_light

    # Add soft golden/emerald ambient bloom behind where the money will sit (center)
    bloom = np.exp(-((r_dist * 1.8)**2))
    r_chan += 20 * bloom
    g_chan += 35 * bloom
    b_chan += 25 * bloom

    r_chan = np.clip(r_chan, 0, 255).astype(np.uint8)
    g_chan = np.clip(g_chan, 0, 255).astype(np.uint8)
    b_chan = np.clip(b_chan, 0, 255).astype(np.uint8)
    a_chan = np.full((size, size), 255, dtype=np.uint8)

    base_img = Image.fromarray(np.dstack([r_chan, g_chan, b_chan, a_chan]))

    # If rounded_squircle and not full maskable, apply rounded rectangle / squircle mask
    if rounded_squircle and not is_maskable:
        mask = Image.new('L', (size, size), 0)
        draw = ImageDraw.Draw(mask)
        radius = int(size * 0.22)  # modern iOS / macOS / Android squircle radius
        draw.rounded_rectangle([0, 0, size, size], radius=radius, fill=255)
        
        # Border highlight (sleek 1.5px subtle metallic blue / gold shimmer)
        border = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        bdraw = ImageDraw.Draw(border)
        bdraw.rounded_rectangle([1, 1, size - 2, size - 2], radius=radius, outline=(90, 150, 255, 120), width=int(size * 0.007))
        
        base_img.putalpha(mask)
        base_img = Image.alpha_composite(base_img, border)

    # Now calculate subject size
    # Subject aspect ratio is 267 / 182 = 1.467
    target_width = int(size * (0.76 if is_maskable else 0.78))
    target_height = int(target_width * (subject.size[1] / subject.size[0]))
    resized_subj = subject.resize((target_width, target_height), Image.Resampling.LANCZOS)

    # Position: centered horizontally, slightly centered/elevated vertically
    sub_x = (size - target_width) // 2
    sub_y = (size - target_height) // 2 + int(size * 0.02)

    # Soft dark drop shadow under the subject
    shadow_pad = 20
    shadow = Image.new('RGBA', (target_width + shadow_pad * 2, target_height + shadow_pad * 2), (0, 0, 0, 0))
    # Extract alpha of resized subject
    s_alpha = np.array(resized_subj.split()[3])
    # Dark shadow
    sh_arr = np.zeros((target_height, target_width, 4), dtype=np.uint8)
    sh_arr[:, :, 3] = (s_alpha * 0.55).astype(np.uint8)
    sh_img = Image.fromarray(sh_arr)
    shadow.paste(sh_img, (shadow_pad, shadow_pad + 8), mask=sh_img)
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=int(size * 0.035)))

    # Composite layers
    comp = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    comp.alpha_composite(base_img)
    comp.alpha_composite(shadow, (sub_x - shadow_pad, sub_y - shadow_pad))
    comp.alpha_composite(resized_subj, (sub_x, sub_y))

    return comp

# Generate all required icon assets
print("Generating 512x512 deep blue base icon...")
icon512 = make_deep_blue_icon(512, is_maskable=False, rounded_squircle=True)
icon512.save(os.path.join(dest_dir, 'icon-512.png'), format='PNG')

print("Generating 512x512 maskable deep blue base icon...")
icon512_mask = make_deep_blue_icon(512, is_maskable=True, rounded_squircle=False)
icon512_mask.save(os.path.join(dest_dir, 'icon-maskable-512.png'), format='PNG')

print("Generating 192x192 deep blue base icon...")
icon192 = icon512.resize((192, 192), Image.Resampling.LANCZOS)
icon192.save(os.path.join(dest_dir, 'icon-192.png'), format='PNG')

print("Generating 180x180 Apple touch icon...")
icon180 = icon512.resize((180, 180), Image.Resampling.LANCZOS)
icon180.save(os.path.join(dest_dir, 'apple-touch-icon.png'), format='PNG')

print("Generating favicons...")
fav32 = icon512.resize((32, 32), Image.Resampling.LANCZOS)
fav32.save(os.path.join(dest_dir, 'favicon.png'), format='PNG')

# Generate multi-size icon.ico for Windows desktop executable & shortcuts
ico_sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
icon512.save(os.path.join(dest_dir, 'favicon.ico'), format='ICO', sizes=ico_sizes)
icon512.save(os.path.join(dest_dir, 'icon.ico'), format='ICO', sizes=ico_sizes)

# Also save a copy to the root workspace `d:\my saving bank`
icon512.save(r'D:\my saving bank\icon.ico', format='ICO', sizes=ico_sizes)
icon512.save(r'D:\my saving bank\icon-512.png', format='PNG')

print("All icons generated successfully with deep blue base!")
