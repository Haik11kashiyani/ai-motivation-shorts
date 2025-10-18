"""
🚀 FAST VIRAL SHORTS GENERATOR 🚀
Optimized for speed while maintaining quality
Renders in 3-5 minutes guaranteed!
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

# ============================================================================
# FAST CONFIG
# ============================================================================

class FastConfig:
    WIDTH = 1080
    HEIGHT = 1920
    FPS = 30  # Optimal balance
    DURATION = 20  # Fixed duration for predictable render time
    
    # ElevenLabs
    ELEVEN_API_KEYS = [
        os.getenv('ELEVEN_API_KEY_1', ''),
        os.getenv('ELEVEN_API_KEY_2', ''),
        os.getenv('ELEVEN_API_KEY_3', ''),
    ]
    VOICE_ID = 'pNInz6obpgDQGcFmaJgB'  # Adam - Deep male
    
    # Viral colors
    COLORS = [
        {'bg': '#000000', 'text': '#FFD700', 'glow': '#FFA500'},
        {'bg': '#1a0000', 'text': '#FF0000', 'glow': '#FF6666'},
        {'bg': '#001a33', 'text': '#00D4FF', 'glow': '#66E0FF'},
        {'bg': '#1a002b', 'text': '#B026FF', 'glow': '#E699FF'},
    ]


# ============================================================================
# FAST VOICE GENERATOR
# ============================================================================

class FastVoiceGen:
    def __init__(self):
        self.keys = [k for k in FastConfig.ELEVEN_API_KEYS if k]
        
    def generate(self, text):
        # Try ElevenLabs
        if self.keys:
            try:
                print("🎤 Generating voice with ElevenLabs...")
                url = f"https://api.elevenlabs.io/v1/text-to-speech/{FastConfig.VOICE_ID}"
                
                response = requests.post(
                    url,
                    json={
                        "text": text,
                        "model_id": "eleven_monolingual_v1",
                        "voice_settings": {
                            "stability": 0.7,
                            "similarity_boost": 0.85
                        }
                    },
                    headers={
                        "xi-api-key": self.keys[0],
                        "Content-Type": "application/json"
                    },
                    timeout=20
                )
                
                if response.status_code == 200:
                    path = 'voice.mp3'
                    with open(path, 'wb') as f:
                        f.write(response.content)
                    print("✅ Premium voice ready!")
                    return path
            except Exception as e:
                print(f"⚠️ ElevenLabs failed: {e}")
        
        # Fallback to gTTS
        from gtts import gTTS
        print("🎤 Using gTTS...")
        tts = gTTS(text, lang='en', slow=False)
        path = 'voice.mp3'
        tts.save(path)
        return path


# ============================================================================
# FAST VIDEO GENERATOR
# ============================================================================

class FastVideoGen:
    def __init__(self):
        self.w = FastConfig.WIDTH
        self.h = FastConfig.HEIGHT
        
    def create(self, content):
        print("\n" + "="*60)
        print("🚀 CREATING FAST VIRAL SHORT")
        print("="*60)
        print(f"📝 {content['text'][:50]}...")
        
        try:
            # Voice
            voice_gen = FastVoiceGen()
            audio_path = voice_gen.generate(content['text'])
            audio = AudioFileClip(audio_path)
            duration = FastConfig.DURATION
            
            # Colors
            colors = random.choice(FastConfig.COLORS)
            print(f"🎨 Colors: {colors}")
            
            # Create video
            print("🎬 Rendering video (3-5 minutes)...")
            
            def make_frame(t):
                return self.create_frame(t, content['text'], colors, duration)
            
            video = VideoClip(make_frame, duration=duration)
            video = video.set_audio(audio)
            
            # Output
            output = f"output/viral_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
            os.makedirs('output', exist_ok=True)
            
            video.write_videofile(
                output,
                fps=FastConfig.FPS,
                codec='libx264',
                audio_codec='aac',
                preset='ultrafast',  # FASTEST preset
                threads=4,
                bitrate='4000k',
                logger=None
            )
            
            video.close()
            audio.close()
            
            size = os.path.getsize(output) / (1024*1024)
            print("\n" + "="*60)
            print("✅ SUCCESS!")
            print(f"📹 {output}")
            print(f"📏 {size:.1f} MB")
            print(f"⏱️ {duration}s")
            print("="*60 + "\n")
            
            return output
            
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def create_frame(self, t, text, colors, duration):
        """Create single frame - optimized for speed"""
        # Background with gradient
        img = Image.new('RGB', (self.w, self.h), colors['bg'])
        draw = ImageDraw.Draw(img)
        
        # Simple animated gradient
        for y in range(0, self.h, 20):  # Every 20px for speed
            wave = math.sin(t * 0.5 + y/100) * 0.3
            brightness = int(20 + 15 * wave)
            color = tuple(min(255, c + brightness) for c in self.hex_to_rgb(colors['bg']))
            draw.rectangle([0, y, self.w, y+20], fill=color)
        
        # Character (simplified for speed)
        cx = self.w // 2
        cy = int(self.h * 0.7)
        breath = int(5 * math.sin(t * 2))
        
        # Body
        draw.ellipse([cx-80, cy-200+breath, cx+80, cy+100+breath], 
                    fill=(40, 40, 50))
        
        # Head
        draw.ellipse([cx-60, cy-300+breath, cx+60, cy-180+breath], 
                    fill=(50, 50, 60))
        
        # Glowing eyes
        glow = int(200 + 50 * math.sin(t * 3))
        draw.ellipse([cx-35, cy-260+breath, cx-15, cy-240+breath], 
                    fill=(glow, glow, 255))
        draw.ellipse([cx+15, cy-260+breath, cx+35, cy-240+breath], 
                    fill=(glow, glow, 255))
        
        # Energy aura (simple)
        aura = int(300 + 50 * math.sin(t * 1.5))
        for i in range(3):
            offset = i * 30
            draw.ellipse([cx-aura+offset, cy-300+offset, 
                         cx+aura-offset, cy+150-offset],
                        outline=self.hex_to_rgb(colors['glow'], 100-i*30), 
                        width=3)
        
        # Text (word-by-word reveal)
        words = text.split()
        wps = len(words) / duration
        visible = ' '.join(words[:int(t * wps) + 1])
        
        if visible:
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 90)
            except:
                font = ImageFont.load_default()
            
            # Wrap text
            lines = []
            current = []
            for word in visible.split():
                test = ' '.join(current + [word])
                bbox = draw.textbbox((0, 0), test, font=font)
                if bbox[2] - bbox[0] < self.w - 100:
                    current.append(word)
                else:
                    if current:
                        lines.append(' '.join(current))
                    current = [word]
            if current:
                lines.append(' '.join(current))
            
            # Draw text
            y = 120
            for line in lines[:3]:  # Max 3 lines
                bbox = draw.textbbox((0, 0), line, font=font)
                x = (self.w - (bbox[2] - bbox[0])) // 2
                
                # Glow
                for g in range(8, 0, -2):
                    alpha = 60 - g*5
                    glow_color = self.hex_to_rgb(colors['glow'], alpha)
                    for ox, oy in [(-g,0), (g,0), (0,-g), (0,g)]:
                        draw.text((x+ox, y+oy), line, font=font, fill=glow_color)
                
                # Stroke
                for ox in [-4, 0, 4]:
                    for oy in [-4, 0, 4]:
                        if ox or oy:
                            draw.text((x+ox, y+oy), line, font=font, fill=(0,0,0))
                
                # Main text
                draw.text((x, y), line, font=font, fill=self.hex_to_rgb(colors['text']))
                y += 110
        
        return np.array(img)
    
    def hex_to_rgb(self, hex_color, alpha=255):
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        if alpha < 255:
            return (r, g, b, alpha)
        return (r, g, b)


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║     🚀 FAST VIRAL SHORTS GENERATOR 🚀                 ║
    ║        Renders in 3-5 minutes!                        ║
    ╚════════════════════════════════════════════════════════╝
    """)
    
    try:
        # Load content
        with open('motivational_content.json', 'r') as f:
            data = json.load(f)
        
        quote = random.choice(data['quotes'])
        
        # Generate
        gen = FastVideoGen()
        result = gen.create(quote)
        
        if result:
            print("🎉 Video ready!")
        else:
            print("❌ Failed!")
            exit(1)
            
    except Exception as e:
        print(f"❌ FATAL: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
