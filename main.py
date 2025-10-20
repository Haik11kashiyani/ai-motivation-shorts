"""
🎬 MODERN STUNNING VIRAL SHORTS 2024 🎬
✨ No characters - Pure cinematic text focus
✨ Fixed continuous voice
✨ Modern trending effects
✨ Professional typography
✨ Viral-optimized design
"""

import sys
import os
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', buffering=1)

print("🎬 STARTING MODERN VIRAL SHORTS GENERATOR...", flush=True)

import json
import random
from datetime import datetime
from moviepy.editor import VideoClip, AudioFileClip, CompositeAudioClip
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import requests
import math

print("✅ Libraries loaded!", flush=True)

# ============================================================================
# CONFIGURATION - Modern & Trending
# ============================================================================

WIDTH = 1080
HEIGHT = 1920
FPS = 30
MIN_DURATION = 15
MAX_DURATION = 25

# ElevenLabs API
API_KEYS = [
    os.getenv('ELEVEN_API_KEY_1', ''),
    os.getenv('ELEVEN_API_KEY_2', ''),
    os.getenv('ELEVEN_API_KEY_3', '')
]

# BEST voices for virality
VOICES = {
    'deep_male': 'pNInz6obpgDQGcFmaJgB',     # Adam - Most viral
    'powerful': 'VR6AewLTigWG4xSOukaG',      # Arnold - Strong
    'smooth': 'yoZ06aMxZJJ28mfd3POQ',        # Sam - Smooth
}

# Modern 2024 trending color schemes
MODERN_COLORS = [
    {
        'name': 'Neon Gold',
        'bg_start': (10, 10, 15),
        'bg_end': (30, 25, 0),
        'text_primary': (255, 223, 0),
        'text_secondary': (255, 255, 255),
        'accent': (255, 180, 0),
        'glow': (255, 215, 0)
    },
    {
        'name': 'Electric Blue',
        'bg_start': (5, 10, 20),
        'bg_end': (10, 20, 40),
        'text_primary': (0, 255, 255),
        'text_secondary': (255, 255, 255),
        'accent': (0, 200, 255),
        'glow': (100, 200, 255)
    },
    {
        'name': 'Fire Red',
        'bg_start': (20, 5, 5),
        'bg_end': (40, 10, 0),
        'text_primary': (255, 50, 50),
        'text_secondary': (255, 255, 255),
        'accent': (255, 100, 0),
        'glow': (255, 150, 100)
    },
    {
        'name': 'Royal Purple',
        'bg_start': (15, 5, 25),
        'bg_end': (30, 10, 50),
        'text_primary': (200, 100, 255),
        'text_secondary': (255, 255, 255),
        'accent': (180, 50, 255),
        'glow': (220, 150, 255)
    },
]

os.makedirs('output', exist_ok=True)

# ============================================================================
# FIXED VOICE GENERATOR - Continuous Audio
# ============================================================================

