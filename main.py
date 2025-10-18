"""
🔥 VIRAL-WORTHY MOTIVATION SHORTS GENERATOR 🔥
Professional quality like the top viral channels
- Cinematic visuals with smooth animations
- Professional deep male voice
- Eye-catching text effects
- Dynamic transitions
- Proven viral formula
"""

import os
import json
import random
from datetime import datetime
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import numpy as np
import requests
import math

# ============================================================================
# CONFIGURATION
# ============================================================================

class ViralConfig:
    # Video specs (optimized for virality)
    WIDTH = 1080
    HEIGHT = 1920
    FPS = 60  # Smoother = more premium feel
    DURATION_MIN = 25  # Longer engagement
    DURATION_MAX = 35
    
    # ElevenLabs API for PREMIUM voice
    ELEVEN_API_KEYS = [
        os.getenv('ELEVEN_API_KEY_1', ''),
        os.getenv('ELEVEN_API_KEY_2', ''),
        os.getenv('ELEVEN_API_KEY_3', ''),
    ]
    
    # BEST voices for motivation (deep, authoritative)
    VOICE_OPTIONS = {
        'deep_male': 'pNInz6obpgDQGcFmaJgB',      # Adam - Deep, authoritative
        'powerful': 'VR6AewLTigWG4xSOukaG',       # Arnold - Strong, powerful
        'epic': 'EXAVITQu4vr4xnSDxMaL',           # Bella - Epic, dramatic
        'smooth': 'yoZ06aMxZJJ28mfd3POQ',         # Sam - Smooth, confident
    }
    
    # Viral color schemes (proven to get views)
    VIRAL_COLORS = [
        # Gold & Black (luxury)
        {'bg1': '#000000', 'bg2': '#1a1a1a', 'text': '#FFD700', 'accent': '#FFA500', 'glow': '#FFFF00'},
        # Red Energy
        {'bg1': '#0d0d0d', 'bg2': '#1a0000', 'text': '#FF0000', 'accent': '#FF4444', 'glow': '#FF6666'},
        # Blue Power
        {'bg1': '#000a1a', 'bg2': '#001a33', 'text': '#00D4FF', 'accent': '#0099FF', 'glow': '#66E0FF'},
        # Purple Luxury
        {'bg1': '#0d0015', 'bg2': '#1a002b', 'text': '#B026FF', 'accent': '#D966FF', 'glow': '#E699FF'},
    ]


# ============================================================================
# PREMIUM VOICE GENERATOR
# ============================================================================

class PremiumVoiceGenerator:
    def __init__(self):
        self.api_keys = [k for k in ViralConfig.ELEVEN_API_KEYS if k]
        self.current_key_index = 0
        
    def generate_premium_voice(self, text, voice_type='deep_male'):
        """Generate premium quality voice with ElevenLabs"""
        
        voice_id = ViralConfig.VOICE_OPTIONS.get(voice_type, ViralConfig.VOICE_OPTIONS['deep_male'])
        
        if not self.api_keys:
            print("⚠️  No ElevenLabs API key - using enhanced gTTS")
            return self.generate_enhanced_gtts(text)
        
        # Try each API key
        for attempt in range(len(self.api_keys)):
            api_key = self.api_keys[self.current_key_index]
            
            try:
                print(f"🎤 Generating PREMIUM voice (Attempt {attempt + 1})...")
                
                url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
                
                headers = {
                    "Accept": "audio/mpeg",
                    "Content-Type": "application/json",
                    "xi-api-key": api_key
                }
                
                # Premium settings for viral quality
                data = {
                    "text": text,
                    "model_id": "eleven_multilingual_v2",  # Better model
                    "voice_settings": {
                        "stability": 0.65,        # Slight variation = more natural
                        "similarity_boost": 0.90,  # Very similar to original
                        "style": 0.75,            # More expressive
                        "use_speaker_boost": True
                    }
                }
                
                response = requests.post(url, json=data, headers=headers, timeout=30)
                
                if response.status_code == 200:
                    output_path = 'premium_voice.mp3'
                    with open(output_path, 'wb') as f:
                        f.write(response.content)
                    print(f"✅ Premium voice generated!")
                    return output_path
                else:
                    print(f"⚠️  API returned {response.status_code}, trying next key...")
                    self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
                    
            except Exception as e:
                print(f"⚠️  Error: {e}, trying next key...")
                self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        
        # Fallback to enhanced gTTS
        return self.generate_enhanced_gtts(text)
    
    def generate_enhanced_gtts(self, text):
        """Enhanced gTTS with audio processing"""
        from gtts import gTTS
        
        print("🎤 Using enhanced gTTS voice...")
        
        # Use UK English (deeper voice)
        tts = gTTS(text=text, lang='en', slow=False, tld='com.au')  # Australian = deeper
        base_path = 'gtts_voice.mp3'
        tts.save(base_path)
        
        # Try to enhance with audio effects
        try:
            audio = AudioFileClip(base_path)
            
            # Slow down slightly for deeper sound
            enhanced = audio.fx(vfx.speedx, 0.92)  # 8% slower = deeper
            
            enhanced_path = 'enhanced_voice.mp3'
            enhanced.write_audiofile(enhanced_path, logger=None)
            enhanced.close()
            audio.close()
            
            return enhanced_path
        except:
            return base_path


