import random
import time
import os
import sys

# Platform-independent getch implementation
try:
    import msvcrt  # Windows
    def getch():
        return msvcrt.getch().decode('utf-8')
except ImportError:
    import termios  # Unix
    import tty
    def getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

# Global game state
player1 = None
player2 = None
snoop = None
Snoopjoin = False
GAME_DELAY = 1.5

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

class Roulette:
    def __init__(self):
        self.range = list(range(50))
        self.result = random.choice(self.range)
        
    def spin(self, bullet_count=6):
        bullets = []
        for i in range(bullet_count):
            self.result = random.choice(self.range)
            if self.result % 2 == 0:
                bullets.append(0)  # Even - safe
            else:
                bullets.append(1)  # Odd - bang
        return bullets

class Start:
    def roll(self, bullet_count=6):
        r = Roulette()
        outcome = r.spin(bullet_count)
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
    def progress_bar(text, duration=2):
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

class NameGenerator:
    def __init__(self):
        self.first_names = [
            "Wobble", "Fluffy", "Noodle", "Pickle", "Bumble", "Fizzy", "Gizmo", "Wiggles",
            "Squishy", "Boop", "Zany", "Doodle", "Fuzzy", "Bloop", "Glitch", "Snickerdoodle",
            "Wonky", "Zigzag", "Bouncy", "Gloop", "Sprocket", "Twinkle", "Bonk", "Flump",
            "Squiggle", "Blorp", "Fidget", "Gobble", "Wacky", "Zoink", "Bingbong", "Flapjack",
            "Snorkel", "Booger", "Dingus", "Floop", "Gubbins", "Kerfuffle", "Mumbo", "Nerts",
            "Piddles", "Quibble", "Razzle", "Sassafras", "Thingamajig", "Whatchamacallit", "Yikes", "Zucchini"
        ]
        self.last_names = [
            "McSnort", "Butterpants", "Von Gigglesnort", "Fancybottom", "McGoo", "Pickleberry",
            "Wobblebottom", "Snickerdoodle", "Fluffernutter", "Bumblepants", "Gigglesworth",
            "Doodlebug", "Fizzlebottom", "Boopadoop", "Zanypants", "Wigglesworth", "Squishmallow",
            "Blooperton", "Glitchypants", "Bonkerson", "Flumpadoodle", "Squigglebottom",
            "Blorpington", "Fidgetspinner", "Gobbledygook", "Wackadoo", "Zoinksalot", "Bingbongle",
            "Flapdoodle", "Snorkelberry", "Boogermeyer", "Dingusburg", "Flooperdooper", "Gubbinsmith",
            "Kerfuffleton", "Mumbotron", "Nertsworthy", "Piddleston", "Quibblequist", "Razzledazzle",
            "Sassypants", "Thingamabob", "Whatchamaccallit", "Yikeroni", "Zucchinibottom", "McGoofball"
        ]
    
    def generate_player_name(self):
        return random.choice(self.first_names) + " " + random.choice(self.last_names) + " (You)"
    
    def generate_opponent_name(self):
        name1 = ["Bobbert", "Lulabelle", "Chuckles", "Fanny", "Doodle", "Waldo", 
                "Binky", "Squeaky", "Muffet", "Gus", "Snuggles", "Wobble", "Fizz"]
        name2 = ["Nedward", "Pippy", "Snuffy", "Trixie", "Jasperino", "Frodo", 
                "Ziggy", "Bubbles", "Clumsy", "Wiggles", "Doodle", "Fumble", "Giggle"]
        return random.choice(name1) + " " + random.choice(name2)

class Player:
    def __init__(self, name, lives=3):
        self.name = name
        self.lives = lives
        self.shield = False
        self.shield_turns = 0
        self.drunk_turns = 0
        self.confused = False
        self.misses_next_turn = False
    
    def add_shield(self, turns=1):
        self.shield = True
        self.shield_turns = turns
    
    def make_drunk(self, turns=2):
        self.drunk_turns = turns
        self.confused = True
    
    def miss_next_turn(self):
        self.misses_next_turn = True
    
    def update_status(self):
        if self.drunk_turns > 0:
            self.drunk_turns -= 1
            if self.drunk_turns == 0:
                self.confused = False
        
        # Reset missed turn flag after processing
        self.misses_next_turn = False
    
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
        status_parts = [f"{self.name}: {self.lives}"]
        if self.shield:
            status_parts.append(f"Shield({self.shield_turns})")
        if self.confused:
            status_parts.append("Drunk")
        if self.misses_next_turn:
            status_parts.append("Misses")
        return " ".join(status_parts)

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
    global player1, player2, snoop
    
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
    time.sleep(GAME_DELAY)
    hazard["effect"]()
    return hazard["name"]

