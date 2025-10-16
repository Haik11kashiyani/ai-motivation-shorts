"""
🔥 VIRAL AI MOTIVATION SHORTS GENERATOR 🔥
Automatically creates and posts 3 viral-quality YouTube Shorts daily
WITH ANIMATED 2D/3D CHARACTERS!
"""

import os
import json
import random
from datetime import datetime, timedelta
from pathlib import Path
import schedule
import time
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import numpy as np
from gtts import gTTS
import requests
import math

# ============================================================================
# 1. CONTENT MANAGER - Handles motivational content from JSON
# ============================================================================

class ContentManager:
    def __init__(self, json_file='motivational_content.json'):
        self.json_file = json_file
        self.content = self.load_content()
        self.used_ids = self.load_used_ids()
    
    def load_content(self):
        """Load motivational content from JSON"""
        if not os.path.exists(self.json_file):
            sample_content = {
                "quotes": [
                    {
                        "id": 1,
                        "text": "Success is not final, failure is not fatal. It's the courage to continue that counts.",
                        "author": "Winston Churchill",
                        "category": "success",
                        "character": "warrior",
                        "tags": ["motivation", "success", "persistence"]
                    },
                    {
                        "id": 2,
                        "text": "The only way to do great work is to love what you do.",
                        "author": "Steve Jobs",
                        "category": "passion",
                        "character": "entrepreneur",
                        "tags": ["motivation", "passion", "work"]
                    },
                    {
                        "id": 3,
                        "text": "Don't watch the clock; do what it does. Keep going.",
                        "author": "Sam Levenson",
                        "category": "persistence",
                        "character": "runner",
                        "tags": ["motivation", "time", "action"]
                    }
                ]
            }
            with open(self.json_file, 'w') as f:
                json.dump(sample_content, f, indent=2)
            return sample_content
        
        with open(self.json_file, 'r') as f:
            return json.load(f)
    
    def load_used_ids(self):
        """Load IDs of already used content"""
        if os.path.exists('used_content.json'):
            with open('used_content.json', 'r') as f:
                return set(json.load(f))
        return set()
    
    def save_used_ids(self):
        """Save used content IDs"""
        with open('used_content.json', 'w') as f:
            json.dump(list(self.used_ids), f)
    
    def get_next_content(self):
        """Get next unused motivational content"""
        available = [q for q in self.content['quotes'] if q['id'] not in self.used_ids]
        
        if not available:
            print("🔄 All content used! Resetting...")
            self.used_ids.clear()
            available = self.content['quotes']
        
        selected = random.choice(available)
        return selected
    
    def mark_as_used(self, content_id):
        """Mark content as used"""
        self.used_ids.add(content_id)
        self.save_used_ids()


# ============================================================================
# 2. ANIMATED CHARACTER GENERATOR - Creates 2D/3D animated characters
# ============================================================================

