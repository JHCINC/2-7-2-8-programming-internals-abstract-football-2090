import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import os
import time
import math
import random


# -------------------------------------------------------Variables------------------------------------------------------


state = 'main_menu' # State Decides What the Program Do in Every Loop
last_time = 0
past_time = 0
game_time = {'minute': 0, 'second': 0}
period = 0.5 # This Value Can Be Changed to Change the Gap of Every Cycle in the Game - Set to Half Minute as Default
next_cycle = period

configuration_name ='default' # The Default Configuration Name Is 'default'
team_data = None # Team Data Have Not Loaded
team_logos = {'main_menu': {}, 'game': {}}
track_images = {'blue_track': None, 'red_track': None, 'blue_sign': None, 'red_sign': None, 'full_track': None}
playing_teams = {'home_team': None, 'away_team': None}
number_teams = {1: 'home_team', -1: 'away_team'} # 1 Represents Home Team - -1 Represents Away Team
playing_players = {'home_team': {}, 'away_team': {}}

score = {'home_team': 0, 'away_team': 0}
position = 0
possession = 1
delayed = False # This Variable Means Whether the Advancing of the Ball Is Delayed - If Positive the Game Will Skip One Advance Action

# Root Is the Core of the Program
root = tk.Tk()
root.resizable(width=False, height=False)
root.title('Abstract Football 2025')

# ---------------------------------------------------Main Menu Widgets--------------------------------------------------

# instantiation of Frame "main_menu" as the Master of All the Main Menu Widgets
main_menu = tk.Frame(root, bg='#1D1D29')
main_menu.pack() # Display Main Menu from the Beginning

# Labels for Heading and Subheading
lb_heading1 = tk.Label(main_menu, text='Abstract Football 2025', font=('Times New Roman', 35, 'bold italic'), fg='lightgrey', bg='#1D1D29')
lb_heading2 = tk.Label(main_menu, text='Team Selection', font=('Verdana', 15, 'bold'), fg='lightgrey', bg='#1D1D29')

# Labels for Team Logos and the "VS" between
main_menu_home_team_logo = tk.Label(main_menu, bg='white', width=250, height=250)
main_menu_away_team_logo = tk.Label(main_menu, bg='white', width=250, height=250)
lb_vs = tk.Label(main_menu, text='V\u2009S', font=('Franklin Gothic Demi', 45, 'italic'), fg='White', bg='#1D1D29') # \u2009 is a quarter space

# Team Selection Dropdown
cbox_home_team = ttk.Combobox(main_menu, width=20, font=('Times New Roman', 12, 'bold'), state='readonly')
cbox_away_team = ttk.Combobox(main_menu, width=20, font=('Times New Roman', 12, 'bold'), state='readonly')

# Start Game Button
btn_start_game = tk.Button(main_menu, text='Start Game!', font=('Helvetica', 20, 'bold'), fg='lightgrey', bg='#c0392b')

# Label, Dropdowns and Button for Configuration Selection
lb_configurations = tk.Label(main_menu, text='Configuration Selection', font=('Verdana', 15, 'bold'), fg='lightgrey', bg='#1D1D29')
cbox_configuration = ttk.Combobox(main_menu, width=25, font=('Times New Roman', 12, 'bold'), state='readonly')
cbox_configuration['values'] = [file.split('.')[0] for file in os.listdir(os.path.abspath('.\\configurations'))]
if 'default' in cbox_configuration['values']:
    cbox_configuration.set('default') # Use the "default" Configuration if Exist
btn_load_configuration = tk.Button(main_menu, text='Load Configuration', font=('Helvetica', 20, 'bold'), fg='lightgrey', bg='#2c3e50')