# ============================================================================
# CINEMATIC VISUAL GENERATOR
# ============================================================================

class CinematicVisuals:
    def __init__(self):
        self.width = ViralConfig.WIDTH
        self.height = ViralConfig.HEIGHT
        
    def create_premium_background(self, t, colors, duration):
        """Create cinematic animated background"""
        img = Image.new('RGB', (self.width, self.height), colors['bg1'])
        draw = ImageDraw.Draw(img)
        
        # Animated gradient with depth
        for y in range(self.height):
            progress = y / self.height
            
            # Multi-layer gradient animation
            wave1 = math.sin(t * 0.3 + progress * 4) * 0.3
            wave2 = math.sin(t * 0.5 + progress * 2) * 0.2
            wave_combined = (wave1 + wave2 + 1) / 2  # Normalize to 0-1
            
            # Interpolate between background colors
            r1, g1, b1 = self.hex_to_rgb(colors['bg1'])
            r2, g2, b2 = self.hex_to_rgb(colors['bg2'])
            
            r = int(r1 + (r2 - r1) * (progress + wave_combined * 0.3))
            g = int(g1 + (g2 - g1) * (progress + wave_combined * 0.3))
            b = int(b1 + (b2 - b1) * (progress + wave_combined * 0.3))
            
            draw.line([(0, y), (self.width, y)], fill=(r, g, b))
        
        # Add subtle particle effects
        for i in range(30):
            particle_t = (t * 0.5 + i * 0.3) % duration
            x = int((self.width * 0.1) + (self.width * 0.8) * ((i * 37) % 100) / 100)
            y = int((particle_t / duration) * self.height)
            
            if 0 <= y < self.height:
                size = int(3 + 5 * math.sin(t * 2 + i))
                alpha = int(100 + 100 * math.sin(t * 3 + i * 0.5))
                color = self.hex_to_rgb(colors['glow'], alpha)
                
                # Draw glow
                for r in range(size, 0, -1):
                    a = int(alpha * (size - r) / size)
                    draw.ellipse([x-r, y-r, x+r, y+r], 
                                fill=self.hex_to_rgb(colors['glow'], a))
        
        return img
    
    def create_viral_text_overlay(self, text, t, duration, colors):
        """Create viral-style text with premium effects"""
        img = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Word-by-word reveal (keeps attention)
        words = text.split()
        words_per_second = len(words) / duration
        current_word_idx = min(int(t * words_per_second * 1.2), len(words))  # Slightly faster
        visible_text = ' '.join(words[:current_word_idx])
        
        if not visible_text:
            return img
        
        # Load premium font (BOLD for impact)
        try:
            font_size = 95  # BIGGER = More viral
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # Smart text wrapping
        lines = self.wrap_text_smart(visible_text, font, draw, self.width - 120)
        
        # Position in upper-middle (optimal viewing area)
        line_height = 120
        total_height = len(lines) * line_height
        start_y = (self.height - total_height) // 3  # Top third
        
        for i, line in enumerate(lines):
            if not line.strip():
                continue
                
            y_pos = start_y + i * line_height
            
            # Get text dimensions
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x_pos = (self.width - text_width) // 2
            
            # Fade in animation per line
            line_start_time = (i / max(len(lines), 1)) * duration * 0.4
            alpha = min(255, int((t - line_start_time) * 800))
            alpha = max(0, alpha)
            
            if alpha > 0:
                # Animated glow effect (pulsating)
                glow_intensity = 0.7 + 0.3 * math.sin(t * 4 + i)
                glow_size = int(12 * glow_intensity)
                
                # Multiple glow layers for premium look
                for g in range(glow_size, 0, -2):
                    glow_alpha = int(alpha * 0.4 * (glow_size - g) / glow_size)
                    glow_color = self.hex_to_rgb(colors['glow'], glow_alpha)
                    
                    for offset_x in [-g, 0, g]:
                        for offset_y in [-g, 0, g]:
                            if offset_x or offset_y:
                                draw.text((x_pos + offset_x, y_pos + offset_y), 
                                        line, font=font, fill=glow_color)
                
                # Heavy black stroke (readability)
                stroke_width = 8
                for offset_x in range(-stroke_width, stroke_width + 1):
                    for offset_y in range(-stroke_width, stroke_width + 1):
                        if offset_x or offset_y:
                            draw.text((x_pos + offset_x, y_pos + offset_y), 
                                    line, font=font, fill=(0, 0, 0, alpha))
                
                # Main text (vibrant color)
                text_color = self.hex_to_rgb(colors['text'], alpha)
                draw.text((x_pos, y_pos), line, font=font, fill=text_color)
                
                # Highlight current word (extra attention)
                if i == len(lines) - 1:  # Last line
                    words_in_line = line.split()
                    if words_in_line:
                        last_word = words_in_line[-1]
                        
                        # Calculate last word position
                        words_before = ' '.join(words_in_line[:-1])
                        if words_before:
                            bbox_before = draw.textbbox((0, 0), words_before + ' ', font=font)
                            last_word_x = x_pos + (bbox_before[2] - bbox_before[0])
                        else:
                            last_word_x = x_pos
                        
                        # Pulsating highlight
                        highlight_alpha = int(alpha * 0.5 * (0.7 + 0.3 * math.sin(t * 8)))
                        highlight_color = self.hex_to_rgb(colors['accent'], highlight_alpha)
                        
                        # Underline effect
                        bbox_word = draw.textbbox((0, 0), last_word, font=font)
                        word_width = bbox_word[2] - bbox_word[0]
                        underline_y = y_pos + font_size + 10
                        
                        draw.line([(last_word_x, underline_y), 
                                  (last_word_x + word_width, underline_y)], 
                                 fill=highlight_color, width=6)
        
        return img
    
    def wrap_text_smart(self, text, font, draw, max_width):
        """Smart text wrapping for maximum impact"""
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
        
        # Limit to 3 lines max for mobile viewing
        if len(lines) > 3:
            # Combine into 3 balanced lines
            all_words = text.split()
            words_per_line = len(all_words) // 3
            lines = [
                ' '.join(all_words[:words_per_line]),
                ' '.join(all_words[words_per_line:words_per_line*2]),
                ' '.join(all_words[words_per_line*2:])
            ]
        
        return lines
    
    def hex_to_rgb(self, hex_color, alpha=255):
        """Convert hex to RGBA"""
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return (r, g, b, alpha)


