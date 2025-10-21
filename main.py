"""
📖 STORY-BASED MOTIVATIONAL SHORTS GENERATOR
Creates emotional storytelling videos with:
- Scene-by-scene narration
- Visual storytelling elements
- Background music (40% volume)
- Emotional pacing
- Like "The Last Message" style
"""

print("🎬 Story-Based Shorts Generator Starting...")

import os
import json
import random
from datetime import datetime
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import math
import requests

print("✅ Libraries loaded")

# ============================================================================
# CONFIG
# ============================================================================

WIDTH = 1080
HEIGHT = 1920
FPS = 30

# ElevenLabs
API_KEYS = [
    os.getenv('ELEVEN_API_KEY_1', ''),
    os.getenv('ELEVEN_API_KEY_2', ''),
    os.getenv('ELEVEN_API_KEY_3', '')
]
VOICE_ID = 'pNInz6obpgDQGcFmaJgB'  # Deep emotional voice

os.makedirs('output', exist_ok=True)
os.makedirs('music', exist_ok=True)

# ============================================================================
# STORY SCENES DATABASE
# ============================================================================

STORY_SCENES = {
    "the_last_message": {
        "title": "The Last Message",
        "scenes": [
            {
                "time": [0, 5],
                "narration": "I ignored his call... I was busy chasing success. I thought I'd call back later.",
                "visual": "phone_ringing",
                "emotion": "regret_building"
            },
            {
                "time": [5, 10],
                "narration": "Later never came. That night, he met with an accident... and I never got to say goodbye.",
                "visual": "clock_ticking",
                "emotion": "shock"
            },
            {
                "time": [10, 20],
                "narration": "We always think we have more time. But time... doesn't wait.",
                "visual": "regret_face",
                "emotion": "deep_sadness"
            },
            {
                "time": [20, 30],
                "narration": "So call them now. Text them now. Don't wait for 'later'. Because sometimes, later... becomes never.",
                "visual": "sunrise_hope",
                "emotion": "hopeful_message"
            }
        ]
    },
    
    "the_empty_chair": {
        "title": "The Empty Chair",
        "scenes": [
            {
                "time": [0, 7],
                "narration": "She said 'I'm fine' with a smile. But her eyes... her eyes told a different story.",
                "visual": "fake_smile",
                "emotion": "hidden_pain"
            },
            {
                "time": [7, 15],
                "narration": "I didn't ask twice. I just nodded and walked away. I assumed she'd tell me if something was really wrong.",
                "visual": "walking_away",
                "emotion": "regret"
            },
            {
                "time": [15, 25],
                "narration": "Three days later, I found out. She wasn't fine. She needed someone... and I wasn't there.",
                "visual": "empty_chair",
                "emotion": "deep_regret"
            },
            {
                "time": [25, 30],
                "narration": "Sometimes 'I'm fine' is the biggest cry for help. Ask again. Look deeper. Be there.",
                "visual": "caring_hands",
                "emotion": "lesson_learned"
            }
        ]
    },
    
    "the_last_goodbye": {
        "title": "The Last Goodbye",
        "scenes": [
            {
                "time": [0, 6],
                "narration": "I was angry. We fought over something so small, I can't even remember what it was.",
                "visual": "argument",
                "emotion": "anger"
            },
            {
                "time": [6, 12],
                "narration": "I slammed the door and left. I thought I'd come back tomorrow... when things cooled down.",
                "visual": "door_slam",
                "emotion": "frustration"
            },
            {
                "time": [12, 20],
                "narration": "But tomorrow... tomorrow never came for them. And that fight... became our last conversation.",
                "visual": "empty_room",
                "emotion": "crushing_regret"
            },
            {
                "time": [20, 28],
                "narration": "Life is too short for anger. Too precious for grudges. Say I love you... before it's too late.",
                "visual": "forgiveness",
                "emotion": "powerful_lesson"
            }
        ]
    }
}

# ============================================================================
# VOICE GENERATOR
# ============================================================================