# Place all the Widgets through Grid
lb_heading1.grid(column=0, columnspan=3, row=0, pady=25)
lb_heading2.grid(column=0, columnspan=3, row=1, pady=10)
lb_vs.grid(column=1, row=2)
main_menu_home_team_logo.grid(column=0, row=2, pady=20, padx=80)
main_menu_away_team_logo.grid(column=2, row=2, pady=20, padx=80)
cbox_home_team.grid(column=0, row=3, pady=40)
cbox_away_team.grid(column=2, row=3, pady=40)
btn_start_game.grid(column=1, row=3, pady=30)
lb_configurations.grid(column=1, row=4, pady=20)
cbox_configuration.grid(column=1, row=5, pady=5)
btn_load_configuration.grid(column=1, row=6, pady=40)

# -------------------------------------------------Game interface Widget------------------------------------------------

# instantiation of Frame "game_interface" as the Master of All the Game interface Widget
game_interface = tk.Frame(root, width=800, height=800)

# Timer for the Game
lb_timer = tk.Label(game_interface, font=('Ariel', 25), fg='red')

# Labels for Team Logos
game_home_team_logo = tk.Label(game_interface)
game_away_team_logo = tk.Label(game_interface)

# Labels for Team Names - Blue for the Home Team - Red for the Away Team
lb_home_team_name = tk.Label(game_interface, font=('Times New Roman', 20, 'bold'), fg='#3A86FF')
lb_away_team_name = tk.Label(game_interface, font=('Times New Roman', 20, 'bold'), fg='#c0392b')

# Labels for Team Scores and the Colon Between
lb_home_team_score = tk.Label(game_interface, font=('Ariel', 80), fg='red')
lb_away_team_score = tk.Label(game_interface, font=('Ariel', 80), fg='red')
lb_colon = tk.Label(game_interface, text=':', font=('Ariel', 60), fg='red')

# List Box to Display All the Major Events in the Game
event_box = tk.Listbox(game_interface, width=100, height=8)

# Track and Sign to Display the Position and Possession of the Ball
track = tk.Label(game_interface)
sign = tk.Label(game_interface, border=0)

# Buttons for Functions Return, Pause and Restart
btn_return = tk.Button(game_interface, width=8, height=1, text='Return', font=('Helvetica', 15, 'bold'), bg='orange', fg='white')
btn_pause = tk.Button(game_interface, width=8, height=1, text='Pause', font=('Helvetica', 15, 'bold'), bg='orange', fg='white')
btn_restart = tk.Button(game_interface, width=8, height=1, text='Restart', font=('Helvetica', 15, 'bold'), bg='orange', fg='white')

# Place All the Widgets through Grid
lb_timer.grid(column=3, row=0, pady=10)
game_home_team_logo.grid(column=1, row=1)
game_away_team_logo.grid(column=5, row=1)
lb_home_team_score.grid(column=2, row=1)
lb_away_team_score.grid(column=4, row=1)
lb_colon.grid(column=3, row=1)
lb_home_team_name.grid(column=1, row=2, pady=20)
lb_away_team_name.grid(column=5, row=2, pady=20)
event_box.grid(column=2, columnspan=3, row=2)
track.grid(column=1, columnspan=5, row=3, padx=100, pady=30)
btn_return.place(x=500, y=910)
btn_pause.place(x=690, y=910)
btn_restart.place(x=880, y=910)

