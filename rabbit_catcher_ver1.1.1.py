import tkinter as tk
import random
import time

# --- Game State Variables ---
score = 0
time_left = 30
game_active = False
game_paused = False
timer_enabled = True
rabbit_speed = 2500
difficulty = "custom"
rabbit_auto_move = True
timer_tick = 1.0
regain_time = True
regain_amount = 2  # Default for normal/medium, will be set per difficulty

# --- Animation Constants ---
HOVER_COLOR = "lightgray"
CLICK_RELIEF = "sunken"
ORIGINAL_RELIEF = "raised"
SPINNER_CHARS = ["Loading", "Loading.", "Loading..", "Loading..."]
SPINNER_DELAY = 300  # milliseconds (adjust for speed)
TRANSITION_DELAY = 2000
SLIDE_DURATION = 500  # milliseconds
SLIDE_STEPS = 20

# --- Animation Variables ---
spinner_index = 0
spinner_running = False
animating = False

# --- Widgets ---
spinner_label = None
game_title_label = None
start_button = None
exit_button = None
settings_button = None
score_label = None
timer_label = None
rabbit_button = None
pause_button = None
quit_button = None

# --- Emoji Options ---
EMOJI_OPTIONS = [
    ("Rabbit (Default)", "🐇"),
    ("Frog", "🐸"),
    ("Chicken", "🐔"),
    ("Cricket", "🦗"),
    ("Ladybug", "🐞"),
    ("Monkey", "🐒"),
]
# selected_emoji will be initialized after window is created

