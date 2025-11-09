import random
import time
import os
import msvcrt  # for Windows getch functionality
import sys

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_separator():
    print("=" * 50)

def print_header(title):
    print_separator()
    print(f"|{title:^48}|")
    print_separator()

def print_centered(text):
    print(f"{text:^50}")

def animate_text(text, delay=0.03):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

class Roulette:
    def __init__(self):
        self.range = list(range(50))
        self.result = random.choice(self.range)
        
    def spin(self):
        bullets = []
        for i in range(6):
            self.result = random.choice(self.range)
            if self.result % 2 == 0:
                bullets.append(0)  # Even - safe
            else:
                bullets.append(1)  # Odd - bang
        return bullets

class Start:
    def roll(self):
        r = Roulette()
        outcome = r.spin()
        return outcome

class Animations:
    @staticmethod
    def spinning_animation(text, duration=2):
        frames = ["\\", "|", "/", "-", "\\", "|", "/", "-"]
        end_time = time.time() + duration
        while time.time() < end_time:
            for frame in frames:
                print(f"{text} {frame}", end="\r", flush=True)
                time.sleep(0.1)
        print(" " * 60, end="\r")
    
    @staticmethod
    def progress_bar(text, duration=4):
        width = 30
        steps = 20
        for i in range(steps + 1):
            progress = i / steps
            bar = "|" * int(width * progress) + "\\" * (width - int(width * progress))
            print(f"{text} [{bar}] {int(progress*100)}%", end="\r", flush=True)
            time.sleep(duration / steps)
        print(" " * 60, end="\r")
    
    @staticmethod
    def typewriter(text, delay=0.03):
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()

class OpponentName:
    def __init__(self):
        self.name = ""
    
    def name_generator(self):
        name1 = ["Bobbert", "Lulabelle", "Chuckles", "Fanny", "Doodle", "Waldo", "Binky", "Squeaky", "Muffet", "Gus"]
        name2 = ["Nedward", "Pippy", "Snuffy", "Trixie", "Jasperino", "Frodo", "Ziggy", "Bubbles", "Clumsy", "Wiggles"]
        self.name = random.choice(name1) + " " + random.choice(name2)
        return self.name

class Player:
    def __init__(self, name, lives=3):
        self.name = name
        self.lives = lives
        self.shield = False
        self.shield_turns = 0
        self.drunk_turns = 0
        self.confused = False
    
    def add_shield(self, turns=1):
        self.shield = True
        self.shield_turns = turns
    
    def make_drunk(self, turns=2):
        self.drunk_turns = turns
        self.confused = True
    
    def update_status(self):
        if self.drunk_turns > 0:
            self.drunk_turns -= 1
            if self.drunk_turns == 0:
                self.confused = False
    
    def use_shield(self):
        if self.shield and self.shield_turns > 0:
            self.shield_turns -= 1
            if self.shield_turns == 0:
                self.shield = False
            return True
        return False
    
    def take_damage(self, amount=1):
        if self.use_shield():
            print(f"{self.name}'s shield blocked the damage!")
            return 0
        self.lives -= amount
        return amount
    
    def is_alive(self):
        return self.lives > 0
    
    def get_status(self):
        shield_status = " (Shield)" if self.shield else ""
        drunk_status = " (Drunk)" if self.confused else ""
        return f"{self.name}: {self.lives}{shield_status}{drunk_status}"

def display_stats(player1, player2, snoop=None):
    print_header("CURRENT STATUS")
    
    status_lines = [
        f"{player1.get_status()}",
        f"{player2.get_status()}"
    ]
    
    if snoop and snoop.is_alive():
        status_lines.append(f"{snoop.get_status()}")
    
    for line in status_lines:
        print(f"| {line:<46} |")
    
    print_separator()
    print()

def display_bullets_chamber(bullets, current_index):
    print("   Chamber: ", end="")
    for i in range(len(bullets)):
        if i == current_index:
            print("|C|", end=" ")  # Current bullet
        elif i < current_index:
            print("|U|", end=" ")  # Used bullet
        else:
            print("|?|", end=" ")  # Remaining bullet
    print(f"({len(bullets) - current_index} left)\n")

def drunk_text_effect(text):
    """Display text with drunk effect"""
    drunk_text = ""
    for char in text:
        if random.random() < 0.3:  # 30% chance to mess up each character
            if char.isalpha():
                drunk_text += random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
            else:
                drunk_text += char
        else:
            drunk_text += char
    return drunk_text

def drunk_display(text, delay=0.05):
    """Display text with drunk typing effect"""
    for char in text:
        if random.random() < 0.1:  # 10% chance of typo
            wrong_char = random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()')
            print(wrong_char, end='', flush=True)
            time.sleep(0.1)
            print('\b', end='', flush=True)  # Backspace
            print(char, end='', flush=True)
        else:
            print(char, end='', flush=True)
        time.sleep(delay)
    print()