# Player Boxes to Display All the Attributes of All the Players
player_box_parts = [] # These Parts are Labels in Boxes Need to be Updated in Every Game Cycle
for player in range(22):
    if player <= 10:
        border_color = '#3A86FF'
    else:
        border_color = '#c0392b'

    # Labels for Attributes in Player Boxes
    player_box = tk.Frame(game_interface, width=250, height=60, highlightbackground=border_color, highlightthickness=2)
    lb_player_name = tk.Label(player_box)
    lb_player_position = tk.Label(player_box)
    lb_player_advance = tk.Label(player_box)
    lb_player_defence = tk.Label(player_box)
    lb_player_dribbling = tk.Label(player_box)
    lb_player_finishing = tk.Label(player_box)
    lb_player_stamina = tk.Label(player_box)
    lb_player_energy = tk.Label(player_box)

    # Place All the Labels Through Grid
    lb_player_name.grid(column=0, row=0)
    lb_player_position.grid(column=0, row=1)
    lb_player_advance.grid(column=1, row=0)
    lb_player_defence.grid(column=1, row=1)
    lb_player_dribbling.grid(column=2, row=0)
    lb_player_finishing.grid(column=2, row=1)
    lb_player_stamina.grid(column=3, row=0)
    lb_player_energy.grid(column=3, row=1)

    # Add the Labels in the List to Update Them Every Cycle
    player_box_parts.append(
        [lb_player_name, lb_player_position, lb_player_advance, lb_player_defence, lb_player_dribbling, lb_player_finishing,
         lb_player_stamina, lb_player_energy]
    )

    # Arrange Player Boxes - Home Team on Left - Away Team on Right
    if player <= 5:
        column = 1
        row = 4 + player
        sticky = 'W'
    elif player <= 10:
        column = 2
        row = 4 + (player % 6)
        sticky = 'W'
    elif player <= 16:
        column = 5
        row = 4 + (player % 11)
        sticky = 'E'
    else:
        column = 4
        row = 4 + (player % 17)
        sticky = 'E'
    player_box.grid(column=column, row=row, padx=5, pady=10, sticky=sticky)


# -------------------------------------------------------Functions------------------------------------------------------


# When instantiating the Buttons, the Command of Buttons May Not Defined So We Must Bind Them Together Later
def bind_button_commands():
    btn_start_game.config(command=start_game)
    btn_load_configuration.config(command=load_configuration)
    btn_return.config(command=return_main_menu)
    btn_pause.config(command=pause)
    btn_restart.config(command=initialise_game)


# Configuration includes the Data of Teams and Players
def load_configuration():
    global team_data
    path = os.path.abspath('.\\configurations\\' + cbox_configuration.get() + '.txt') # Get the Path of the Configuration File
    with open(path) as configuration:
        team_data = eval(configuration.read()) # The Configuration Is Written in the form of Dictionary - It Can Be Read Directly

    # Set the Terms of Choosing Boxes of Teams - Set to Select a Team as Default
    teams = list(team_data.keys())
    teams.insert(0, 'Select a Team')
    cbox_home_team['values'] = cbox_away_team['values'] = teams
    cbox_home_team.current(0), cbox_away_team.current(0)

    # Reload the Logos of Teams
    team_logos['main_menu'].clear(), team_logos['game'].clear()
    for team in teams:
        team_logos['main_menu'][team] = ImageTk.PhotoImage(Image.open(os.path.abspath('.\\asset\\team_logos\\' + team + '.png')).resize((250, 250)))
        team_logos['game'][team] = ImageTk.PhotoImage(Image.open(os.path.abspath('.\\asset\\team_logos\\' + team + '.png')).resize((200, 200)))
        

# Load the Images of the Track
def load_track_images():
    for image in ('blue_track', 'red_track'):
        track_images[image] = Image.open((os.path.abspath('.\\asset\\track_images\\' + image + '.png')))
    for image in ('blue_sign', 'red_sign'):
        track_images[image] = ImageTk.PhotoImage(Image.open((os.path.abspath('.\\asset\\track_images\\' + image + '.png'))))




# Start the Game - Switch Between Main Menu and Game interface
def start_game():
    global state
    
    # Error Preventing - Pop Up a Message Box If the User Has Not Select Both Two Teams
    if playing_teams['home_team'] == 'Select a Team' or playing_teams['away_team'] == 'Select a Team':
        tk.messagebox.showwarning('Warning', 'You must select both two teams.')
        return

    state = 'playing'
    main_menu.pack_forget()
    game_interface.pack()
    initialise_game()


# Return to Main Menu - Switch Between Game interface and Main Menu
def return_main_menu():
    global state
    state = 'main_menu'
    game_interface.pack_forget()
    main_menu.pack()


# initialise the Football Game - Execute When Starting the Game or Restarting the Game
def initialise_game():
    global state
    state = 'playing'

    score['home_team'] = score['away_team'] = game_time['minute'] = game_time['second'] = 0

    global position, past_time, last_time
    position = past_time = last_time = 0

    global next_cycle
    next_cycle = period

    global possession
    possession = 1

    global delayed
    delayed = False

    event_box.delete(0, tk.END)

    initialise_players()
    initialise_game_team_logos()
    initialise_game_team_names()
    update_score()
    update_track()
    update_player_box_parts()

    last_time = time.time()


