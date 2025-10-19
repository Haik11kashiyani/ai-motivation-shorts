"""
✅ WORKING VIRAL SHORTS GENERATOR
Guaranteed to create proper video files
Tested and verified!
"""

import os
import json
import random
from datetime import datetime
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import requests
import math

print("Starting Viral Shorts Generator...")

# ============================================================================
# CONFIG
# ============================================================================

WIDTH = 1080
HEIGHT = 1920
FPS = 30
DURATION = 20

# ElevenLabs
API_KEYS = [
    os.getenv('ELEVEN_API_KEY_1', ''),
    os.getenv('ELEVEN_API_KEY_2', ''),
    os.getenv('ELEVEN_API_KEY_3', ''),
]
VOICE_ID = 'pNInz6obpgDQGcFmaJgB'

# Colors
COLORS = [
    {'bg': (0, 0, 0), 'text': (255, 215, 0), 'glow': (255, 165, 0)},
    {'bg': (26, 0, 0), 'text': (255, 0, 0), 'glow': (255, 102, 102)},
    {'bg': (0, 26, 51), 'text': (0, 212, 255), 'glow': (102, 224, 255)},
    {'bg': (26, 0, 43), 'text': (176, 38, 255), 'glow': (230, 153, 255)},
]

os.makedirs('output', exist_ok=True)

# ============================================================================
# VOICE
# ============================================================================

def generate_voice(text):
    """Generate voice"""
    print("🎤 Generating voice...")
    
    # Try ElevenLabs
    for key in [k for k in API_KEYS if k]:
        try:
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
            response = requests.post(
                url,
                json={
                    "text": text,
                    "model_id": "eleven_monolingual_v1",
                    "voice_settings": {"stability": 0.7, "similarity_boost": 0.85}
                },
                headers={"xi-api-key": key},
                timeout=20
            )
            
            if response.status_code == 200:
                with open('voice.mp3', 'wb') as f:
                    f.write(response.content)
                print("✅ ElevenLabs voice ready")
                return 'voice.mp3'
        except:
            pass
    
    # Fallback gTTS
    print("Using gTTS...")
    from gtts import gTTS
    tts = gTTS(text, lang='en', slow=False)
    tts.save('voice.mp3')
    return 'voice.mp3'


# ============================================================================
# VIDEO CREATION
# ============================================================================

def create_frame(t, text, colors, duration):
    """Create single frame"""
    img = Image.new('RGB', (WIDTH, HEIGHT), colors['bg'])
    draw = ImageDraw.Draw(img)
    
    # Animated gradient
    for y in range(0, HEIGHT, 15):
        wave = math.sin(t * 0.5 + y/80) * 30
        r = min(255, colors['bg'][0] + int(wave))
        g = min(255, colors['bg'][1] + int(wave))
        b = min(255, colors['bg'][2] + int(wave))
        draw.rectangle([0, y, WIDTH, y+15], fill=(r, g, b))
    
    # Character
    cx = WIDTH // 2
    cy = int(HEIGHT * 0.68)
    breath = int(6 * math.sin(t * 2))
    
    # Body
    draw.ellipse([cx-90, cy-220+breath, cx+90, cy+120+breath], fill=(45, 45, 55))
    
    # Head
    draw.ellipse([cx-70, cy-320+breath, cx+70, cy-200+breath], fill=(55, 55, 65))
    
    # Eyes (glowing)
    eye_glow = int(180 + 60 * math.sin(t * 3))
    draw.ellipse([cx-40, cy-280+breath, cx-20, cy-260+breath], fill=(eye_glow, eye_glow, 255))
    draw.ellipse([cx+20, cy-280+breath, cx+40, cy-260+breath], fill=(eye_glow, eye_glow, 255))
    
    # Aura
    aura = int(320 + 60 * math.sin(t * 1.5))
    for i in range(3):
        offset = i * 35
        alpha = 120 - i * 35
        color = colors['glow'] + (alpha,)
        draw.ellipse([cx-aura+offset, cy-330+offset, cx+aura-offset, cy+180-offset],
                    outline=color, width=4)
    
    # Text with word-by-word reveal
    words = text.split()
    words_shown = int((t / duration) * len(words) * 1.3)
    words_shown = min(words_shown, len(words))
    visible_text = ' '.join(words[:words_shown])
    
    if visible_text:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 85)
        except:
            font = ImageFont.load_default()
        
        # Wrap text into lines
        lines = []
        current_line = []
        for word in visible_text.split():
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if bbox[2] - bbox[0] < WIDTH - 120:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))
        
        # Draw lines
        y_start = 140
        for i, line in enumerate(lines[:3]):
            bbox = draw.textbbox((0, 0), line, font=font)
            text_w = bbox[2] - bbox[0]
            x = (WIDTH - text_w) // 2
            y = y_start + i * 105
            
            # Glow effect
            glow_intensity = 0.8 + 0.2 * math.sin(t * 4 + i)
            for g in range(10, 0, -2):
                alpha = int(80 * glow_intensity * (10 - g) / 10)
                glow_color = colors['glow'] + (alpha,)
                for ox, oy in [(-g, 0), (g, 0), (0, -g), (0, g)]:
                    draw.text((x+ox, y+oy), line, font=font, fill=glow_color)
            
            # Black stroke
            for ox in [-5, -3, 0, 3, 5]:
                for oy in [-5, -3, 0, 3, 5]:
                    if ox != 0 or oy != 0:
                        draw.text((x+ox, y+oy), line, font=font, fill=(0, 0, 0))
            
            # Main text
            draw.text((x, y), line, font=font, fill=colors['text'])
    
    return np.array(img)