def environmental_hazard():
    """Random environmental hazard affecting all players"""
    hazards = [
        {
            "name": "Lightning Storm",
            "message": "A sudden lightning storm strikes the area!",
            "effect": lambda: lightning_storm_effect()
        },
        {
            "name": "Gas Leak",
            "message": "A mysterious gas leak causes everyone to feel dizzy!",
            "effect": lambda: gas_leak_effect()
        },
        {
            "name": "Power Outage",
            "message": "The power goes out! Everything is dark and confusing!",
            "effect": lambda: power_outage_effect()
        },
        {
            "name": "Earthquake",
            "message": "The ground shakes violently!",
            "effect": lambda: earthquake_effect()
        },
        {
            "name": "Toxic Rain",
            "message": "Acidic rain starts falling from the sky!",
            "effect": lambda: toxic_rain_effect()
        }
    ]
    
    hazard = random.choice(hazards)
    print_header("ENVIRONMENTAL HAZARD")
    Animations.typewriter(hazard["message"])
    time.sleep(delay)
    hazard["effect"]()
    return hazard["name"]

def lightning_storm_effect():
    """Lightning randomly strikes players"""
    targets = [player for player in [player1, player2, snoop] if player and player.is_alive()]
    if targets:
        target = random.choice(targets)
        Animations.typewriter(f"Lightning strikes {target.name}!")
        target.take_damage(1)
        time.sleep(delay)

def gas_leak_effect():
    """Gas leak makes players drunk"""
    targets = [player for player in [player1, player2, snoop] if player and player.is_alive()]
    for target in targets:
        if random.random() < 0.7:  # 70% chance to affect each player
            target.make_drunk(random.randint(1, 3))
            Animations.typewriter(f"{target.name} starts seeing double!")
            time.sleep(0.5)

def power_outage_effect():
    """Power outage causes confusion and missed turns"""
    print("The screen flickers...")
    time.sleep(1)
    clear_console()
    print("SYSTEM REBOOTING...")
    time.sleep(2)
    clear_console()
    # Random player might miss a turn
    if random.random() < 0.4:
        targets = [player for player in [player1, player2, snoop] if player and player.is_alive()]
        if targets:
            target = random.choice(targets)
            Animations.typewriter(f"{target.name} is disoriented and misses a turn!")
            # This will be handled in the main loop by skipping their turn

def earthquake_effect():
    """Earthquake causes random damage to all"""
    Animations.typewriter("The ground splits beneath your feet!")
    for player in [player1, player2, snoop]:
        if player and player.is_alive():
            if random.random() < 0.6:  # 60% chance to take damage
                player.take_damage(1)
                Animations.typewriter(f"{player.name} falls and takes damage!")
                time.sleep(0.5)

def toxic_rain_effect():
    """Toxic rain damages everyone over time"""
    Animations.typewriter("The acidic rain burns everything it touches!")
    for player in [player1, player2, snoop]:
        if player and player.is_alive():
            player.take_damage(1)
            Animations.typewriter(f"{player.name} takes damage from the toxic rain!")
            time.sleep(0.5)

def spin_event():
    global player1, player2, snoop, Snoopjoin
    
    Animations.spinning_animation("Spinning the event wheel")
    
    event_result = random.randint(0, 6)
    events = {
        0: mysterious_man_event,
        1: nothing_event,
        2: potion_event,
        3: earthquake_event,
        4: animal_event,
        5: shield_event,
        6: snoop_dogg_event
    }
    
    events[event_result]()

def mysterious_man_event():
    Animations.typewriter("A mysterious man appeared...")
    time.sleep(delay)
    Animations.typewriter("He reaches into his pockets...")
    time.sleep(delay)
    Animations.typewriter("He has two pistols!")
    time.sleep(delay)
    
    if Snoopjoin and snoop.is_alive():
        target = random.choice([player1, player2, snoop])
    else:
        target = random.choice([player1, player2])
    
    Animations.typewriter(f"He aims at {target.name}!")
    time.sleep(delay)
    print("BANG! BANG!")
    time.sleep(delay)
    damage = target.take_damage(2)
    if damage > 0:
        Animations.typewriter(f"{target.name} loses 2 lives!")
    time.sleep(delay)

def nothing_event():
    Animations.typewriter("The roulette spins wildly...")
    time.sleep(delay)
    print("But nothing happens! Phew...")
    time.sleep(delay)

