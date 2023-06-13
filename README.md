# Telegram Username Checker

The Telegram Username Checker is a Python script that allows you to check the validity of Telegram usernames. It automates the process of checking whether a username is available or already taken on Telegram.

## Features

- Validates Telegram usernames by checking the corresponding user profile page.
- Uses XPath to identify the presence of a specific HTML element indicating a valid username.
- Saves the list of valid usernames to a separate file for further analysis or use.
- Displays a progress bar in the terminal console to provide real-time feedback on the checking process.

## Usage

1. Prepare a list of usernames to check by adding them to a file (e.g., `list.txt`), with each username on a separate line.
2. Update the script to set the correct file paths for the input list and the output file where valid usernames will be saved.
3. Go to the folder on the terminal: `cd Telegram-Username-Checker`.
4. To run a script, you need to install the necessary dependencies or requirements. The command:  `pip install -r requirements.txt`.
5. Run the script using Python: `python main.py`.
6. The script will check each username in the list, display a progress bar, and print the valid usernames.
7. The valid usernames will also be saved to the specified output file (e.g., `valid.txt`).

## Dependencies

The script relies on the following Python libraries:

- `requests` - For making HTTP requests to the Telegram website.
- `lxml` - For parsing HTML content and extracting information using XPath.
- `tqdm` - For creating the progress bar and displaying real-time progress in the terminal.

Make sure to install these dependencies using `pip` before running the script.

## Contribution

Contributions to the Telegram Username Checker are welcome! If you encounter any issues, have ideas for improvements, or would like to add new features, please open an issue or submit a pull request.

## Disclaimer

Please note that this tool is intended for educational and research purposes only. Use it responsibly and respect Telegram's terms of service. The tool does not make any changes to the Telegram service; it simply provides an automated way to check username availability.
