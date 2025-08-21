import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import pandas as pd
import os
import json
import tkinter as tk

class CoordinateRecorder:
    def __init__(self, image_path, csv_path, config_path):
        self.image_path = image_path
        self.csv_path = csv_path
        self.config_path = config_path
        self.coords = []
        self.plotted_points = []
        self.action = None
        self.team = None
        self.player = None
        self.img = plt.imread(image_path)

        self.load_config()

        self.fig, self.ax = plt.subplots()
        plt.subplots_adjust(left=0.05, right=0.75, bottom=0.2, top=0.9)

        self.ax.imshow(self.img)
        self.ax.axis('off')

        self.cid = self.fig.canvas.mpl_connect('button_press_event', self.onclick)

        self.add_buttons()

        # Utility buttons
        ax_config_button = plt.axes((0.75, 0.02, 0.18, 0.04))
        config_button = Button(ax_config_button, 'Edit Config')
        config_button.on_clicked(self.open_config_editor)

        ax_open_folder_button = plt.axes((0.75, 0.08, 0.18, 0.04))
        open_folder_button = Button(ax_open_folder_button, 'Open CSV Folder')
        open_folder_button.on_clicked(self.open_csv_folder)

        ax_open_file_button = plt.axes((0.75, 0.14, 0.18, 0.04))
        open_file_button = Button(ax_open_file_button, 'Open CSV File')
        open_file_button.on_clicked(self.open_csv_file)

        ax_remove_last_button = plt.axes((0.75, 0.20, 0.18, 0.04))
        remove_last_button = Button(ax_remove_last_button, 'Remove Last Tag')
        remove_last_button.on_clicked(self.remove_last_entry)

        plt.show()

    def load_config(self):
        with open(self.config_path, 'r') as f:
            self.config = json.load(f)

    def add_buttons(self):
        self.buttons = []

        # Add team labels
        team1, team2 = self.config["teams"]
        self.team1_label = self.fig.text(0.78, 0.95, team1, ha='center', va='center', fontsize=12, weight='bold')
        self.team2_label = self.fig.text(0.88, 0.95, team2, ha='center', va='center', fontsize=12, weight='bold')

        # Player buttons for team1
        for i, player in enumerate(self.config["players"][team1]):
            ax_button = plt.axes((0.75, 0.9 - i * 0.05, 0.08, 0.04))
            button = Button(ax_button, player)
            button.on_clicked(lambda event, t=team1, p=player: self.set_player(t, p))
            self.buttons.append(button)

        # Player buttons for team2
        for i, player in enumerate(self.config["players"][team2]):
            ax_button = plt.axes((0.85, 0.9 - i * 0.05, 0.08, 0.04))
            button = Button(ax_button, player)
            button.on_clicked(lambda event, t=team2, p=player: self.set_player(t, p))
            self.buttons.append(button)

        # Action buttons (split into two rows)
        button_positions_row1 = [0.1, 0.22, 0.34, 0.46, 0.58]
        button_positions_row2 = [0.1, 0.22, 0.34, 0.46, 0.58]

        for i, action in enumerate(self.config["actions"][:5]):
            ax_button = plt.axes((button_positions_row1[i], 0.1, 0.1, 0.075))
            button = Button(ax_button, action)
            button.on_clicked(lambda event, a=action: self.set_action(a))
            self.buttons.append(button)

        for i, action in enumerate(self.config["actions"][5:]):
            ax_button = plt.axes((button_positions_row2[i], 0.02, 0.1, 0.075))
            button = Button(ax_button, action)
            button.on_clicked(lambda event, a=action: self.set_action(a))
            self.buttons.append(button)

    def set_player(self, team, player):
        self.team = team
        self.player = player

    def set_action(self, action):
        self.action = action

    def onclick(self, event):
        if event.inaxes == self.ax and event.xdata is not None and event.ydata is not None and self.action and self.team and self.player:
            self.coords.append((event.xdata, event.ydata))
            point, = self.ax.plot(event.xdata, event.ydata, 'ro')
            self.plotted_points.append(point)
            plt.draw()
            if len(self.coords) == 2:
                self.save_coordinates()
                self.clear_points()

    def save_coordinates(self):
        start_x, start_y = self.coords[0]
        end_x, end_y = self.coords[1]

        start_x = int((start_x / self.img.shape[1]) * 100)
        start_y = int((start_y / self.img.shape[0]) * 100)
        end_x = int((end_x / self.img.shape[1]) * 100)
        end_y = int((end_y / self.img.shape[0]) * 100)

        df = pd.DataFrame([{
            'team': self.team,
            'player': self.player,
            'action': self.action,
            'start_x': start_x,
            'start_y': start_y,
            'end_x': end_x,
            'end_y': end_y
        }])

        file_exists = os.path.isfile(self.csv_path)
        df.to_csv(self.csv_path, mode='a', header=not file_exists, index=False)

        print(f"Saved: {self.team}, {self.player}, {self.action}")

    def clear_points(self):
        for point in self.plotted_points:
            point.remove()
        self.plotted_points.clear()
        self.coords.clear()
        plt.draw()

    def remove_last_entry(self, event):
        if self.plotted_points:
            point = self.plotted_points.pop()
            point.remove()
            self.coords.pop()
            plt.draw()
        else:
            print("No points to remove.")

    def clear_buttons(self):
        for button in self.buttons:
            button.ax.clear()
            button.ax.set_visible(False)
        self.buttons.clear()
        self.team1_label.set_visible(False)
        self.team2_label.set_visible(False)

    def open_config_editor(self, event):
        ConfigEditor(self.config_path, self)

    def open_csv_folder(self, event):
        folder_path = os.path.dirname(self.csv_path)
        os.startfile(folder_path)

    def open_csv_file(self, event):
        os.startfile(self.csv_path)

    def refresh_ui(self):
        self.clear_buttons()
        self.load_config()
        self.add_buttons()