def open_settings():
    print("Opening settings...")
    # Hide start menu elements
    if game_title_label: game_title_label.place_forget()
    if start_button: start_button.place_forget()
    if exit_button: exit_button.place_forget()
    if settings_button: settings_button.place_forget()
    window.update()

    # Make window bigger for settings
    window.geometry("500x600")  # Increased height to fit new slider

    # --- Settings State ---
    global timer_enabled, rabbit_speed, difficulty, time_left, regain_amount, selected_emoji, timer_tick

    # Settings Title
    settings_title_label = tk.Label(window, text="Settings", font=("Arial", 28, "bold"))
    settings_title_label.place(relx=0.5, rely=0.08, anchor=tk.CENTER)

    # Defaults for settings
    if 'rabbit_speed' not in globals():
        globals()['rabbit_speed'] = 2500  # ms
    if 'difficulty' not in globals():
        globals()['difficulty'] = "custom"
    if 'timer_tick' not in globals():
        globals()['timer_tick'] = 1.0

    # Tkinter variables
    timer_var = tk.BooleanVar(value=timer_enabled)
    speed_var = tk.IntVar(value=rabbit_speed)
    difficulty_var = tk.StringVar(value=difficulty)
    regain_amount_var = tk.IntVar(value=regain_amount)
    timer_tick_var = tk.DoubleVar(value=timer_tick)

    # --- Emoji Dropdown ---
    emoji_name_var = tk.StringVar(value=EMOJI_OPTIONS[0][0])

    def on_emoji_change(selected_name):
        for name, emoji in EMOJI_OPTIONS:
            if name == selected_name:
                selected_emoji.set(emoji)
                if rabbit_button:
                    rabbit_button.config(text=emoji)
                break

    emoji_label = tk.Label(window, text="Choose Button Emoji:")
    emoji_label.place(relx=0.5, rely=0.15, anchor=tk.CENTER)
    emoji_names = [name for name, emoji in EMOJI_OPTIONS]
    emoji_menu = tk.OptionMenu(window, emoji_name_var, *emoji_names, command=on_emoji_change)
    emoji_menu.place(relx=0.5, rely=0.20, anchor=tk.CENTER)

    # --- Difficulty Presets ---
    def apply_difficulty(diff):
        if diff == "custom":
            timer_check.config(state="normal")
            speed_slider.config(state="normal")
            regain_amount_entry.config(state="normal")
            timer_tick_slider.config(state="normal")
        elif diff == "easy":
            timer_var.set(True)
            speed_var.set(999999)
            regain_amount_var.set(3)
            timer_tick_var.set(1.0)
            timer_check.config(state="disabled")
            speed_slider.config(state="disabled")
            regain_amount_entry.config(state="disabled")
            timer_tick_slider.config(state="disabled")
        elif diff == "normal":
            timer_var.set(True)
            speed_var.set(2500)
            regain_amount_var.set(2)
            timer_tick_var.set(1.0)
            timer_check.config(state="disabled")
            speed_slider.config(state="disabled")
            regain_amount_entry.config(state="disabled")
            timer_tick_slider.config(state="disabled")
        elif diff == "hard":
            timer_var.set(True)
            speed_var.set(1200)
            regain_amount_var.set(1)
            timer_tick_var.set(0.7)
            timer_check.config(state="disabled")
            speed_slider.config(state="disabled")
            regain_amount_entry.config(state="disabled")
            timer_tick_slider.config(state="disabled")
        elif diff == "super hard":
            timer_var.set(True)
            speed_var.set(900)
            regain_amount_var.set(0)
            timer_tick_var.set(0.5)
            timer_check.config(state="disabled")
            speed_slider.config(state="disabled")
            regain_amount_entry.config(state="disabled")
            timer_tick_slider.config(state="disabled")
        update_timer_display()

    def on_difficulty_change(*args):
        diff = difficulty_var.get()
        apply_difficulty(diff)

    # --- Timer Toggle ---
    def update_timer_display():
        global timer_label, timer_enabled, time_left
        timer_enabled = timer_var.get()
        if timer_label is not None and hasattr(timer_label, "winfo_exists") and timer_label.winfo_exists():
            if not timer_enabled:
                timer_label.config(text="∞", fg="red", font=("Arial", 24))
            else:
                timer_label.config(text=f"Time: {time_left}", fg="black", font=("Arial", 16))

    timer_check = tk.Checkbutton(window, text="Enable Timer", variable=timer_var, command=update_timer_display)
    timer_check.place(relx=0.5, rely=0.25, anchor=tk.CENTER)

    # --- Rabbit Speed Slider ---
    speed_label = tk.Label(window, text="Rabbit Speed (ms, lower is faster):")
    speed_label.place(relx=0.5, rely=0.33, anchor=tk.CENTER)
    speed_slider = tk.Scale(window, from_=300, to=4000, orient=tk.HORIZONTAL, variable=speed_var, resolution=100, length=200)
    speed_slider.place(relx=0.5, rely=0.39, anchor=tk.CENTER)

    # --- Timer Tick Speed Slider ---
    timer_tick_label = tk.Label(window, text="Timer Tick Speed (sec per tick):")
    timer_tick_label.place(relx=0.5, rely=0.47, anchor=tk.CENTER)
    timer_tick_slider = tk.Scale(window, from_=0.2, to=2.0, orient=tk.HORIZONTAL, variable=timer_tick_var, resolution=0.05, length=200, digits=3)
    timer_tick_slider.place(relx=0.5, rely=0.53, anchor=tk.CENTER)

    # --- Difficulty Dropdown ---
    diff_label = tk.Label(window, text="Difficulty:")
    diff_label.place(relx=0.5, rely=0.61, anchor=tk.CENTER)
    difficulty_options = ["custom", "easy", "normal", "hard", "super hard"]
    difficulty_menu = tk.OptionMenu(window, difficulty_var, *difficulty_options, command=lambda _: on_difficulty_change())
    difficulty_menu.place(relx=0.5, rely=0.67, anchor=tk.CENTER)

    # --- Regain Amount Entry (for custom) ---
    regain_label = tk.Label(window, text="Time Gain per Catch:")
    regain_label.place(relx=0.5, rely=0.73, anchor=tk.CENTER)
    regain_amount_entry = tk.Entry(window, textvariable=regain_amount_var, width=5, justify="center")
    regain_amount_entry.place(relx=0.5, rely=0.78, anchor=tk.CENTER)

    # --- Back Button ---
    def back_to_menu():
        global timer_enabled, rabbit_speed, difficulty, time_left, rabbit_auto_move, timer_tick, regain_time, regain_amount, selected_emoji
        timer_enabled = timer_var.get()
        rabbit_speed = speed_var.get()
        difficulty = difficulty_var.get()
        regain_amount = regain_amount_var.get()
        # Save emoji selection
        if rabbit_button:
            rabbit_button.config(text=selected_emoji.get())
        # Set timer_tick from slider if custom, else use preset
        if difficulty == "custom":
            timer_tick = timer_tick_var.get()
            regain_time = True
            regain_amount = regain_amount_var.get()
        elif difficulty == "easy":
            rabbit_auto_move = False
            timer_tick = 1.0
            regain_time = True
            time_left = 30
            regain_amount = 3
        elif difficulty == "hard":
            rabbit_auto_move = True
            timer_tick = 0.7
            regain_time = True
            time_left = 30
            regain_amount = 1
        elif difficulty == "super hard":
            rabbit_auto_move = True
            timer_tick = 0.5
            regain_time = False
            time_left = 40
            regain_amount = 0
        elif difficulty == "normal":
            rabbit_auto_move = True
            timer_tick = 1.0
            regain_time = True
            time_left = 30
            regain_amount = 2
        else:
            regain_time = True
            regain_amount = regain_amount_var.get()
        # Remove all settings widgets
        for widget in [
            timer_check, speed_slider, difficulty_menu, speed_label, diff_label,
            regain_label, regain_amount_entry, back_button, settings_title_label,
            emoji_label, emoji_menu, timer_tick_label, timer_tick_slider
        ]:
            try:
                widget.place_forget()
            except Exception:
                pass
        show_start_menu()
        window.geometry("400x350")

    back_button = tk.Button(window, text="Back to Menu", font=("Arial", 16), command=back_to_menu)
    back_button.place(relx=0.5, rely=0.90, anchor=tk.CENTER)

    apply_difficulty(difficulty_var.get())
    update_timer_display()