def generate_continuous_voice(text):
    """Generate CONTINUOUS voice that doesn't stop"""
    print("\n🎤 Generating continuous voice...", flush=True)
    
    # Try ElevenLabs
    for i, key in enumerate([k for k in API_KEYS if k]):
        try:
            print(f"   Attempt {i+1}: ElevenLabs API...", flush=True)
            
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICES['deep_male']}"
            
            response = requests.post(
                url,
                json={
                    "text": text,
                    "model_id": "eleven_multilingual_v2",
                    "voice_settings": {
                        "stability": 0.75,              # More stable = continuous
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
                timeout=30
            )
            
            if response.status_code == 200:
                with open('voice.mp3', 'wb') as f:
                    f.write(response.content)
                
                # Verify audio
                audio = AudioFileClip('voice.mp3')
                duration = audio.duration
                audio.close()
                
                if duration > 3:  # Must be at least 3 seconds
                    print(f"   ✅ Premium voice generated! ({duration:.1f}s)", flush=True)
                    return 'voice.mp3', duration
                else:
                    print(f"   ⚠️ Audio too short ({duration:.1f}s)", flush=True)
                    
        except Exception as e:
            print(f"   ⚠️ Error: {e}", flush=True)
    
    # Enhanced gTTS fallback
    print("   Using enhanced gTTS...", flush=True)
    from gtts import gTTS
    
    # Use slower speech for better quality
    tts = gTTS(text=text, lang='en', slow=False, tld='co.uk')
    tts.save('voice_base.mp3')
    
    # Load and check duration
    audio = AudioFileClip('voice_base.mp3')
    duration = audio.duration
    audio.close()
    
    print(f"   ✅ Voice generated! ({duration:.1f}s)", flush=True)
    return 'voice_base.mp3', duration


# ============================================================================
# MODERN BACKGROUND - Trending 2024 Style
# ============================================================================

def create_modern_background(t, colors, duration):
    """Create modern trending background with depth"""
    img = Image.new('RGB', (WIDTH, HEIGHT), colors['bg_start'])
    draw = ImageDraw.Draw(img)
    
    # Multi-layer gradient (trending effect)
    for y in range(HEIGHT):
        progress = y / HEIGHT
        
        # Animated waves for depth
        wave1 = math.sin(t * 0.4 + progress * 3) * 0.2
        wave2 = math.cos(t * 0.3 + progress * 2) * 0.15
        blend = (progress + wave1 + wave2) / 1.35
        blend = max(0, min(1, blend))
        
        # Interpolate colors
        r = int(colors['bg_start'][0] + (colors['bg_end'][0] - colors['bg_start'][0]) * blend)
        g = int(colors['bg_start'][1] + (colors['bg_end'][1] - colors['bg_start'][1]) * blend)
        b = int(colors['bg_start'][2] + (colors['bg_end'][2] - colors['bg_start'][2]) * blend)
        
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))
    
    # Modern light rays (trending effect)
    num_rays = 5
    for i in range(num_rays):
        angle = (t * 10 + i * 360/num_rays) % 360
        rad = math.radians(angle)
        
        # Ray properties
        length = HEIGHT * 1.5
        width = 80
        
        # Calculate ray position
        center_x = WIDTH // 2
        center_y = HEIGHT // 2
        
        start_x = center_x + int(300 * math.cos(rad))
        start_y = center_y + int(300 * math.sin(rad))
        end_x = center_x + int(length * math.cos(rad))
        end_y = center_y + int(length * math.sin(rad))
        
        # Ray opacity
        opacity = int(20 + 15 * math.sin(t * 2 + i))
        
        # Draw ray with gradient
        for w in range(width, 0, -5):
            alpha = int(opacity * (width - w) / width)
            ray_color = colors['accent'] + (alpha,)
            
            # Create polygon for ray
            perp_x = -math.sin(rad) * w/2
            perp_y = math.cos(rad) * w/2
            
            points = [
                (start_x + perp_x, start_y + perp_y),
                (start_x - perp_x, start_y - perp_y),
                (end_x - perp_x, end_y - perp_y),
                (end_x + perp_x, end_y + perp_y)
            ]
            
            # Draw on separate layer
            ray_img = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
            ray_draw = ImageDraw.Draw(ray_img)
            ray_draw.polygon(points, fill=ray_color)
            
            # Blend with main image
            img = Image.alpha_composite(img.convert('RGBA'), ray_img).convert('RGB')
    
    # Floating orbs (modern aesthetic)
    for i in range(8):
        cycle = (t * 0.4 + i * 0.4) % duration
        
        x = int(WIDTH * 0.2 + WIDTH * 0.6 * ((i * 67) % 100) / 100)
        y = int((cycle / duration) * HEIGHT)
        
        if 0 <= y < HEIGHT - 50:
            size = int(15 + 10 * math.sin(t * 2 + i))
            brightness = 0.5 + 0.5 * math.sin(t * 3 + i * 0.7)
            
            # Orb with glow
            for r in range(size, 0, -3):
                alpha = int(200 * brightness * (size - r) / size)
                orb_color = colors['glow'] + (alpha,)
                
                orb_img = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
                orb_draw = ImageDraw.Draw(orb_img)
                orb_draw.ellipse([x-r, y-r, x+r, y+r], fill=orb_color)
                
                img = Image.alpha_composite(img.convert('RGBA'), orb_img).convert('RGB')
    
    return img


# ============================================================================
# MODERN TEXT - Viral Typography 2024
# ============================================================================

