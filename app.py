import tkinter as tk
from tkinter import font, ttk
import sys
import winsound
import threading
import random
import struct
import io
import math
import os
import json

try:
    import pygame
    pygame.mixer.init()
    PYGAME_AVAILABLE = True
except:
    PYGAME_AVAILABLE = False
    print("pygame not available - background music disabled")

CURRENT_MUSIC_TYPE = None # Track what's currently playing

# Game State
state = {
    "cereal": None,
    "music": None,
    "offer": None,
    "colin_follow": False,
    "mohan_counter": 0,
    "inventory": [],
    "volume": 0.3
}

# Font Configuration
# We prefer 'Special Elite' (Google Font), fallback to 'Courier New' for typewriter feel
GAME_FONT = "Special Elite"
GAME_FONT_BOLD = ("Special Elite", 11, "bold")
GAME_FONT_NORMAL = ("Special Elite", 11)
GAME_FONT_TITLE = ("Special Elite", 48, "bold")
GAME_FONT_SUBTITLE = ("Special Elite", 16)

def get_font(size, bold=False):
    # Try Special Elite, then Courier New
    # Check if Special Elite exists in the system font list
    weight = "bold" if bold else "normal"
    families = font.families()
    if "Special Elite" in families:
        return ("Special Elite", size, weight)
    else:
        # Fallback to Courier New which has a similar typewriter feel
        return ("Courier New", size, weight)

def generate_click_sound(duration_ms=10, volume=0.5):
    """Generates a short burst of white noise (mechanical click) in WAV format"""
    sample_rate = 44100
    num_samples = int(sample_rate * (duration_ms / 1000.0))
    
    # WAV Header
    header = b'RIFF' + struct.pack('<I', 36 + num_samples) + b'WAVEfmt ' + struct.pack('<IHHIIHH', 16, 1, 1, sample_rate, sample_rate, 1, 8) + b'data' + struct.pack('<I', num_samples)
    
    # Noise Data (Unsigned 8-bit: 0-255, silence is 128)
    data = bytearray()
    for i in range(num_samples):
        # Apply a quick envelope to make it crisp (fade out)
        envelope = 1.0 - (i / num_samples)
        noise = (random.random() * 2.0) - 1.0 # -1 to 1
        sample_val = 128 + int(noise * 127 * volume * envelope)
        sample_val = max(0, min(255, sample_val))
        data.append(sample_val)
        
    return header + data

def load_custom_sound(filename, default_generator):
    """Try to load a WAV file; fall back to generator if not found"""
    if os.path.exists(filename):
        try:
            with open(filename, "rb") as f:
                return f.read()
        except Exception as e:
            print(f"Error loading {filename}: {e}")
    return default_generator()

# Load sounds using pygame for better performance if available
TYPE_SOUND_OBJ = None
CLICK_SOUND_OBJ = None

def init_pygame_sounds():
    global TYPE_SOUND_OBJ, CLICK_SOUND_OBJ
    if not PYGAME_AVAILABLE:
        return
        
    # Load Click
    click_data = load_custom_sound("click.wav", lambda: generate_click_sound(duration_ms=4, volume=0.8))
    CLICK_SOUND_OBJ = pygame.mixer.Sound(io.BytesIO(click_data))
    
    # Load Typing
    type_data = load_custom_sound("typing.wav", lambda: generate_click_sound(duration_ms=3, volume=0.2))
    TYPE_SOUND_OBJ = pygame.mixer.Sound(io.BytesIO(type_data))

# Initialize immediately
init_pygame_sounds()

def play_click():
    if CLICK_SOUND_OBJ:
        CLICK_SOUND_OBJ.play()
    else:
        # Fallback to winsound if pygame failed
        click_data = load_custom_sound("click.wav", lambda: generate_click_sound(duration_ms=4, volume=0.8))
        threading.Thread(target=lambda: winsound.PlaySound(click_data, winsound.SND_MEMORY), daemon=True).start()

