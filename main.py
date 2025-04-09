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

configuration_name ='default'
team_data = None
team_logos = {'main_menu': {}, 'game': {}}
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

main_menu_home_team_logo = tk.Label(main_menu, bg='white', width=250, height=250)
main_menu_away_team_logo = tk.Label(main_menu, bg='white', width=250, height=250)

# Team Selection Dropdown

cbox_home_team = ttk.Combobox(main_menu, width=20, font=("Times New Roman", 12, "bold"), state="readonly")
cbox_away_team = ttk.Combobox(main_menu, width=20, font=("Times New Roman", 12, "bold"), state="readonly")

btn_start_game = tk.Button(main_menu, text='Start Game!', font=("Times New Roman", 20, "bold"), fg="red", bg="lightblue")

lb_heading1.grid(column=0, columnspan=3, row=0, pady=10)
lb_heading2.grid(column=0, columnspan=3, row=1, pady=10)
lb_heading3.grid(column=0, columnspan=3, row=2, pady=20)
lb_vs.grid(column=1, row=3)
main_menu_home_team_logo.grid(column=0, row=3, pady=20, padx=80)
main_menu_away_team_logo.grid(column=2, row=3, pady=20, padx=80)
cbox_home_team.grid(column=0, row=4, pady=40)
cbox_away_team.grid(column=2, row=4, pady=40)
btn_start_game.grid(column=1, row=4)


game_interface = tk.Frame(root, width=800, height=800)


lb_timer = tk.Label(game_interface, font=("Ariel", 25), fg="red")

game_home_team_logo = tk.Label(game_interface)
game_away_team_logo = tk.Label(game_interface)

lb_home_team_name = tk.Label(game_interface, font=('Times New Roman', 20), fg='red')
lb_away_team_name = tk.Label(game_interface, font=('Times New Roman', 20), fg='red')

lb_home_team_score = tk.Label(game_interface, font=("Ariel", 80), fg="red")
lb_away_team_score = tk.Label(game_interface, font=("Ariel", 80), fg="red")
lb_colon = tk.Label(game_interface, text=':', font=("Ariel", 60), fg="red")

track = tk.Label(game_interface)
sign = tk.Label(game_interface, border=0)

lb_timer.grid(column=3, row=0, pady=10)
game_home_team_logo.grid(column=1, row=1)
game_away_team_logo.grid(column=5, row=1)
lb_home_team_name.grid(column=1, row=2, pady=40)
lb_away_team_name.grid(column=5, row=2, pady=40)
lb_home_team_score.grid(column=2, row=1)
lb_away_team_score.grid(column=4, row=1)
lb_colon.grid(column=3, row=1)
track.grid(column=1, columnspan=5, row=3, padx=100, pady=30)


def bind_button_commands():
    btn_start_game.config(command=start_game)


def load_team_data():
    global team_data
    path = os.path.abspath('.\\configurations\\' + configuration_name + '.txt')
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
    state = 'playing'
    main_menu.destroy()
    game_interface.pack()
    initialise_game()


def initialise_game():
    score['home_team'] = score['away_team'] = game_time['minute'] = game_time['second'] = 0

    global position, past_time, last_minute, last_time
    position = past_time = last_minute = 0

    initialise_players()
    initialise_game_team_logos()
    initialise_game_team_names()
    update_score()
    update_track()

    last_time = time.time()


def initialise_players():
    playing_players['home_team'] = team_data[playing_teams['home_team']]['players'].copy()
    for player in playing_players['home_team'].values():
        player['energy'] = 100

    playing_players['away_team'] = team_data[playing_teams['away_team']]['players'].copy()
    for player in playing_players['away_team'].values():
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


def update_actions():
    print(last_minute)


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
    sign.place(x=11 + int(((position + 100) / 200) * 1367), y=400)


def update_score():
    lb_home_team_score.config(text=str(score['home_team']))
    lb_away_team_score.config(text=str(score['away_team']))



def end_game():
    global state
    state = 'game_ended'
    game_time['minute'] = 90
    game_time['second'] = 0


def main():
    global last_minute

    if state == 'main_menu':
        update_main_menu()

    elif state == 'playing':
        update_time()
        if game_time['minute'] > last_minute:
            last_minute = game_time['minute']
            update_actions()
            update_track()
            if last_minute>= 90:
                end_game()

    elif state == 'end_game':
        pass


    root.after(1, main)


load_team_data()
load_track_images()
bind_button_commands()
root.after(1, main)
root.mainloop()