def create_modern_text(t, text, colors, duration):
    """Create modern viral-style text"""
    img = Image.new('RGB', (WIDTH, HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Word-by-word reveal (keeps attention)
    words = text.split()
    words_per_second = len(words) / duration
    current_word = int(t * words_per_second * 1.2)
    current_word = min(current_word, len(words))
    
    visible_text = ' '.join(words[:current_word])
    
    if not visible_text:
        return img
    
    # Load modern font (bold, impactful)
    try:
        # Try to use a bold font
        font_main = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 95)
    except:
        font_main = ImageFont.load_default()
    
    # Smart text wrapping (max 2 lines for impact)
    lines = []
    current_line = []
    
    for word in visible_text.split():
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font_main)
        
        if bbox[2] - bbox[0] < WIDTH - 140:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    
    if current_line:
        lines.append(' '.join(current_line))
    
    # Max 2 lines for modern clean look
    lines = lines[:2]
    
    # Center vertically
    line_height = 125
    total_height = len(lines) * line_height
    start_y = (HEIGHT - total_height) // 2
    
    for i, line in enumerate(lines):
        y_pos = start_y + i * line_height
        
        # Get text dimensions
        bbox = draw.textbbox((0, 0), line, font=font_main)
        text_width = bbox[2] - bbox[0]
        x_pos = (WIDTH - text_width) // 2
        
        # Fade in per line
        line_start = (i / max(len(lines), 1)) * duration * 0.3
        fade = min(1.0, max(0.0, (t - line_start) * 4))
        
        if fade > 0:
            # Modern glow effect (subtle but impactful)
            glow_intensity = 0.8 + 0.2 * math.sin(t * 5)
            
            # Multiple glow layers
            for glow_size in range(20, 0, -4):
                glow_alpha = int(fade * 100 * glow_intensity * (20 - glow_size) / 20)
                
                gr = int(colors['glow'][0] * glow_alpha / 255)
                gg = int(colors['glow'][1] * glow_alpha / 255)
                gb = int(colors['glow'][2] * glow_alpha / 255)
                
                # Draw glow
                for angle in range(0, 360, 45):
                    rad = math.radians(angle)
                    ox = int(glow_size * math.cos(rad))
                    oy = int(glow_size * math.sin(rad))
                    draw.text((x_pos + ox, y_pos + oy), line, font=font_main, fill=(gr, gg, gb))
            
            # Strong black outline (modern style)
            outline_width = 8
            for ox in range(-outline_width, outline_width + 1, 2):
                for oy in range(-outline_width, outline_width + 1, 2):
                    if ox or oy:
                        draw.text((x_pos + ox, y_pos + oy), line, font=font_main, fill=(0, 0, 0))
            
            # Main text with gradient effect
            # Draw main color
            text_r = int(colors['text_primary'][0] * fade)
            text_g = int(colors['text_primary'][1] * fade)
            text_b = int(colors['text_primary'][2] * fade)
            
            draw.text((x_pos, y_pos), line, font=font_main, fill=(text_r, text_g, text_b))
            
            # Highlight effect on current word
            if i == len(lines) - 1:  # Last line
                words_in_line = line.split()
                if words_in_line and current_word == len(text.split()):
                    # Pulsating underline
                    pulse = 0.7 + 0.3 * math.sin(t * 10)
                    
                    # Get last word position
                    last_word = words_in_line[-1]
                    words_before = ' '.join(words_in_line[:-1])
                    
                    if words_before:
                        bbox_before = draw.textbbox((0, 0), words_before + ' ', font=font_main)
                        last_x = x_pos + (bbox_before[2] - bbox_before[0])
                    else:
                        last_x = x_pos
                    
                    bbox_word = draw.textbbox((0, 0), last_word, font=font_main)
                    word_width = bbox_word[2] - bbox_word[0]
                    
                    # Modern underline with glow
                    underline_y = y_pos + 105
                    underline_thickness = 8
                    
                    ur = int(colors['accent'][0] * pulse * fade)
                    ug = int(colors['accent'][1] * pulse * fade)
                    ub = int(colors['accent'][2] * pulse * fade)
                    
                    # Glowing underline
                    for thick in range(underline_thickness, 0, -2):
                        alpha = int(pulse * fade * 255 * thick / underline_thickness)
                        draw.line(
                            [(last_x, underline_y), (last_x + word_width, underline_y)],
                            fill=(ur, ug, ub, alpha), width=thick
                        )
    
    return img


# ============================================================================
# MAIN VIDEO GENERATOR
# ============================================================================