def play_type():
    if TYPE_SOUND_OBJ:
        # Loop for continuous typing sound if needed, but per request we play once 
        # and stop. If it's a short click, we just play.
        # However, user said the sound IS multiple characters, so we play it.
        TYPE_SOUND_OBJ.play()

def stop_type():
    """Stop the typing sound"""
    if TYPE_SOUND_OBJ:
        TYPE_SOUND_OBJ.stop()
    else:
        try:
            winsound.PlaySound(None, winsound.SND_PURGE)
        except:
            pass

def start_background_music(music_type="normal"):
    """Start playing background music in a loop, handling transitions between types"""
    global CURRENT_MUSIC_TYPE
    if not PYGAME_AVAILABLE:
        return
    
    # Don't restart if already playing this type
    if music_type == CURRENT_MUSIC_TYPE:
        return
        
    # Track selection
    if music_type == "intense":
        files = [ "intense.wav"]
    else:
        files = ["background.wav"]

    # Try different file formats
    for music_file in files:
        if os.path.exists(music_file):
            try:
                # Use current volume from state
                vol = state.get("volume", 0.3)

                pygame.mixer.music.load(music_file)
                pygame.mixer.music.set_volume(vol) 
                pygame.mixer.music.play(-1)  # -1 means loop forever
                CURRENT_MUSIC_TYPE = music_type
                print(f"Switched background music to: {music_file} ({music_type})")
                return
            except Exception as e:
                print(f"Error loading {music_file}: {e}")
    
    print(f"No {music_type} background music file found.")

def stop_background_music():
    """Stop background music"""
    if PYGAME_AVAILABLE:
        try:
            pygame.mixer.music.stop()
        except:
            pass

class RoundedBubble(tk.Canvas):
    def __init__(self, parent, text, max_width=400, bg_color="#ffffff", fg_color="#000000", is_user=False):
        super().__init__(parent, bg=parent["bg"], highlightthickness=0)
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.is_user = is_user
        self.radius = 15  # Slightly tighter radius
        self.padding = 10 # Reduced padding (was 15)
        
        # Create Text Item first to measure size
        self.text_id = self.create_text(
            self.padding, 
            self.padding, 
            text=text, 
            fill=self.fg_color, 
            font=get_font(11), 
            anchor="nw", 
            width=max_width - (self.padding * 2)
        )
        
        # Calculate Bounding Box
        self.update_dimensions()

    def update_dimensions(self):
        bbox = self.bbox(self.text_id)
        if not bbox:
            text_width, text_height = 0, 0
        else:
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

        # Calculate Canvas Dimensions
        canvas_width = text_width + (self.padding * 2) + 5 # Tighter fit
        canvas_height = text_height + (self.padding * 2)
        
        # Ensure minimums
        canvas_width = max(canvas_width, 40)
        canvas_height = max(canvas_height, 35)

        self.config(width=canvas_width, height=canvas_height)
        
        # Draw Rounded Rect behind text
        self.delete("bg_rect") # Remove old if exists
        self.create_rounded_rect(0, 0, canvas_width, canvas_height, self.radius, self.bg_color, "bg_rect")
        self.tag_lower("bg_rect", self.text_id)

    def create_rounded_rect(self, x1, y1, x2, y2, r, color, tag):
        points = [x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1]
        return self.create_polygon(points, smooth=True, fill=color, tags=tag)

    def update_text(self, new_text):
        self.itemconfig(self.text_id, text=new_text)
        self.update_dimensions()