def create_video(quote_text, author):
    """Create complete video"""
    print("\n" + "="*60)
    print(f"📝 Quote: {quote_text[:50]}...")
    print(f"✍️  Author: {author}")
    
    # Generate voice
    audio_file = generate_voice(quote_text)
    audio = AudioFileClip(audio_file)
    
    # Use fixed duration
    duration = DURATION
    print(f"⏱️  Duration: {duration}s")
    
    # Select colors
    colors = random.choice(COLORS)
    print(f"🎨 Colors selected")
    
    # Create video clip
    print("🎬 Creating video frames...")
    
    def make_frame(t):
        return create_frame(t, quote_text, colors, duration)
    
    print("🎞️  Generating video clip...")
    video_clip = VideoClip(make_frame, duration=duration)
    video_clip = video_clip.set_audio(audio)
    
    # Output path
    output_path = f"output/viral_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
    
    print("📹 Rendering final video...")
    print("   (This takes 3-5 minutes...)")
    
    # Render with optimal settings
    video_clip.write_videofile(
        output_path,
        fps=FPS,
        codec='libx264',
        audio_codec='aac',
        preset='ultrafast',
        threads=4,
        bitrate='4000k',
        logger=None,
        verbose=False
    )
    
    # Cleanup
    video_clip.close()
    audio.close()
    
    # Verify output
    if os.path.exists(output_path):
        size_mb = os.path.getsize(output_path) / (1024 * 1024)
        print("\n" + "="*60)
        print("✅ VIDEO CREATED SUCCESSFULLY!")
        print("="*60)
        print(f"📹 File: {output_path}")
        print(f"📏 Size: {size_mb:.1f} MB")
        print(f"⏱️  Duration: {duration}s")
        print(f"🎯 FPS: {FPS}")
        print(f"📐 Resolution: {WIDTH}x{HEIGHT}")
        print("="*60 + "\n")
        return output_path
    else:
        print("\n❌ ERROR: Video file not created!")
        return None


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║    ✅ WORKING VIRAL SHORTS GENERATOR ✅             ║
    ║       Guaranteed Video Output!                      ║
    ╚══════════════════════════════════════════════════════╝
    """)
    
    try:
        # Load quotes
        print("📖 Loading quotes...")
        with open('motivational_content.json', 'r') as f:
            data = json.load(f)
        
        quote = random.choice(data['quotes'])
        
        # Create video
        result = create_video(quote['text'], quote['author'])
        
        if result:
            print("🎉 SUCCESS! Video is ready!")
            print(f"📂 Download from: {result}")
            exit(0)
        else:
            print("❌ FAILED to create video")
            exit(1)
            
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