# initialise the Players - Set Energy to 100 for Every One
def initialise_players():
    playing_players['home_team'] = team_data[playing_teams['home_team']]['players'].copy()
    for player in playing_players['home_team']:
        player['energy'] = 100

    playing_players['away_team'] = team_data[playing_teams['away_team']]['players'].copy()
    for player in playing_players['away_team']:
        player['energy'] = 100


# initialise Team Logos in the Game interface
def initialise_game_team_logos():
    game_home_team_logo.config(image=team_logos['game'][playing_teams['home_team']])
    game_away_team_logo.config(image=team_logos['game'][playing_teams['away_team']])


# initialise the Labels of Team Names in the Game interface
def initialise_game_team_names():
    lb_home_team_name.config(text=playing_teams['home_team'])
    lb_away_team_name.config(text=playing_teams['away_team'])


# Pause the Game
def pause():
    global state
    if state == 'pause':
        state = 'playing'
    else:
        state = 'pause'


# This Function Is Used to Calculate the Position Modification of Every Player - Different Type of Players Have Different Calculation Method
def calculate_modification(player, side):
    relative_position = position * side # Relative Position Is The Distance to Opponent's Goal
    
    # Keepers Do Not Participate in Tackle or Advance - They Only Defend in Shooting
    if player['position'] == 'keeper':
        return 0
    
    elif player['position'] == 'attacker':
        # Attackers Have No Efficiency in the Half Field Close to Their Own Goal
        if relative_position <= 0:
            return 0
        # Closer to Their Opponent's Goal, They Have Bigger Efficiency
        elif 0 < relative_position < 60:
            return 0.4 + relative_position * 0.01
        # Attackers Have 100% Efficiency in the One Fifth Field Close to Their Opponent's Goal
        elif relative_position >= 60:
            return 1

    elif player['position'] == 'midfield':
        # Midfielder Have 40% Efficiency in the One Fifth Field Close to Their Own Goal
        if relative_position <= -60:
            return 0.4
        # Closer to the Middle, They Have Bigger Efficiency
        elif -60 < relative_position < -20:
            return 1 - (-20 - relative_position) * 0.015
        # Midfielder Have 100% Efficiency in the One Fifth Field in the Middle
        elif -20 <= relative_position <= 20:
            return 1
        # Closer to the Middle, They Have Bigger Efficiency
        elif 20 < relative_position < 60:
            return 1 - (60 - relative_position) * 0.015
        # Midfielder Have 40% Efficiency in the One Fifth Field Close to Their Opponent's Goal
        elif relative_position >= 60:
            return 0.4

    elif player['position'] == 'defender':
        # Defenders Have 100% Efficiency in the One Fifth Field Close to Their Own Goal
        if relative_position <= -60:
            return 1
        # Closer to Their Own Goal, They Have Bigger Efficiency
        elif -60 < relative_position < 0:
            return 1 + relative_position * 0.01
        # Midfielder Have No Efficiency in the Half Field Close to Their Opponent's Goal
        elif relative_position >= 0:
            return 0


# This Function Is Used to Calculate the Attributes of Players After Their Energy's Effect
def calculate_ability(player):
    # There Is No Effect When They Have More Than 70% Energy
    if player['energy'] > 70:
        return 1
    # Their Attributes Will Be Between 95% and 80% When They Have Energy Between 70% and 40% (Not including 40%)
    elif player['energy'] > 40:
        return 0.95 - (70 - player['energy']) / 200
    # Their Attributes Will Be Between 70% and 50% When They Have Energy Between 40% and 0%
    elif player['energy'] > 0:
        return 0.7 - (40 - player['energy']) / 200
    # Their Attributes Will Be 50% When They Have Zero Energy
    else:
        return 0.5