# --- Functions ---
def move_rabbit():
    global rabbit_button, game_active, game_paused
    if game_active and not game_paused:
        window.update_idletasks()
        window_width = window.winfo_width()
        window_height = window.winfo_height()
        button_width = rabbit_button.winfo_width()
        button_height = rabbit_button.winfo_height()
        max_x = window_width - button_width
        max_y = window_height - button_height
        max_x = max(0, max_x)
        max_y = max(0, max_y)
        new_x = random.randint(0, max_x)
        new_y = random.randint(0, max_y)
        rabbit_button.place(x=new_x, y=new_y)

def catch_rabbit():
    global score, score_label, time_left, game_active, game_paused, regain_time, timer_enabled, regain_amount
    if game_active and not game_paused:
        score += 1
        score_label.config(text=f"Score: {score}")
        if timer_enabled and regain_time and regain_amount > 0:
            time_left += regain_amount
            timer_label.config(text=f"Time: {time_left}")
        move_rabbit()

def update_timer():
    global time_left, timer_label, game_active, game_paused, rabbit_button, timer_enabled, timer_tick
    if game_active and not game_paused and timer_enabled:
        if time_left > 0:
            timer_label.config(text=f"Time: {time_left}")
            time_left -= 1
            window.after(int(1000 * timer_tick), update_timer)
        elif time_left == 0:
            game_active = False
            if rabbit_button.winfo_ismapped():
                rabbit_button.place_forget()
            timer_label.config(text="Time's Up!")
            start_menu_transition()