def lightning_storm_effect():
    """Lightning randomly strikes players"""
    global player1, player2, snoop
    
    targets = [player for player in [player1, player2, snoop] if player and player.is_alive()]
    if targets:
        target = random.choice(targets)
        Animations.typewriter(f"Lightning strikes {target.name}!")
        target.take_damage(1)
        time.sleep(GAME_DELAY)

def gas_leak_effect():
    """Gas leak makes players drunk"""
    global player1, player2, snoop
    
    targets = [player for player in [player1, player2, snoop] if player and player.is_alive()]
    for target in targets:
        if random.random() < 0.7:  # 70% chance to affect each player
            target.make_drunk(random.randint(1, 3))
            Animations.typewriter(f"{target.name} starts seeing double!")
            time.sleep(0.5)

def power_outage_effect():
    """Power outage causes confusion and missed turns"""
    global player1, player2, snoop
    
    print("The screen flickers...")
    time.sleep(1)
    clear_console()
    print("SYSTEM REBOOTING...")
    time.sleep(2)
    clear_console()
    
    # Random player might miss a turn
    targets = [player for player in [player1, player2, snoop] if player and player.is_alive()]
    if targets and random.random() < 0.4:
        target = random.choice(targets)
        target.miss_next_turn()
        Animations.typewriter(f"{target.name} is disoriented and will miss next turn!")

def earthquake_effect():
    """Earthquake causes random damage to all"""
    global player1, player2, snoop
    
    Animations.typewriter("The ground splits beneath your feet!")
    for player in [player1, player2, snoop]:
        if player and player.is_alive():
            if random.random() < 0.6:  # 60% chance to take damage
                player.take_damage(1)
                Animations.typewriter(f"{player.name} falls and takes damage!")
                time.sleep(0.5)

def toxic_rain_effect():
    """Toxic rain damages everyone over time"""
    global player1, player2, snoop
    
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
    global player1, player2, snoop, Snoopjoin
    
    Animations.typewriter("A mysterious man appeared...")
    time.sleep(GAME_DELAY)
    Animations.typewriter("He reaches into his pockets...")
    time.sleep(GAME_DELAY)
    Animations.typewriter("He has two pistols!")
    time.sleep(GAME_DELAY)
    
    if Snoopjoin and snoop and snoop.is_alive():
        target = random.choice([player1, player2, snoop])
    else:
        target = random.choice([player1, player2])
    
    Animations.typewriter(f"He aims at {target.name}!")
    time.sleep(GAME_DELAY)
    print("BANG! BANG!")
    time.sleep(GAME_DELAY)
    damage = target.take_damage(2)
    if damage > 0:
        Animations.typewriter(f"{target.name} loses 2 lives!")
    time.sleep(GAME_DELAY)

def nothing_event():
    Animations.typewriter("The roulette spins wildly...")
    time.sleep(GAME_DELAY)
    print("But nothing happens! Phew...")
    time.sleep(GAME_DELAY)

def potion_event():
    global player1, player2
    
    Animations.typewriter("A wild potion appeared!")
    time.sleep(GAME_DELAY)
    
    potion_type = random.randint(1, 3)
    if potion_type == 1:
        player1.lives += 1
        print(f"{player1.name} gained an extra life!")
        time.sleep(GAME_DELAY)
    elif potion_type == 2:
        player2.lives += 1
        print("The potion flew across the room due to butter fingers!")
        print(f"{player2.name} gained an extra life!")
        time.sleep(GAME_DELAY)
    else:
        print("The potion exploded harmlessly!")
        time.sleep(GAME_DELAY)

