"""
🔥 UPGRADED VIRAL AI MOTIVATION SHORTS 🔥
- Realistic animated characters with lip-sync
- Deep motivational male voice (ElevenLabs)
- Professional text animations
- Background gameplay/video support
- AI photo animation support
- Minimum 20 seconds duration
"""

import os
import json
import random
from datetime import datetime
from pathlib import Path
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import numpy as np
import requests
import math

# ============================================================================
# CONFIGURATION
# ============================================================================

class Config:
    # ElevenLabs API (Free tier - 10,000 chars/month)
    ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY', '')  # Add your key
    ELEVENLABS_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Deep male voice (Rachel)
    # You can use: "pNInz6obpgDQGcFmaJgB" for Adam (deep male)
    
    # Video settings
    WIDTH = 1080
    HEIGHT = 1920
    FPS = 30
    MIN_DURATION = 20  # Minimum 20 seconds
    
    # Text animation style
    TEXT_STYLE = "professional"  # professional, modern, minimal
    
    # Background options
    USE_GAMEPLAY_BG = True  # Set to True to use gameplay/video background
    GAMEPLAY_DIR = "backgrounds"  # Folder with background videos
    
    # AI Character options
    USE_AI_PHOTOS = True  # Use AI-generated character photos
    AI_PHOTOS_DIR = "ai_characters"  # Folder with AI character images


# ============================================================================
# CONTENT MANAGER
# ============================================================================

class ContentManager:
    def __init__(self, json_file='motivational_content.json'):
        self.json_file = json_file
        self.content = self.load_content()
        self.used_ids = set()
    
    def load_content(self):
        with open(self.json_file, 'r') as f:
            return json.load(f)
    
    def get_next_content(self):
        available = [q for q in self.content['quotes'] if q['id'] not in self.used_ids]
        if not available:
            available = self.content['quotes']
        return random.choice(available)


# ============================================================================
# VOICE GENERATOR - Deep Male Voice (ElevenLabs)
# ============================================================================

class VoiceGenerator:
    def __init__(self):
        self.api_key = Config.ELEVENLABS_API_KEY
        self.voice_id = Config.ELEVENLABS_VOICE_ID
        
    def generate_deep_voice(self, text, output_path='voiceover.mp3'):
        """Generate deep male motivational voice using ElevenLabs"""
        
        if not self.api_key:
            print("⚠️ ElevenLabs API key not set, using gTTS fallback")
            return self.generate_gtts_voice(text, output_path)
        
        try:
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"
            
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": self.api_key
            }
            
            data = {
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.75,  # More stable = more consistent
                    "similarity_boost": 0.85,  # Higher = more like original voice
                    "style": 0.5,  # Expressiveness
                    "use_speaker_boost": True
                }
            }
            
            print("🎤 Generating deep motivational voice with ElevenLabs...")
            response = requests.post(url, json=data, headers=headers)
            
            if response.status_code == 200:
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                print(f"✅ Deep voice generated: {output_path}")
                return output_path
            else:
                print(f"⚠️ ElevenLabs error: {response.status_code}, using fallback")
                return self.generate_gtts_voice(text, output_path)
                
        except Exception as e:
            print(f"⚠️ ElevenLabs failed: {e}, using fallback")
            return self.generate_gtts_voice(text, output_path)
    
    def generate_gtts_voice(self, text, output_path):
        """Fallback: Generate voice using gTTS"""
        from gtts import gTTS
        
        # Make it slower and deeper sounding
        tts = gTTS(text=text, lang='en', slow=False, tld='co.uk')  # UK accent = deeper
        tts.save(output_path)
        
        # Try to pitch shift down (make deeper)
        try:
            audio = AudioFileClip(output_path)
            # Speed down slightly to make it sound deeper
            slower_audio = audio.fx(vfx.speedx, 0.9)
            slower_audio.write_audiofile(output_path.replace('.mp3', '_deep.mp3'))
            audio.close()
            slower_audio.close()
            return output_path.replace('.mp3', '_deep.mp3')
        except:
            return output_path


# ============================================================================
# REALISTIC CHARACTER ANIMATOR - With Lip Sync
# ============================================================================