# ============================================================================
# CHARACTER ANIMATOR (PREMIUM QUALITY)
# ============================================================================

class PremiumCharacterAnimator:
    def __init__(self):
        self.width = ViralConfig.WIDTH
        self.height = ViralConfig.HEIGHT
    
    def create_animated_character(self, t, style='silhouette'):
        """Create premium animated character"""
        img = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Character position (lower third for text space)
        center_x = self.width // 2
        center_y = int(self.height * 0.70)
        
        # Breathing animation
        breath = math.sin(t * 2) * 8
        
        # Scale pulse
        scale = 1.0 + math.sin(t * 1.5) * 0.03
        
        # Character silhouette (professional look)
        self.draw_professional_character(draw, center_x, center_y + int(breath), scale, t)
        
        # Convert to RGB for compositing
        rgb_img = Image.new('RGB', (self.width, self.height), (0, 0, 0))
        rgb_img.paste(img, (0, 0), img)
        
        return rgb_img
    
    def draw_professional_character(self, draw, x, y, scale, t):
        """Draw a professional animated character"""
        # Head
        head_size = int(140 * scale)
        draw.ellipse([x - head_size, y - 500, x + head_size, y - 220], 
                    fill=(30, 30, 40, 255), outline=(100, 100, 120, 255), width=4)
        
        # Glowing eyes
        eye_glow = int(200 + 55 * math.sin(t * 3))
        draw.ellipse([x - 60, y - 400, x - 20, y - 360], 
                    fill=(eye_glow, eye_glow, 255, 255))
        draw.ellipse([x + 20, y - 400, x + 60, y - 360], 
                    fill=(eye_glow, eye_glow, 255, 255))
        
        # Body (torso)
        body_width = int(200 * scale)
        body_height = int(300 * scale)
        draw.ellipse([x - body_width, y - 220, x + body_width, y + body_height], 
                    fill=(40, 40, 50, 255), outline=(100, 100, 120, 255), width=4)
        
        # Arms (animated)
        arm_angle = math.sin(t * 2.5) * 15
        
        # Left arm
        arm_points = [
            (x - body_width, y - 150),
            (x - body_width - 80, y + int(arm_angle)),
            (x - body_width - 100, y + 100 + int(arm_angle)),
            (x - body_width - 60, y + 120)
        ]
        draw.polygon(arm_points, fill=(35, 35, 45, 255), outline=(90, 90, 110, 255), width=3)
        
        # Right arm  
        arm_points_r = [
            (x + body_width, y - 150),
            (x + body_width + 80, y - int(arm_angle)),
            (x + body_width + 100, y + 100 - int(arm_angle)),
            (x + body_width + 60, y + 120)
        ]
        draw.polygon(arm_points_r, fill=(35, 35, 45, 255), outline=(90, 90, 110, 255), width=3)
        
        # Energy aura (viral effect)
        aura_radius = int(400 + 80 * math.sin(t * 1.5))
        for i in range(5):
            alpha = int(40 - i * 8)
            offset = i * 30
            draw.ellipse([
                x - aura_radius + offset, y - 400 - offset,
                x + aura_radius - offset, y + 300 + offset
            ], outline=(100, 200, 255, alpha), width=4)


