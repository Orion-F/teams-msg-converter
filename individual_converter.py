import os
import extract_msg
from tqdm import tqdm
from datetime import datetime
from bs4 import BeautifulSoup

def sanitize_filename(text):
    file_name = "".join(c for c in text if c.isalnum() or c in (' ', '-', '_')).strip()
    return file_name + ".txt"

def generate_unique_filename(msg_date, uid):
    # Use the date and UID for a unique and meaningful filename
    formatted_date_str = msg_date.strftime("%Y-%m-%d_%H-%M-%S")
    return f"{formatted_date_str}_{uid}"

def convert_msg_to_txt(source_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Collect all .msg files
    msg_files = [
        os.path.join(root, file)
        for root, _, files in os.walk(source_folder)
        for file in files if file.lower().endswith(".msg")
    ]

    # Iterate through files with tqdm for progress bar
    for idx, file_path in enumerate(tqdm(msg_files, desc="Converting .msg files", unit="file")):
        try:
            with extract_msg.openMsg(file_path) as msg:
                msg = extract_msg.Message(file_path)
                msg_date = msg.date or "Unknown Date"
                uid = idx + 1
                html_body = msg.htmlBody or "No Body"
                text_body = BeautifulSoup(html_body, "html.parser").get_text()

                # Generate a unique filename
                unique_filename = generate_unique_filename(msg_date, uid)
                output_file_path = os.path.join(output_folder, sanitize_filename(unique_filename))

                with open(output_file_path, "w", encoding="utf-8") as txt_file:
                    txt_file.write(f"Date: {msg_date}\n")
                    txt_file.write(f"Sender: {msg.sender or 'Unknown'}\n")
                    txt_file.write(f"Recipients: {msg.to or 'Unknown'}\n")
                    txt_file.write(f"Message:\n{text_body}\n")
        except Exception as e:
            print(f"Failed to convert {file_path}: {e}")


if __name__ == "__main__":
    source_folder = r"TeamsMessagesData"
    output_folder = r"Converted"
    convert_msg_to_txt(source_folder, output_folder)
