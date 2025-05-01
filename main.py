import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import os
import time
import math
import random


state = 'main_menu'
last_time = 0
past_time = 0
game_time = {'minute': 0, 'second': 0}
period = 0.5
next_cycle = period

configuration_name ='default'
team_data = None
team_logos = {'main_menu': {}, 'game': {}}
playing_teams = {'home_team': None, 'away_team': None}
number_teams = {1: 'home_team', -1: 'away_team'}
playing_players = {'home_team': {}, 'away_team': {}}
score = {'home_team': 0, 'away_team': 0}
position = 0
possession = 1
delayed = False
track_images = {'blue_track': None, 'red_track': None, 'blue_sign': None, 'red_sign': None, 'full_track': None}


root = tk.Tk()
root.resizable(width=False, height=False)
root.title('Abstract Football 2025')

# ---------------------------------------------------Main Menu Widgets--------------------------------------------------

# Instantiation of Frame "main_menu" as the Master of All the Main Menu Widgets
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

# -------------------------------------------------Game Interface Widget------------------------------------------------

# Instantiation of Frame "game_interface" as the Master of All the Game Interface Widget
game_interface = tk.Frame(root, width=800, height=800)

# Timer for the Game
lb_timer = tk.Label(game_interface, font=('Ariel', 25), fg='red')

# Labels for Team Logos
game_home_team_logo = tk.Label(game_interface)
game_away_team_logo = tk.Label(game_interface)

# Labels for Team Names - Blue for the Home Team - Red for the Away Team
lb_home_team_name = tk.Label(game_interface, font=('Times New Roman', 20), fg='#3A86FF')
lb_away_team_name = tk.Label(game_interface, font=('Times New Roman', 20), fg='#c0392b')

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
btn_return = tk.Button(game_interface, width=8, height=1, text='Return', font=('Times New Roman', 15), bg='yellow')
btn_pause = tk.Button(game_interface, width=8, height=1, text='Pause', font=('Times New Roman', 15), bg='yellow')
btn_restart = tk.Button(game_interface, width=8, height=1, text='Restart', font=('Times New Roman', 15), bg='yellow')

# Place all the Widgets through Grid
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
btn_return.place(x=540, y=910)
btn_pause.place(x=690, y=910)
btn_restart.place(x=840, y=910)

# Player Box to Display All the Attributes of All the Players
player_box_parts = [] # These Parts are Labels in Boxes Need to be Updated in Every Game Cycle
for player in range(22):
    if player <= 10:
        border_color = '#3A86FF'
    else:
        border_color = '#c0392b'
    player_box = tk.Frame(game_interface, width=250, height=60, highlightbackground=border_color, highlightthickness=2)
    lb_player_name = tk.Label(player_box)
    lb_player_position = tk.Label(player_box)
    lb_player_advance = tk.Label(player_box)
    lb_player_defence = tk.Label(player_box)
    lb_player_dribbling = tk.Label(player_box)
    lb_player_finishing = tk.Label(player_box)
    lb_player_stamina = tk.Label(player_box)
    lb_player_energy = tk.Label(player_box)

    lb_player_name.grid(column=0, row=0)
    lb_player_position.grid(column=0, row=1)
    lb_player_advance.grid(column=1, row=0)
    lb_player_defence.grid(column=1, row=1)
    lb_player_dribbling.grid(column=2, row=0)
    lb_player_finishing.grid(column=2, row=1)
    lb_player_stamina.grid(column=3, row=0)
    lb_player_energy.grid(column=3, row=1)

    player_box_parts.append(
        [lb_player_name, lb_player_position, lb_player_advance, lb_player_defence, lb_player_dribbling, lb_player_finishing,
         lb_player_stamina, lb_player_energy]
    )

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


def bind_button_commands():
    btn_start_game.config(command=start_game)
    btn_load_configuration.config(command=load_configuration)
    btn_return.config(command=return_main_menu)
    btn_pause.config(command=pause)
    btn_restart.config(command=initialise_game)


def load_configuration():
    global team_data
    path = os.path.abspath('.\\configurations\\' + cbox_configuration.get() + '.txt')
    with open(path) as configuration:
        team_data = eval(configuration.read())

    teams = list(team_data.keys())
    teams.insert(0, 'Select a Team')
    cbox_home_team['values'] = cbox_away_team['values'] = teams
    cbox_home_team.current(0), cbox_away_team.current(0)

    team_logos['main_menu'].clear(), team_logos['game'].clear()
    for team in teams:
        team_logos['main_menu'][team] = ImageTk.PhotoImage(Image.open(os.path.abspath('.\\asset\\team_logos\\' + team + '.png')).resize((250, 250)))
        team_logos['game'][team] = ImageTk.PhotoImage(Image.open(os.path.abspath('.\\asset\\team_logos\\' + team + '.png')).resize((200, 200)))

