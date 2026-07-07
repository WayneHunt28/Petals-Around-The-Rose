import time
import random

from petals.dice import roll_dice
from petals.logic import calculate_petals

from random import randint

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.columns import Columns
from rich.live import Live
from rich.console import Group
from rich.align import Align

console = Console()

game_state = {
    "round": 0,
    "score": 0,
    "streak": 0,
    "last_roll": [],
    "difficulty": 1,
    "hint_level": 0
}

# Difficulty tracker
def update_difficulty():
    streak = game_state["streak"]
    
    if streak >= 4:
        game_state["difficulty"] = 3  # hard mode
    elif streak >= 2:
        game_state["difficulty"] = 2  # medium mode
    else:
        game_state["difficulty"] = 1  # easy mode

# Provide hints that cycle through with each incorrect guess
def get_hint(level, dice=None):
    if level == 0:
        return None
    
    hints = [
        "👀  Look for symmetry in the dice...",
        "🧠  Only certain dice values contribute to the score...",
        "🔍  Focus on odd number dice, they behave differently...",
        "👀  Try comparing several rolls to discover the rule...",
        "🔥  Ignore the total shown on the dice..."
    ]
    
    index = (level - 1) % len(hints)
    return hints[index]

# Streak tracker
def get_momentum():
    streak = game_state.get("streak", 0)
    
    if streak >= 3:
        return ("HOT", "red")
    elif streak== 2:
        return ("WARM", "yellow")
    else:
        return ("COLD", "blue")

# Performance tracker
def get_performance():
    score = game_state.get("score", 0)
    round_num = max(game_state.get("round", 1), 1)
    
    avg = score / round_num
    
    if avg >= 2:
        return ("STRONG", "green")
    elif avg >= 1:
        return ("NORMAL", "cyan")
    else:
        return ("LOW", "red")

# Live updating scoreboard for each round
def build_hud(message=""):
    momentum, m_colour = get_momentum()
    perf, p_colour = get_performance()
    
    hud = Text()
    
    hud.append(f"🎲   Round: {game_state['round']}\n", style="bold cyan")
    hud.append(f"🔥   Streak: {game_state['streak']} ({momentum})\n", style=m_colour)
    hud.append(f"📊   Performance: {perf}\n", style=p_colour)
    hud.append(f"⚙    Difficulty: {game_state['difficulty']}\n", style="magenta")
    hud.append(f"💡   Hint Level: {game_state['hint_level']}\n", style="cyan")
    
    if message:
        hud.append(f"\n {message}\n", style="bold yellow")
        
    # Progressive hint system (only based on hint_level)
    hint = get_hint(game_state["hint_level"])
    if hint:
        hud.append(f"\n💡  Hint: {hint}", style="yellow")
        
    return Panel(hud, title="🧠  Game Intelligence", border_style="magenta", width=80)

# How the dice display
def dice_face(value: int):
    P = Text("●", style="red")
    E = Text(" ")
 
    # 3x3 pip grid
    layouts = {
        1: [E, E, E,
            E, P, E,
            E, E, E],
        2: [P, E, E,
            E, E, E,
            E, E, P],
        3: [P, E, E, 
            E, P, E,
            E, E, P],
        4: [P, E, P,
            E, E, E,
            P, E, P],
        5: [P, E, P,
            E, P, E,
            P, E, P],
        6: [P, E, P,
            P, E, P,
            P, E, P],
    }
 
    g = layouts[value]
 
    def row(i):
        return Text.assemble(
            "│ ",
            g[i], " ",
            g[i+1], " ",
            g[i+2],
            " │"            
        )
        
    return [
        Text("╭───────╮"),
        row(0),
        row(3),
        row(6),
        Text("╰───────╯"),
    ]

# Dice animation, randomises the pips visually
def roll_animation(duration=2.0, fps=6):
    start = time.time()

    with Live(console=console, refresh_per_second=fps) as live:
        
        roll_message = "Rolling dice..."

        # Animation Loop
        while time.time() - start < duration:
            
            # Generate dice
            dice = [randint(1, 6) for _ in range(5)]
            game_state["last_roll"] = dice
            
            # Update difficulty (based on current state)
            update_difficulty()
            
            # Build dice display
            dice_display = [
                Text("\n").join(dice_face(d))
                for d in dice
            ]
            
            # Build full frame (HUD + dice)
            frame = Group(
                build_hud(roll_message),
                Columns(dice_display, padding=2)
            )
            
            # Render
            live.update(frame)
            time.sleep(1 / fps)

        # Final Result with Red pips
        final_dice = [randint(1, 6) for _ in range(5)]
        game_state["last_roll"] = final_dice
        
        update_difficulty()

        dice_display = [
            Text("\n").join(dice_face(d))
            for d in final_dice
        ]
        
        frame = Group(
            build_hud(),
            Columns(dice_display, padding=2)
        )
        
        live.update(frame)
        time.sleep(1)

        return final_dice

class colours:
    RESET = "\033[0m"
    BOLD = "\033[1m"

    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"

def pause(seconds=1):
    # Pause the game for the specified number of seconds
    time.sleep(seconds)

BOX_WIDTH = 80 # can adjust this anytime to resize ALL boxes
INNER_WIDTH = BOX_WIDTH - 2

def print_box_top():
    print("╔" + "═" * INNER_WIDTH + "╗")