class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, command, width=250, height=45, radius=22, bg="#333333", fg="#FFFFFF", hover_bg="#555555", glow_color=None):
        # Slightly larger canvas if glowing to accommodate the light
        self.glow_color = glow_color
        self.glow_padding = 4 if glow_color else 0
        super().__init__(parent, width=width + (self.glow_padding*2), height=height + (self.glow_padding*2), bg=parent["bg"], highlightthickness=0)
        
        self.command = command
        self.text = text
        self.radius = radius
        self.bg_color = bg
        self.fg_color = fg
        self.hover_bg = hover_bg
        self.default_bg = bg
        
        self.width = width
        self.height = height
        self.is_blinking = False
        self.blink_state = True

        # Create glow shape if specified
        self.glow_rect = None
        if self.glow_color:
            self.glow_rect = self.create_rounded_rect(
                0, 0, 
                width + (self.glow_padding*2), 
                height + (self.glow_padding*2), 
                radius + 2, 
                self.glow_color
            )
        
        # Create main button shape
        self.rect = self.create_rounded_rect(
            self.glow_padding, 
            self.glow_padding, 
            width + self.glow_padding, 
            height + self.glow_padding, 
            radius, 
            self.default_bg
        )
        
        self.text_id = self.create_text(
            (width/2) + self.glow_padding, 
            (height/2) + self.glow_padding, 
            text=text, 
            fill=self.fg_color, 
            font=get_font(11, bold=True)
        )

        # Bind events
        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def create_rounded_rect(self, x1, y1, x2, y2, r, color):
        points = [x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1]
        return self.create_polygon(points, smooth=True, fill=color)

    def start_blinking(self, interval=500):
        if not self.glow_rect: return
        self.is_blinking = True
        self._toggle_blink(interval)

    def _toggle_blink(self, interval):
        if not self.is_blinking: return
        self.blink_state = not self.blink_state
        color = self.glow_color if self.blink_state else self.master["bg"]
        self.itemconfig(self.glow_rect, fill=color)
        self.after(interval, self._toggle_blink, interval)

    def _on_click(self, event):
        play_click()
        if self.command:
            self.command()

    def _on_enter(self, event):
        self.itemconfig(self.rect, fill=self.hover_bg)

    def _on_leave(self, event):
        self.itemconfig(self.rect, fill=self.default_bg)


class ScrollableFrame(tk.Frame):
    def __init__(self, parent, bg="#121212", *args, **kwargs):
        super().__init__(parent, bg=bg, *args, **kwargs)
        
        # Style for Scrollbar
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            "Vertical.TScrollbar", 
            gripcount=0,
            background="#333333", 
            darkcolor="#121212", 
            lightcolor="#121212",
            troughcolor="#121212",
            bordercolor="#121212", 
            arrowcolor="#aaaaaa"
        )

        self.canvas = tk.Canvas(self, bg=bg, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview, style="Vertical.TScrollbar")
        self.scrollable_frame = tk.Frame(self.canvas, bg=bg)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", tags="frame")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Determine width to fit window
        self.canvas.bind('<Configure>', self._on_canvas_configure)
        
        # Mousewheel
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig("frame", width=event.width)
    
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    def auto_scroll(self):
        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1.0)


class BandersnatchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bandersnatch")
        self.root.geometry("900x700")
        self.root.configure(bg="#121212")

        self.typing_speed = 25  # ms
        self.current_node = None
        self.current_music_type = "normal" 
        self.input_locked = False # Prevent double clicks
        self.chat_history = [] # To save entire interaction
        
        # Main Container to hold screens
        self.container = tk.Frame(root, bg="#121212")
        self.container.pack(fill="both", expand=True)
        
        # Screens
        self.title_frame = None
        self.game_frame = None
        
        self.setup_title_screen()

    def setup_title_screen(self):
        self.title_frame = tk.Frame(self.container, bg="#121212")
        self.title_frame.pack(fill="both", expand=True)
        
        # Spacer
        tk.Label(self.title_frame, text="", bg="#121212", height=8).pack()
        
        # Title
        tk.Label(
            self.title_frame, 
            text="BANDERSNATCH", 
            font=get_font(48, bold=True), 
            bg="#121212", 
            fg="#ffffff"
        ).pack(pady=10)
        
        # Subtitle
        tk.Label(
            self.title_frame, 
            text="July 9th, 1984", 
            font=get_font(16), 
            bg="#121212", 
            fg="#888888"
        ).pack(pady=5)
        
        # Buttons Frame
        btn_frame = tk.Frame(self.title_frame, bg="#121212")
        btn_frame.pack(pady=50)
        
        save_path = "savegame.json"
        if os.path.exists(save_path):
            # Continue Button
            RoundedButton(
                btn_frame, 
                text="CONTINUE INTERACTION", 
                command=self.continue_game,
                width=300,
                height=60,
                radius=30,
                bg="#444444",
                fg="white"
            ).pack(pady=10)
            
            # New Game Button
            RoundedButton(
                btn_frame, 
                text="NEW GAME", 
                command=self.start_game,
                width=300,
                height=60,
                radius=30,
                bg="#333333",
                fg="#bbbbbb"
            ).pack(pady=10)
        else:
            # Start Button
            RoundedButton(
                btn_frame, 
                text="START INTERACTION", 
                command=self.start_game,
                width=300,
                height=60,
                radius=30,
                bg="#333333",
                fg="white"
            ).pack()

    def save_game(self):
        """Save current progress to JSON"""
        if not self.current_node: return
        data = {
            "current_node": self.current_node,
            "state": state,
            "chat_history": self.chat_history
        }
        try:
            with open("savegame.json", "w") as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Error saving game: {e}")

    def continue_game(self):
        """Load progress and start"""
        try:
            if os.path.exists("savegame.json"):
                with open("savegame.json", "r") as f:
                    data = json.load(f)
                    
                # Restore state
                global state
                # Ensure all keys from save are restored
                for k, v in data.get("state", {}).items():
                    state[k] = v
                
                # Restore history
                self.chat_history = data.get("chat_history", [])
                
                # Close title and start
                if self.title_frame:
                    self.title_frame.destroy()
                    self.title_frame = None
                
                # Add a brief delay before showing game
                self.root.after(1000, lambda: self._show_game_screen(
                    node_id=data.get("current_node", "start"),
                    history=self.chat_history
                ))
        except Exception as e:
            print(f"Error loading game: {e}")
            self.start_game()

    def setup_game_ui(self):
        self.game_frame = tk.Frame(self.container, bg="#121212")
        # Do not pack yet, waiting for transition
        
        # UI Components within Game Frame
        self.chat_area = ScrollableFrame(self.game_frame, bg="#0d1117") 
        self.chat_area.pack(expand=True, fill="both")

        self.button_frame = tk.Frame(self.game_frame, bg="#121212", pady=15)
        self.button_frame.pack(fill="x")
        
        # Volume control in bottom right
        self.volume_frame = tk.Frame(self.game_frame, bg="#121212")
        self.volume_frame.place(relx=1.0, rely=1.0, anchor="se", x=-20, y=-20)
        
        # Volume icon (clickable)
        self.volume_icon = tk.Label(
            self.volume_frame,
            text="🔊",
            bg="#121212",
            fg="#ffffff",
            font=("Segoe UI", 12),
            cursor="hand2"
        )
        self.volume_icon.pack(side="left", padx=5)
        self.volume_icon.bind("<Button-1>", lambda e: self.toggle_volume_slider())
        
        # Volume slider (initially hidden)
        self.volume_slider = tk.Scale(
            self.volume_frame,
            from_=0,
            to=100,
            orient="horizontal",
            bg="#333333",
            fg="#ffffff",
            highlightthickness=0,
            troughcolor="#121212",
            activebackground="#555555",
            length=150,
            width=15,
            command=self.on_volume_change
        )
        self.volume_slider.set(30)  # Default 30%
        self.slider_visible = False  # Start hidden

    def toggle_volume_slider(self):
        """Show/hide volume slider"""
        if self.slider_visible:
            self.volume_slider.pack_forget()
            self.slider_visible = False
        else:
            self.volume_slider.pack(side="left")
            self.slider_visible = True

    def on_volume_change(self, value):
        """Update background music volume"""
        if PYGAME_AVAILABLE:
            try:
                volume = float(value) / 100.0
                state["volume"] = volume
                pygame.mixer.music.set_volume(volume)
            except:
                pass

    def start_game(self):
        # Clear existing save if starting fresh
        if os.path.exists("savegame.json"):
            try:
                os.remove("savegame.json")
            except:
                pass
        
        # Reset state to default
        global state
        state["cereal"] = None
        state["music"] = None
        state["offer"] = None
        state["colin_follow"] = False
        state["mohan_counter"] = 0
        state["inventory"] = []
        # Keep volume setting
        
        self.chat_history = [] 

        # Destroy title screen
        if self.title_frame:
            self.title_frame.destroy()
            self.title_frame = None
        
        # Add a brief delay before showing game (fade-like effect)
        self.root.after(1500, self._show_game_screen)
    
    def _show_game_screen(self, node_id="start", history=None):
        # Setup and show game
        self.setup_game_ui()
        self.game_frame.pack(fill="both", expand=True)
        
        # Restore chat history if any
        if history:
            for msg in history:
                self.create_bubble(msg["text"], is_user=msg["is_user"], add_to_history=False)
        
        # Start baseline music
        self.current_music_type = "normal"
        start_background_music("normal")
        
        # Start Story
        self.load_node(node_id)

    def clear_buttons(self):
        for widget in self.button_frame.winfo_children():
            widget.destroy()

    def create_bubble(self, text, is_user=False, add_to_history=True):
        if add_to_history and text.strip():
            self.chat_history.append({"text": text, "is_user": is_user})
            
        row = tk.Frame(self.chat_area.scrollable_frame, bg="#0d1117", pady=2, padx=10) # Reduced row spacing
        row.pack(fill="x")
        
        if is_user:
            bg_color = "#d9fdd3"
            fg_color = "black"
        else:
            bg_color = "#ffffff"
            fg_color = "black"

        align = "e" if is_user else "w"
        
        bubble = RoundedBubble(
            row,
            text=text,
            max_width=500,
            bg_color=bg_color,
            fg_color=fg_color,
            is_user=is_user
        )
        bubble.pack(side="right" if is_user else "left", anchor=align)
        
        self.chat_area.auto_scroll()
        return bubble

    def animate_text(self, bubble_widget, full_text, index=0):
        if index <= len(full_text):
            # Start typing sound once at the beginning
            if index == 0:
                play_type()
            
            current_text = full_text[:index]
            bubble_widget.update_text(current_text)
            self.chat_area.auto_scroll()
            self.root.after(50, self.animate_text, bubble_widget, full_text, index+1)
        else:
            # Stop typing sound when animation completes (now safe with pygame)
            stop_type()
            # Add final text to history after typing
            self.chat_history.append({"text": full_text, "is_user": False})
            self.save_game()
            self.show_choices()

    def load_node(self, node_id):
        self.current_node = node_id
        # Auto-save
        self.save_game()
        
        if node_id not in STORY_NODES:
            self.create_bubble("End of Line.")
            self.clear_buttons()
            RoundedButton(
                self.button_frame, 
                text="Restart", 
                command=lambda: self.restart_game(),
                bg="#333333", fg="white"
            ).pack(pady=10)
            return

        node = STORY_NODES[node_id]
        
        # Dynamic Music Switch
        music_type = node.get("music", "normal")
        if music_type != self.current_music_type:
            start_background_music(music_type)
            self.current_music_type = music_type
        
        # Resolve text
        text = node["text"]
        if callable(text):
            text = text()
        
        self.clear_buttons()
        self.input_locked = True # Lock input while typing
        
        # Create empty bubble and start typing animation
        bubble = self.create_bubble("", is_user=False)
        self.animate_text(bubble, text)

    def show_choices(self):
        self.input_locked = False # Unlock input
        node = STORY_NODES[self.current_node]
        is_intense = node.get("music") == "intense"
        
        choice_items = list(node["choices"].items())
        for i, (label, next_node_id) in enumerate(choice_items):
            # Blue Pill / Red Pill Effect for Intense Scenes
            glow = None
            if is_intense:
                if i == 0: glow = "#ff4444" # Red
                elif i == 1: glow = "#4444ff" # Blue
                else: glow = "#ffffff" # White for any others
            
            btn = RoundedButton(
                self.button_frame,
                text=label,
                command=lambda l=label, n=next_node_id: self.transition(l, n),
                bg="#333333", 
                fg="#ffffff",
                hover_bg="#555555",
                glow_color=glow
            )
            btn.pack(pady=5)
            
            if is_intense and glow:
                btn.start_blinking(400) # Fast blinking for intensity

    def transition(self, label, next_node_id):
        if self.input_locked:
            return
            
        self.input_locked = True # Lock immediately
        
        # Delay the visual response to separate it from the click sound
        # Sound plays at T=0 (on click)
        # User Bubble appears at T=400ms
        self.root.after(400, lambda: self._finish_transition(label, next_node_id))

    def _finish_transition(self, label, next_node_id):
        # User Bubble
        self.create_bubble(label, is_user=True)
        
        if next_node_id == "quit":
            self.root.quit()
        else:
            # Game Response appears at T=400ms + 800ms
            self.root.after(800, lambda: self.load_node(next_node_id))

    def restart_game(self):
        # Clear chat UI and history
        self.chat_history = []
        for widget in self.chat_area.scrollable_frame.winfo_children():
            widget.destroy()
        
        # We don't necessarily reset 'state' here as some choices might persist in Bandersnatch logic
        # but for a clean 'Restart', we should at least clear the visible history.
        self.load_node("start")