# Player Will Consume Some Energy Once They Participate in Any Action - Bigger the Position Modification, Higher the Energy Consumption
def consume_energy(player, modification):
    player['energy'] -= random.random() * (0.3 - player['stamina'] * 0.02) * modification
    if player['energy'] < 0:
        player['energy'] = 0


# This Function Is Used to Add a Message to the Event Box
def append_event(message, style):
    event_box.insert(0, message)
    event_box.itemconfig(0, style)


def end_game():
    global state
    state = 'game_ended'
    game_time['minute'] = 90
    game_time['second'] = 0


# --------------------------------------------------------Update--------------------------------------------------------
# Update the Main Menu 
def update_main_menu():
    playing_teams['home_team'] = cbox_home_team.get()
    playing_teams['away_team'] = cbox_away_team.get()
    main_menu_home_team_logo.config(image=team_logos['main_menu'][playing_teams['home_team']])
    main_menu_away_team_logo.config(image=team_logos['main_menu'][playing_teams['away_team']])


# Update the Time in the Game 
def update_time():
    global last_time, past_time
    now = time.time()
    past_time += (now - last_time) * 0.5 # This Value Can Be Changed to Change the Speed of the Game
    last_time = now
    game_time['minute'] = math.trunc(past_time) # Covert the Change of Real Time into Game Time
    game_time['second'] = math.trunc(math.modf(past_time)[0] * 60)
    lb_timer.config(text=str(game_time['minute']).zfill(2) + ' : ' + str(game_time['second']).zfill(2)) # Update the Timer


# Update the Showing Score Board in the Game
def update_score():
    lb_home_team_score.config(text=str(score['home_team']))
    lb_away_team_score.config(text=str(score['away_team']))


# Update the Track in the Game to Show the Position of the Ball
def update_track():
    blue_track = track_images['blue_track'].crop((0, 0, int(((position + 100) / 200) * 1278), 67))
    red_track = track_images['red_track'].crop((int(((position + 100) / 200) * 1278), 0, 1278, 67))
    full_track = Image.new('RGB', (1278, 67))
    full_track.paste(blue_track, (0, 0))
    full_track.paste(red_track, (blue_track.width, 0))
    track_images['full_track'] = ImageTk.PhotoImage(full_track)
    track.config(image=track_images['full_track'])

    if possession == 1:
        sign.config(image=track_images['blue_sign'])
    else:
        sign.config(image=track_images['red_sign'])
    sign.place(x=11 + int(((position + 100) / 200) * 1367), y=430)


# Update Player Boxes to Show the Attributes of Players
def update_player_box_parts():
    for index in range(22):
        if index <= 10:
            player = playing_players['home_team'][index]
        else:
            player = playing_players['away_team'][index % 11]
        parts = player_box_parts[index]
        parts[0].config(text=player['name'])
        parts[1].config(text=player['position'])
        parts[2].config(text='advance: ' + str(round(player['advance'] * calculate_ability(player), 1)))
        parts[3].config(text='defence: ' + str(round(player['defence'] * calculate_ability(player), 1)))
        parts[4].config(text='dribbling: ' + str(round(player['dribbling'] * calculate_ability(player), 1)))
        parts[5].config(text='finishing: ' + str(round(player['finishing'] * calculate_ability(player), 1)))
        parts[6].config(text='stamina: ' + str(player['stamina']))
        parts[7].config(text='energy: ' + str(round(player['energy'])))


# --------------------------------------------------------Actions-------------------------------------------------------


# Update Actions in Every Cycle - Composed of Update Tackle, Update Advance and Update Shooting - The Order Does Matter
def update_actions():
    update_tackle()
    update_advance()
    update_shooting()


'''In the process of update tackle, attackers are players who control the ball and they need attribute Dribbling to 
keep the ball from being tackle by defenders, who need the attribute Defence. Every attacker and every defender will 
have a dice value generated randomly with some advantage to attackers. Each attacker will compare the sum of Dribbling
value and dice value to each defender with sum of Defence value and dice value. If one attacker win, the difficulty of 
tackle will increase by a value calculated from the attacker's Dribbling. After calculated the difficulty of tackle,
every defender will have a base value calculated from Defence value. Use this base value to divide by the difficulty of 
tackle is the possibility to this defender to successful tackle the ball. The modifications of position and energy of 
players will be calculated and affect the result.'''

