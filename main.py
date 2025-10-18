"""
Simple test version - GUARANTEED TO WORK
Focuses on core functionality without complex compositing
"""

import os
import json
import random
from datetime import datetime
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from gtts import gTTS
import math

# Create output folder
os.makedirs('output', exist_ok=True)

print("🎬 Starting simple video generation test...")

# Load content
with open('motivational_content.json', 'r') as f:
    data = json.load(f)
    quote = random.choice(data['quotes'])

print(f"📝 Quote: {quote['text'][:60]}...")
print(f"✍️  Author: {quote['author']}")

# Generate voice
print("🎤 Generating voiceover...")
tts = gTTS(text=quote['text'], lang='en', slow=False)
audio_file = 'temp_audio.mp3'
tts.save(audio_file)

# Get audio duration
audio = AudioFileClip(audio_file)
duration = max(audio.duration, 20)  # Minimum 20 seconds
print(f"⏱️  Duration: {duration:.1f}s")

# Video dimensions
WIDTH, HEIGHT = 1080, 1920
FPS = 30

def create_frame(t):
    """Create a single frame at time t"""
    # Create black background
    img = Image.new('RGB', (WIDTH, HEIGHT), '#000000')
    draw = ImageDraw.Draw(img)
    
    # Add animated gradient
    for y in range(HEIGHT):
        progress = y / HEIGHT
        r = int(20 + 40 * math.sin(t * 0.5 + progress * 2))
        g = int(10 + 30 * math.sin(t * 0.3 + progress * 3))
        b = int(40 + 60 * math.sin(t * 0.4 + progress))
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))
    
    # Draw animated character
    center_x = WIDTH // 2
    center_y = int(HEIGHT * 0.65)
    
    # Character - Simple animated person
    scale = 1 + 0.05 * math.sin(t * 2)
    
    # Legs
    leg_width = int(60 * scale)
    leg_height = 200
    draw.rectangle([center_x - 80, center_y, center_x - 20, center_y + leg_height], fill='#8B4513')
    draw.rectangle([center_x + 20, center_y, center_x + 80, center_y + leg_height], fill='#8B4513')
    
    # Body
    draw.rectangle([center_x - 90, center_y - 250, center_x + 90, center_y], fill='#CD853F')
    
    # Arms - animated
    arm_move = int(30 * math.sin(t * 4))
    draw.rectangle([center_x - 150, center_y - 180, center_x - 90, center_y - 100], fill='#CD853F')
    draw.rectangle([center_x + 90, center_y - 180, center_x + 150 + arm_move, center_y - 100], fill='#CD853F')
    
    # Head
    draw.ellipse([center_x - 50, center_y - 350, center_x + 50, center_y - 250], fill='#DEB887')
    
    # Eyes
    draw.ellipse([center_x - 30, center_y - 320, center_x - 10, center_y - 300], fill='#000000')
    draw.ellipse([center_x + 10, center_y - 320, center_x + 30, center_y - 300], fill='#000000')
    
    # Animated mouth (lip-sync)
    mouth_open = abs(math.sin(t * 15))
    if mouth_open > 0.3:
        mouth_height = int(10 + 15 * mouth_open)
        draw.ellipse([center_x - 20, center_y - 280 - mouth_height//2,
                     center_x + 20, center_y - 280 + mouth_height//2], fill='#8B4513')
    
    # Add glowing aura
    glow_radius = int(250 + 50 * math.sin(t * 2))
    for i in range(5):
        alpha = int(50 - i * 10)
        color = (255, 215, int(alpha))
        # Approximation of glow (simplified)
        if i == 0:
            draw.ellipse([center_x - glow_radius, center_y - 400,
                         center_x + glow_radius, center_y + 200], outline=color, width=2)
    
    # Add text overlay
    words = quote['text'].split()
    words_per_second = len(words) / duration
    visible_words = int(t * words_per_second) + 1
    current_text = ' '.join(words[:visible_words])
    
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 70)
    except:
        font = ImageFont.load_default()
    
    # Wrap text
    lines = []
    current_line = []
    for word in current_text.split():
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] - bbox[0] < WIDTH - 150:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))
    
    # Draw text
    y_pos = 150
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x_pos = (WIDTH - text_width) // 2
        
        # Black outline
        for offset in [(-3,-3), (-3,3), (3,-3), (3,3)]:
            draw.text((x_pos + offset[0], y_pos + offset[1]), line, font=font, fill=(0,0,0))
        
        # Gold text
        draw.text((x_pos, y_pos), line, font=font, fill=(255, 215, 0))
        y_pos += 100
    
    # Author name at bottom
    try:
        author_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 50)
    except:
        author_font = font
    
    author_text = f"- {quote['author']}"
    bbox = draw.textbbox((0, 0), author_text, font=author_font)
    text_width = bbox[2] - bbox[0]
    x_pos = (WIDTH - text_width) // 2
    y_pos = HEIGHT - 200
    
    draw.text((x_pos+2, y_pos+2), author_text, font=author_font, fill=(0,0,0))
    draw.text((x_pos, y_pos), author_text, font=author_font, fill=(255, 165, 0))
    
    return np.array(img)

# Create video
print("🎥 Creating video clip...")
video = VideoClip(create_frame, duration=duration)
video = video.set_audio(audio)

# Export
output_file = f"output/viral_short_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
print("📹 Rendering video (this may take a few minutes)...")

video.write_videofile(
    output_file,
    fps=FPS,
    codec='libx264',
    audio_codec='aac',
    preset='ultrafast',
    threads=4,
    logger=None
)

# Cleanup
video.close()
audio.close()

# Check result
if os.path.exists(output_file):
    size_mb = os.path.getsize(output_file) / (1024 * 1024)
    print(f"\n✅ SUCCESS!")
    print(f"📹 Video: {output_file}")
    print(f"📏 Size: {size_mb:.2f} MB")
    print(f"⏱️  Duration: {duration:.1f}s")
else:
    print("\n❌ FAILED!")
    exit(1)