# Story Data (Placeholder for now)
STORY_NODES = {
    "start": {
        "text": "July 9th, 1984.\n\nYou wake up. The morning light filters through the curtains. It's a big day for you at Tuckersoft.",
        "choices": {
            "Wake Up": "cereal",
        }
    },
    "cereal": {
        "text": "You walk into the kitchen. Your dad is rustling the newspaper.\n\nStefan, what do you want for breakfast?",
        "choices": {
            "Kellogg's Frosties": "bus_frosties",
            "Quaker Sugar Puffs": "bus_puffs"
        }
    },
    "bus_frosties": {
        "text": "You crunch on the Frosties. Sweet, predictable power. You catch the bus to Tuckersoft.",
        "choices": {
            "Pick Music": "music_selection"
        }
    },
    "bus_puffs": {
        "text": "Sugar Puffs. The rush hits you. You catch the bus to Tuckersoft.",
        "choices": {
            "Pick Music": "music_selection"
        }
    },
    "music_selection": {
        "text": "You put on your headphones. The world outside is gray. You need a soundtrack.",
        "choices": {
            "Now That's What I Call Music": "music_now",
            "Thompson Twins": "music_thompson"
        }
    },
    "music_now": {
        "text": "'Here Comes The Rain' plays. A synth-pop anthem for a gray sky.",
        "choices": {
            "Arrive at Tuckersoft": "meet_tucker"
        }
    },
    "music_thompson": {
        "text": "'Hold Me Now' plays. Sentimental. Maybe too sentimental.",
        "choices": {
            "Arrive at Tuckersoft": "meet_tucker"
        }
    },
    "meet_tucker": {
        "text": "You arrive at Tuckersoft. Mohan Tucker is impressed by your demo.\n\n'We want to publish it properly. Team, office, the works. Will you do it?'",
        "choices": {
            "Accept Offer": "offer_accept",
            "Refuse Offer": "offer_refuse"
        }
    },
    "offer_accept": {
        "text": "You accept. The team takes over. The vision is diluted. \n\nFive months later, Bandersnatch is released to mediocre reviews (0/5 Stars). a 'rushed job'.\n\nDEAD END.",
        "choices": {
            "Try Again": "meet_tucker"
        }
    },
    "offer_refuse": {
        "text": "You refuse. 'I need to do this myself,' you say.\n\nTucker looks stunned but agrees. 'Okay, deliver it by September 12th.' \n\nYou leave.",
        "choices": {
            "Visit Therapist": "therapist_mom"
        }
    },
    "therapist_mom": {
        "text": "Dr. Haynes office. She asks about your past. \n\n'Do you want to talk about your mother?'",
        "music": "intense",
        "choices": {
            "Yes": "mom_yes",
            "No": "mom_no"
        }
    },
    "mom_no": {
        "text": "'We can't make progress if you're not honest, Stefan.'",
        "choices": {
            "Okay, Talk": "mom_yes",
            "Refuse": "mom_no_persist"
        }
    },
    "mom_no_persist": {
        "text": "The session ends early.",
        "choices": {
            "Go to Record Store": "record_store"
        }
    },
    "mom_yes": {
        "text": "You talk about the rabbit. The train. The delay. Her death.\n\nIt still hurts.",
        "music": "intense",
        "choices": {
            "Go to Record Store": "record_store"
        }
    },
    "record_store": {
        "text": "You need inspiration. Which vinyl do you buy?",
        "choices": {
            "The Bermuda Triangle": "vinyl_bermuda",
            "Phaedra": "vinyl_phaedra"
        }
    },
    "vinyl_bermuda": {
        "text": "Bermuda Triangle. Mysterious. Just like the code.",
        "choices": {
            "Work on Game": "dad_lunch"
        }
    },
    "vinyl_phaedra": {
        "text": "Phaedra. Electronic. Tangerine Dream. Perfect for coding.",
        "choices": {
            "Work on Game": "dad_lunch"
        }
    },
    "dad_lunch": {
        "text": "You're working. Dad interrupts. 'Lunch time, Stefan.'\n\nYou're in the zone. He's ruining it.",
        "choices": {
            "Throw Tea on Computer": "lunch_tea",
            "Shout at Dad": "lunch_shout"
        }
    },
    "lunch_tea": {
        "text": "You snap. The tea flies. The computer fizzes and dies.\n\nYears of work lost.\n\nDEAD END.",
        "music": "intense",
        "choices": {
            "Try Again": "dad_lunch"
        }
    },
    "lunch_shout": {
        "text": "You scream at him. He backs off, hurt. \n\nHe takes you to Dr. Haynes again the next day.",
        "choices": {
            "Go to Clinic": "clinic_colin"
        }
    },
    "clinic_colin": {
        "text": "Outside the clinic, you see Colin walking away.",
        "choices": {
            "See Dr. Haynes": "visit_haynes",
            "Follow Colin": "follow_colin"
        }
    },
    "visit_haynes": {
        "text": "You see Dr. Haynes. She increases your dosage.\n\n'Take them, Stefan. They help.'",
        "music": "intense",
        "choices": {
            "Take Pills": "pills_take",
            "Flush Pills": "pills_flush"
        }
    },
    "pills_take": {
        "text": "You take the pills. The world stops spinning. The game releases on time.\n\n2.5/5 Stars. 'Soulless', say the reviews.\n\nDEAD END.",
        "choices": {
            "Try Again": "clinic_colin"
        }
    },
    "pills_flush": {
        "text": "The pills swirl down the toilet. You are in control.\n\nBut the deadline looms.",
        "choices": {
            "Work (Frustrated)": "frustrated_choice"
        }
    },
    "follow_colin": {
        "text": "You follow Colin to his flat. Reality feels... thin here.\n\n'Offer you something to expand the mind?' he asks.",
        "music": "intense",
        "choices": {
            "Take LSD": "lsd_yes",
            "Refuse": "lsd_no"
        }
    },
    "lsd_no": {
        "text": "You refuse. Colin spikes your tea anyway. The walls begin to breathe.",
        "music": "intense",
        "choices": {
            "Listen to Colin": "colin_balcony"
        }
    },
    "lsd_yes": {
        "text": "You accept. The world melts. Colin talks about timelines. PAC-MAN. Control.",
        "music": "intense",
        "choices": {
            "Listen to Colin": "colin_balcony"
        }
    },
    "colin_balcony": {
        "text": "Balcony edge. 'One of us has to jump,' Colin says. 'To show it doesn't matter.'\n\nWho jumps?",
        "music": "intense",
        "choices": {
            "Stefan": "jump_stefan",
            "Colin": "jump_colin"
        }
    },
    "jump_stefan": {
        "text": "You step off. Gravity takes over. \n\nThe game is finished without you. \n\nDEAD END.",
        "music": "intense",
        "choices": {
            "Try Again": "colin_balcony"
        }
    },
    "jump_colin": {
        "text": "Colin steps off. He creates a mess.\n\nYou wake up. Was it a dream?\n\nBack to work.",
        "music": "intense",
        "choices": {
            "Work (Frustrated)": "frustrated_choice"
        }
    },
    "frustrated_choice": {
        "text": "The code is broken. The bugs are crawling under the screen.\n\nHow do you react?",
        "music": "intense",
        "choices": {
            "Hit Desk": "item_bed",
            "Destroy Computer": "destroy_pc"
        }
    },
    "destroy_pc": {
        "text": "You smash the computer. It's over.\n\nDEAD END.",
        "choices": {
            "Try Again": "frustrated_choice"
        }
    },
    "item_bed": {
        "text": "You hit the desk. You need comfort. You go to your room.\n\nWhat do you pick up?",
        "choices": {
            "Book (Bandersnatch)": "dad_safe",
            "Family Photo": "mirror_travel"
        }
    },
    "dad_safe": {
        "text": "You find the book. And something else... keys to the safe.",
        "choices": {
            "Enter Password": "password_entry"
        }
    },
    "mirror_travel": {
        "text": "You look at the photo. The mirror calls to you. You travel back to the train station.",
        "choices": {
            "Go with Mom?": "train_death"
        }
    },
    "train_death": {
        "text": "You go with her. The train crashes.\n\nStefan dies in the chair in the present day.",
        "choices": {
            "Restart": "start"
        }
    },
    "password_entry": {
        "text": "The safe needs a password.",
        "choices": {
            "PAX": "pass_pax",
            "TOY": "pass_toy",
            "JFD": "pass_jfd"
        }
    },
    "pass_pax": {
        "text": "The monster PAX appears! It's a hallucination. You wake up.",
        "music": "intense",
        "choices": {
            "Work": "symbol_choice"
        }
    },
    "pass_jfd": {
        "text": "Jerome F. Davies appears. He laughs. Madness.",
        "music": "intense",
        "choices": {
            "Work": "symbol_choice"
        }
    },
    "pass_toy": {
        "text": "You find the rabbit. You place it under the bed.\n\nTimeline corrected?",
        "choices": {
            "Wake Up": "start"
        }
    },
    "symbol_choice": {
        "text": "The symbol is everywhere. You are not in control.\n\nKill Dad?",
        "music": "intense",
        "choices": {
            "Back Off": "frustrated_choice",
            "Kill Dad": "kill_dad"
        }
    },
    "kill_dad": {
        "text": "You did it. He's dead.\n\nWhat now?",
        "music": "intense",
        "choices": {
            "Bury Him": "bury_dad",
            "Chop Him Up": "chop_dad"
        }
    },
    "bury_dad": {
        "text": "You bury him. The dog finds him later. Jail.",
        "music": "intense",
        "choices": {
            "Restart": "start"
        }
    },
    "chop_dad": {
        "text": "You chop him up. Grim. But effective.\n\nThe game is released. 5/5 Stars. ",
        "music": "intense",
        "choices": {
            "Future Ending": "pearl_ending"
        }
    },
    "pearl_ending": {
        "text": "Years later, Pearl Ritchie remakes the game. She finds the bugs...",
        "music": "intense",
        "choices": {
            "Destroy Computer": "pearl_destroy"
        }
    },
    "pearl_destroy": {
        "text": "She destroys the computer. History repeats itself.\n\nEnd of Line.",
        "music": "intense",
        "choices": {
            "Restart": "start"
        }
    }
}

if __name__ == "__main__":
    root = tk.Tk()
    app = BandersnatchApp(root)
    root.mainloop()

