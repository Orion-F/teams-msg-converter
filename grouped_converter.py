import os
import extract_msg
from tqdm import tqdm
from datetime import datetime
from bs4 import BeautifulSoup

def sanitize_filename(text):
    file_name = "".join(c for c in text if c.isalnum() or c in (' ', '-', '_')).strip()
    return file_name + ".txt"

def generate_unique_filename(base_name, index):
    return f"{base_name}_{index:04d}.txt"

def convert_msg_to_txt(source_folder, output_folder, group_size=100):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Collect all .msg files
    msg_files = [
        os.path.join(root, file)
        for root, _, files in os.walk(source_folder)
        for file in files if file.lower().endswith(".msg")
    ]

    total_batches = (len(msg_files) + group_size - 1) // group_size
    grouped_messages = []
    group_index = 1

    # Process files in batches
    for batch_start in tqdm(range(0, len(msg_files), group_size), desc="Processing batches", unit="batch", total=total_batches):
        current_group = []
        batch_files = msg_files[batch_start:batch_start + group_size]

        for file_path in batch_files:
            try:
                with extract_msg.openMsg(file_path) as msg:
                    msg_date = msg.date or "Unknown Date"
                    html_body = msg.htmlBody or "No Body"
                    text_body = BeautifulSoup(html_body, "html.parser").get_text()

                    current_group.append(f"Date: {msg_date}\n")
                    current_group.append(f"Sender: {msg.sender or 'Unknown'}\n")
                    current_group.append(f"Recipients: {msg.to or 'Unknown'}\n")
                    current_group.append(f"Message:\n{text_body}\n\n")

            except Exception as e:
                print(f"Failed to convert {file_path}: {e}")

        # Save current batch to file
        base_name = "GroupedMessages"
        output_file_path = os.path.join(output_folder, generate_unique_filename(base_name, group_index))
        with open(output_file_path, "w", encoding="utf-8") as txt_file:
            txt_file.writelines(current_group)

        group_index += 1

if __name__ == "__main__":
    source_folder = r"TeamsMessagesData"
    output_folder = r"Converted"
    convert_msg_to_txt(source_folder, output_folder)