def start_rabbit_movement():
    global game_active, game_paused, rabbit_auto_move, rabbit_speed
    if game_active and not game_paused and rabbit_auto_move:
        window.after(rabbit_speed, move_rabbit_repeatedly)

def move_rabbit_repeatedly():
    global game_active, game_paused, rabbit_auto_move, rabbit_speed
    if game_active and not game_paused and rabbit_auto_move:
        move_rabbit()
        window.after(rabbit_speed, move_rabbit_repeatedly)

def pause_game():
    global game_paused, pause_button, game_active
    if not game_active:
        return
    game_paused = not game_paused
    if game_paused:
        pause_button.config(text="Resume")
    else:
        pause_button.config(text="Pause")
        start_rabbit_movement()
        update_timer()

def quit_game():
    global game_active, score_label, timer_label, rabbit_button, pause_button, quit_button, score, time_left, game_paused, animating
    if animating:
        return
    animating = True
    game_active = False
    game_paused = False
    score = 0
    time_left = 30
    slide_out_game()
    slide_in_menu()

def exit_game():
    window.destroy()

def start_game():
    global game_active, score, time_left, rabbit_button, spinner_label, animating, difficulty, timer_tick, regain_time, rabbit_auto_move, rabbit_speed, timer_enabled, regain_amount
    if animating:
        return
    animating = True
    if spinner_label and spinner_label.winfo_ismapped():
        spinner_label.place_forget()
        stop_spinner()
    score = 0
    if difficulty == "super hard":
        time_left = 40
        timer_tick = 0.5
        regain_time = False
        rabbit_auto_move = True
        rabbit_speed = 900
        timer_enabled = True
        regain_amount = 0
    elif difficulty == "hard":
        time_left = 30
        timer_tick = 0.7
        regain_time = True
        rabbit_auto_move = True
        rabbit_speed = 1200
        timer_enabled = True
        regain_amount = 1
    elif difficulty == "normal":
        time_left = 30
        timer_tick = 1.0
        regain_time = True
        rabbit_auto_move = True
        rabbit_speed = 2500
        timer_enabled = True
        regain_amount = 2
    elif difficulty == "easy":
        time_left = 30
        timer_tick = 1.0
        regain_time = True
        rabbit_auto_move = False
        rabbit_speed = 999999
        timer_enabled = True
        regain_amount = 3
    else:
        # custom
        regain_time = True
        # regain_amount already set from settings
    game_active = True
    slide_out_menu()
    slide_in_game()

def show_start_menu():
    global spinner_label, game_title_label, start_button, exit_button, rabbit_button, settings_button
    global score_label, timer_label, pause_button, quit_button, animating
    animating = False
    if spinner_label and spinner_label.winfo_ismapped():
        spinner_label.place_forget()
        stop_spinner()
    # Hide all game elements BEFORE placing menu buttons
    if rabbit_button and rabbit_button.winfo_ismapped():
        rabbit_button.place_forget()
    if score_label and score_label.winfo_ismapped():
        score_label.place_forget()
    if timer_label and timer_label.winfo_ismapped():
        timer_label.place_forget()
    if pause_button and pause_button.winfo_ismapped():
        pause_button.place_forget()
    if quit_button and quit_button.winfo_ismapped():
        quit_button.place_forget()
    # Now place menu buttons
    game_title_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
    start_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    exit_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)
    settings_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

def show_game_elements():
    global score_label, timer_label, rabbit_button, pause_button, quit_button, animating, spinner_label
    animating = False
    if spinner_label and spinner_label.winfo_ismapped():
        spinner_label.place_forget()
        stop_spinner()
    # Use .place instead of .pack for score_label and timer_label for consistency
    score_label.place(x=10, y=10)
    timer_label.place(x=window.winfo_width() - 120, y=10)
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    button_width = rabbit_button.winfo_width()
    button_height = rabbit_button.winfo_height()
    max_x = window_width - button_width
    max_y = window_height - button_height
    initial_x = random.randint(0, max_x)
    initial_y = random.randint(0, max_y)
    rabbit_button.place(x=initial_x, y=initial_y)
    pause_button.place(relx=1.0, rely=1.0, anchor=tk.SE, x=-10, y=-10)
    quit_button.place(relx=1.0, rely=1.0, anchor=tk.SE, x=-80, y=-10)
    start_rabbit_movement()
    update_timer()