def earthquake_event():
    global player1, player2
    
    Animations.typewriter("A sudden earthquake shakes the ground!")
    time.sleep(GAME_DELAY)
    print("Both players lose a life trying to stay balanced!")
    time.sleep(GAME_DELAY)
    player1.take_damage(1)
    player2.take_damage(1)

def animal_event():
    global player1, player2
    
    animals = ["snake", "wolf", "bear", "lion", "alligator"]
    animal = random.choice(animals)
    Animations.typewriter(f"{animal} dashes through the area!")
    time.sleep(GAME_DELAY)
    
    target = random.choice([player1, player2])
    print(f"It bit {target.name}!")
    time.sleep(GAME_DELAY)
    target.take_damage(1)

def shield_event():
    global player1, player2
    
    Animations.typewriter("You found a magical shield!")
    Animations.progress_bar("Charging shield")
    
    shield_target = random.choice([player1, player2])
    turns = random.randint(1, 2)
    shield_target.add_shield(turns)
    print(f"{shield_target.name} gained a shield for {turns} turn(s)!")
    time.sleep(GAME_DELAY)

def snoop_dogg_event():
    global Snoopjoin, snoop, player1, player2
    
    if not Snoopjoin:
    
        Animations.typewriter("A wild Snoop Dogg appeared!")
        time.sleep(GAME_DELAY)
        print("He loves playing Russian Roulette!")
        time.sleep(GAME_DELAY)
        
        event_type = random.randint(1, 4)
        if event_type == 1:
            print("He takes a shot into the air and leaves!")
            time.sleep(GAME_DELAY)
            target = random.choice([player1, player2])
            print(f"The bullet fell back and hit {target.name}!")
            time.sleep(GAME_DELAY)
            target.take_damage(1)
        elif event_type == 2:
            print("He shoots both of you and leaves!")
            time.sleep(GAME_DELAY)
            player1.take_damage(1)
            player2.take_damage(1)
        elif event_type == 3:
            print("He challenges both of you to a quick duel!")
            time.sleep(1)
            winner = random.choice([player1, player2])
            print(f"{winner.name} was faster and shot Snoop Dogg!")
            time.sleep(GAME_DELAY)
            if snoop:
                snoop.take_damage(1)
        else:
            if not Snoopjoin:  # Only join if not already in game
                print("He decided to join the game and play along!")
                time.sleep(GAME_DELAY)
                Snoopjoin = True
                if not snoop:
                    snoop = Player("Snoop Dogg", 3)
            # else:
            #     print("Snoop Dogg is already here! He just watches this time.")
            #     time.sleep(GAME_DELAY)   
    else:
        Animations.typewriter("A wild Hatsune Miku appeared!")
        time.sleep(GAME_DELAY)
        print("Po-pi-po-pi-po-po-pi-po")
        time.sleep(GAME_DELAY)
        print("Po-pi-po-pi-po-po-pi-po")
        time.sleep(GAME_DELAY)
        
        event_type = random.randint(1, 3)
        if event_type == 1:
            print("She throws her onion leek into the air!")
            time.sleep(GAME_DELAY)
            target = random.choice([player1, player2, snoop])
            print(f"The onion leek fell back and hit {target.name}!")
            time.sleep(GAME_DELAY)
            target.take_damage(1)
        elif event_type == 2:
            print("She hit both of you with her onion leek and leaves!")
            time.sleep(GAME_DELAY)
            player1.take_damage(1)
            player2.take_damage(1)
            snoop.take_damage(1)
        else:
            print("She challenges both of you to a quick duel!")
            time.sleep(1)
            winner = random.choice([player1, player2, snoop])
            print(f"{winner.name} was faster and shot Hatsune Miku!")
            time.sleep(GAME_DELAY)
        

def get_valid_input(prompt, valid_choices):
    """Get validated input from user"""
    while True:
        print(prompt, end="", flush=True)
        try:
            choice = getch().lower()
            print(choice)  # Echo the choice
            if choice in valid_choices:
                return choice
            else:
                print(f"Invalid input. Please enter one of: {', '.join(valid_choices)}")
        except (EOFError, KeyboardInterrupt):
            print("\nGame interrupted. Exiting...")
            sys.exit(1)

