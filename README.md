# teams-msg-converter

This repository contains a Python script for converting `.msg` files (Microsoft Teams/Outlook message files) into grouped text files. The script processes batches of messages, grouping up to 100 messages into a single text file, making it easier to handle and analyze large volumes of email data.

## Features

- Converts `.msg` files into plain text.
- Groups messages into batches of up to 100 messages per text file.
- Includes metadata such as date, sender, and recipients in the output.
- Handles errors gracefully and skips problematic files.
- Displays progress using `tqdm` with batch-level granularity.

## Requirements

- Python 3.7 or higher
- Required Python libraries:
  - `os`
  - `extract_msg`
  - `tqdm`
  - `bs4` (BeautifulSoup)

You can install the required libraries using pip:

```bash
pip install extract-msg tqdm beautifulsoup4
```

## Usage

1. **Prepare Your Folders:**
   - Place all `.msg` files you want to convert into a source folder (e.g., `TeamsMessagesData`).
   - Create an output folder where the grouped text files will be saved (e.g., `Converted`).

2. **Run the Script:**
   Update the `source_folder` and `output_folder` variables in the script with the paths to your source and output folders.

   Run the script:

   ```bash
   python group_messages_conversion.py
   ```

3. **Output:**
   - The converted messages will be saved in the output folder.
   - Each file contains up to 100 messages, with metadata and message body included.

## Script Overview

- **`sanitize_filename(text):`** Cleans a string to make it safe for use as a filename.
- **`generate_unique_filename(base_name, index):`** Generates unique filenames for grouped message batches.
- **`convert_msg_to_txt(source_folder, output_folder, group_size=100):`** Main function that processes `.msg` files and saves them in grouped text files.

## Example Output

Each output file contains:

```
Date: 2024-12-30
Sender: sender@example.com
Recipients: recipient1@example.com, recipient2@example.com
Message:
This is the message body.

Date: 2024-12-30
Sender: another_sender@example.com
Recipients: recipient3@example.com
Message:
Another message body.

...
```

## Notes

- Default group size is 100 messages per file. You can adjust this by modifying the `group_size` parameter in the script.
- The script skips files that cannot be processed and logs the errors to the console.

## Contributing

Feel free to submit issues or pull requests to enhance the functionality or fix bugs.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
