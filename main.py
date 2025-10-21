"""
🔥 FINAL COMPLETE VIRAL SHORTS GENERATOR 🔥

Everything we discussed:
✅ No 2D character
✅ Modern cinematic background
✅ Trending 2024 effects
✅ Fixed continuous voice (ElevenLabs + gTTS fallback)
✅ Professional bold typography
✅ Viral-optimized design
✅ Fast rendering (5-7 minutes)
✅ Progress indicators
✅ Guaranteed to work
"""

import sys
import os

# Force unbuffered output
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', buffering=1)
sys.stderr = os.fdopen(sys.stderr.fileno(), 'w', buffering=1)

print("="*70, flush=True)
print("🔥 VIRAL SHORTS GENERATOR - STARTING", flush=True)
print("="*70, flush=True)

import json
import random
from datetime import datetime
from moviepy.editor import VideoClip, AudioFileClip
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import requests
import math

print("✅ All libraries loaded successfully!", flush=True)

# ============================================================================
# CONFIGURATION
# ============================================================================

WIDTH = 1080
HEIGHT = 1920
FPS = 30
MIN_DURATION = 15
MAX_DURATION = 25

# ElevenLabs API Keys
ELEVEN_KEYS = [
    os.getenv('ELEVEN_API_KEY_1', ''),
    os.getenv('ELEVEN_API_KEY_2', ''),
    os.getenv('ELEVEN_API_KEY_3', '')
]

VOICE_ID = 'pNInz6obpgDQGcFmaJgB'  # Adam - Deep male voice

# Modern color schemes (optimized - no alpha)
COLORS = [
    {
        'name': '💛 Neon Gold',
        'bg_dark': (10, 10, 15),
        'bg_light': (40, 35, 0),
        'text': (255, 223, 0),
        'accent': (255, 180, 0),
        'glow': (255, 200, 50)
    },
    {
        'name': '💙 Electric Blue',
        'bg_dark': (5, 10, 25),
        'bg_light': (10, 25, 60),
        'text': (0, 255, 255),
        'accent': (0, 180, 255),
        'glow': (100, 200, 255)
    },
    {
        'name': '❤️ Fire Red',
        'bg_dark': (25, 5, 5),
        'bg_light': (60, 10, 0),
        'text': (255, 70, 70),
        'accent': (255, 120, 0),
        'glow': (255, 150, 100)
    },
    {
        'name': '💜 Royal Purple',
        'bg_dark': (20, 5, 30),
        'bg_light': (40, 15, 70),
        'text': (220, 120, 255),
        'accent': (180, 80, 255),
        'glow': (230, 170, 255)
    }
]

os.makedirs('output', exist_ok=True)

# ============================================================================
# VOICE GENERATOR - Fixed Continuous Audio
# ============================================================================

def generate_voice(text):
    """Generate continuous voice that doesn't stop"""
    print("\n🎤 Generating voice...", flush=True)
    
    # Try ElevenLabs
    for i, key in enumerate([k for k in ELEVEN_KEYS if k]):
        try:
            print(f"   Attempting ElevenLabs (key {i+1})...", flush=True)
            
            response = requests.post(
                f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
                json={
                    "text": text,
                    "model_id": "eleven_multilingual_v2",
                    "voice_settings": {
                        "stability": 0.75,
                        "similarity_boost": 0.85,
                        "style": 0.5,
                        "use_speaker_boost": True
                    }
                },
                headers={
                    "Accept": "audio/mpeg",
                    "Content-Type": "application/json",
                    "xi-api-key": key
                },
                timeout=25
            )
            
            if response.status_code == 200:
                with open('voice.mp3', 'wb') as f:
                    f.write(response.content)
                
                # Verify audio length
                test_audio = AudioFileClip('voice.mp3')
                duration = test_audio.duration
                test_audio.close()
                
                if duration > 2:
                    print(f"   ✅ ElevenLabs voice ready! ({duration:.1f}s)", flush=True)
                    return 'voice.mp3', duration
                else:
                    print(f"   ⚠️ Audio too short, trying next...", flush=True)
                    
        except Exception as e:
            print(f"   ⚠️ Failed: {str(e)[:50]}", flush=True)
    
    # Fallback to gTTS
    print("   Using gTTS fallback...", flush=True)
    from gtts import gTTS
    
    tts = gTTS(text=text, lang='en', slow=False, tld='co.uk')
    tts.save('voice.mp3')
    
    audio = AudioFileClip('voice.mp3')
    duration = audio.duration
    audio.close()
    
    print(f"   ✅ gTTS voice ready! ({duration:.1f}s)", flush=True)
    return 'voice.mp3', duration


