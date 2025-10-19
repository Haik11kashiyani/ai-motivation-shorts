"""
🚀 FAST BEAUTIFUL VIRAL SHORTS 🚀
Complex animations but optimized for speed
Renders in 3-4 minutes guaranteed!
"""

import sys
import os
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', buffering=1)

print("SCRIPT STARTED!", flush=True)
print("Importing libraries...", flush=True)

import json
import random
from datetime import datetime
from moviepy.editor import VideoClip, AudioFileClip
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import requests
import math

print("Libraries imported!", flush=True)

# CONFIG
WIDTH = 1080
HEIGHT = 1920
FPS = 30
DURATION = 20

API_KEYS = [os.getenv('ELEVEN_API_KEY_1', ''), os.getenv('ELEVEN_API_KEY_2', ''), os.getenv('ELEVEN_API_KEY_3', '')]
VOICE_ID = 'pNInz6obpgDQGcFmaJgB'

COLORS = [
    {'name': 'Gold', 'bg1': (0,0,0), 'bg2': (20,20,0), 'text': (255,215,0), 'glow': (255,180,0)},
    {'name': 'Red', 'bg1': (15,0,0), 'bg2': (30,0,0), 'text': (255,0,0), 'glow': (255,100,100)},
    {'name': 'Blue', 'bg1': (0,15,30), 'bg2': (0,25,50), 'text': (0,212,255), 'glow': (100,220,255)},
    {'name': 'Purple', 'bg1': (15,0,25), 'bg2': (25,0,40), 'text': (180,50,255), 'glow': (220,150,255)},
]

os.makedirs('output', exist_ok=True)

print("="*70, flush=True)
print("🔥 FAST BEAUTIFUL VIRAL SHORTS GENERATOR", flush=True)
print("="*70, flush=True)

# ============================================================================
# VOICE
# ============================================================================

def generate_voice(text):
    print("\n🎤 Generating voice...", flush=True)
    
    for i, key in enumerate([k for k in API_KEYS if k]):
        try:
            print(f"   Attempt {i+1}: ElevenLabs...", flush=True)
            response = requests.post(
                f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
                json={"text": text, "model_id": "eleven_monolingual_v1",
                      "voice_settings": {"stability": 0.7, "similarity_boost": 0.85}},
                headers={"xi-api-key": key},
                timeout=20
            )
            
            if response.status_code == 200:
                with open('voice.mp3', 'wb') as f:
                    f.write(response.content)
                print("   ✅ Premium voice ready!", flush=True)
                return 'voice.mp3'
        except Exception as e:
            print(f"   ⚠️ {e}", flush=True)
    
    print("   Using gTTS...", flush=True)
    from gtts import gTTS
    tts = gTTS(text, lang='en', slow=False)
    tts.save('voice.mp3')
    print("   ✅ Voice ready!", flush=True)
    return 'voice.mp3'

# ============================================================================
# OPTIMIZED FRAME GENERATOR
# ============================================================================