def print_box_bottom():
    print("╚" + "═" * INNER_WIDTH + "╝")

def print_box_line(text="", color=""):
    print("║" + color + text.center(INNER_WIDTH) + colours.RESET + "║")

# display the game title screen.
def display_title():
    
    print()
    print_box_top()
    print_box_line("PETALS AROUND THE ROSE", colours.MAGENTA + colours.BOLD)
    print_box_line("")
    print_box_line("Version 1.0.4", colours.CYAN)
    print_box_line("Created by Wayne Train", colours.YELLOW)
    print_box_bottom()
    print()

    print(f"{colours.BOLD}A game of observation, logic and mystery{colours.RESET}\n")
    input("Press ENTER to begin...")

# display dice using Rich panels.
def render_dice(dice):
    dice_faces = {
        1: "\n  ●  \n",
        2: "●    \n\n    ●",
        3: "●    \n  ●  \n    ●",
        4: "●   ●\n\n●   ●",
        5: "●   ●\n  ●  \n●   ●",
        6: "●   ●\n●   ●\n●   ●",
    }
 
    panels = []
 
    for die in dice:
        text = Text(dice_faces[die], style="bold red")
        panel = Panel(
            text,
            width=9,
            height=5,
            border_style="bright_white",
        )
        panels.append(panel)
 
    console.print(Columns(panels, equal=True, expand=False))      

# create celebration burst for perfect game.
def celebration_burst():
    symbols = ["🎉", "🙌", "🎈", "🎊", "💫", "🎀", "🤩"]

    print(f"{colours.BOLD}\n ** CELEBRATION MODE ACTIVATED **{colours.RESET} \n")
    pause(0.5)

    for _ in range(7):
        line = "".join(random.choice(symbols) for _ in range(30))
        print(line)
        pause(0.1)

def get_rank(score):
    if score == 10:
        return "👑  POTENTATE OF THE ROSE"
    elif score >= 8:
        return "🌹  ADEPT OF THE ROSE"
    elif score >= 5:
        return "🌿  DISCIPLE OF THE ROSE"
    else:
        return "🌱  APPRENTICE OF THE ROSE"

def get_guess():
    # Prompt the user until they enter a valid integer.
    while True:
        user_input = input("\n🤷  How many petals? (or -1 to quit):  ")

        # Allow quit
        if user_input == "-1":
            return -1
        
        # Block obvious command-like input
        suspicious_keywords = ["rm", "del", "shutdown", "sudo", "cmd", "powershell", "import", "os", "system", "root"]

        if any(word in user_input.lower() for word in suspicious_keywords):
            print("\n😏  Nice try... the roses do not respond to that language 🌹")
            pause(1)
            continue

        # Normal numeric validation
        try:
            return int(user_input)
        except ValueError:
            print("\n❌  Please enter a number.")
            pause(1)

# Play a single round and return (guess, answer) or -1 if the player quits.
def play_round():
    game_state["round"] += 1
    
    dice = roll_animation()
    pause(0.5)

    guess = get_guess()

    if guess == -1:
        return -1
    
    answer = calculate_petals(dice)
    
    if guess == answer:
        game_state["score"] += 1
        game_state["streak"] += 1
        game_state["hint_level"] = 0    # reset hint on success
    else:
        game_state["streak"] = 0
        game_state["hint_level"] += 1    # Escalate hint

    return guess, answer

# Game play logic.
def play():
    while True:
        display_title()
        
        print(f"\n{colours.YELLOW}The name of the game is important...{colours.RESET}\n")
        pause(1)

        # RESET GAME STATE (single source of truth)
        game_state["score"] = 0
        game_state["round"] = 0
        game_state["streak"] = 0
        game_state["difficulty"] = 1
        game_state["last_roll"] = []
        
        # MAIN GAME LOOP
        while game_state["round"] < 10:
            result = play_round()
            
            # Allow quit
            if result == -1:
                print("\n👋👋  GOODBYE!!\n")
                return                

            guess, answer = result

            if guess == answer:
                print(f"{colours.GREEN}\n✅ CORRECT!!{colours.RESET}")
                pause(0.5)
            else:
                print(f"{colours.RED}\n❌  No, the answer was{colours.BOLD} {answer}{colours.RESET}")
                pause(0.5)

        # End of game summary
        print(f"{colours.YELLOW}\n🏁🏁  GAME OVER  🏁🏁{colours.RESET}")
        pause(0.5)
        
        print(f"Final Score: {game_state["score"]}/10\n")
        pause(0.5)
        
        rank = get_rank(game_state["score"])
        print(f"🏆  Rank: {colours.BOLD}{colours.MAGENTA}{rank}{colours.RESET}\n")

        # Perfect game celebration
        if game_state["score"] == 10:
            print("🏆  PERFECT GAME!! 🏆")
            pause(1.5)

            celebration_burst() 

            pause(1)
            print(" \nYou have mastered the mystery of the roses...\n") 
            pause(1)

            print(f"👑  You are now the {colours.MAGENTA}{colours.BOLD}POTENTATE OF THE ROSE!! 👑{colours.RESET}\n\n")  
            pause(1)   

        # Replay system
        while True:
            again = input("Play again? (y/n): ").strip().lower()

            if again == "y":
                break
            elif again == "n":
                print("\nThanks for playing 🌹🌹\n")
                return
            else:
                print("Please enter y or n.")

if __name__ == "__main__":
    play()