class RealisticCharacterAnimator:
    def __init__(self):
        self.width = Config.WIDTH
        self.height = Config.HEIGHT
        self.ai_photos_dir = Config.AI_PHOTOS_DIR
        
    def get_character_image(self):
        """Get AI character image or create placeholder"""
        if Config.USE_AI_PHOTOS and os.path.exists(self.ai_photos_dir):
            photos = [f for f in os.listdir(self.ai_photos_dir) 
                     if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            if photos:
                photo_path = os.path.join(self.ai_photos_dir, random.choice(photos))
                return Image.open(photo_path).convert('RGBA')
        
        # Create placeholder realistic character
        return self.create_realistic_character()
    
    def create_realistic_character(self):
        """Create a realistic-looking character placeholder"""
        img = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Character position (centered, portrait style)
        center_x = self.width // 2
        center_y = self.height // 2
        
        # Create realistic human silhouette
        # Head (oval)
        head_width = 350
        head_height = 450
        draw.ellipse([
            center_x - head_width//2, center_y - 400,
            center_x + head_width//2, center_y - 400 + head_height
        ], fill='#D4A574')  # Skin tone
        
        # Neck
        neck_width = 150
        draw.rectangle([
            center_x - neck_width//2, center_y - 400 + head_height - 50,
            center_x + neck_width//2, center_y - 400 + head_height + 80
        ], fill='#C9945E')
        
        # Shoulders and torso
        shoulder_width = 500
        torso_height = 600
        draw.ellipse([
            center_x - shoulder_width//2, center_y - 400 + head_height + 30,
            center_x + shoulder_width//2, center_y - 400 + head_height + torso_height
        ], fill='#2C3E50')  # Dark clothing
        
        # Hair
        draw.ellipse([
            center_x - head_width//2 - 20, center_y - 450,
            center_x + head_width//2 + 20, center_y - 250
        ], fill='#1A1A1A')  # Dark hair
        
        # Eyes
        eye_y = center_y - 330
        draw.ellipse([center_x - 100, eye_y, center_x - 50, eye_y + 40], fill='#FFFFFF')
        draw.ellipse([center_x + 50, eye_y, center_x + 100, eye_y + 40], fill='#FFFFFF')
        draw.ellipse([center_x - 85, eye_y + 10, center_x - 65, eye_y + 30], fill='#2C3E50')
        draw.ellipse([center_x + 65, eye_y + 10, center_x + 85, eye_y + 30], fill='#2C3E50')
        
        # Nose
        nose_y = center_y - 270
        draw.polygon([
            (center_x, nose_y),
            (center_x - 20, nose_y + 60),
            (center_x + 20, nose_y + 60)
        ], fill='#BF8F5E')
        
        # Mouth (closed - will animate)
        mouth_y = center_y - 190
        draw.ellipse([center_x - 60, mouth_y, center_x + 60, mouth_y + 25], 
                    fill='#8B4513', outline='#6B3410', width=3)
        
        return img
    
    def animate_character_talking(self, t, audio_duration):
        """Animate character with lip-sync"""
        img = self.get_character_image()
        
        # Resize and position character
        target_height = int(self.height * 0.85)
        aspect_ratio = img.width / img.height
        target_width = int(target_height * aspect_ratio)
        img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
        
        # Create canvas
        canvas = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        
        # Center character
        x_pos = (self.width - target_width) // 2
        y_pos = (self.height - target_height) // 2 + 100  # Slightly lower
        
        # Add subtle breathing/movement
        breath = int(5 * math.sin(t * 2))
        
        # Paste character
        canvas.paste(img, (x_pos, y_pos + breath), img)
        
        # Add lip-sync overlay (mouth movements)
        if t < audio_duration:
            self.add_lip_sync(canvas, t, x_pos + target_width//2, y_pos + int(target_height * 0.6))
        
        # Add subtle glow/highlight
        enhancer = ImageEnhance.Brightness(canvas)
        glow_factor = 1.0 + 0.1 * math.sin(t * 3)
        canvas = enhancer.enhance(glow_factor)
        
        return canvas
    
    def add_lip_sync(self, canvas, t, mouth_x, mouth_y):
        """Add animated mouth movements for speech"""
        draw = ImageDraw.Draw(canvas)
        
        # Mouth animation cycle (opens and closes with speech rhythm)
        mouth_open = abs(math.sin(t * 15))  # Fast mouth movement
        
        if mouth_open > 0.3:
            # Mouth open
            mouth_height = int(15 + 20 * mouth_open)
            draw.ellipse([
                mouth_x - 40, mouth_y - mouth_height//2,
                mouth_x + 40, mouth_y + mouth_height//2
            ], fill=(139, 69, 19, 200))  # Brown mouth
        else:
            # Mouth closed
            draw.ellipse([
                mouth_x - 40, mouth_y - 5,
                mouth_x + 40, mouth_y + 5
            ], fill=(139, 69, 19, 150))


# ============================================================================
# PROFESSIONAL TEXT ANIMATOR
# ============================================================================

class ProfessionalTextAnimator:
    def __init__(self):
        self.width = Config.WIDTH
        self.height = Config.HEIGHT
        
    def create_pro_text_overlay(self, text, t, duration):
        """Create professional motivational-style text"""
        canvas = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(canvas)
        
        # Word-by-word reveal
        words = text.split()
        words_per_second = len(words) / duration
        visible_words = int(t * words_per_second) + 1
        current_text = ' '.join(words[:visible_words])
        
        # Load bold font
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 85)
            author_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 55)
        except:
            font = ImageFont.load_default()
            author_font = font
        
        # Word wrap for multiple lines
        lines = self.wrap_text(current_text, font, draw, self.width - 150)
        
        # Calculate total text height
        line_height = 110
        total_height = len(lines) * line_height
        start_y = 150  # Top third
        
        # Draw each line with animations
        for i, line in enumerate(lines):
            y_pos = start_y + i * line_height
            
            # Fade in animation for each line
            line_appear_time = (i / len(lines)) * duration * 0.3
            alpha = min(255, int((t - line_appear_time) * 500))
            alpha = max(0, alpha)
            
            if alpha > 0:
                # Get text dimensions
                bbox = draw.textbbox((0, 0), line, font=font)
                text_width = bbox[2] - bbox[0]
                x_pos = (self.width - text_width) // 2
                
                # Draw text with outline (for readability)
                # Outline
                for offset_x in [-4, -2, 0, 2, 4]:
                    for offset_y in [-4, -2, 0, 2, 4]:
                        if offset_x != 0 or offset_y != 0:
                            draw.text((x_pos + offset_x, y_pos + offset_y), 
                                    line, font=font, fill=(0, 0, 0, alpha))
                
                # Main text with gradient effect
                colors = [(255, 215, 0, alpha), (255, 165, 0, alpha), (255, 215, 0, alpha)]
                color = colors[i % len(colors)]
                draw.text((x_pos, y_pos), line, font=font, fill=color)
                
                # Add subtle highlight on current word
                if i == len(lines) - 1:
                    glow_size = 10
                    for g in range(glow_size):
                        glow_alpha = int(alpha * 0.1 * (glow_size - g) / glow_size)
                        draw.text((x_pos - g, y_pos), line, font=font, 
                                fill=(255, 255, 255, glow_alpha))
        
        return canvas
    
    def wrap_text(self, text, font, draw, max_width):
        """Wrap text to fit within max_width"""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            width = bbox[2] - bbox[0]
            
            if width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines


# ============================================================================
# BACKGROUND VIDEO MANAGER
# ============================================================================

class BackgroundManager:
    def __init__(self):
        self.gameplay_dir = Config.GAMEPLAY_DIR
        
    def get_background_video(self, duration):
        """Get gameplay/background video"""
        if not Config.USE_GAMEPLAY_BG or not os.path.exists(self.gameplay_dir):
            return self.create_gradient_background(duration)
        
        # Get random gameplay video
        videos = [f for f in os.listdir(self.gameplay_dir) 
                 if f.lower().endswith(('.mp4', '.avi', '.mov'))]
        
        if not videos:
            return self.create_gradient_background(duration)
        
        video_path = os.path.join(self.gameplay_dir, random.choice(videos))
        
        try:
            clip = VideoFileClip(video_path)
            
            # Resize to fit (crop to 9:16)
            clip = clip.resize(height=Config.HEIGHT)
            
            # Center crop to width
            if clip.w > Config.WIDTH:
                x_center = clip.w // 2
                clip = clip.crop(x1=x_center - Config.WIDTH//2,
                               x2=x_center + Config.WIDTH//2)
            
            # Loop if needed
            if clip.duration < duration:
                clip = clip.loop(duration=duration)
            else:
                clip = clip.subclip(0, duration)
            
            # Dim the background (so text is readable)
            clip = clip.fx(vfx.colorx, 0.4)  # 40% brightness
            clip = clip.fx(vfx.lum_contrast, contrast=0.1)  # Low contrast
            
            return clip
            
        except Exception as e:
            print(f"⚠️ Could not load background video: {e}")
            return self.create_gradient_background(duration)
    
    def create_gradient_background(self, duration):
        """Create animated gradient background"""
        def make_frame(t):
            img = Image.new('RGB', (Config.WIDTH, Config.HEIGHT), '#000000')
            draw = ImageDraw.Draw(img)
            
            # Animated gradient
            for y in range(Config.HEIGHT):
                progress = y / Config.HEIGHT
                # Color shift over time
                r = int(20 + 40 * math.sin(t * 0.5 + progress * 2))
                g = int(10 + 30 * math.sin(t * 0.3 + progress * 3))
                b = int(40 + 60 * math.sin(t * 0.4 + progress))
                
                draw.line([(0, y), (Config.WIDTH, y)], fill=(r, g, b))
            
            return np.array(img)
        
        return VideoClip(make_frame, duration=duration)


# ============================================================================
# UPGRADED VIDEO GENERATOR
# ============================================================================

class UpgradedVideoGenerator:
    def __init__(self):
        self.voice_gen = VoiceGenerator()
        self.char_animator = RealisticCharacterAnimator()
        self.text_animator = ProfessionalTextAnimator()
        self.bg_manager = BackgroundManager()
        
    def create_viral_short(self, content):
        """Create upgraded viral short"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = f"output/viral_short_{timestamp}.mp4"
        os.makedirs('output', exist_ok=True)
        
        print(f"\n🎬 Creating UPGRADED viral short...")
        print(f"📝 Quote: {content['text'][:60]}...")
        
        try:
            # Generate deep voice
            audio_path = self.voice_gen.generate_deep_voice(content['text'])
            
            # Get audio duration
            audio_clip = AudioFileClip(audio_path)
            audio_duration = max(audio_clip.duration, Config.MIN_DURATION)
            
            print(f"⏱️  Video duration: {audio_duration:.1f} seconds")
            
            # Create background
            print("🎨 Creating background...")
            background = self.bg_manager.get_background_video(audio_duration)
            
            # Create character overlay
            print("👤 Animating character...")
            def make_character_frame(t):
                return np.array(self.char_animator.animate_character_talking(t, audio_duration))
            
            character_clip = VideoClip(make_character_frame, duration=audio_duration).set_pos(('center', 'center'))
            
            # Create text overlay
            print("✍️  Creating text animations...")
            def make_text_frame(t):
                return np.array(self.text_animator.create_pro_text_overlay(content['text'], t, audio_duration))
            
            text_clip = VideoClip(make_text_frame, duration=audio_duration).set_pos(('center', 'top'))
            
            # Composite everything
            print("🎞️  Compositing layers...")
            final_video = CompositeVideoClip([
                background,
                character_clip.set_opacity(0.95),
                text_clip
            ], size=(Config.WIDTH, Config.HEIGHT))
            
            # Add audio
            final_video = final_video.set_audio(audio_clip)
            
            # Export
            print("📹 Rendering final video...")
            final_video.write_videofile(
                output_path,
                fps=Config.FPS,
                codec='libx264',
                audio_codec='aac',
                preset='medium',
                threads=4,
                logger=None
            )
            
            # Cleanup
            background.close()
            character_clip.close()
            text_clip.close()
            final_video.close()
            audio_clip.close()
            
            file_size = os.path.getsize(output_path) / (1024*1024)
            print(f"\n✅ SUCCESS!")
            print(f"📹 Video: {output_path}")
            print(f"📏 Size: {file_size:.2f} MB")
            print(f"⏱️  Duration: {audio_duration:.1f}s")
            
            return output_path
            
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
            return None


# ============================================================================
# MAIN - TEST SINGLE VIDEO
# ============================================================================

if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║      🔥 UPGRADED VIRAL SHORTS GENERATOR 🔥                    ║
    ║                                                                ║
    ║  ✨ Realistic animated characters                              ║
    ║  🎤 Deep motivational voice (ElevenLabs)                      ║
    ║  ✍️  Professional text animations                              ║
    ║  🎮 Background video support                                   ║
    ║  ⏱️  Minimum 20 seconds duration                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    
    try:
        os.makedirs('output', exist_ok=True)
        
        content_mgr = ContentManager()
        video_gen = UpgradedVideoGenerator()
        
        content = content_mgr.get_next_content()
        
        video_path = video_gen.create_viral_short(content)
        
        if video_path:
            print("\n🎉 Video generation complete!")
        else:
            print("\n❌ Video generation failed")
            exit(1)
            
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