def update_tackle():
    global possession, delayed, position
    # Get Attackers and Defenders Who Have More Than 0 Position Efficiency
    attackers = [player for player in playing_players[number_teams[possession]] if calculate_modification(player, possession) > 0]
    defenders = [player for player in playing_players[number_teams[possession * -1]] if calculate_modification(player, possession * -1) > 0]
    attack_dices = [random.randint(0, 10) for _ in attackers] # Generate Random Dice Values

    for defender in defenders:
        tackle_difficulty = 5
        defence_ability = defender['defence'] * calculate_ability(defender) # Attribute Value Is Affected by Energy
        defence_modification = calculate_modification(defender, possession * -1) # Tackle Base Value Is Affected by Position
        defence_dice = random.randint(0, 8) # Generate Random Dice Value

        consume_energy(defender, defence_modification)

        for attacker_index in range(len(attackers)):
            attacker = attackers[attacker_index]
            attack_ability = attacker['dribbling'] * calculate_ability(attacker) # Attribute Value Is Affected by Energy
            attack_modification = calculate_modification(attacker, possession) # increasing Tackle Difficulty Is Affected by Position
            attack_dice = attack_dices[attacker_index]

            consume_energy(attacker, attack_modification)

            if attack_ability + attack_dice >= defence_ability + defence_dice: # If Attacker Win the Comparison, Tackle Difficulty Will increase
                difficulty_increase = (10 + attack_ability) * attack_modification 
                tackle_difficulty += difficulty_increase

        # Tackle Possibility Equals Tackle Base Divided by Tackle Difficulty
        tackle_possibility = ((1 + defence_ability * 0.3) * defence_modification) / tackle_difficulty
        if random.random() < tackle_possibility: # If Tackle Successes
            if random.randint(0, 1): # There Is One Half Possibility That Defenders Can Tackle The Ball
                random_time = past_time - random.random() * period # Generate Random Time for Event Message 
                message = defender['name'] + ' tackled the ball at ' + str(math.trunc(random_time)).zfill(2) + ' : ' + str(math.trunc(math.modf(random_time)[0] * 60)).zfill(2) + '.'
                append_event(message, {'fg': {1: '#c0392b', -1: '#3A86FF'}[possession]})
                possession *= -1
                return

            else: # There Is Another Half Possibility That Defenders Can Delay The Advancing Of The Ball
                delayed = True
                position -= round(random.randint(5, 15) * possession) # Randomly Generate the Delaying Distance

                if position > 100:
                    position = 100
                elif position < -100:
                    position = -100
                return


def update_advance():
    global delayed, position

    if delayed:
        delayed = False
        return

    advance_result = 0
    attackers = [player for player in playing_players[number_teams[possession]] if calculate_modification(player, possession) > 0]
    defenders = [player for player in playing_players[number_teams[possession * -1]] if calculate_modification(player, possession * -1) > 0]
    defence_dices = [random.randrange(0, 5) for _ in defenders] # Generate Random Dice Values

    for attacker in attackers:
        attack_efficiency = 1
        attack_ability = attacker['advance'] * calculate_ability(attacker) # Attribute Value Is Affected by Energy
        attack_modification = calculate_modification(attacker, possession)
        attack_dice = random.randrange(0, 6) # Generate Random Dice Value
        attack_expectation = 2 + 0.4 * attack_ability * attack_modification

        consume_energy(attacker, attack_modification)

        for defender_index in range(len(defenders)):
            defender = defenders[defender_index]
            defence_ability = defender['defence'] * calculate_ability(defender) # Attribute Value Is Affected by Energy
            defence_modification = calculate_modification(defender, possession * -1)
            defence_dice = defence_dices[defender_index]

            consume_energy(defender, defence_modification)

            if (defence_ability + defence_dice) > (attack_ability + attack_dice):
                attack_efficiency -= (0.1 + defence_ability * 0.02) * defence_modification

        if attack_efficiency > 0:
            attack_result = attack_efficiency * attack_expectation
            advance_result += attack_result

    random_modification = random.randint(0, 8)
    position += round(advance_result + random_modification) * possession

    if position > 100:
        position = 100
    elif position < -100:
        position = -100