def ai_decision_maker(ai_player, target_player):
    """Make strategic decision for AI player"""
    if ai_player.confused:
        # Drunk AI makes random choices
        return random.choice(['1', '2', '3'])
    
    # Strategic decision making
    if ai_player.lives <= 1:
        # Desperate - try special event for potential help
        return '3'
    elif target_player.lives <= 1 and random.random() < 0.7:
        # Finish off weak opponent
        return '2'
    elif ai_player.lives >= 3 and random.random() < 0.4:
        # Healthy and confident - shoot opponent
        return '2'
    elif random.random() < 0.3:
        # Occasionally try special event
        return '3'
    else:
        # Default to self-shot (safer)
        return '1'

def player_turn(player, target, bullets, current_index):
    global player1, player2, snoop, Snoopjoin
    
    display_stats(player1, player2, snoop if Snoopjoin else None)
    display_bullets_chamber(bullets, current_index)
    
    print_header(f"{player.name.upper()}'S TURN")
    
    if player.misses_next_turn:
        print(f"{player.name} is disoriented and misses this turn!")
        time.sleep(GAME_DELAY)
        return current_index
    
    if player.shield:
        print(f"{player.name} has a shield for {player.shield_turns} more turn(s)!")
    
    if player.confused:
        print(f"{player.name} is drunk and confused!")
    
    print("Choose your action:")
    print("1. Pull the trigger on yourself")
    print("2. Shoot your opponent")
    print("3. Feeling lucky")
    print()
    
    if player == player1:  # Human player (now with random name)
        choice = get_valid_input("Enter your choice (1-3): ", ['1', '2', '3'])
    else:
        # AI player
        time.sleep(1)
        choice = ai_decision_maker(player, target)
        print(f"{player.name} chooses option {choice}")
    
    print()
    
    # Apply drunk effect to choice
    if player.confused and random.random() < 0.4:  # 40% chance to mess up choice
        original_choice = choice
        choices = ['1', '2', '3']
        if original_choice in choices:
            choices.remove(original_choice)
        choice = random.choice(choices)
        drunk_display(f"{player.name} meant to choose {original_choice} but chose {choice} instead!", 0.05)
    
    if choice == '1':
        Animations.spinning_animation("Pulling the trigger")
        time.sleep(GAME_DELAY)
        return handle_trigger_pull(player, None, bullets, current_index)
    
    elif choice == '2':
        print(f"{player.name} aims at {target.name}!")
        Animations.spinning_animation("Taking aim")
        time.sleep(GAME_DELAY)
        return handle_trigger_pull(player, target, bullets, current_index)
    
    else:  # choice == '3'
        print(f"{player.name} tries their luck!")
        spin_event()
        # Special event costs the player's turn but doesn't use a bullet
        return current_index

def handle_trigger_pull(shooter, target, bullets, current_index):
    if current_index >= len(bullets):
        print("No more bullets in the chamber! Reloading...")
        return 0  # Reset to start new chamber
    
    # Check for misfire
    misfire = random.randint(1, 10) == 1  # 10% chance
    
    if misfire:
        print("MISFIRE! The gun jams!")
        time.sleep(GAME_DELAY)
        return current_index  # Bullet not consumed
    
    if bullets[current_index] == 1:  # Bang!
        if target:
            # Shooting at opponent
            damage = target.take_damage(1)
            if damage > 0:
                print(f"BANG! {target.name} loses a life!")
                print(f"{target.name} now has {target.lives} lives")
                time.sleep(GAME_DELAY)
            else:
                print(f"{target.name}'s shield protected them!")
                time.sleep(GAME_DELAY)
        else:
            # Shooting self
            damage = shooter.take_damage(1)
            if damage > 0:
                print(f"BANG! {shooter.name} loses a life!")
                print(f"{shooter.name} now has {shooter.lives} lives")
                time.sleep(GAME_DELAY)
            else:
                print(f"{shooter.name}'s shield protected you!")
                time.sleep(GAME_DELAY)
    else:  # Click!
        print("CLICK! Safe this turn.")
        if target:
            print(f"{target.name} breathes a sigh of relief!")
            time.sleep(GAME_DELAY)
        else:
            print(f"{shooter.name} breathes a sigh of relief!")
            time.sleep(GAME_DELAY)
    
    return current_index + 1

