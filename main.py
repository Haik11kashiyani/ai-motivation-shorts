"""
🎥 GUARANTEED VIDEO OUTPUT
This WILL create a proper MP4 video file, not an image!
Minimal effects but 100% working
"""

print("Starting video generator...")

import os
import json
import random
from datetime import datetime
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import math

print("Step 1: Imports complete")

# Create output folder
os.makedirs('output', exist_ok=True)

# Load quote
print("Step 2: Loading quote...")
with open('motivational_content.json') as f:
    data = json.load(f)

quote = random.choice(data['quotes'])
text = quote['text']
print(f"Quote: {text[:50]}...")

# Generate voice
print("Step 3: Generating voice...")
from gtts import gTTS
tts = gTTS(text, lang='en', slow=False)
tts.save('audio.mp3')
print("Voice saved")

# Import MoviePy AFTER gTTS (important!)
print("Step 4: Importing MoviePy...")
from moviepy.editor import VideoClip, AudioFileClip
print("MoviePy imported")

# Load audio
print("Step 5: Loading audio...")
audio = AudioFileClip('audio.mp3')
duration = 15  # Fixed 15 seconds
print(f"Audio duration: {audio.duration:.1f}s, Using: {duration}s")

# Video settings
WIDTH = 1080
HEIGHT = 1920
FPS = 30

print(f"Step 6: Video settings - {WIDTH}x{HEIGHT} @ {FPS}fps")

# Color
colors = {
    'bg': (10, 10, 15),
    'text': (255, 215, 0),
    'glow': (255, 180, 0)
}

print("Step 7: Creating frame generator function...")

# Frame counter for progress
frame_num = [0]
total_frames = duration * FPS

def make_video_frame(t):
    """Generate single frame"""
    
    frame_num[0] += 1
    
    # Progress every 10%
    if frame_num[0] % (total_frames // 10) == 0:
        pct = int((frame_num[0] / total_frames) * 100)
        print(f"  Rendering: {pct}%")
    
    # Create image
    img = Image.new('RGB', (WIDTH, HEIGHT), colors['bg'])
    draw = ImageDraw.Draw(img)
    
    # Simple animated gradient
    for y in range(0, HEIGHT, 40):
        brightness = int(20 + 15 * math.sin(t * 0.5 + y/150))
        r = colors['bg'][0] + brightness
        g = colors['bg'][1] + brightness
        b = colors['bg'][2] + brightness
        draw.rectangle([0, y, WIDTH, y+40], fill=(r, g, b))
    
    # Moving orbs
    for i in range(4):
        cycle = (t * 0.6 + i * 0.4) % duration
        x = int(300 + 480 * ((i * 37) % 100) / 100)
        y = int((cycle / duration) * HEIGHT)
        
        if 0 <= y < HEIGHT:
            size = int(10 + 6 * math.sin(t * 2 + i))
            brightness = 0.7 + 0.3 * math.sin(t * 3 + i)
            
            cr = int(colors['glow'][0] * brightness)
            cg = int(colors['glow'][1] * brightness)
            cb = int(colors['glow'][2] * brightness)
            
            draw.ellipse([x-size, y-size, x+size, y+size], fill=(cr, cg, cb))
    
    # Text
    words = text.split()
    shown = int((t / duration) * len(words) * 1.2)
    shown = min(shown, len(words))
    visible = ' '.join(words[:shown])
    
    if visible:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 85)
        except:
            font = ImageFont.load_default()
        
        # Simple wrap
        lines = []
        current = []
        for word in visible.split():
            test = ' '.join(current + [word])
            bbox = draw.textbbox((0, 0), test, font=font)
            if bbox[2] - bbox[0] < WIDTH - 120:
                current.append(word)
            else:
                if current:
                    lines.append(' '.join(current))
                current = [word]
        if current:
            lines.append(' '.join(current))
        
        lines = lines[:2]
        
        # Draw text
        y = (HEIGHT - len(lines) * 110) // 2
        
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            tw = bbox[2] - bbox[0]
            x = (WIDTH - tw) // 2
            
            # Glow
            for g in [10, 6, 3]:
                ga = 0.3
                gr = int(colors['glow'][0] * ga)
                gg = int(colors['glow'][1] * ga)
                gb = int(colors['glow'][2] * ga)
                
                for ox, oy in [(-g,0), (g,0), (0,-g), (0,g)]:
                    draw.text((x+ox, y+oy), line, font=font, fill=(gr, gg, gb))
            
            # Outline
            for ox in [-5, -3, 0, 3, 5]:
                for oy in [-5, -3, 0, 3, 5]:
                    if ox or oy:
                        draw.text((x+ox, y+oy), line, font=font, fill=(0, 0, 0))
            
            # Main
            draw.text((x, y), line, font=font, fill=colors['text'])
            
            y += 110
    
    return np.array(img)

print("Step 8: Creating VideoClip object...")
video = VideoClip(make_video_frame, duration=duration)

print("Step 9: Adding audio to video...")
video = video.set_audio(audio)

# Output path
output = f"output/video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"

print(f"Step 10: Starting render to {output}")
print(f"This will take 3-5 minutes for {duration}s video...")
print("Progress will show every 10%\n")

# RENDER VIDEO
video.write_videofile(
    output,
    fps=FPS,
    codec='libx264',
    audio_codec='aac',
    preset='ultrafast',
    bitrate='4000k',
    threads=4,
    logger=None,
    verbose=False
)

print("\nStep 11: Closing video objects...")
video.close()
audio.close()

print("Step 12: Verifying output...")

# CHECK IF VIDEO EXISTS
if os.path.exists(output):
    size_mb = os.path.getsize(output) / (1024 * 1024)
    
    # Check if it's actually a video (not just a small file)
    if size_mb > 0.5:  # Must be at least 0.5 MB
        print("\n" + "="*60)
        print("✅ SUCCESS! VIDEO CREATED!")
        print("="*60)
        print(f"File: {output}")
        print(f"Size: {size_mb:.2f} MB")
        print(f"Duration: {duration}s")
        print(f"Resolution: {WIDTH}x{HEIGHT}")
        print(f"FPS: {FPS}")
        print("="*60)
        
        # List all files in output
        print("\nAll files in output folder:")
        for f in os.listdir('output'):
            fsize = os.path.getsize(os.path.join('output', f)) / (1024 * 1024)
            print(f"  - {f} ({fsize:.2f} MB)")
        
        exit(0)
    else:
        print(f"\n❌ ERROR: File created but too small ({size_mb:.2f} MB)")
        print("This might be a corrupted file or thumbnail image")
        exit(1)
else:
    print("\n❌ ERROR: Output file does not exist!")
    print(f"Expected: {output}")
    print("\nFiles in output folder:")
    if os.path.exists('output'):
        for f in os.listdir('output'):
            print(f"  - {f}")
    else:
        print("  (output folder doesn't exist)")
    exit(1)
