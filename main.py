"""
🔥 VIRAL AI MOTIVATION SHORTS GENERATOR - TEST VERSION 🔥
This version generates ONE test video without scheduling
"""

import os
import json
import random
from datetime import datetime
from pathlib import Path
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from gtts import gTTS
import math

# ============================================================================
# CONTENT MANAGER
# ============================================================================

class ContentManager:
    def __init__(self, json_file='motivational_content.json'):
        self.json_file = json_file
        self.content = self.load_content()
        self.used_ids = set()
    
    def load_content(self):
        """Load motivational content from JSON"""
        with open(self.json_file, 'r') as f:
            return json.load(f)
    
    def get_next_content(self):
        """Get next unused motivational content"""
        available = [q for q in self.content['quotes'] if q['id'] not in self.used_ids]
        
        if not available:
            available = self.content['quotes']
        
        selected = random.choice(available)
        return selected


# ============================================================================
# ANIMATED CHARACTER
# ============================================================================

class AnimatedCharacter:
    """Creates animated 2D/3D characters"""
    
    def __init__(self):
        self.width = 1080
        self.height = 1920
        
    def create_3d_character_frame(self, t, character_style="warrior"):
        """Create 3D animated character frame"""
        img = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
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
        """Draw animated warrior character"""
        scale = 1 + 0.05 * math.sin(t * 2)
        
        # Legs
        leg_width = int(60 * scale)
        leg_height = int(200 * scale)
        draw.rectangle([x - 80, y, x - 80 + leg_width, y + leg_height], fill='#8B4513')
        draw.rectangle([x + 20, y, x + 20 + leg_width, y + leg_height], fill='#8B4513')
        
        # Body
        body_width = int(180 * scale)
        body_height = int(250 * scale)
        draw.rectangle([x - 90, y - body_height, x + 90, y], fill='#CD853F')
        
        # Arms
        arm_angle = math.sin(t * 3) * 20
        draw.rectangle([x - 150, y - 180, x - 90, y - 100], fill='#CD853F')
        punch_extend = int(50 + 30 * math.sin(t * 4))
        draw.rectangle([x + 90, y - 180, x + 150 + punch_extend, y - 100], fill='#CD853F')
        
        # Head
        head_size = int(100 * scale)
        draw.ellipse([x - head_size//2, y - body_height - head_size, 
                      x + head_size//2, y - body_height], fill='#DEB887')
        
        # Eyes
        draw.ellipse([x - 30, y - body_height - 60, x - 10, y - body_height - 40], fill='#000000')
        draw.ellipse([x + 10, y - body_height - 60, x + 30, y - body_height - 40], fill='#000000')
        
        # Glow effect
        glow_radius = int(250 + 50 * math.sin(t * 2))
        for i in range(5):
            alpha = int(50 - i * 10)
            draw.ellipse([x - glow_radius + i*20, y - 200 - glow_radius//2 + i*20,
                         x + glow_radius - i*20, y + 200 - glow_radius//2 - i*20],
                        outline=(255, 215, 0, alpha), width=3)
        
        return draw._image
    
    def _draw_entrepreneur_character(self, draw, x, y, t):
        """Draw entrepreneur character"""
        # Simplified version for speed
        draw.rectangle([x - 70, y, x - 20, y + 180], fill='#2C3E50')
        draw.rectangle([x + 20, y, x + 70, y + 180], fill='#2C3E50')
        draw.rectangle([x - 100, y - 240, x + 100, y], fill='#1C2833')
        draw.ellipse([x - 50, y - 310, x + 50, y - 200], fill='#DEB887')
        draw.ellipse([x - 25, y - 275, x - 10, y - 260], fill='#000000')
        draw.ellipse([x + 10, y - 275, x + 25, y - 260], fill='#000000')
        return draw._image
    
    def _draw_runner_character(self, draw, x, y, t):
        """Draw runner character"""
        run_cycle = t * 6
        leg_angle = math.sin(run_cycle) * 40
        
        # Legs
        front_leg_x = int(x + leg_angle)
        draw.ellipse([front_leg_x - 30, y + 100, front_leg_x + 30, y + 160], fill='#34495E')
        draw.rectangle([front_leg_x - 25, y, front_leg_x + 25, y + 100], fill='#5D6D7E')
        
        # Body
        lean = int(20 * math.cos(run_cycle))
        draw.rectangle([x - 70 + lean, y - 200, x + 70 + lean, y], fill='#E74C3C')
        
        # Head
        draw.ellipse([x - 45 + lean, y - 270, x + 45 + lean, y - 180], fill='#DEB887')
        draw.ellipse([x - 25 + lean, y - 235, x - 10 + lean, y - 220], fill='#000000')
        draw.ellipse([x + 10 + lean, y - 235, x + 25 + lean, y - 220], fill='#000000')
        
        return draw._image
    
    def _draw_thinker_character(self, draw, x, y, t):
        """Draw thinker character"""
        draw.rectangle([x - 60, y, x - 20, y + 160], fill='#5D6D7E')
        draw.rectangle([x + 20, y, x + 60, y + 160], fill='#5D6D7E')
        draw.rectangle([x - 90, y - 220, x + 90, y], fill='#8E44AD')
        draw.ellipse([x - 55, y - 310, x + 55, y - 200], fill='#DEB887')
        draw.ellipse([x - 25, y - 275, x - 10, y - 260], fill='#000000')
        draw.ellipse([x + 10, y - 275, x + 25, y - 260], fill='#000000')
        return draw._image
    
    def _draw_motivational_speaker(self, draw, x, y, t):
        """Draw motivational speaker"""
        energy = 1 + 0.08 * math.sin(t * 3)
        
        draw.rectangle([x - 80, y, x - 30, y + 200], fill='#34495E')
        draw.rectangle([x + 30, y, x + 80, y + 200], fill='#34495E')
        draw.rectangle([x - 100, y - 250, x + 100, y], fill='#E74C3C')
        
        arm_height = int(50 * math.sin(t * 2.5))
        draw.rectangle([x - 140, y - 280 - arm_height, x - 100, y - 180], fill='#DEB887')
        draw.rectangle([x + 100, y - 280 - arm_height, x + 140, y - 180], fill='#DEB887')
        
        draw.ellipse([x - 60, y - 340, x + 60, y - 220], fill='#DEB887')
        draw.ellipse([x - 30, y - 300, x - 10, y - 280], fill='#FFFFFF')
        draw.ellipse([x + 10, y - 300, x + 30, y - 280], fill='#FFFFFF')
        draw.ellipse([x - 25, y - 295, x - 15, y - 285], fill='#000000')
        draw.ellipse([x + 15, y - 295, x + 25, y - 285], fill='#000000')
        
        return draw._image


# ============================================================================
# VIDEO GENERATOR
# ============================================================================

class ViralVideoGenerator:
    def __init__(self, width=1080, height=1920):
        self.width = width
        self.height = height
        self.fps = 30
        self.duration = 12  # Shorter for testing
        self.character_animator = AnimatedCharacter()
        
        self.color_schemes = [
            {'bg': '#0A0E27', 'text': '#FFD700', 'accent': '#FF6B35'},
            {'bg': '#1A1A2E', 'text': '#00FFF0', 'accent': '#FF2E63'},
            {'bg': '#000000', 'text': '#FFFFFF', 'accent': '#FF0055'},
            {'bg': '#2C1654', 'text': '#FFA500', 'accent': '#00FF87'},
        ]
    
    def create_viral_video(self, content):
        """Create viral-quality motivation short"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = f"output/viral_short_{timestamp}.mp4"
        os.makedirs('output', exist_ok=True)
        
        print(f"🎨 Creating viral video...")
        
        colors = random.choice(self.color_schemes)
        character_type = content.get('character', 'motivational_speaker')
        
        try:
            # Generate voiceover
            audio_path = self.generate_voiceover(content['text'])
            audio_duration = 12
            
            if os.path.exists(audio_path):
                audio_clip = AudioFileClip(audio_path)
                audio_duration = audio_clip.duration
                audio_clip.close()
            
            # Create video
            video_clip = self.create_character_video_clip(content, colors, character_type, audio_duration)
            
            # Add audio
            if os.path.exists(audio_path):
                audio = AudioFileClip(audio_path)
                video_clip = video_clip.set_audio(audio)
            
            # Export
            print(f"📹 Rendering video...")
            video_clip.write_videofile(
                output_path,
                fps=self.fps,
                codec='libx264',
                audio_codec='aac',
                preset='ultrafast',
                threads=4,
                logger=None
            )
            
            video_clip.close()
            print(f"✅ Video created: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def create_character_video_clip(self, content, colors, character_type, duration):
        """Create video clip with character"""
        text = content['text']
        
        def make_frame(t):
            # Background
            img = Image.new('RGB', (self.width, self.height), colors['bg'])
            
            # Add character
            char_img = self.character_animator.create_3d_character_frame(t, character_type)
            img.paste(char_img, (0, 0), char_img)
            
            # Add text
            text_img = self.create_animated_text(text, t, duration, colors)
            img.paste(text_img, (0, 0), text_img)
            
            return np.array(img)
        
        return VideoClip(make_frame, duration=duration)
    
    def create_animated_text(self, text, t, total_duration, colors):
        """Create animated text"""
        img = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Word reveal
        words = text.split()
        words_per_second = len(words) / total_duration
        current_word_index = min(int(t * words_per_second), len(words))
        visible_text = ' '.join(words[:current_word_index + 1])
        
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 70)
        except:
            font = ImageFont.load_default()
        
        # Simple centered text
        bbox = draw.textbbox((0, 0), visible_text, font=font)
        text_width = bbox[2] - bbox[0]
        x = (self.width - text_width) // 2
        y = 150
        
        # Shadow
        draw.text((x+4, y+4), visible_text, font=font, fill='#000000')
        # Main text
        draw.text((x, y), visible_text, font=font, fill=colors['text'])
        
        return img
    
    def hex_to_rgb(self, hex_color, alpha=255):
        """Convert hex to RGBA"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4)) + (alpha,)
    
    def generate_voiceover(self, text):
        """Generate voiceover"""
        output_path = 'temp_voiceover.mp3'
        try:
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(output_path)
            return output_path
        except Exception as e:
            print(f"⚠️ Voiceover failed: {e}")
            return None


# ============================================================================
# MAIN - SINGLE VIDEO TEST
# ============================================================================

if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════════════════════════╗
    ║         🔥 VIRAL SHORTS GENERATOR - TEST MODE 🔥              ║
    ║              Generating ONE test video...                      ║
    ╚════════════════════════════════════════════════════════════════╝
    """)
    
    try:
        # Create output directory
        os.makedirs('output', exist_ok=True)
        
        # Initialize
        content_mgr = ContentManager()
        video_gen = ViralVideoGenerator()
        
        # Get content
        content = content_mgr.get_next_content()
        print(f"\n📝 Quote: {content['text'][:60]}...")
        print(f"✍️  Author: {content['author']}")
        print(f"🎭 Character: {content.get('character', 'speaker')}\n")
        
        # Generate video
        video_path = video_gen.create_viral_video(content)
        
        if video_path and os.path.exists(video_path):
            file_size = os.path.getsize(video_path) / (1024*1024)
            print(f"\n✅ SUCCESS!")
            print(f"📹 Video: {video_path}")
            print(f"📏 Size: {file_size:.2f} MB")
        else:
            print(f"\n❌ FAILED!")
            exit(1)
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