def check_game_over():
    global player1, player2, snoop
    
    alive_players = []
    if player1.is_alive():
        alive_players.append(player1)
    if player2.is_alive():
        alive_players.append(player2)
    if snoop and snoop.is_alive():
        alive_players.append(snoop)
    
    return len(alive_players) <= 1, alive_players

def initialize_game():
    """Initialize the game state"""
    global player1, player2, snoop, Snoopjoin
    
    Animations.progress_bar("Loading game", 1)
    time.sleep(1)
    
    # Generate random names for both players
    name_gen = NameGenerator()
    player_name = name_gen.generate_player_name()
    opponent_name = name_gen.generate_opponent_name()
    
    print(f"\nYour name: {player_name}")
    print(f"Opponent: {opponent_name}")
    time.sleep(2)
    
    # Initialize players with random names
    player1 = Player(player_name, 3)
    player2 = Player(opponent_name, 3)
    snoop = None
    Snoopjoin = False

def main():
    global player1, player2, snoop, Snoopjoin
    
    initialize_game()
    
    # Generate initial bullets
    game = Start()
    bullets = game.roll(6)  # 6 bullets per chamber
    current_bullet = 0
    
    hazard_cooldown = 0
    turn_count = 0
    
    clear_console()
    
    # Main game loop
    while True:
        turn_count += 1
        
        # Environmental hazard check (every 3-5 turns)
        if hazard_cooldown <= 0 and random.random() < 0.25:  # 25% chance every turn after cooldown
            hazard_name = environmental_hazard()
            hazard_cooldown = random.randint(3, 5)
            time.sleep(2)
            clear_console()
        else:
            hazard_cooldown = max(0, hazard_cooldown - 1)
        
        # Player 1 turn (human player with random name)
        if player1.is_alive():
            current_bullet = player_turn(player1, player2, bullets, current_bullet)
            player1.update_status()
            
            # Check if we need to reload
            if current_bullet >= len(bullets):
                print("\n*** Chamber empty! Reloading... ***")
                bullets = game.roll(6)
                current_bullet = 0
                time.sleep(GAME_DELAY)
            
            game_over, winners = check_game_over()
            if game_over:
                break
            
            if player1.is_alive():
                Animations.progress_bar("Passing turn", 1)
                clear_console()
        
        # Player 2 turn
        if player2.is_alive():
            current_bullet = player_turn(player2, player1, bullets, current_bullet)
            player2.update_status()
            
            # Check if we need to reload
            if current_bullet >= len(bullets):
                print("\n*** Chamber empty! Reloading... ***")
                bullets = game.roll(6)
                current_bullet = 0
                time.sleep(GAME_DELAY)
            
            game_over, winners = check_game_over()
            if game_over:
                break
            
            if player2.is_alive():
                Animations.progress_bar("Passing turn", 1)
                clear_console()
        
        # Snoop Dogg turn
        if Snoopjoin and snoop and snoop.is_alive():
            # Choose a target from alive players
            alive_players = [p for p in [player1, player2] if p.is_alive()]
            if alive_players:
                target = random.choice(alive_players)
                current_bullet = player_turn(snoop, target, bullets, current_bullet)
                snoop.update_status()
                
                # Check if we need to reload
                if current_bullet >= len(bullets):
                    print("\n*** Chamber empty! Reloading... ***")
                    bullets = game.roll(6)
                    current_bullet = 0
                    time.sleep(GAME_DELAY)
                
                game_over, winners = check_game_over()
                if game_over:
                    break
                
                if snoop.is_alive():
                    Animations.progress_bar("Passing turn", 1)
                    clear_console()
    
    # Game over sequence
    clear_console()
    print_header("GAME OVER")
    time.sleep(GAME_DELAY)
    
    alive_players = [p for p in [player1, player2, snoop] if p and p.is_alive()]
    
    if len(alive_players) == 1:
        winner = alive_players[0]
        print(f"WINNER: {winner.name}!")
        print(f"Final lives: {winner.lives}")
        
        if winner == player1:
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
        
    elif len(alive_players) > 1:
        print("It's a tie!")
        print("Alive players:")
        for player in alive_players:
            print(f"  {player.name} with {player.lives} lives")
    else:
        print("All players have been eliminated!")
        print("It's a complete wipeout!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGame interrupted by user. Thanks for playing!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Please restart the game.")