def load_track_images():
    for image in ('blue_track', 'red_track'):
        track_images[image] = Image.open((os.path.abspath('.\\asset\\track_images\\' + image + '.png')))
    for image in ('blue_sign', 'red_sign'):
        track_images[image] = ImageTk.PhotoImage(Image.open((os.path.abspath('.\\asset\\track_images\\' + image + '.png'))))


def update_main_menu():
    playing_teams['home_team'] = cbox_home_team.get()
    playing_teams['away_team'] = cbox_away_team.get()
    main_menu_home_team_logo.config(image=team_logos['main_menu'][playing_teams['home_team']])
    main_menu_away_team_logo.config(image=team_logos['main_menu'][playing_teams['away_team']])


def start_game():
    global state

    if playing_teams['home_team'] == 'Select a Team' or playing_teams['away_team'] == 'Select a Team':
        tk.messagebox.showwarning('Warning', 'You must select both two teams.')
        return

    state = 'playing'
    main_menu.pack_forget()
    game_interface.pack()
    initialise_game()


def return_main_menu():
    global state
    state = 'main_menu'
    game_interface.pack_forget()
    main_menu.pack()

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


def initialise_players():
    playing_players['home_team'] = team_data[playing_teams['home_team']]['players'].copy()
    for player in playing_players['home_team']:
        player['energy'] = 100

    playing_players['away_team'] = team_data[playing_teams['away_team']]['players'].copy()
    for player in playing_players['away_team']:
        player['energy'] = 100


def initialise_game_team_logos():
    game_home_team_logo.config(image=team_logos['game'][playing_teams['home_team']])
    game_away_team_logo.config(image=team_logos['game'][playing_teams['away_team']])


def initialise_game_team_names():
    lb_home_team_name.config(text=playing_teams['home_team'])
    lb_away_team_name.config(text=playing_teams['away_team'])


def update_time():
    global last_time, past_time

    now = time.time()
    past_time += (now - last_time) * 0.5
    last_time = now
    game_time['minute'] = math.trunc(past_time)
    game_time['second'] = math.trunc(math.modf(past_time)[0] * 60)
    lb_timer.config(text=str(game_time['minute']).zfill(2) + ' : ' + str(game_time['second']).zfill(2))


def pause():
    global state
    if state == 'pause':
        state = 'playing'
    else:
        state = 'pause'


def calculate_modification(player, side):
    relative_position = position * side
    if player['position'] == 'keeper':
        return 0

    elif player['position'] == 'attacker':
        if relative_position <= 0:
            return 0
        elif 0 < relative_position < 60:
            return 0.4 + relative_position * 0.01
        elif relative_position >= 60:
            return 1

    elif player['position'] == 'midfield':
        if relative_position <= -60:
            return 0.4
        elif -60 < relative_position < -20:
            return 1 - (-20 - relative_position) * 0.015
        elif -20 <= relative_position <= 20:
            return 1
        elif 20 < relative_position < 60:
            return 1 - (60 - relative_position) * 0.015
        elif relative_position >= 60:
            return 0.4

    elif player['position'] == 'defender':
        if relative_position <= -60:
            return 1
        elif -60 < relative_position < 0:
            return 1 + relative_position * 0.01
        elif relative_position >= 0:
            return 0


def calculate_ability(player):
    if player['energy'] > 70:
        return 1
    elif player['energy'] > 40:
        return 0.95 - (70 - player['energy']) / 200
    elif player['energy'] > 0:
        return 0.7 - (40 - player['energy']) / 200
    else:
        return 0.5


def update_actions():
    update_tackle()
    update_advance()
    update_shooting()