def create_frame(t, text, colors, duration):
    """Optimized frame generation - FAST but still beautiful"""
    
    # Create background with simple gradient
    img = Image.new('RGB', (WIDTH, HEIGHT), colors['bg1'])
    draw = ImageDraw.Draw(img)
    
    # Animated gradient (optimized - every 20px)
    for y in range(0, HEIGHT, 20):
        wave = math.sin(t * 0.5 + y/100) * 0.3
        progress = y / HEIGHT
        
        r = int(colors['bg1'][0] + (colors['bg2'][0] - colors['bg1'][0]) * (progress + wave))
        g = int(colors['bg1'][1] + (colors['bg2'][1] - colors['bg1'][1]) * (progress + wave))
        b = int(colors['bg1'][2] + (colors['bg2'][2] - colors['bg1'][2]) * (progress + wave))
        
        r, g, b = max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b))
        
        draw.rectangle([0, y, WIDTH, y+20], fill=(r, g, b))
    
    # Simple but beautiful particles (10 instead of 30 for speed)
    for i in range(10):
        cycle = (t * 0.5 + i * 0.3) % duration
        x = int(WIDTH * 0.2 + WIDTH * 0.6 * ((i * 37) % 100) / 100)
        y = int((cycle / duration) * HEIGHT)
        
        if 0 <= y < HEIGHT:
            size = int(3 + 3 * math.sin(t * 2 + i))
            brightness = 0.6 + 0.4 * math.sin(t * 3 + i)
            
            pr = int(colors['glow'][0] * brightness)
            pg = int(colors['glow'][1] * brightness)
            pb = int(colors['glow'][2] * brightness)
            
            # Simple particle (no complex blending)
            draw.ellipse([x-size, y-size, x+size, y+size], fill=(pr, pg, pb))
    
    # Character
    cx = WIDTH // 2
    cy = int(HEIGHT * 0.68)
    breath = int(6 * math.sin(t * 2))
    
    # Body
    draw.ellipse([cx-90, cy-220+breath, cx+90, cy+120+breath], fill=(45, 45, 55))
    
    # Head
    draw.ellipse([cx-70, cy-320+breath, cx+70, cy-200+breath], fill=(55, 55, 65))
    
    # Glowing eyes
    glow = int(150 + 100 * abs(math.sin(t * 3)))
    draw.ellipse([cx-40, cy-280+breath, cx-20, cy-260+breath], fill=(glow, glow, 255))
    draw.ellipse([cx+20, cy-280+breath, cx+40, cy-260+breath], fill=(glow, glow, 255))
    
    # Energy aura (4 layers instead of 6)
    aura = int(330 + 60 * math.sin(t * 1.5))
    for i in range(4):
        offset = i * 30
        draw.ellipse([cx-aura+offset, cy-330+offset, cx+aura-offset, cy+180-offset],
                    outline=colors['glow'], width=4)
    
    # Energy rays (8 instead of 12)
    for i in range(8):
        angle = (t * 1.5 + i * 45) % 360
        rad = math.radians(angle)
        length = 180 + 60 * math.sin(t * 2 + i)
        
        sx = cx + int(140 * math.cos(rad))
        sy = cy - 50 + breath + int(140 * math.sin(rad))
        ex = cx + int(length * math.cos(rad))
        ey = cy - 50 + breath + int(length * math.sin(rad))
        
        draw.line([(sx, sy), (ex, ey)], fill=colors['glow'], width=3)
    
    # Text with optimized effects
    words = text.split()
    shown = int((t / duration) * len(words) * 1.3)
    shown = min(shown, len(words))
    visible = ' '.join(words[:shown])
    
    if visible:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 85)
        except:
            font = ImageFont.load_default()
        
        # Wrap text
        lines = []
        current = []
        for word in visible.split():
            test = ' '.join(current + [word])
            bbox = draw.textbbox((0, 0), test, font=font)
            if bbox[2] - bbox[0] < WIDTH - 100:
                current.append(word)
            else:
                if current:
                    lines.append(' '.join(current))
                current = [word]
        if current:
            lines.append(' '.join(current))
        
        lines = lines[:3]
        
        # Draw text
        y = 120
        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font)
            tw = bbox[2] - bbox[0]
            x = (WIDTH - tw) // 2
            
            fade = min(1.0, (t - i * 0.3) * 3)
            
            if fade > 0:
                # Optimized glow (6 layers instead of 12)
                glow_size = int(10 * (0.7 + 0.3 * math.sin(t * 4)))
                for g in range(glow_size, 0, -2):
                    alpha = fade * (glow_size - g) / glow_size
                    gr = int(colors['glow'][0] * alpha * 0.5)
                    gg = int(colors['glow'][1] * alpha * 0.5)
                    gb = int(colors['glow'][2] * alpha * 0.5)
                    
                    for ox, oy in [(-g, 0), (g, 0), (0, -g), (0, g)]:
                        draw.text((x+ox, y+oy), line, font=font, fill=(gr, gg, gb))
                
                # Black stroke (5px instead of 7)
                for ox in [-5, -3, 0, 3, 5]:
                    for oy in [-5, -3, 0, 3, 5]:
                        if ox or oy:
                            draw.text((x+ox, y+oy), line, font=font, fill=(0, 0, 0))
                
                # Main text
                tr = int(colors['text'][0] * fade)
                tg = int(colors['text'][1] * fade)
                tb = int(colors['text'][2] * fade)
                draw.text((x, y), line, font=font, fill=(tr, tg, tb))
                
                # Highlight last word
                if i == len(lines) - 1:
                    words_in_line = line.split()
                    if words_in_line:
                        pulse = 0.6 + 0.4 * math.sin(t * 8)
                        
                        words_before = ' '.join(words_in_line[:-1])
                        if words_before:
                            bbox_b = draw.textbbox((0, 0), words_before + ' ', font=font)
                            lx = x + (bbox_b[2] - bbox_b[0])
                        else:
                            lx = x
                        
                        bbox_w = draw.textbbox((0, 0), words_in_line[-1], font=font)
                        ww = bbox_w[2] - bbox_w[0]
                        uy = y + 95
                        
                        ur = int(colors['glow'][0] * pulse * fade)
                        ug = int(colors['glow'][1] * pulse * fade)
                        ub = int(colors['glow'][2] * pulse * fade)
                        
                        draw.line([(lx, uy), (lx + ww, uy)], fill=(ur, ug, ub), width=5)
            
            y += 105
    
    return np.array(img)