def start_menu_transition():
    global spinner_label
    slide_out_game(on_complete=show_start_menu)
    if not spinner_label:
        spinner_label = tk.Label(window, text="", font=("Arial", 16))
    spinner_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    start_spinner()

def show_loading_screen():
    global game_title_label, start_button, exit_button, spinner_label, settings_button
    game_title_label.place_forget()
    start_button.place_forget()
    exit_button.place_forget()
    settings_button.place_forget()
    if not spinner_label:
        spinner_label = tk.Label(window, text="Loading...", font=("Arial", 16))
    spinner_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    start_spinner()
    window.after(TRANSITION_DELAY, start_game)

def animate_spinner():
    global spinner_index, spinner_label, spinner_running
    if spinner_running and spinner_label:
        spinner_label.config(text=SPINNER_CHARS[spinner_index % len(SPINNER_CHARS)])
        spinner_index += 1
        window.after(SPINNER_DELAY, animate_spinner)

def start_spinner():
    global spinner_running
    spinner_running = True
    animate_spinner()

def stop_spinner():
    global spinner_running
    spinner_running = False
    global spinner_index
    spinner_index = 0

def slide_out_menu(step=0):
    global game_title_label, start_button, exit_button, settings_button, SLIDE_STEPS, SLIDE_DURATION, animating
    if step < SLIDE_STEPS:
        offset = (window.winfo_height() / SLIDE_STEPS) * (step + 1)
        game_title_label.place(relx=0.5, rely=0.3 - offset / window.winfo_height(), anchor=tk.CENTER)
        start_button.place(relx=0.5, rely=0.5 - offset / window.winfo_height(), anchor=tk.CENTER)
        exit_button.place(relx=0.5, rely=0.7 - offset / window.winfo_height(), anchor=tk.CENTER)
        settings_button.place(relx=0.5, rely=0.9 - offset / window.winfo_height(), anchor=tk.CENTER)
        window.after(SLIDE_DURATION // SLIDE_STEPS, slide_out_menu, step + 1)
    else:
        game_title_label.place_forget()
        start_button.place_forget()
        exit_button.place_forget()
        settings_button.place_forget()

def slide_in_game(step=0):
    global score_label, timer_label, pause_button, quit_button, SLIDE_STEPS, SLIDE_DURATION, animating
    if step < SLIDE_STEPS:
        offset = (window.winfo_height() / SLIDE_STEPS) * (SLIDE_STEPS - step)
        score_label.place(y=-offset + 10, x=10)
        timer_label.place(y=-offset + 10, x=window.winfo_width() - 80)
        pause_button.place(relx=1.0, rely=1.0 - offset / window.winfo_height(), anchor=tk.SE, x=-10, y=-10)
        quit_button.place(relx=1.0, rely=1.0 - offset / window.winfo_height(), anchor=tk.SE, x=-80, y=-10)
        window.after(SLIDE_DURATION // SLIDE_STEPS, slide_in_game, step + 1)
    else:
        show_game_elements()
        animating = False

def slide_out_game(step=0, on_complete=None):
    global score_label, timer_label, rabbit_button, pause_button, quit_button, SLIDE_STEPS, SLIDE_DURATION, animating
    if step < SLIDE_STEPS:
        offset = (window.winfo_height() / SLIDE_STEPS) * (step + 1)
        score_label.place(y=offset + 10, x=10)
        timer_label.place(y=offset + 10, x=window.winfo_width() - 80)
        rabbit_button.place(relx=0.5, rely=0.5 + offset / window.winfo_height(), anchor=tk.CENTER)
        pause_button.place(relx=1.0, rely=1.0 + offset / window.winfo_height(), anchor=tk.SE, x=-10, y=-10)
        quit_button.place(relx=1.0, rely=1.0 + offset / window.winfo_height(), anchor=tk.SE, x=-80, y=-10)
        window.after(SLIDE_DURATION // SLIDE_STEPS, slide_out_game, step + 1, on_complete)
    else:
        score_label.place_forget()
        timer_label.place_forget()
        rabbit_button.place_forget()
        pause_button.place_forget()
        quit_button.place_forget()
        if on_complete:
            on_complete()

def slide_in_menu(step=0):
    global game_title_label, start_button, exit_button, settings_button, SLIDE_STEPS, SLIDE_DURATION, animating
    # Fixed typo: SLIDE_STPS -> SLIDE_STEPS
    if step < SLIDE_STEPS:
        offset = (window.winfo_height() / SLIDE_STEPS) * (SLIDE_STEPS - step)
        game_title_label.place(relx=0.5, rely=0.3 + offset / window.winfo_height(), anchor=tk.CENTER)
        start_button.place(relx=0.5, rely=0.5 + offset / window.winfo_height(), anchor=tk.CENTER)
        exit_button.place(relx=0.5, rely=0.7 + offset / window.winfo_height(), anchor=tk.CENTER)
        settings_button.place(relx=0.5, rely=0.9 + offset / window.winfo_height(), anchor=tk.CENTER)
        window.after(SLIDE_DURATION // SLIDE_STEPS, slide_in_menu, step + 1)
    else:
        game_title_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
        start_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        exit_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)
        settings_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)
        animating = False

# --- Button Animation Functions ---
def on_enter(event):
    event.widget.config(bg=HOVER_COLOR)

def on_leave(event):
    event.widget.config(bg=event.widget.original_bg)

def on_press(event):
    event.widget.config(relief=CLICK_RELIEF)

def on_release(event):
    event.widget.config(relief=ORIGINAL_RELIEF)

# --- Main Window Setup ---
window = tk.Tk()
window.title("Catch the Rabbit!")
window.geometry("400x350")

# --- Emoji StringVar (must be after window is created) ---
selected_emoji = tk.StringVar(value="🐇")

# --- Start Menu Elements ---
game_title_label = tk.Label(window, text="Catch the Rabbit!", font=("Arial", 24))
start_button = tk.Button(window, text="Start Game", font=("Arial", 16), command=show_loading_screen)
exit_button = tk.Button(window, text="Exit Game", font=("Arial", 16), command=exit_game)
settings_button = tk.Button(window, text="Settings", font=("Arial", 16), command=open_settings)

# --- Game Elements (Initially Hidden) ---
score_label = tk.Label(window, text=f"Score: {score}", font=("Arial", 16))
timer_label = tk.Label(window, text=f"Time: {time_left}", font=("Arial", 16))
rabbit_button = tk.Button(window, text="🐇", font=("Arial", 24), command=catch_rabbit)
pause_button = tk.Button(window, text="Pause", font=("Arial", 12), command=pause_game)
quit_button = tk.Button(window, text="Return to Menu", font=("Arial", 12), command=quit_game)

# --- Store Original Button Backgrounds and Bind Events ---
for button in [start_button, exit_button, rabbit_button, pause_button, quit_button, settings_button]:
    button.original_bg = button["bg"]
    button.config(relief=ORIGINAL_RELIEF)
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)
    button.bind("<ButtonPress-1>", on_press)
    button.bind("<ButtonRelease-1>", on_release)

# --- Place initial Start Menu Elements ---
start_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
exit_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)
settings_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

# --- Initial Loading Screen Display ---
show_loading_screen()

# --- Start the Tkinter Event Loop ---
window.mainloop()