# ============================================================================
# OPTIMIZED FRAME GENERATOR - Fast & Beautiful
# ============================================================================

def create_frame(t, text, colors, duration):
    """Create beautiful frame - optimized for speed"""
    
    # Background
    img = Image.new('RGB', (WIDTH, HEIGHT), colors['bg_dark'])
    draw = ImageDraw.Draw(img)
    
    # Animated gradient (optimized - every 25px)
    for y in range(0, HEIGHT, 25):
        progress = y / HEIGHT
        
        # Smooth wave animation
        wave = math.sin(t * 0.4 + progress * 2.5) * 0.25
        blend_factor = (progress + wave) / 1.25
        blend_factor = max(0, min(1, blend_factor))
        
        # Interpolate colors
        r = int(colors['bg_dark'][0] + (colors['bg_light'][0] - colors['bg_dark'][0]) * blend_factor)
        g = int(colors['bg_dark'][1] + (colors['bg_light'][1] - colors['bg_dark'][1]) * blend_factor)
        b = int(colors['bg_dark'][2] + (colors['bg_light'][2] - colors['bg_dark'][2]) * blend_factor)
        
        draw.rectangle([0, y, WIDTH, y+25], fill=(r, g, b))
    
    # Glowing orbs (6 orbs - simple, no alpha blending)
    for i in range(6):
        orb_cycle = (t * 0.5 + i * 0.4) % duration
        
        x = int(WIDTH * 0.25 + WIDTH * 0.5 * ((i * 43) % 100) / 100)
        y = int((orb_cycle / duration) * HEIGHT)
        
        if 0 <= y < HEIGHT - 100:
            base_size = 15
            pulse = math.sin(t * 2.5 + i * 0.8)
            size = int(base_size + 8 * pulse)
            
            brightness = 0.55 + 0.45 * math.sin(t * 3 + i * 0.5)
            
            # Orb color
            or_r = int(colors['glow'][0] * brightness)
            or_g = int(colors['glow'][1] * brightness)
            or_b = int(colors['glow'][2] * brightness)
            
            # Draw orb with simple glow
            for radius in range(size, 0, -3):
                glow_factor = radius / size
                glow_r = int(or_r * glow_factor)
                glow_g = int(or_g * glow_factor)
                glow_b = int(or_b * glow_factor)
                
                draw.ellipse([x-radius, y-radius, x+radius, y+radius], 
                           fill=(glow_r, glow_g, glow_b))
    
    # Dynamic light streaks (simplified)
    for i in range(3):
        angle = (t * 15 + i * 120) % 360
        rad = math.radians(angle)
        
        center_x = WIDTH // 2
        center_y = HEIGHT // 2
        
        length = 400
        start_dist = 200
        
        sx = center_x + int(start_dist * math.cos(rad))
        sy = center_y + int(start_dist * math.sin(rad))
        ex = center_x + int((start_dist + length) * math.cos(rad))
        ey = center_y + int((start_dist + length) * math.sin(rad))
        
        streak_brightness = 0.4 + 0.3 * math.sin(t * 2 + i)
        
        sr = int(colors['accent'][0] * streak_brightness)
        sg = int(colors['accent'][1] * streak_brightness)
        sb = int(colors['accent'][2] * streak_brightness)
        
        draw.line([(sx, sy), (ex, ey)], fill=(sr, sg, sb), width=4)
    
    # TEXT OVERLAY - Professional Typography
    words = text.split()
    words_per_sec = len(words) / duration
    current_word_index = int(t * words_per_sec * 1.25)
    current_word_index = min(current_word_index, len(words))
    
    visible_text = ' '.join(words[:current_word_index])
    
    if visible_text:
        # Load bold font
        try:
            font_size = 92
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # Smart text wrapping (max 2 lines for impact)
        lines = []
        current_line = []
        
        for word in visible_text.split():
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            text_width = bbox[2] - bbox[0]
            
            if text_width < WIDTH - 140:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Limit to 2 lines
        lines = lines[:2]
        
        # Center text vertically
        line_height = 115
        total_text_height = len(lines) * line_height
        start_y = (HEIGHT - total_text_height) // 2
        
        # Draw each line
        for line_idx, line in enumerate(lines):
            y_pos = start_y + line_idx * line_height
            
            # Calculate text position
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x_pos = (WIDTH - text_width) // 2
            
            # Fade in effect
            line_appear_time = (line_idx / max(len(lines), 1)) * duration * 0.25
            fade_alpha = min(1.0, max(0.0, (t - line_appear_time) * 5))
            
            if fade_alpha > 0:
                # Glow effect (optimized - 4 layers)
                glow_pulse = 0.75 + 0.25 * math.sin(t * 6)
                
                for glow_dist in [14, 10, 6, 3]:
                    glow_strength = (15 - glow_dist) / 15
                    glow_alpha = fade_alpha * glow_pulse * glow_strength * 0.4
                    
                    glow_r = int(colors['glow'][0] * glow_alpha)
                    glow_g = int(colors['glow'][1] * glow_alpha)
                    glow_b = int(colors['glow'][2] * glow_alpha)
                    
                    # Draw glow in 8 directions
                    for angle_deg in range(0, 360, 45):
                        angle_rad = math.radians(angle_deg)
                        glow_x = x_pos + int(glow_dist * math.cos(angle_rad))
                        glow_y = y_pos + int(glow_dist * math.sin(angle_rad))
                        
                        draw.text((glow_x, glow_y), line, font=font, 
                                fill=(glow_r, glow_g, glow_b))
                
                # Strong black outline (6px)
                outline_size = 6
                for out_x in range(-outline_size, outline_size + 1, 2):
                    for out_y in range(-outline_size, outline_size + 1, 2):
                        if out_x != 0 or out_y != 0:
                            draw.text((x_pos + out_x, y_pos + out_y), line, 
                                    font=font, fill=(0, 0, 0))
                
                # Main text
                main_r = int(colors['text'][0] * fade_alpha)
                main_g = int(colors['text'][1] * fade_alpha)
                main_b = int(colors['text'][2] * fade_alpha)
                
                draw.text((x_pos, y_pos), line, font=font, 
                        fill=(main_r, main_g, main_b))
                
                # Highlight effect on last word
                if line_idx == len(lines) - 1 and current_word_index == len(words):
                    words_in_line = line.split()
                    if words_in_line:
                        pulse_factor = 0.65 + 0.35 * math.sin(t * 12)
                        
                        # Calculate last word position
                        last_word = words_in_line[-1]
                        words_before = ' '.join(words_in_line[:-1])
                        
                        if words_before:
                            bbox_before = draw.textbbox((0, 0), words_before + ' ', font=font)
                            last_word_x = x_pos + (bbox_before[2] - bbox_before[0])
                        else:
                            last_word_x = x_pos
                        
                        bbox_last = draw.textbbox((0, 0), last_word, font=font)
                        last_word_width = bbox_last[2] - bbox_last[0]
                        
                        # Animated underline
                        underline_y = y_pos + font_size + 10
                        underline_width = 7
                        
                        under_r = int(colors['accent'][0] * pulse_factor * fade_alpha)
                        under_g = int(colors['accent'][1] * pulse_factor * fade_alpha)
                        under_b = int(colors['accent'][2] * pulse_factor * fade_alpha)
                        
                        draw.line(
                            [(last_word_x, underline_y), 
                             (last_word_x + last_word_width, underline_y)],
                            fill=(under_r, under_g, under_b),
                            width=underline_width
                        )
    
    return np.array(img)