def generate_emotional_voice(text):
    """Generate emotional narration voice"""
    print("\n🎤 Generating emotional voice...")
    
    # Try ElevenLabs for better emotion
    for key in [k for k in API_KEYS if k]:
        try:
            print("   Using ElevenLabs...")
            r = requests.post(
                f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
                json={
                    "text": text,
                    "model_id": "eleven_multilingual_v2",
                    "voice_settings": {
                        "stability": 0.60,  # Lower for more emotion
                        "similarity_boost": 0.80,
                        "style": 0.85,  # Higher style for emotional delivery
                        "use_speaker_boost": True
                    }
                },
                headers={"xi-api-key": key},
                timeout=30
            )
            
            if r.status_code == 200:
                with open('narration.mp3', 'wb') as f:
                    f.write(r.content)
                
                from moviepy.editor import AudioFileClip
                audio = AudioFileClip('narration.mp3')
                dur = audio.duration
                audio.close()
                
                print(f"   ✅ Emotional voice ready ({dur:.1f}s)")
                return 'narration.mp3', dur
        except Exception as e:
            print(f"   ⚠️ {e}")
    
    # Fallback
    print("   Using gTTS...")
    from gtts import gTTS
    tts = gTTS(text, lang='en', slow=True)  # Slow for emotional impact
    tts.save('narration.mp3')
    
    from moviepy.editor import AudioFileClip
    audio = AudioFileClip('narration.mp3')
    dur = audio.duration
    audio.close()
    
    print(f"   ✅ Voice ready ({dur:.1f}s)")
    return 'narration.mp3', dur

# ============================================================================
# BACKGROUND MUSIC
# ============================================================================

def get_background_music():
    """Get sad/emotional background music"""
    
    # Check if music exists
    if os.path.exists('music') and os.listdir('music'):
        music_files = [f for f in os.listdir('music') if f.endswith('.mp3')]
        if music_files:
            return os.path.join('music', random.choice(music_files))
    
    print("   ⚠️ No background music found in music/ folder")
    print("   Add emotional piano/sad music MP3 files to music/ folder")
    return None

# ============================================================================
# SCENE VISUAL GENERATOR
# ============================================================================

