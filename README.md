# Football Events Tagger

Football Events Tagger is a Python-based application that allows users to visually tag football events on a field image. This tool is useful for coaches, analysts, and enthusiasts to record and analyze football events by tagging them with specific actions, players, and teams. The coordinates of these events are normalized and saved to a CSV file for further analysis.

## Features

- **Interactive Image Tagging**: Click on the image to record coordinates for football events.
- **Player and Action Selection**: Choose players and actions from pre-defined lists to tag events.
- **Configurable Teams and Actions**: Edit team names, player names, and actions via a configuration file.
- **Real-Time Coordinate Saving**: Save tagged events to a CSV file with normalized coordinates.
- **Config Editor**: Easily edit the configuration file for team names, player names, and actions.

## Installation


1. Clone the repository:
   ```sh
   git clone https://github.com/MrBubune/Football-Event-Tagger.git
   ```
2. Navigate to the project directory:
   ```sh
   cd Football-Event-Tagger
   ```
3. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

### Running the Application

To run the application, use the following command:
```sh
python football_events_tagger.py
```

### Tagging Events

1. **Load the Image**: The application will load the specified field image.
2. **Select a Player and Action**: Choose a player and an action from the buttons on the right.
3. **Click on the Image**: Click on two points on the image to record the start and end coordinates of the event.
4. **Save Coordinates**: The coordinates will be normalized and saved to the specified CSV file.
5. **Remove Last Entry**: If you made a mistake, use the "Remove Last" button to remove the last tagged event.

### Configuration

The configuration file (`config.json`) allows you to specify team names, player names, and actions. You can edit the configuration using the built-in config editor.

To open the config editor, click the "Edit Config" button in the application.

### Example Configuration (`config.json`)

```json
{
  "team_names": {
    "team1": "Team 1",
    "team2": "Team 2"
  },
  "team_one": ["Player 1", "Player 2", "Player 3"],
  "team_two": ["Player A", "Player B", "Player C"],
  "actions": ["Pass", "Shot", "Dribble", "Tackle", "Foul"]
}
```

## Use Cases

- **Coaches**: Analyze player movements and events during training or matches.
- **Analysts**: Record and review key events to improve team strategies.
- **Enthusiasts**: Tag and share notable events from favorite matches.


## Contributing

I'd love contributions from the community. If you have any suggestions or improvements, please create an issue or submit a pull request.

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes.
4. Push to your branch.
5. Create a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries or support, feel free to contact me through my [email](mailto:daryl.narh@gmail.com).

---

Thank you for using Football Events Tagger! We hope this tool helps you in analyzing and improving your football strategies.