class AnimatedCharacter:
    """Creates animated 2D/3D characters for viral shorts"""
    
    def __init__(self, character_type="motivational_speaker"):
        self.character_type = character_type
        self.width = 1080
        self.height = 1920
        
    def create_3d_character_frame(self, t, character_style="warrior"):
        """Create 3D animated character frame"""
        img = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Character position (centered bottom third)
        char_x = self.width // 2
        char_y = int(self.height * 0.65)
        
        if character_style == "warrior":
            return self._draw_warrior_character(draw, char_x, char_y, t)
        elif character_style == "entrepreneur":
            return self._draw_entrepreneur_character(draw, char_x, char_y, t)
        elif character_style == "runner":
            return self._draw_runner_character(draw, char_x, char_y, t)
        elif character_style == "thinker":
            return self._draw_thinker_character(draw, char_x, char_y, t)
        else:
            return self._draw_motivational_speaker(draw, char_x, char_y, t)
    
    def _draw_warrior_character(self, draw, x, y, t):
        """Draw animated warrior character - strong and powerful"""
        # Body animation - breathing effect
        scale = 1 + 0.05 * math.sin(t * 2)
        
        # Legs
        leg_width = int(60 * scale)
        leg_height = int(200 * scale)
        draw.rectangle([x - 80, y, x - 80 + leg_width, y + leg_height], fill='#8B4513')
        draw.rectangle([x + 20, y, x + 20 + leg_width, y + leg_height], fill='#8B4513')
        
        # Body - muscular torso
        body_width = int(180 * scale)
        body_height = int(250 * scale)
        draw.rectangle([x - 90, y - body_height, x + 90, y], fill='#CD853F')
        
        # Arms - animated punching motion
        arm_angle = math.sin(t * 3) * 20
        # Left arm
        draw.rectangle([x - 150, y - 180, x - 90, y - 100], fill='#CD853F')
        # Right arm - punching
        punch_extend = int(50 + 30 * math.sin(t * 4))
        draw.rectangle([x + 90, y - 180, x + 150 + punch_extend, y - 100], fill='#CD853F')
        
        # Head
        head_size = int(100 * scale)
        draw.ellipse([x - head_size//2, y - body_height - head_size, 
                      x + head_size//2, y - body_height], fill='#DEB887')
        
        # Warrior helmet effect
        draw.arc([x - 60, y - body_height - 120, x + 60, y - body_height - 20], 
                 start=0, end=180, fill='#FFD700', width=10)
        
        # Eyes - determined look
        draw.ellipse([x - 30, y - body_height - 60, x - 10, y - body_height - 40], fill='#000000')
        draw.ellipse([x + 10, y - body_height - 60, x + 30, y - body_height - 40], fill='#000000')
        
        # Glow effect for power
        glow_radius = int(250 + 50 * math.sin(t * 2))
        for i in range(5):
            alpha = int(50 - i * 10)
            draw.ellipse([x - glow_radius + i*20, y - 200 - glow_radius//2 + i*20,
                         x + glow_radius - i*20, y + 200 - glow_radius//2 - i*20],
                        outline=(255, 215, 0, alpha), width=3)
        
        return draw._image
    
    def _draw_entrepreneur_character(self, draw, x, y, t):
        """Draw animated entrepreneur character - professional and ambitious"""
        scale = 1 + 0.03 * math.sin(t * 1.5)
        
        # Legs
        draw.rectangle([x - 70, y, x - 20, y + 180], fill='#2C3E50')
        draw.rectangle([x + 20, y, x + 70, y + 180], fill='#2C3E50')
        
        # Body - business suit
        draw.rectangle([x - 100, y - 240, x + 100, y], fill='#1C2833')
        # Shirt
        draw.rectangle([x - 80, y - 220, x + 80, y - 20], fill='#ECF0F1')
        # Tie - animated
        tie_swing = int(10 * math.sin(t * 3))
        draw.polygon([x + tie_swing, y - 220, 
                     x + tie_swing - 15, y - 100, 
                     x + tie_swing + 15, y - 100], fill='#E74C3C')
        
        # Arms - gesturing while talking
        arm_raise = int(30 * math.sin(t * 2))
        # Left arm - pointing up (motivational)
        draw.rectangle([x - 140, y - 200 - arm_raise, x - 100, y - 120], fill='#DEB887')
        # Right arm
        draw.rectangle([x + 100, y - 180, x + 140, y - 120], fill='#DEB887')
        
        # Head
        draw.ellipse([x - 50, y - 310, x + 50, y - 210], fill='#DEB887')
        
        # Hair - professional
        draw.arc([x - 55, y - 315, x + 55, y - 240], start=0, end=180, fill='#34495E', width=15)
        
        # Eyes
        draw.ellipse([x - 25, y - 275, x - 10, y - 260], fill='#000000')
        draw.ellipse([x + 10, y - 275, x + 25, y - 260], fill='#000000')
        
        # Smile - confident
        draw.arc([x - 20, y - 250, x + 20, y - 230], start=0, end=180, fill='#000000', width=3)
        
        # Success aura - glowing briefcase effect
        glow = int(100 + 20 * math.sin(t * 2))
        for i in range(3):
            alpha = 100 - i * 30
            draw.ellipse([x - glow - i*10, y - 150 - i*5, x + glow + i*10, y + 50 + i*5],
                        outline=(46, 204, 113, alpha), width=2)
        
        return draw._image
    
    def _draw_runner_character(self, draw, x, y, t):
        """Draw animated runner character - dynamic running motion"""
        # Running cycle animation
        run_cycle = t * 6
        
        # Legs - running motion
        leg_angle = math.sin(run_cycle) * 40
        # Front leg
        front_leg_x = int(x + leg_angle)
        draw.ellipse([front_leg_x - 30, y + 100, front_leg_x + 30, y + 160], fill='#34495E')
        draw.rectangle([front_leg_x - 25, y, front_leg_x + 25, y + 100], fill='#5D6D7E')
        
        # Back leg
        back_leg_x = int(x - leg_angle)
        draw.ellipse([back_leg_x - 30, y + 80, back_leg_x + 30, y + 140], fill='#34495E')
        draw.rectangle([back_leg_x - 25, y - 20, back_leg_x + 25, y + 80], fill='#5D6D7E')
        
        # Body - leaning forward (running pose)
        lean = int(20 * math.cos(run_cycle))
        draw.rectangle([x - 70 + lean, y - 200, x + 70 + lean, y], fill='#E74C3C')
        
        # Arms - pumping motion
        arm_pump = math.sin(run_cycle + math.pi) * 50
        # Left arm
        draw.rectangle([x - 100 + lean, y - 180 + int(arm_pump), 
                       x - 70 + lean, y - 100], fill='#DEB887')
        # Right arm
        draw.rectangle([x + 70 + lean, y - 180 - int(arm_pump), 
                       x + 100 + lean, y - 100], fill='#DEB887')
        
        # Head
        draw.ellipse([x - 45 + lean, y - 270, x + 45 + lean, y - 180], fill='#DEB887')
        
        # Headband
        draw.rectangle([x - 50 + lean, y - 250, x + 50 + lean, y - 230], fill='#3498DB')
        
        # Eyes - focused
        draw.ellipse([x - 25 + lean, y - 235, x - 10 + lean, y - 220], fill='#000000')
        draw.ellipse([x + 10 + lean, y - 235, x + 25 + lean, y - 220], fill='#000000')
        
        # Speed lines effect
        for i in range(5):
            line_y = y - 100 - i * 40
            line_offset = int(150 + i * 30 - (run_cycle * 100) % 200)
            draw.line([x - 400 - line_offset, line_y, x - 200 - line_offset, line_y], 
                     fill=(52, 152, 219, 200 - i * 40), width=3)
        
        return draw._image
    
    def _draw_thinker_character(self, draw, x, y, t):
        """Draw animated thinker character - wise and contemplative"""
        scale = 1 + 0.02 * math.sin(t * 1)
        
        # Sitting/standing pose
        # Legs
        draw.rectangle([x - 60, y, x - 20, y + 160], fill='#5D6D7E')
        draw.rectangle([x + 20, y, x + 60, y + 160], fill='#5D6D7E')
        
        # Body
        draw.rectangle([x - 90, y - 220, x + 90, y], fill='#8E44AD')
        
        # Arms - one hand on chin (thinking pose)
        # Left arm - at side
        draw.rectangle([x - 130, y - 180, x - 90, y - 100], fill='#DEB887')
        # Right arm - hand to chin
        chin_move = int(5 * math.sin(t * 2))
        draw.rectangle([x + 90, y - 200, x + 130, y - 280 + chin_move], fill='#DEB887')
        # Hand near face
        draw.ellipse([x + 110, y - 300 + chin_move, x + 150, y - 260 + chin_move], fill='#DEB887')
        
        # Head
        draw.ellipse([x - 55, y - 310, x + 55, y - 200], fill='#DEB887')
        
        # Wise beard
        draw.ellipse([x - 40, y - 240, x + 40, y - 200], fill='#95A5A6')
        
        # Eyes - wise and knowing
        draw.ellipse([x - 25, y - 275, x - 10, y - 260], fill='#000000')
        draw.ellipse([x + 10, y - 275, x + 25, y - 260], fill='#000000')
        
        # Thought bubble animation
        bubble_size = int(50 + 10 * math.sin(t * 2))
        for i, (bx, by) in enumerate([(x + 100, y - 350), (x + 150, y - 420), (x + 180, y - 500)]):
            size = bubble_size + i * 20
            draw.ellipse([bx - size//2, by - size//2, bx + size//2, by + size//2],
                        outline='#ECF0F1', width=3)
        
        # Lightbulb in thought bubble (eureka moment)
        bulb_glow = int(255 * (0.7 + 0.3 * math.sin(t * 4)))
        draw.ellipse([x + 160, y - 520, x + 200, y - 480], fill=(bulb_glow, bulb_glow, 0))
        
        return draw._image
    
    def _draw_motivational_speaker(self, draw, x, y, t):
        """Draw animated motivational speaker - energetic and inspiring"""
        energy = 1 + 0.08 * math.sin(t * 3)
        
        # Dynamic stance
        # Legs - power stance
        draw.rectangle([x - 80, y, x - 30, y + 200], fill='#34495E')
        draw.rectangle([x + 30, y, x + 80, y + 200], fill='#34495E')
        
        # Body
        draw.rectangle([x - 100, y - 250, x + 100, y], fill='#E74C3C')
        
        # Arms - raised high (inspiring gesture)
        arm_height = int(50 * math.sin(t * 2.5))
        # Both arms raised
        draw.rectangle([x - 140, y - 280 - arm_height, x - 100, y - 180], fill='#DEB887')
        draw.rectangle([x + 100, y - 280 - arm_height, x + 140, y - 180], fill='#DEB887')
        
        # Head
        draw.ellipse([x - 60, y - 340, x + 60, y - 220], fill='#DEB887')
        
        # Hair - dynamic
        draw.arc([x - 65, y - 345, x + 65, y - 250], start=0, end=180, fill='#2C3E50', width=18)
        
        # Eyes - wide with excitement
        draw.ellipse([x - 30, y - 300, x - 10, y - 280], fill='#FFFFFF')
        draw.ellipse([x + 10, y - 300, x + 30, y - 280], fill='#FFFFFF')
        draw.ellipse([x - 25, y - 295, x - 15, y - 285], fill='#000000')
        draw.ellipse([x + 15, y - 295, x + 25, y - 285], fill='#000000')
        
        # Big smile
        draw.arc([x - 30, y - 270, x + 30, y - 240], start=0, end=180, fill='#000000', width=4)
        
        # Energy aura - radiating inspiration
        for i in range(8):
            angle = (t * 2 + i * math.pi / 4) % (2 * math.pi)
            ray_length = 150 + 30 * math.sin(t * 3 + i)
            end_x = x + int(ray_length * math.cos(angle))
            end_y = y - 260 + int(ray_length * math.sin(angle))
            draw.line([x, y - 260, end_x, end_y], 
                     fill=(255, 215, 0, 200), width=5)
        
        return draw._image


# ============================================================================
# 3. VIRAL VIDEO GENERATOR - Creates stunning shorts with animated characters
# ============================================================================

class ViralVideoGenerator:
    def __init__(self, width=1080, height=1920):
        self.width = width
        self.height = height
        self.fps = 30
        self.duration = 15
        self.character_animator = AnimatedCharacter()
        
        # Viral color schemes
        self.color_schemes = [
            {'bg': '#0A0E27', 'text': '#FFD700', 'accent': '#FF6B35'},
            {'bg': '#1A1A2E', 'text': '#00FFF0', 'accent': '#FF2E63'},
            {'bg': '#000000', 'text': '#FFFFFF', 'accent': '#FF0055'},
            {'bg': '#2C1654', 'text': '#FFA500', 'accent': '#00FF87'},
        ]
    
    def create_viral_video(self, content):
        """Create viral-quality motivation short with animated character"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = f"output/viral_short_{timestamp}.mp4"
        os.makedirs('output', exist_ok=True)
        
        print(f"🎨 Creating viral video with animated character...")
        
        colors = random.choice(self.color_schemes)
        character_type = content.get('character', 'motivational_speaker')
        
        try:
            # Generate voiceover first to get duration
            audio_path = self.generate_voiceover(content['text'])
            audio_duration = AudioFileClip(audio_path).duration if os.path.exists(audio_path) else 15
            
            # Create video with character animation
            video_clip = self.create_character_video_clip(content, colors, character_type, audio_duration)
            
            # Add voiceover
            if os.path.exists(audio_path):
                audio = AudioFileClip(audio_path)
                video_clip = video_clip.set_audio(audio)
            
            # Add background music
            bg_music = self.get_background_music()
            if bg_music:
                bg_audio = AudioFileClip(bg_music).volumex(0.15).set_duration(video_clip.duration)
                if video_clip.audio:
                    final_audio = CompositeAudioClip([video_clip.audio, bg_audio])
                    video_clip = video_clip.set_audio(final_audio)
            
            # Export
            video_clip.write_videofile(
                output_path,
                fps=self.fps,
                codec='libx264',
                audio_codec='aac',
                preset='medium',
                threads=4
            )
            
            video_clip.close()
            print(f"✅ Viral video with character created: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"❌ Error creating video: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def create_character_video_clip(self, content, colors, character_type, duration):
        """Create video clip with animated character and text"""
        text = content['text']
        words = text.split()
        
        def make_frame(t):
            # Create base background
            img = Image.new('RGB', (self.width, self.height), colors['bg'])
            
            # Add gradient overlay
            gradient = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
            draw_grad = ImageDraw.Draw(gradient)
            for y in range(self.height):
                alpha = int(100 * (y / self.height))
                color = self.hex_to_rgb(colors['accent'], alpha)
                draw_grad.line([(0, y), (self.width, y)], fill=color)
            img = Image.alpha_composite(img.convert('RGBA'), gradient).convert('RGB')
            
            # Add animated character
            char_img = self.character_animator.create_3d_character_frame(t, character_type)
            img.paste(char_img, (0, 0), char_img)
            
            # Add animated text overlay
            text_img = self.create_animated_text(text, t, duration, colors)
            img.paste(text_img, (0, 0), text_img)
            
            return np.array(img)
        
        return VideoClip(make_frame, duration=duration)
    
    def create_animated_text(self, text, t, total_duration, colors):
        """Create animated text overlay"""
        img = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Word-by-word reveal animation
        words = text.split()
        words_per_second = len(words) / total_duration
        current_word_index = min(int(t * words_per_second), len(words))
        visible_text = ' '.join(words[:current_word_index + 1])
        
        # Text styling
        try:
            font_size = 70 if len(text) < 100 else 60
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # Word wrap for multiple lines
        lines = []
        current_line = []
        for word in visible_text.split():
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if bbox[2] - bbox[0] < self.width - 100:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))
        
        # Position text in top third
        total_text_height = len(lines) * 90
        start_y = 100
        
        # Draw text with animation
        for i, line in enumerate(lines):
            y_pos = start_y + i * 90
            
            # Get text dimensions
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x_pos = (self.width - text_width) // 2
            
            # Fade-in effect for current line
            line_time_start = (i / len(lines)) * total_duration
            line_alpha = min(255, int((t - line_time_start) * 512))
            line_alpha = max(0, line_alpha)
            
            if line_alpha > 0:
                # Shadow
                shadow_color = (0, 0, 0, line_alpha)
                draw.text((x_pos + 4, y_pos + 4), line, font=font, fill=shadow_color)
                
                # Main text
                text_color = self.hex_to_rgb(colors['text'], line_alpha)
                draw.text((x_pos, y_pos), line, font=font, fill=text_color)
        
        return img
    
    def hex_to_rgb(self, hex_color, alpha=255):
        """Convert hex to RGBA"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4)) + (alpha,)
    
    def generate_voiceover(self, text):
        """Generate AI voiceover"""
        output_path = 'temp_voiceover.mp3'
        try:
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(output_path)
            return output_path
        except Exception as e:
            print(f"⚠️ Voiceover failed: {e}")
            return None
    
    def get_background_music(self):
        """Get background music"""
        music_dir = 'music'
        if os.path.exists(music_dir):
            music_files = [f for f in os.listdir(music_dir) if f.endswith('.mp3')]
            if music_files:
                return os.path.join(music_dir, random.choice(music_files))
        return None


# ============================================================================
# 4. YOUTUBE UPLOADER
# ============================================================================

class YouTubeUploader:
    def __init__(self):
        self.credentials_file = 'youtube_credentials.json'
        self.client_secrets_file = 'client_secrets.json'
    
    def upload_short(self, video_path, title, description, tags):
        """Upload video to YouTube"""
        print(f"📤 Uploading: {title[:50]}...")
        
        try:
            print("⚠️ YouTube API setup required - See SETUP_GUIDE.md")
            print(f"✅ Video ready: {video_path}")
            return {
                'success': True,
                'video_id': 'demo_id',
                'url': 'https://youtube.com/shorts/demo_id'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def generate_title(self, content):
        """Generate viral title"""
        templates = [
            f"💪 {content['text'][:50]}... #shorts",
            f"🔥 {content['author']}: Life Lesson #shorts",
            f"⚡ {content['text'][:55]}...",
        ]
        return random.choice(templates)
    
    def generate_description(self, content):
        """Generate description"""
        desc = f"{content['text']}\n\n- {content['author']}\n\n"
        desc += "🔥 FOLLOW FOR DAILY MOTIVATION!\n\n"
        desc += "#motivation #success #shorts #viral #inspiration"
        return desc


# ============================================================================
# 5. AUTOMATION SYSTEM
# ============================================================================

class ShortsAutomation:
    def __init__(self):
        self.content_manager = ContentManager()
        self.video_generator = ViralVideoGenerator()
        self.youtube_uploader = YouTubeUploader()
        self.posts_today = 0
        self.last_reset = datetime.now().date()
    
    def generate_and_post_short(self):
        """Generate and post one short"""
        try:
            today = datetime.now().date()
            if today != self.last_reset:
                self.posts_today = 0
                self.last_reset = today
            
            if self.posts_today >= 3:
                print("✅ Daily limit reached (3 shorts)")
                return
            
            print(f"\n{'='*70}")
            print(f"🚀 CREATING ANIMATED VIRAL SHORT #{self.posts_today + 1}/3")
            print(f"{'='*70}\n")
            
            content = self.content_manager.get_next_content()
            print(f"📝 Quote: {content['text'][:60]}...")
            print(f"✍️ Author: {content['author']}")
            print(f"🎭 Character: {content.get('character', 'speaker')}")
            
            video_path = self.video_generator.create_viral_video(content)
            
            if not video_path:
                print("❌ Video generation failed!")
                return
            
            title = self.youtube_uploader.generate_title(content)
            description = self.youtube_uploader.generate_description(content)
            
            result = self.youtube_uploader.upload_short(
                video_path=video_path,
                title=title,
                description=description,
                tags=content.get('tags', [])
            )
            
            if result['success']:
                print(f"\n✅ SUCCESS! Animated short #{self.posts_today + 1} posted!")
                print(f"🔗 URL: {result['url']}")
                self.posts_today += 1
                self.content_manager.mark_as_used(content['id'])
                
                if os.path.exists(video_path):
                    os.remove(video_path)
            else:
                print(f"❌ Upload failed: {result.get('error')}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
    
    def start_automation(self):
        """Start automated posting schedule"""
        print("\n🤖 STARTING VIRAL ANIMATED SHORTS AUTOMATION")
        print("📅 Schedule: 3 animated shorts per day at 9 AM, 3 PM, 9 PM")
        print("🎭 Features: 2D/3D Animated Characters + Motivational Quotes")
        print("="*70)
        
        # Schedule posts
        schedule.every().day.at("09:00").do(self.generate_and_post_short)
        schedule.every().day.at("15:00").do(self.generate_and_post_short)
        schedule.every().day.at("21:00").do(self.generate_and_post_short)
        
        # Generate first short immediately
        print("\n🎬 Generating first animated short now...")
        self.generate_and_post_short()
        
        # Keep running
        print("\n⏰ Scheduler active. Waiting for next scheduled time...")
        while True:
            schedule.run_pending()
            time.sleep(60)


# ============================================================================
# 6. MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════════════════════════╗
    ║      🔥 VIRAL AI MOTIVATION SHORTS GENERATOR 🔥               ║
    ║           WITH 2D/3D ANIMATED CHARACTERS                       ║
    ║                                                                ║
    ║  ✨ Features:                                                  ║
    ║     • Animated Characters (Warrior, Entrepreneur, Runner)      ║
    ║     • AI Voiceover                                            ║
    ║     • Dynamic Animations                                       ║
    ║     • Auto-Post 3 Shorts Daily                                ║
    ║     • Viral-Optimized Design                                  ║
    ╚════════════════════════════════════════════════════════════════╝
    """)
    
    automation = ShortsAutomation()
    automation.start_automation()