def create_scene_visual(t, scene_type, emotion, text_to_show, duration):
    """Create visual for specific scene type"""
    
    img = Image.new('RGB', (WIDTH, HEIGHT), (15, 15, 20))
    draw = ImageDraw.Draw(img)
    
    # Emotional color schemes
    colors = {
        "regret_building": {'bg': (20, 15, 25), 'dark': (10, 5, 15), 'accent': (120, 80, 150)},
        "shock": {'bg': (25, 10, 10), 'dark': (15, 5, 5), 'accent': (180, 50, 50)},
        "deep_sadness": {'bg': (10, 10, 20), 'dark': (5, 5, 10), 'accent': (80, 80, 120)},
        "hopeful_message": {'bg': (15, 20, 30), 'dark': (25, 35, 50), 'accent': (100, 150, 200)},
        "hidden_pain": {'bg': (18, 12, 20), 'dark': (10, 5, 12), 'accent': (100, 70, 110)},
        "regret": {'bg': (20, 12, 15), 'dark': (12, 7, 9), 'accent': (130, 80, 95)},
        "deep_regret": {'bg': (12, 12, 18), 'dark': (6, 6, 10), 'accent': (90, 90, 130)},
        "lesson_learned": {'bg': (18, 22, 28), 'dark': (28, 35, 45), 'accent': (110, 140, 180)},
        "anger": {'bg': (25, 8, 8), 'dark': (15, 4, 4), 'accent': (160, 40, 40)},
        "frustration": {'bg': (22, 10, 8), 'dark': (14, 6, 4), 'accent': (140, 60, 40)},
        "crushing_regret": {'bg': (8, 8, 12), 'dark': (4, 4, 6), 'accent': (70, 70, 100)},
        "powerful_lesson": {'bg': (20, 24, 30), 'dark': (32, 40, 52), 'accent': (120, 150, 190)},
    }
    
    color_scheme = colors.get(emotion, colors['deep_sadness'])
    
    # Emotional gradient
    for y in range(0, HEIGHT, 30):
        p = y / HEIGHT
        wave = math.sin(t * 0.3 + p * 2) * 0.2
        blend = (p + wave) / 1.2
        
        r = int(color_scheme['dark'][0] + (color_scheme['bg'][0] - color_scheme['dark'][0]) * blend)
        g = int(color_scheme['dark'][1] + (color_scheme['bg'][1] - color_scheme['dark'][1]) * blend)
        b = int(color_scheme['dark'][2] + (color_scheme['bg'][2] - color_scheme['dark'][2]) * blend)
        
        draw.rectangle([0, y, WIDTH, y+30], fill=(r, g, b))
    
    # Visual elements based on scene
    if scene_type == "phone_ringing":
        # Phone icon glow
        cx = WIDTH // 2
        cy = int(HEIGHT * 0.65)
        
        pulse = 0.6 + 0.4 * math.sin(t * 3)
        size = int(100 + 30 * pulse)
        
        # Phone shape
        draw.rounded_rectangle([cx-size//2, cy-size, cx+size//2, cy+size], 
                              radius=20, fill=(40, 40, 50))
        
        # Screen glow
        screen_size = int(size * 0.7)
        for i in range(10, 0, -2):
            alpha = int(pulse * 255 * i / 10)
            glow_r = int(color_scheme['accent'][0] * alpha / 255)
            glow_g = int(color_scheme['accent'][1] * alpha / 255)
            glow_b = int(color_scheme['accent'][2] * alpha / 255)
            
            draw.ellipse([cx-screen_size-i, cy-screen_size//2-i, 
                         cx+screen_size+i, cy+screen_size//2+i],
                        outline=(glow_r, glow_g, glow_b))
    
    elif scene_type == "clock_ticking":
        # Clock hands
        cx = WIDTH // 2
        cy = int(HEIGHT * 0.65)
        
        radius = 120
        
        # Clock circle
        draw.ellipse([cx-radius, cy-radius, cx+radius, cy+radius],
                    outline=color_scheme['accent'], width=8)
        
        # Hour hand
        angle = (t * 30) % 360
        rad = math.radians(angle - 90)
        ex = cx + int(radius * 0.5 * math.cos(rad))
        ey = cy + int(radius * 0.5 * math.sin(rad))
        draw.line([(cx, cy), (ex, ey)], fill=color_scheme['accent'], width=8)
        
        # Minute hand
        angle2 = (t * 180) % 360
        rad2 = math.radians(angle2 - 90)
        ex2 = cx + int(radius * 0.8 * math.cos(rad2))
        ey2 = cy + int(radius * 0.8 * math.sin(rad2))
        draw.line([(cx, cy), (ex2, ey2)], fill=color_scheme['accent'], width=6)
    
    elif scene_type == "empty_chair":
        # Simple chair silhouette
        cx = WIDTH // 2
        cy = int(HEIGHT * 0.7)
        
        fade = 0.5 + 0.5 * math.sin(t * 0.5)
        
        # Chair
        chair_color = tuple(int(c * fade) for c in color_scheme['accent'])
        
        # Seat
        draw.rectangle([cx-80, cy-30, cx+80, cy], fill=chair_color)
        # Back
        draw.rectangle([cx-80, cy-150, cx-60, cy-30], fill=chair_color)
        draw.rectangle([cx+60, cy-150, cx+80, cy-30], fill=chair_color)
        draw.rectangle([cx-80, cy-150, cx+80, cy-130], fill=chair_color)
    
    # TEXT OVERLAY - Emotional Typography
    if text_to_show:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 75)
        except:
            font = ImageFont.load_default()
        
        # Wrap text
        words = text_to_show.split()
        lines = []
        current = []
        
        for word in words:
            test = ' '.join(current + [word])
            bbox = draw.textbbox((0, 0), test, font=font)
            if bbox[2] - bbox[0] < WIDTH - 140:
                current.append(word)
            else:
                if current:
                    lines.append(' '.join(current))
                current = [word]
        if current:
            lines.append(' '.join(current))
        
        lines = lines[:3]
        
        # Position text
        line_height = 95
        total_height = len(lines) * line_height
        start_y = HEIGHT - total_height - 200
        
        for i, line in enumerate(lines):
            y = start_y + i * line_height
            
            bbox = draw.textbbox((0, 0), line, font=font)
            tw = bbox[2] - bbox[0]
            x = (WIDTH - tw) // 2
            
            # Soft glow
            for g in [8, 5, 3]:
                for ox, oy in [(-g,0), (g,0), (0,-g), (0,g)]:
                    draw.text((x+ox, y+oy), line, font=font, 
                            fill=(40, 40, 50))
            
            # Black outline
            for ox in [-4, -2, 0, 2, 4]:
                for oy in [-4, -2, 0, 2, 4]:
                    if ox or oy:
                        draw.text((x+ox, y+oy), line, font=font, fill=(0, 0, 0))
            
            # Main text
            draw.text((x, y), line, font=font, fill=(240, 240, 245))
    
    return np.array(img)

# ============================================================================
# STORY VIDEO GENERATOR
# ============================================================================

def create_story_video():
    """Create story-based motivational video"""
    
    print("\n" + "="*60)
    print("📖 CREATING STORY-BASED MOTIVATIONAL SHORT")
    print("="*60)
    
    # Select story
    story_key = random.choice(list(STORY_SCENES.keys()))
    story = STORY_SCENES[story_key]
    
    print(f"\n📚 Story: {story['title']}")
    
    # Combine all narrations
    full_narration = " ".join([scene['narration'] for scene in story['scenes']])
    
    print(f"📝 Full script: {len(full_narration)} characters")
    
    # Generate voice
    audio_path, audio_duration = generate_emotional_voice(full_narration)
    
    duration = max(audio_duration, 25)
    duration = min(duration, 35)
    
    print(f"⏱️  Video duration: {duration:.1f}s")
    
    # Load narration audio
    from moviepy.editor import AudioFileClip, CompositeAudioClip
    
    narration_audio = AudioFileClip(audio_path)
    
    # Add background music (40% volume)
    bg_music_path = get_background_music()
    
    if bg_music_path:
        print("🎵 Adding background music (40% volume)...")
        bg_music = AudioFileClip(bg_music_path)
        bg_music = bg_music.volumex(0.4)  # 40% volume
        bg_music = bg_music.set_duration(duration)
        
        # Composite: Narration + Background music
        final_audio = CompositeAudioClip([narration_audio, bg_music])
    else:
        final_audio = narration_audio
    
    print("\n🎬 Rendering scenes...")
    
    frame_count = [0]
    total_frames = int(duration * FPS)
    
    def make_story_frame(t):
        """Generate frame based on current scene"""
        
        frame_count[0] += 1
        if frame_count[0] % 30 == 0:
            pct = int((frame_count[0] / total_frames) * 100)
            print(f"   Progress: {pct}%")
        
        # Find current scene
        current_scene = story['scenes'][0]
        for scene in story['scenes']:
            scene_start = scene['time'][0]
            scene_end = scene['time'][1]
            
            # Scale scene times to video duration
            scaled_start = (scene_start / 30) * duration
            scaled_end = (scene_end / 30) * duration
            
            if scaled_start <= t < scaled_end:
                current_scene = scene
                break
        
        # Get text to show (split narration into parts)
        text_words = current_scene['narration'].split()
        scene_duration = scaled_end - scaled_start
        scene_time = t - scaled_start
        
        words_to_show = int((scene_time / scene_duration) * len(text_words))
        words_to_show = min(words_to_show, len(text_words))
        
        text_to_show = ' '.join(text_words[:words_to_show])
        
        return create_scene_visual(
            t, 
            current_scene['visual'],
            current_scene['emotion'],
            text_to_show,
            duration
        )
    
    print("Creating video clip...")
    from moviepy.editor import VideoClip
    
    video = VideoClip(make_story_frame, duration=duration)
    video = video.set_audio(final_audio)
    
    output = f"output/story_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
    
    print(f"\nRendering to: {output}")
    print("This takes 4-6 minutes...\n")
    
    video.write_videofile(
        output,
        fps=FPS,
        codec='libx264',
        audio_codec='aac',
        preset='ultrafast',
        bitrate='4500k',
        threads=4,
        logger=None,
        verbose=False
    )
    
    video.close()
    narration_audio.close()
    if bg_music_path:
        bg_music.close()
    
    if os.path.exists(output):
        size = os.path.getsize(output) / (1024*1024)
        print("\n" + "="*60)
        print("✅ STORY VIDEO CREATED!")
        print("="*60)
        print(f"📹 {output}")
        print(f"📏 {size:.1f} MB")
        print(f"⏱️  {duration:.1f}s")
        print(f"📚 Story: {story['title']}")
        print("="*60)
        return output
    else:
        print("\n❌ FAILED")
        return None

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════════════╗
    ║  📖 STORY-BASED MOTIVATIONAL SHORTS                   ║
    ║                                                        ║
    ║  ✨ Emotional storytelling                            ║
    ║  ✨ Scene-by-scene visuals                           ║
    ║  ✨ Background music (40%)                           ║
    ║  ✨ Deep emotional voice                             ║
    ║  ✨ Like "The Last Message"                          ║
    ╚═══════════════════════════════════════════════════════╝
    """)
    
    result = create_story_video()
    
    if result:
        print("\n🎉 SUCCESS!")
        print("\n💡 Tips:")
        print("   - Add emotional piano/sad music to music/ folder")
        print("   - Music will auto-play at 40% volume")
        print("   - Add more stories to STORY_SCENES dictionary")
    else:
        print("\n❌ FAILED")
        exit(1)
