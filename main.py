import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import time
import math


state = 'main_menu'
last_time = 0
past_time = 0
game_time = {'minute': 0, 'second': 0}
last_minute = 0
team_data = {
    'Manchester City': {'players':{}},
    'Real Madrid': {'players':{}},
    'Barcelona': {'players':{}},
    'Arsenal': {'players':{}},
    'Liverpool': {'players':{}},
    'Bayern Munich': {'players':{}}
    }
team_logos = {}
playing_teams = {'home_team': None, 'away_team': None}
playing_players = {'home_team': {}, 'away_team': {}}
score = {'home_team': 0, 'away_team': 0}
position = 0
possession = 'home_team'
track_images = {'blue_track': None, 'red_track': None, 'blue_sign': None, 'red_sign': None, 'full_track': None}


root = tk.Tk()
root.resizable(width=False, height=False)
root.title("Abstract Football 2025")


main_menu = tk.Frame(root, bg="#1D1D29")
main_menu.pack()

# Labels for Heading and Subheading of GUIS
lb_heading1 = tk.Label(main_menu, text="Ultimate Team Football 2025", font=("Times New Roman", 28, "bold italic"), fg="lightgrey", bg="#1D1D29")
lb_heading2 = tk.Label(main_menu, text="Team Selection", font=("Times New Roman", 20, "bold"), fg="lightgrey", bg="#1D1D29")

# Labels for teams
lb_heading3 = tk.Label(main_menu, text="Select Your Teams:", font=("Ariel", 15), fg="lightgrey", bg="#1D1D29")
lb_vs = tk.Label(main_menu, text="VS", font=("Sans-serif", 25, "bold italic"), fg="White", bg="#1D1D29")

home_team_logo_frame = tk.Frame(main_menu, bg='white', bd=0, cursor='hand2', height=180,
                      highlightthickness=0, relief=tk.RAISED, width=150)

away_team_logo_frame = tk.Frame(main_menu, bg='white', bd=0, cursor='hand2', height=180,
                      highlightthickness=0, relief=tk.RAISED, width=150)

home_team_logo = tk.Label(home_team_logo_frame)
away_team_logo = tk.Label(away_team_logo_frame)

# Team Selection Dropdown

cbox_home_team = ttk.Combobox(main_menu, width=20, font=("Times New Roman", 12, "bold"), state="readonly")
cbox_away_team = ttk.Combobox(main_menu, width=20, font=("Times New Roman", 12, "bold"), state="readonly")

btn_start_game = tk.Button(main_menu, text='Start Game!', font=("Times New Roman", 20, "bold"), fg="red", bg="lightblue")

lb_heading1.grid(column=0, columnspan=3, row=0, pady=10)
lb_heading2.grid(column=0, columnspan=3, row=1, pady=10)
lb_heading3.grid(column=0, columnspan=3, row=2, pady=20)
lb_vs.grid(column=1, row=3)
home_team_logo_frame.grid(column=0, row=3, pady=20, padx=80)
away_team_logo_frame.grid(column=2, row=3, pady=20, padx=80)
home_team_logo.pack()
away_team_logo.pack()
cbox_home_team.grid(column=0, row=4, pady=40)
cbox_away_team.grid(column=2, row=4, pady=40)
btn_start_game.grid(column=1, row=4)


game_interface = tk.Frame(root, width=800, height=800)

lb_timer = tk.Label(game_interface, font=("Ariel", 15), fg="red")

track = tk.Label(game_interface)
sign = tk.Label(game_interface, border=0)

lb_timer.grid(column=2, row=0)
track.grid(column=0, columnspan=5, row=1, padx=100, pady=50)


def bind_button_commands():
    btn_start_game.config(command=start_game)


def load_team_data():
    teams = list(team_data.keys())
    teams.insert(0, 'Select a Team')
    cbox_home_team['values'] = cbox_away_team['values'] = teams
    cbox_home_team.current(0), cbox_away_team.current(0)

    team_logos.clear()
    for team in teams:
        team_logos[team] = ImageTk.PhotoImage(Image.open(os.path.abspath('.\\asset\\team_logos\\' + team + '.png')).resize((200, 200)))


def load_track_images():
    for image in ('blue_track', 'red_track'):
        track_images[image] = Image.open((os.path.abspath('.\\asset\\track_images\\' + image + '.png')))
    for image in ('blue_sign', 'red_sign'):
        track_images[image] = ImageTk.PhotoImage(Image.open((os.path.abspath('.\\asset\\track_images\\' + image + '.png'))))


def start_game():
    global state
    state = 'playing'
    main_menu.destroy()
    game_interface.pack()
    initialise_game()


def initialise_game():
    score['home_team'] = score['away_team'] = 0

    global position, past_time, last_minute
    position = past_time = last_minute = 40

    playing_players['home_team'] = team_data[playing_teams['home_team']]['players'].copy()
    for player in playing_players['home_team']:
        player['energy'] = 100

    playing_players['away_team'] = team_data[playing_teams['away_team']]['players'].copy()
    for player in playing_players['away_team']:
        player['energy'] = 100

    game_time['minute'] = game_time['second'] = 0

    global last_time
    last_time = time.time()

    update_track()


def update_playing_teams():
    playing_teams['home_team'] = cbox_home_team.get()
    playing_teams['away_team'] = cbox_away_team.get()
    home_team_logo.config(image=team_logos[playing_teams['home_team']])
    away_team_logo.config(image=team_logos[playing_teams['away_team']])

def update_time():
    global last_time, past_time

    now = time.time()
    past_time += (now - last_time) * 0.25
    last_time = now
    game_time['minute'] = math.trunc(past_time)
    game_time['second'] = math.trunc(math.modf(past_time)[0] * 60)
    lb_timer.config(text=str(game_time['minute']) + ' : ' + str(game_time['second']))


def update_actions():
    pass


def update_track():
    blue_track = track_images['blue_track'].crop((0, 0, int(((position + 100) / 200) * 1278), 67))
    red_track = track_images['red_track'].crop((int(((position + 100) / 200) * 1278), 0, 1278, 67))
    full_track = Image.new('RGB', (1278, 67))
    full_track.paste(blue_track, (0, 0))
    full_track.paste(red_track, (blue_track.width, 0))
    track_images['full_track'] = ImageTk.PhotoImage(full_track)
    track.config(image=track_images['full_track'])

    if possession == 'home_team':
        sign.config(image=track_images['blue_sign'])
    else:
        sign.config(image=track_images['red_sign'])
    sign.place(x=11 + int(((position + 100) / 200) * 1367), y=63)


def main():
    global last_minute

    if state == 'main_menu':
        update_playing_teams()

    elif state == 'playing':
        update_time()
        if game_time['minute'] > last_minute:
            last_minute = game_time['minute']
            update_actions()
            update_track()


    root.after(1, main)


load_team_data()
load_track_images()
bind_button_commands()
root.after(1, main)
root.mainloop()
