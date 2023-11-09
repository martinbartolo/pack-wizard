# Pack Wizard

Pack Wizard is a Python tool that sends random beat packs via email. It selects a specified number of mp3 files randomly from a directory and sends them to an email address.

## Instructions

1. Install Requirements: `pip install python-dotenv`
2. Setup .env:<br/>
   EMAIL_ADDRESS=<your-email@gmail.com><br/>
   PASSWORD=password <br/>
   (NOTE: password must be an app password. See <https://support.google.com/mail/answer/185833?hl=en>)
3. Run: `python main.py <arguments>`

## Arguments

- **--email_address or -e**: Email address to send beats to (required)
- **--directory or -d**: Folder to choose mp3 files from (defaults to cwd)
- **--num_files or -n**: Number of beats to send (defaults to 5)
