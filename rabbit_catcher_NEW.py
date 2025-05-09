import tkinter as tk
import random
import time

def open_settings():
    print("Opening settings...")
    # Hide start menu elements
    game_title_label.place_forget()
    start_button.place_forget()
    exit_button.place_forget()
    settings_button.place_forget()
    window.update()

    # --- Settings State ---
    global timer_enabled, rabbit_speed, difficulty, time_left

    # Defaults for settings
    if 'rabbit_speed' not in globals():
        globals()['rabbit_speed'] = 2500  # ms
    if 'difficulty' not in globals():
        globals()['difficulty'] = "custom"

    # Tkinter variables
    timer_var = tk.BooleanVar(value=timer_enabled)
    speed_var = tk.IntVar(value=rabbit_speed)
    difficulty_var = tk.StringVar(value=difficulty)

    # --- Difficulty Presets ---
    def apply_difficulty(diff):
        if diff == "custom":
            timer_check.config(state="normal")
            speed_slider.config(state="normal")
        elif diff == "easy":
            timer_var.set(True)
            speed_var.set(999999)
            timer_check.config(state="disabled")
            speed_slider.config(state="disabled")
        elif diff == "normal":
            timer_var.set(True)
            speed_var.set(2500)
            timer_check.config(state="disabled")
            speed_slider.config(state="disabled")
        elif diff == "hard":
            timer_var.set(True)
            speed_var.set(1200)
            timer_check.config(state="disabled")
            speed_slider.config(state="disabled")
        elif diff == "super hard":
            timer_var.set(True)
            speed_var.set(900)
            timer_check.config(state="disabled")
            speed_slider.config(state="disabled")
        update_timer_display()

    def on_difficulty_change(*args):
        diff = difficulty_var.get()
        apply_difficulty(diff)

    # --- Timer Toggle ---
    def update_timer_display():
        global timer_label, timer_enabled, time_left
        timer_enabled = timer_var.get()
        if timer_label and timer_label.winfo_exists():
            if not timer_enabled:
                timer_label.config(text="∞", fg="red", font=("Arial", 24))
            else:
                timer_label.config(text=f"Time: {time_left}", fg="black", font=("Arial", 16))

    timer_check = tk.Checkbutton(window, text="Enable Timer", variable=timer_var, command=update_timer_display)
    timer_check.place(relx=0.5, rely=0.25, anchor=tk.CENTER)

    # --- Rabbit Speed Slider ---
    speed_label = tk.Label(window, text="Rabbit Speed (ms, lower is faster):")
    speed_label.place(relx=0.5, rely=0.37, anchor=tk.CENTER)
    speed_slider = tk.Scale(window, from_=300, to=4000, orient=tk.HORIZONTAL, variable=speed_var, resolution=100, length=200)
    speed_slider.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

    # --- Difficulty Dropdown ---
    diff_label = tk.Label(window, text="Difficulty:")
    diff_label.place(relx=0.5, rely=0.57, anchor=tk.CENTER)
    difficulty_options = ["custom", "easy", "normal", "hard", "super hard"]
    difficulty_menu = tk.OptionMenu(window, difficulty_var, *difficulty_options, command=lambda _: on_difficulty_change())
    difficulty_menu.place(relx=0.5, rely=0.63, anchor=tk.CENTER)

    # --- Back Button ---
    def back_to_menu():
        global timer_enabled, rabbit_speed, difficulty, time_left, rabbit_auto_move, timer_tick, regain_time
        timer_enabled = timer_var.get()
        rabbit_speed = speed_var.get()
        difficulty = difficulty_var.get()
        if difficulty == "easy":
            rabbit_auto_move = False
            timer_tick = 1.0
            regain_time = True
            time_left = 30
        elif difficulty == "hard":
            rabbit_auto_move = True
            timer_tick = 0.7
            regain_time = True
            time_left = 30
        elif difficulty == "super hard":
            rabbit_auto_move = True
            timer_tick = 0.5
            regain_time = False
            time_left = 40
        elif difficulty == "normal":
            rabbit_auto_move = True
            timer_tick = 1.0
            regain_time = True
            time_left = 30
        else:
            pass
        timer_check.place_forget()
        speed_slider.place_forget()
        difficulty_menu.place_forget()
        speed_label.place_forget()
        diff_label.place_forget()
        back_button.place_forget()
        show_start_menu()

    back_button = tk.Button(window, text="Back to Menu", font=("Arial", 16), command=back_to_menu)
    back_button.place(relx=0.5, rely=0.85, anchor=tk.CENTER)

    apply_difficulty(difficulty_var.get())
    update_timer_display()

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
    global score, score_label, time_left, game_active, game_paused, regain_time, timer_enabled
    if game_active and not game_paused:
        score += 1
        score_label.config(text=f"Score: {score}")
        if timer_enabled and regain_time:
            time_left += 5
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
    global game_active, score, time_left, rabbit_button, spinner_label, animating, difficulty, timer_tick, regain_time, rabbit_auto_move, rabbit_speed, timer_enabled
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
    elif difficulty == "hard":
        time_left = 30
        timer_tick = 0.7
        regain_time = True
        rabbit_auto_move = True
        rabbit_speed = 1200
        timer_enabled = True
    elif difficulty == "normal":
        time_left = 30
        timer_tick = 1.0
        regain_time = True
        rabbit_auto_move = True
        rabbit_speed = 2500
        timer_enabled = True
    elif difficulty == "easy":
        time_left = 30
        timer_tick = 1.0
        regain_time = True
        rabbit_auto_move = False
        rabbit_speed = 999999
        timer_enabled = True
    else:
        pass
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
        score_label.pack_forget()
        score_label.place_forget()
    if timer_label and timer_label.winfo_ismapped():
        timer_label.pack_forget()
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
    score_label.pack(pady=10)
    timer_label.pack()
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