def update_shooting():
    global possession, position, delayed

    if position * possession < 0:
        return

    attackers = [player for player in playing_players[number_teams[possession]] if calculate_modification(player, possession) > 0]
    defenders = [player for player in playing_players[number_teams[possession * -1]] if calculate_modification(player, possession * -1) > 0]
    keeper = [player for player in playing_players[number_teams[possession * -1]] if player['position'] == 'keeper'][0]
    defence_dices = [random.randint(0, 5) for _ in defenders]

    for attacker in attackers:
        shooting_difficulty = 20
        attack_ability = attacker['finishing'] * calculate_ability(attacker) # Attribute Value Is Affected by Energy
        attack_modification = calculate_modification(attacker, possession)
        attack_dice = random.randint(0, 6)
        shooting_ability = attack_ability * 0.3 * attack_modification * (1 + ((position * possession) / 50) ** 2)

        consume_energy(attacker, attack_modification)

        for defender_index in range(len(defenders)):
            defender = defenders[defender_index]
            defence_ability = defender['defence'] * calculate_ability(defender) # Attribute Value Is Affected by Energy
            defence_modification = calculate_modification(defender, possession * -1)
            defence_dice = defence_dices[defender_index]

            consume_energy(defender, defence_modification)

            if defence_ability + defence_dice > attack_ability + attack_dice:
                shooting_difficulty += (defence_ability + 5) * defence_modification
            else:
                shooting_difficulty += (defence_ability + 5) * defence_modification / 2

        if random.random() < shooting_ability / shooting_difficulty:
            shooting_possibility = (attack_ability * (1 + position * possession / 100 * 5)) / (keeper['defence'] * 10 + 80)
            if random.random() < shooting_possibility:
                random_time = past_time - random.random() * period
                message = attacker['name'] + ' scored a Goal at ' + str(math.trunc(random_time)).zfill(2) + ' : ' + str(math.trunc(math.modf(random_time)[0] * 60)).zfill(2) + '!'
                append_event(message, {'bg': {1: '#3A86FF', -1: '#c0392b'}[possession], 'fg': 'white'})
                delayed = True
                score[number_teams[possession]] += 1
                possession *= -1
                position = 0
                return

            else:
                random_time = past_time - random.random() * period
                message = attacker['name'] + ' took a shot at ' + str(math.trunc(random_time)).zfill(2) + ' : ' + str(math.trunc(math.modf(random_time)[0] * 60)).zfill(2) + ' but missed the goal.'
                append_event(message, {'fg': {1: '#3A86FF', -1: '#c0392b'}[possession]})
                delayed = True
                possession *= -1
                position = random.randint(20, 60) * possession * -1
                return


# ---------------------------------------------------------Main---------------------------------------------------------


# The main Function Is the Mainloop of the Game - It Executes Before Every Time When Tkinter Updates the Widgets
def main():
    global next_cycle

    if state == 'main_menu':
        update_main_menu()

    elif state == 'playing':
        update_time() # Update Time When the Game Is Playing
        if past_time > next_cycle: # Determine Whether Reached the Time for a Cycle
            next_cycle += period
            update_actions()
            update_score()
            update_track()
            update_player_box_parts()
            if past_time >= 90: # Determine Whether the Time Is Up
                end_game()

    elif state == 'pause':
        global last_time
        last_time = time.time()

    elif state == 'end_game':
        pass

    root.after(1, main) # This Give the Program the Order to Execute main Function Again


# These Functions Will Be Executed At the First When Start to Run the Program
load_configuration()
load_track_images()
bind_button_commands()
root.after(1, main)
root.mainloop()