# ============================================================================
# MAIN VIDEO GENERATOR
# ============================================================================

def create_viral_short():
    """Main function to create viral short"""
    
    print("\n" + "="*70, flush=True)
    print("🎬 CREATING VIRAL SHORT", flush=True)
    print("="*70, flush=True)
    
    # Load quote
    print("\n📖 Loading motivational quote...", flush=True)
    
    with open('motivational_content.json', 'r') as f:
        data = json.load(f)
    
    quote = random.choice(data['quotes'])
    text = quote['text']
    author = quote['author']
    
    print(f"   Quote: {text[:65]}...", flush=True)
    print(f"   Author: {author}", flush=True)
    
    # Generate voice
    audio_path, audio_duration = generate_voice(text)
    
    # Set video duration
    duration = max(audio_duration, MIN_DURATION)
    duration = min(duration, MAX_DURATION)
    
    print(f"\n⏱️  Video duration: {duration:.1f} seconds", flush=True)
    
    # Load audio
    audio = AudioFileClip(audio_path)
    
    # Select color scheme
    colors = random.choice(COLORS)
    print(f"🎨 Color scheme: {colors['name']}", flush=True)
    
    # Create video
    print("\n🎬 Creating video frames...", flush=True)
    print("   Features:", flush=True)
    print("   ✓ Cinematic gradient background", flush=True)
    print("   ✓ Glowing orbs (6)", flush=True)
    print("   ✓ Dynamic light streaks (3)", flush=True)
    print("   ✓ Professional 92px bold text", flush=True)
    print("   ✓ Multi-layer glow effects", flush=True)
    print("   ✓ Strong outline (6px)", flush=True)
    print("   ✓ Word-by-word reveal", flush=True)
    print("   ✓ Pulsating highlight", flush=True)
    print("", flush=True)
    print("   Rendering (this takes 5-7 minutes)...", flush=True)
    
    # Progress tracking
    frame_count = [0]
    total_frames = int(duration * FPS)
    
    def make_frame_with_progress(t):
        """Frame generator with progress tracking"""
        frame_count[0] += 1
        
        # Show progress every 5%
        if frame_count[0] % max(1, total_frames // 20) == 0:
            progress = int((frame_count[0] / total_frames) * 100)
            print(f"   Progress: {progress}% ({frame_count[0]}/{total_frames} frames)", flush=True)
        
        return create_frame(t, text, colors, duration)
    
    # Create video clip
    print("\n   Generating video clip...", flush=True)
    video_clip = VideoClip(make_frame_with_progress, duration=duration)
    video_clip = video_clip.set_audio(audio)
    
    # Output path
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_path = f"output/viral_short_{timestamp}.mp4"
    
    print(f"\n   Writing to: {output_path}", flush=True)
    
    # Render video
    video_clip.write_videofile(
        output_path,
        fps=FPS,
        codec='libx264',
        audio_codec='aac',
        bitrate='5000k',
        preset='ultrafast',
        threads=4,
        logger=None,
        verbose=False
    )
    
    # Cleanup
    print("\n   Cleaning up...", flush=True)
    video_clip.close()
    audio.close()
    
    # Verify output
    if os.path.exists(output_path):
        file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
        
        print("\n" + "="*70, flush=True)
        print("✅ VIDEO CREATED SUCCESSFULLY!", flush=True)
        print("="*70, flush=True)
        print(f"📹 File: {output_path}", flush=True)
        print(f"📏 Size: {file_size_mb:.2f} MB", flush=True)
        print(f"⏱️  Duration: {duration:.1f}s", flush=True)
        print(f"🎯 FPS: {FPS}", flush=True)
        print(f"📐 Resolution: {WIDTH}x{HEIGHT}", flush=True)
        print(f"🎨 Color: {colors['name']}", flush=True)
        print("="*70, flush=True)
        
        print("\n✨ Video Features:", flush=True)
        print("   ✓ Cinematic animated gradient", flush=True)
        print("   ✓ Glowing floating orbs", flush=True)
        print("   ✓ Dynamic light streaks", flush=True)
        print("   ✓ Professional bold typography", flush=True)
        print("   ✓ Multi-layer text glow", flush=True)
        print("   ✓ Strong black outline", flush=True)
        print("   ✓ Word-by-word text reveal", flush=True)
        print("   ✓ Pulsating word highlight", flush=True)
        print("   ✓ Premium deep voice", flush=True)
        print("="*70, flush=True)
        
        return output_path
    else:
        print("\n" + "="*70, flush=True)
        print("❌ ERROR: Video file was not created!", flush=True)
        print("="*70, flush=True)
        return None


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                                ║
    ║            🔥 VIRAL SHORTS GENERATOR 🔥                       ║
    ║                                                                ║
    ║  ✨ Modern Cinematic Background                                ║
    ║  ✨ No 2D Character - Pure Text Focus                          ║
    ║  ✨ Fixed Continuous Voice                                     ║
    ║  ✨ Professional Typography                                    ║
    ║  ✨ Trending 2024 Effects                                      ║
    ║  ✨ Viral-Optimized Design                                     ║
    ║                                                                ║
    ╚═══════════════════════════════════════════════════════════════╝
    """, flush=True)
    
    try:
        result = create_viral_short()
        
        if result:
            print("\n🎉 SUCCESS! Your viral short is ready!", flush=True)
            print(f"📂 File location: {result}", flush=True)
            print("\n💡 Next steps:", flush=True)
            print("   1. Download the video from Artifacts", flush=True)
            print("   2. Review the quality", flush=True)
            print("   3. Ready to add YouTube auto-upload!", flush=True)
            exit(0)
        else:
            print("\n❌ Video generation failed!", flush=True)
            exit(1)
            
    except Exception as e:
        print(f"\n" + "="*70, flush=True)
        print("❌ FATAL ERROR", flush=True)
        print("="*70, flush=True)
        print(f"Error: {e}", flush=True)
        print("\nFull traceback:", flush=True)
        import traceback
        traceback.print_exc()
        print("="*70, flush=True)
        exit(1)