# ============================================================================
# VIRAL VIDEO GENERATOR (MAIN ENGINE)
# ============================================================================

class ViralVideoGenerator:
    def __init__(self):
        self.voice_gen = PremiumVoiceGenerator()
        self.visuals = CinematicVisuals()
        self.character = PremiumCharacterAnimator()
        
    def create_viral_short(self, content):
        """Generate viral-worthy short"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = f"output/viral_short_{timestamp}.mp4"
        os.makedirs('output', exist_ok=True)
        
        print("\n" + "="*70)
        print("🔥 CREATING VIRAL-WORTHY SHORT")
        print("="*70)
        print(f"📝 Quote: {content['text'][:50]}...")
        print(f"✍️  Author: {content['author']}")
        
        try:
            # Generate premium voice
            print("\n🎤 Generating premium voice...")
            audio_path = self.voice_gen.generate_premium_voice(content['text'], 'deep_male')
            
            # Get duration
            audio_clip = AudioFileClip(audio_path)
            duration = max(audio_clip.duration, ViralConfig.DURATION_MIN)
            duration = min(duration, ViralConfig.DURATION_MAX)
            
            print(f"⏱️  Duration: {duration:.1f}s")
            
            # Select viral color scheme
            colors = random.choice(ViralConfig.VIRAL_COLORS)
            print(f"🎨 Color scheme: {list(colors.values())}")
            
            # Create video
            print("\n🎬 Generating cinematic visuals...")
            
            def make_final_frame(t):
                # Background layer
                bg = self.visuals.create_premium_background(t, colors, duration)
                
                # Character layer
                char = self.character.create_animated_character(t, 'silhouette')
                
                # Blend character (where not black)
                bg_array = np.array(bg)
                char_array = np.array(char)
                
                # Simple blend where character is visible
                mask = np.any(char_array > 20, axis=2)
                bg_array[mask] = char_array[mask]
                
                # Text overlay
                text_img = self.visuals.create_viral_text_overlay(content['text'], t, duration, colors)
                text_array = np.array(text_img.convert('RGB'))
                
                # Blend text (where not black)
                text_mask = np.any(text_array > 20, axis=2)
                bg_array[text_mask] = text_array[text_mask]
                
                return bg_array
            
            print("🎞️  Rendering video...")
            video_clip = VideoClip(make_final_frame, duration=duration)
            video_clip = video_clip.set_audio(audio_clip)
            
            # Export with viral-optimized settings
            video_clip.write_videofile(
                output_path,
                fps=ViralConfig.FPS,
                codec='libx264',
                audio_codec='aac',
                bitrate='8000k',  # High quality
                preset='slow',     # Best compression
                threads=4,
                logger=None
            )
            
            # Cleanup
            video_clip.close()
            audio_clip.close()
            
            # Report
            file_size = os.path.getsize(output_path) / (1024 * 1024)
            print("\n" + "="*70)
            print("✅ VIRAL SHORT CREATED SUCCESSFULLY!")
            print("="*70)
            print(f"📹 File: {output_path}")
            print(f"📏 Size: {file_size:.2f} MB")
            print(f"⏱️  Duration: {duration:.1f}s")
            print(f"🎯 FPS: {ViralConfig.FPS}")
            print(f"🎨 Resolution: {ViralConfig.WIDTH}x{ViralConfig.HEIGHT}")
            print("="*70 + "\n")
            
            return output_path
            
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
            return None


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                                ║
    ║       🔥 VIRAL-WORTHY MOTIVATION SHORTS GENERATOR 🔥          ║
    ║                                                                ║
    ║  Premium Quality • Cinematic Visuals • Deep Voice             ║
    ║  Proven Viral Formula • Professional Effects                  ║
    ║                                                                ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    
    try:
        # Load content
        with open('motivational_content.json', 'r') as f:
            data = json.load(f)
        
        # Get random quote
        quote = random.choice(data['quotes'])
        
        # Generate viral short
        generator = ViralVideoGenerator()
        video_path = generator.create_viral_short(quote)
        
        if video_path:
            print("🎉 SUCCESS! Your viral short is ready!")
            print(f"📂 Location: {video_path}")
        else:
            print("❌ FAILED! Check errors above.")
            exit(1)
            
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