def potion_event():
    Animations.typewriter("A wild potion appeared!")
    time.sleep(delay)
    
    potion_type = random.randint(1, 3)
    if potion_type == 1:
        player1.lives += 1
        print("You gained an extra life!")
        time.sleep(delay)
    elif potion_type == 2:
        player2.lives += 1
        print("The potion flew across the room due to butter fingers!")
        print(f"{player2.name} gained an extra life!")
        time.sleep(delay)
    else:
        print("The potion exploded harmlessly!")
        time.sleep(delay)

def earthquake_event():
    Animations.typewriter("A sudden earthquake shakes the ground!")
    time.sleep(delay)
    print("Both players lose a life trying to stay balanced!")
    time.sleep(delay)
    player1.take_damage(1)
    player2.take_damage(1)

def animal_event():
    animals = ["snake", "wolf", "bear", "lion", "alligator"]
    animal = random.choice(animals)
    Animations.typewriter(f"{animal} dashes through the area!")
    time.sleep(delay)
    
    target = random.choice([player1, player2])
    print(f"It bit {target.name}!")
    time.sleep(delay)
    target.take_damage(1)

def shield_event():
    Animations.typewriter("You found a magical shield!")
    Animations.progress_bar("Charging shield")
    
    shield_target = random.choice([player1, player2])
    turns = random.randint(1, 2)
    shield_target.add_shield(turns)
    print(f"{shield_target.name} gained a shield for {turns} turn(s)!")
    time.sleep(delay)

def snoop_dogg_event():
    global Snoopjoin, snoop
    
    Animations.typewriter("A wild Snoop Dogg appeared!")
    time.sleep(delay)
    print("He loves playing Russian Roulette!")
    time.sleep(delay)
    
    event_type = random.randint(1, 4)
    if event_type == 1:
        print("He takes a shot into the air and leaves!")
        time.sleep(delay)
        target = random.choice([player1, player2])
        print(f"The bullet fell back and hit {target.name}!")
        time.sleep(delay)
        target.take_damage(1)
    elif event_type == 2:
        print("He shoots both of you and leaves!")
        time.sleep(delay)
        player1.take_damage(1)
        player2.take_damage(1)
    elif event_type == 3:
        print("He challenges both of you to a quick duel!")
        time.sleep(1)
        winner = random.choice([player1, player2])
        print(f"{winner.name} was faster and shot Snoop Dogg!")
        time.sleep(delay)
        if snoop:
            snoop.take_damage(1)
    else:
        print("He decided to join the game and play along!")
        time.sleep(delay)
        Snoopjoin = True
        if not snoop:
            snoop = Player("Snoop Dogg", 3)

def player_turn(player, target, bullets, current_index):
    display_stats(player1, player2, snoop if Snoopjoin else None)
    display_bullets_chamber(bullets, current_index)
    
    print_header(f"{player.name.upper()}'S TURN")
    
    if player.shield:
        print(f"{player.name} has a shield for {player.shield_turns} more turn(s)!")
    
    if player.confused:
        print(f"{player.name} is drunk and confused!")
    
    print("Choose your action:")
    print("1. Pull the trigger on yourself")
    print("2. Shoot your opponent")
    print("3. Feeling lucky")
    print()
    
    while True:
        if player.confused:
            drunk_display("Enter your choice (1-3): ", 0.1)
        else:
            print("Enter your choice (1-3): ", end="", flush=True)
            
        if player.name == "You":
            choice = msvcrt.getch().decode("utf-8").lower()
        else:
            # AI decision making
            time.sleep(1)
            if player.confused:
                # Drunk AI makes random choices
                choice = random.choice(['1', '2', '3'])
            elif player.lives <= 1:
                choice = '3'  # Desperate - try special event
            elif target.lives <= 1 and random.random() < 0.6:
                choice = '2'  # Finish opponent
            else:
                choice = random.choice(['1', '2', '3'])
            print(choice)
        
        if choice in ['1', '2', '3']:
            break
        else:
            print("Invalid input. Please enter 1, 2, or 3.")
    
    print()
    
    # Apply drunk effect to choice
    if player.confused and random.random() < 0.4:  # 40% chance to mess up choice
        original_choice = choice
        choices = ['1', '2', '3']
        choices.remove(choice)
        choice = random.choice(choices)
        drunk_display(f"{player.name} meant to choose {original_choice} but chose {choice} instead!", 0.05)
    
    if choice == '1':
        Animations.spinning_animation("Pulling the trigger")
        time.sleep(delay)
        return handle_trigger_pull(player, None, bullets, current_index)
    
    elif choice == '2':
        print(f"{player.name} aims at {target.name}!")
        Animations.spinning_animation("Taking aim")
        time.sleep(delay)
        return handle_trigger_pull(player, target, bullets, current_index)
    
    else:  # choice == '3'
        spin_event()
        return current_index  # No bullet used in special event