# ============================================================================
# MAIN
# ============================================================================

print("\n📖 Loading quote...", flush=True)

with open('motivational_content.json', 'r') as f:
    data = json.load(f)

quote = random.choice(data['quotes'])
text = quote['text']
author = quote['author']

print(f"   Quote: {text[:50]}...", flush=True)
print(f"   Author: {author}", flush=True)

# Voice
audio_path = generate_voice(text)
audio = AudioFileClip(audio_path)
duration = DURATION

print(f"\n⏱️  Duration: {duration}s", flush=True)

# Colors
colors = random.choice(COLORS)
print(f"🎨 Color: {colors['name']}", flush=True)

# Create video
print("\n🎬 Creating video...", flush=True)
print("   Features:", flush=True)
print("   ✓ Animated gradient", flush=True)
print("   ✓ 10 particles", flush=True)
print("   ✓ Character animation", flush=True)
print("   ✓ Energy aura (4 layers)", flush=True)
print("   ✓ Energy rays (8)", flush=True)
print("   ✓ Text effects", flush=True)
print("", flush=True)
print("   Rendering (3-4 minutes)...", flush=True)

def make_frame(t):
    if int(t * 2) % 10 == 0:  # Progress indicator
        print(f"   Progress: {int(t/duration*100)}%", flush=True)
    return create_frame(t, text, colors, duration)

video = VideoClip(make_frame, duration=duration)
video = video.set_audio(audio)

output = f"output/fast_viral_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"

video.write_videofile(
    output,
    fps=FPS,
    codec='libx264',
    audio_codec='aac',
    bitrate='4000k',
    preset='ultrafast',  # ULTRAFAST for speed
    threads=4,
    logger=None,
    verbose=False
)

video.close()
audio.close()

if os.path.exists(output):
    size = os.path.getsize(output) / (1024*1024)
    print("\n" + "="*70, flush=True)
    print("✅ SUCCESS!", flush=True)
    print("="*70, flush=True)
    print(f"📹 File: {output}", flush=True)
    print(f"📏 Size: {size:.1f} MB", flush=True)
    print(f"⏱️  Duration: {duration}s", flush=True)
    print("="*70, flush=True)
else:
    print("\n❌ FAILED!", flush=True)
    exit(1)