def create_modern_viral_short():
    """Generate modern stunning viral short"""
    
    print("\n" + "="*70, flush=True)
    print("🎬 MODERN STUNNING VIRAL SHORTS 2024", flush=True)
    print("="*70, flush=True)
    
    print("\n📖 Loading quote...", flush=True)
    with open('motivational_content.json', 'r') as f:
        data = json.load(f)
    
    quote = random.choice(data['quotes'])
    text = quote['text']
    author = quote['author']
    
    print(f"   Quote: {text[:60]}...", flush=True)
    print(f"   Author: {author}", flush=True)
    
    # Generate continuous voice
    audio_path, audio_duration = generate_continuous_voice(text)
    
    # Set duration based on audio
    duration = max(audio_duration, MIN_DURATION)
    duration = min(duration, MAX_DURATION)
    
    print(f"\n⏱️  Video duration: {duration:.1f}s", flush=True)
    
    # Load audio
    audio = AudioFileClip(audio_path)
    
    # Select modern color scheme
    colors = random.choice(MODERN_COLORS)
    print(f"🎨 Color scheme: {colors['name']}", flush=True)
    
    # Create video
    print("\n🎬 Creating modern video...", flush=True)
    print("   ✨ Cinematic gradient background", flush=True)
    print("   ✨ Modern light rays", flush=True)
    print("   ✨ Floating orbs", flush=True)
    print("   ✨ Viral typography", flush=True)
    print("   ✨ Dynamic text effects", flush=True)
    print("", flush=True)
    print("   Rendering (3-4 minutes)...", flush=True)
    
    frame_count = [0]  # Use list to modify in nested function
    total_frames = duration * FPS
    
    def make_frame(t):
        # Progress indicator
        frame_count[0] += 1
        if frame_count[0] % 30 == 0:
            progress = int((frame_count[0] / total_frames) * 100)
            print(f"   Progress: {progress}%", flush=True)
        
        # Create background
        bg = create_modern_background(t, colors, duration)
        bg_array = np.array(bg)
        
        # Create text overlay
        text_img = create_modern_text(t, text, colors, duration)
        text_array = np.array(text_img)
        
        # Blend text (where not black)
        text_mask = np.any(text_array > 20, axis=2)
        bg_array[text_mask] = text_array[text_mask]
        
        return bg_array
    
    # Create video clip
    video_clip = VideoClip(make_frame, duration=duration)
    video_clip = video_clip.set_audio(audio)
    
    # Output path
    output_path = f"output/modern_viral_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
    
    # Render
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
    video_clip.close()
    audio.close()
    
    # Verify
    if os.path.exists(output_path):
        file_size = os.path.getsize(output_path) / (1024 * 1024)
        
        print("\n" + "="*70, flush=True)
        print("✅ MODERN VIRAL SHORT CREATED!", flush=True)
        print("="*70, flush=True)
        print(f"📹 File: {output_path}", flush=True)
        print(f"📏 Size: {file_size:.2f} MB", flush=True)
        print(f"⏱️  Duration: {duration:.1f}s", flush=True)
        print(f"🎨 Style: {colors['name']}", flush=True)
        print("", flush=True)
        print("✨ Modern Features:", flush=True)
        print("   ✓ Cinematic gradient", flush=True)
        print("   ✓ Light rays animation", flush=True)
        print("   ✓ Floating orbs", flush=True)
        print("   ✓ 95px bold typography", flush=True)
        print("   ✓ Multi-layer glow", flush=True)
        print("   ✓ Strong outlines", flush=True)
        print("   ✓ Word-by-word reveal", flush=True)
        print("   ✓ Pulsating highlights", flush=True)
        print("   ✓ Continuous voice", flush=True)
        print("="*70, flush=True)
        
        return output_path
    else:
        print("\n❌ ERROR: File not created!", flush=True)
        return None


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                                ║
    ║           🎬 MODERN STUNNING VIRAL SHORTS 2024 🎬             ║
    ║                                                                ║
    ║  ✨ No Characters - Pure Cinematic Focus                       ║
    ║  ✨ Fixed Continuous Voice                                     ║
    ║  ✨ Modern Trending Effects                                    ║
    ║  ✨ Professional Typography                                    ║
    ║  ✨ Viral-Optimized Design                                     ║
    ║                                                                ║
    ╚═══════════════════════════════════════════════════════════════╝
    """, flush=True)
    
    try:
        result = create_modern_viral_short()
        
        if result:
            print("\n🎉 SUCCESS! Modern viral short ready!", flush=True)
            print(f"📂 {result}", flush=True)
            exit(0)
        else:
            print("\n❌ FAILED!", flush=True)
            exit(1)
            
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}", flush=True)
        import traceback
        traceback.print_exc()
        exit(1)