def update_tackle():
    global possession, delayed, position
    attackers = [player for player in playing_players[number_teams[possession]] if calculate_modification(player, possession) > 0]
    defenders = [player for player in playing_players[number_teams[possession * -1]] if calculate_modification(player, possession * -1) > 0]

    attack_rolls = [random.randint(0, 10) for _ in attackers]

    for defender in defenders:
        tackle_difficulty = 5
        defence_ability = defender['defence'] * calculate_ability(defender)
        defence_modification = calculate_modification(defender, possession * -1)
        defence_roll = random.randint(0, 8)

        defender['energy'] -= random.random() * (0.5 - defender['stamina'] * 0.035) * defence_modification
        if defender['energy'] < 0:
            defender['energy'] = 0

        for attacker_index in range(len(attackers)):
            attacker = attackers[attacker_index]
            attack_ability = attacker['dribbling'] * calculate_ability(attacker)
            attack_modification = calculate_modification(attacker, possession)
            attack_roll = attack_rolls[attacker_index]

            attacker['energy'] -= random.random() * (0.5 - attacker['stamina'] * 0.035) * attack_modification
            if attacker['energy'] < 0:
                attacker['energy'] = 0

            if attack_ability + attack_roll >= defence_ability + defence_roll:
                difficulty_increase = (10 + attack_ability) * attack_modification
                tackle_difficulty += difficulty_increase

        tackle_possibility = ((1 + defence_ability * 0.3) * defence_modification) / tackle_difficulty
        if random.random() < tackle_possibility:
            if random.randint(0, 1):
                if possession == -1:
                    color = '#3A86FF'
                else:
                    color = '#c0392b'
                possession *= -1
                random_time = past_time - random.random() * period
                message = defender['name'] + ' tackled the ball at ' + str(math.trunc(random_time)).zfill(2) + ' : ' + str(math.trunc(math.modf(random_time)[0] * 60)).zfill(2) + '.'
                event_box.insert(0, message)
                event_box.itemconfig(0, {'fg': color})
                return

            else:
                delayed = True
                position -= random.randint(5, 15)

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
    defence_rolls = [random.randrange(0, 5) for _ in defenders]

    for attacker in attackers:
        attack_efficiency = 1
        attack_ability = attacker['advance'] * calculate_ability(attacker)
        attack_modification = calculate_modification(attacker, possession)
        attack_roll = random.randrange(0, 6)
        attack_expectation = 2 + 0.4 * attack_ability * attack_modification

        attacker['energy'] -= random.random() * (0.5 - attacker['stamina'] * 0.035) * attack_modification
        if attacker['energy'] < 0:
            attacker['energy'] = 0

        for defender_index in range(len(defenders)):
            defender = defenders[defender_index]
            defence_ability = defender['defence'] * calculate_ability(defender)
            defence_modification = calculate_modification(defender, possession * -1)
            defence_roll = defence_rolls[defender_index]

            defender['energy'] -= random.random() * (0.5 - defender['stamina'] * 0.035) * defence_modification
            if defender['energy'] < 0:
                defender['energy'] = 0

            if (defence_ability + defence_roll) > (attack_ability + attack_roll):
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
    defence_rolls = [random.randint(0, 5) for _ in defenders]

    for attacker in attackers:
        shooting_difficulty = 20
        attack_ability = attacker['finishing'] * calculate_ability(attacker)
        attack_modification = calculate_modification(attacker, possession)
        attack_roll = random.randint(0, 6)
        shooting_ability = attack_ability * 0.3 * attack_modification * (1 + ((position * possession) / 50) ** 2)

        attacker['energy'] -= random.random() * (0.5 - attacker['stamina'] * 0.035) * attack_modification
        if attacker['energy'] < 0:
            attacker['energy'] = 0

        for defender_index in range(len(defenders)):
            defender = defenders[defender_index]
            defence_ability = defender['defence'] * calculate_ability(defender)
            defence_modification = calculate_modification(defender, possession * -1)
            defence_roll = defence_rolls[defender_index]

            defender['energy'] -= random.random() * (0.5 - defender['stamina'] * 0.035) * defence_modification
            if defender['energy'] < 0:
                defender['energy'] = 0

            if defence_ability + defence_roll > attack_ability + attack_roll:
                shooting_difficulty += (defence_ability + 5) * defence_modification
            else:
                shooting_difficulty += (defence_ability + 5) * defence_modification / 2

        if random.random() < shooting_ability / shooting_difficulty:
            shooting_possibility = (attack_ability * (1 + position * possession / 100 * 5)) / (keeper['defence'] * 10 + 80)
            if random.random() < shooting_possibility:
                if possession == 1:
                    color = '#3A86FF'
                else:
                    color = '#c0392b'
                delayed = True
                score[number_teams[possession]] += 1
                possession *= -1
                position = 0
                random_time = past_time - random.random() * period
                message = attacker['name'] + ' scored a Goal at ' + str(math.trunc(random_time)).zfill(2) + ' : ' + str(math.trunc(math.modf(random_time)[0] * 60)).zfill(2) + '!'
                event_box.insert(0, message)
                event_box.itemconfig(0, {'bg': color, 'fg': 'white'})
                return

            else:
                if possession == 1:
                    color = '#3A86FF'
                else:
                    color = '#c0392b'
                delayed = True
                possession *= -1
                position = random.randint(20, 60) * possession * -1
                random_time = past_time - random.random() * period
                message = attacker['name'] + ' took a shot at ' + str(math.trunc(random_time)).zfill(2) + ' : ' + str(math.trunc(math.modf(random_time)[0] * 60)).zfill(2) + ' but missed the goal.'
                event_box.insert(0, message)
                event_box.itemconfig(0, {'fg': color})
                return


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


def update_score():
    lb_home_team_score.config(text=str(score['home_team']))
    lb_away_team_score.config(text=str(score['away_team']))


def end_game():
    global state
    state = 'game_ended'
    game_time['minute'] = 90
    game_time['second'] = 0


def main():
    global next_cycle

    if state == 'main_menu':
        update_main_menu()

    elif state == 'playing':
        update_time()
        if past_time > next_cycle:
            next_cycle += period
            update_actions()
            update_score()
            update_track()
            update_player_box_parts()
            if past_time >= 90:
                end_game()

    elif state == 'pause':
        global last_time
        last_time = time.time()

    elif state == 'end_game':
        pass

    root.after(1, main)


load_configuration()
load_track_images()
bind_button_commands()
root.after(1, main)
root.mainloop()