def handle_trigger_pull(shooter, target, bullets, current_index):
    if current_index >= len(bullets):
        print("No more bullets in the chamber! Game over.")
        time.sleep(1)
        return current_index
    
    # Check for misfire
    misfire = random.randint(1, 10) == 1  # 10% chance
    
    if misfire:
        print("MISFIRE! The gun jams!")
        time.sleep(delay)
        return current_index
    
    if bullets[current_index] == 1:  # Bang!
        if target:
            # Shooting at opponent
            damage = target.take_damage(1)
            if damage > 0:
                print(f"BANG! {target.name} loses a life!")
                print(f"{target.name} now has {target.lives} lives")
                time.sleep(delay)
            else:
                print(f"{target.name}'s shield protected them!")
                time.sleep(delay)
        else:
            # Shooting self
            damage = shooter.take_damage(1)
            if damage > 0:
                print(f"BANG! {shooter.name} loses a life!")
                print(f"{shooter.name} now has {shooter.lives} lives")
                time.sleep(delay)
            else:
                print(f"{shooter.name}'s shield protected you!")
                time.sleep(delay)
    else:  # Click!
        print("CLICK! Safe this turn.")
        if target:
            print(f"{target.name} breathes a sigh of relief!")
            time.sleep(delay)
        else:
            print(f"{shooter.name} breathes a sigh of relief!")
            time.sleep(delay)
    
    return current_index + 1

def check_game_over():
    alive_players = []
    if player1.is_alive():
        alive_players.append(player1)
    if player2.is_alive():
        alive_players.append(player2)
    if snoop and snoop.is_alive():
        alive_players.append(snoop)
    
    return len(alive_players) <= 1, alive_players

# Initialize game
Animations.progress_bar("Loading game", 1)
time.sleep(1)

# Initialize players
player1 = Player("You", 3)
opponent = OpponentName()
player2 = Player(opponent.name_generator(), 3)
snoop = None
Snoopjoin = False

# Generate bullets
game = Start()
bullets = game.roll()
current_bullet = 0

delay = 2
hazard_cooldown = 0

clear_console()

# Main game loop
turn_count = 0
while True:
    turn_count += 1
    
    # Environmental hazard check (every 3-5 turns)
    if hazard_cooldown <= 0 and random.random() < 0.3:  # 30% chance every turn after cooldown
        hazard_name = environmental_hazard()
        hazard_cooldown = random.randint(3, 5)
        time.sleep(2)
        clear_console()
    else:
        hazard_cooldown -= 1
    
    # Player 1 turn
    if player1.is_alive():
        current_bullet = player_turn(player1, player2, bullets, current_bullet)
        player1.update_status()
        
        game_over, winners = check_game_over()
        if game_over or current_bullet >= len(bullets):
            break
        
        if player1.is_alive():
            Animations.progress_bar("Passing turn", 1)
            clear_console()
    
    # Player 2 turn
    if player2.is_alive():
        current_bullet = player_turn(player2, player1, bullets, current_bullet)
        player2.update_status()
        
        game_over, winners = check_game_over()
        if game_over or current_bullet >= len(bullets):
            break
        
        if player2.is_alive():
            Animations.progress_bar("Passing turn", 1)
            clear_console()
    
    # Snoop Dogg turn
    if Snoopjoin and snoop and snoop.is_alive():
        current_bullet = player_turn(snoop, random.choice([p for p in [player1, player2] if p.is_alive()]), bullets, current_bullet)
        snoop.update_status()
        
        game_over, winners = check_game_over()
        if game_over or current_bullet >= len(bullets):
            break
        
        if snoop.is_alive():
            Animations.progress_bar("Passing turn", 1)
            clear_console()

# Game over sequence
clear_console()
print_header("GAME OVER")

if current_bullet >= len(bullets):
    print("All bullets have been fired!")
    print("Last player standing wins!")

alive_players = [p for p in [player1, player2, snoop] if p and p.is_alive()]

if len(alive_players) == 1:
    winner = alive_players[0]
    print(f"WINNER: {winner.name}!")
    print(f"Final lives: {winner.lives}")
    
    if winner.name == "You":
        victory_messages = [
            "You survived against all odds!",
            "Lady Luck was on your side!",
            "You're the last one standing!",
            "Victory tastes sweet!",
        ]
    else:
        victory_messages = [
            "Better luck next time!",
            "The odds were not in your favor!",
            "That was a close one!",
        ]
    
    print(f"{random.choice(victory_messages)}")
    
else:
    print("It's a tie!")
    print("Alive players:")
    for player in alive_players:
        print(f"  {player.name} with {player.lives} lives")