class ConfigEditor:
    def __init__(self, config_path, parent):
        self.config_path = config_path
        self.parent = parent

        self.root = tk.Tk()
        self.root.title("Config Editor")

        self.load_config()

        tk.Label(self.root, text="Team 1 Name").grid(row=0, column=0)
        tk.Label(self.root, text="Team 2 Name").grid(row=0, column=1)
        tk.Label(self.root, text="Actions").grid(row=0, column=2)

        self.team1_name_entry = tk.Entry(self.root)
        self.team1_name_entry.grid(row=1, column=0)
        self.team1_name_entry.insert(0, self.config["teams"][0])

        self.team2_name_entry = tk.Entry(self.root)
        self.team2_name_entry.grid(row=1, column=1)
        self.team2_name_entry.insert(0, self.config["teams"][1])

        # Players + Actions
        tk.Label(self.root, text="Team 1 Players").grid(row=2, column=0)
        tk.Label(self.root, text="Team 2 Players").grid(row=2, column=1)

        self.team_one_entries = [tk.Entry(self.root) for _ in self.config["players"][self.config["teams"][0]]]
        self.team_two_entries = [tk.Entry(self.root) for _ in self.config["players"][self.config["teams"][1]]]
        self.action_entries = [tk.Entry(self.root) for _ in self.config["actions"]]

        for i, entry in enumerate(self.team_one_entries):
            entry.grid(row=i + 3, column=0)
            entry.insert(0, self.config["players"][self.config["teams"][0]][i])

        for i, entry in enumerate(self.team_two_entries):
            entry.grid(row=i + 3, column=1)
            entry.insert(0, self.config["players"][self.config["teams"][1]][i])

        for i, entry in enumerate(self.action_entries):
            entry.grid(row=i + 3, column=2)
            entry.insert(0, self.config["actions"][i])

        tk.Button(self.root, text="Save", command=self.save_config).grid(
            row=max(len(self.team_one_entries), len(self.team_two_entries), len(self.action_entries)) + 4,
            column=0, columnspan=3
        )

        self.root.mainloop()

    def load_config(self):
        with open(self.config_path, 'r') as f:
            self.config = json.load(f)

    def save_config(self):
        new_config = {
            "teams": [self.team1_name_entry.get(), self.team2_name_entry.get()],
            "players": {
                self.team1_name_entry.get(): [entry.get() for entry in self.team_one_entries],
                self.team2_name_entry.get(): [entry.get() for entry in self.team_two_entries]
            },
            "actions": [entry.get() for entry in self.action_entries]
        }

        with open(self.config_path, 'w') as f:
            json.dump(new_config, f, indent=4)

        self.parent.refresh_ui()
        self.root.destroy()


# Example usage
base_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(base_dir, "field.png")
csv_path = os.path.join(base_dir, "events.csv")
config_path = os.path.join(base_dir, "config.json")

recorder = CoordinateRecorder(image_path, csv_path, config_path)
