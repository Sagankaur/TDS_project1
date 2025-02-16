import sqlite3
import subprocess
from dateutil.parser import parse
from datetime import datetime
import json
from pathlib import Path
import os
import requests
from scipy.spatial.distance import cosine
from dotenv import load_dotenv
from dateutil.parser import parse
import re
load_dotenv()

AIPROXY_TOKEN = os.getenv('AIPROXY_TOKEN')

DATA_DIR = os.path.join(os.getcwd(), "data")
DATAGEN_URL = "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py"
DATAGEN_PATH = os.path.join(os.getcwd(), "datagen.py")
BASE_DIR = os.path.abspath(os.getcwd())

def download_datagen_script():
    try:
        # Ensure data directory exists
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)

        # Change the permissions to full access (777)
        os.chmod(DATA_DIR, 0o777)
        os.system(f"chmod -R 777 {DATA_DIR}")

        # Download datagen.py if it doesn't exist
        if not os.path.exists(DATAGEN_PATH):
            print(f"Downloading datagen.py from {DATAGEN_URL}...")
            response = requests.get(DATAGEN_URL)
            if response.status_code == 200:
                with open(DATAGEN_PATH, "w", encoding="utf-8") as f:
                    f.write(response.text)
                print("datagen.py downloaded successfully.")
            else:
                raise HTTPException(status_code=500, detail="Failed to download datagen.py")
        else:
            print("datagen.py already exists.")
    except Exception as e:
        print(f"Error: {e}")
import subprocess
from fastapi import HTTPException

def A1(email="xxxxxxxxx@ds.study.iitm.ac.in"):
    try:
        download_datagen_script()
        # Run the external script
        # process = subprocess.Popen(
        #     ["uv", "run", "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py", email],
        #     stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        # )
        process = subprocess.Popen(
            ["uv", "run", DATAGEN_PATH, email, "--root", DATA_DIR],  # Added --root argument
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        os.system(f"chmod -R 777 {DATA_DIR}/*")
        # chmod -R 777 data/*

        # Capture stdout and stderr from the script
        stdout, stderr = process.communicate()
        # Check if the process ran successfully
        if process.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Error: {stderr}")

        

        # Log stdout and stderr for debugging
        print("Standard Output:", stdout)
        print("Standard Error:", stderr)

        # Return the output
        return stdout

    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error: {e.stderr}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected Error: {str(e)}")

# A1()
def A2(prettier_version="prettier@3.4.2", filename="/data/format.md"):
    if filename.startswith("/"):
        filename = filename[1:]
    filename = os.path.abspath( filename) #os.path.join(BASE_DIR,   

    command = ["npx", prettier_version, "--write", filename]

    try:
        subprocess.run(command, check=True)
        print("Prettier executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

WEEKDAY_MAP = {
    "Sunday": 0, "रविवार": 0, "Sun": 0, "SUNDAY": 0,
    "Monday": 1, "सोमवार": 1, "Mon": 1, "MONDAY": 1,
    "Tuesday": 2, "मंगलवार": 2, "Tue": 2, "TUESDAY": 2,
    "Wednesday": 3, "बुधवार": 3, "Wed": 3, "WEDNESDAY": 3,
    "Thursday": 4, "गुरुवार": 4, "Thur": 4, "THURSDAY": 4, "Thu": 4,
    "Friday": 5, "शुक्रवार": 5, "Fri": 5, "FRIDAY": 5,
    "Saturday": 6, "शनिवार": 6, "Sat": 6, "SATURDAY": 6
}
REVERSE_WEEKDAY_MAP = {v: k for k, v in WEEKDAY_MAP.items() if k.istitle()}
def A3(filename='/data/dates.txt', targetfile=None, weekday=3):
    
    if filename.startswith("/"):
        filename = filename[1:]
    input_file = os.path.abspath(filename) 
    print(f"🔍 Checking input file: {input_file}")

    if isinstance(weekday, str):
        weekday = weekday.strip()
        weekday_number = WEEKDAY_MAP.get(weekday)
        if weekday_number is None:
            raise ValueError(f"Invalid weekday: {weekday}")
    elif isinstance(weekday, int) and 0 <= weekday <= 6:
        weekday_number = weekday
    else:
        raise ValueError("Weekday must be an integer (0-6) or a valid weekday name.")

    weekday_name = REVERSE_WEEKDAY_MAP[weekday_number]
    
    if targetfile is None:
        targetfile = os.path.join("/data", f"count-{weekday_name}.txt")
    if targetfile.startswith("/"):
        targetfile = targetfile[1:]
    targetfile = os.path.abspath(targetfile) 
    
    # os.makedirs(os.path.dirname(targetfile), exist_ok=True)  # Ensure directory exists

    weekday_count = 0
    
    date_str = line.strip()
    if not date_str:  # Ignore empty lines
        continue
    try:
        parsed_date = parse(date_str, fuzzy=True)  # Use fuzzy=True to handle minor format issues
        if parsed_date.weekday() == weekday_number:
            weekday_count += 1
    except Exception as e:
        print(f"❌ Skipping invalid date: {date_str} - {e}")

    with open(targetfile, 'w', encoding="utf-8") as file:
        file.write(str(weekday_count))

    print(f"✅ Counted {weekday_count} occurrences of {weekday} and saved to {targetfile}")

# A3()
def A4(filename="/data/contacts.json", targetfile="/data/contacts-sorted.json"):
    # Load the contacts from the JSON file
    if filename.startswith("/"):
            filename = filename[1:]
    input_file = os.path.abspath( filename) #os.path.join(BASE_DIR,

    with open(input_file, 'r') as file:
        contacts = json.load(file)

    # Sort the contacts by last_name and then by first_name
    sorted_contacts = sorted(contacts, key=lambda x: (x['last_name'], x['first_name']))
    output_filename = targetfile
    if output_filename.startswith("/"):
        output_filename = output_filename[1:]
    output_file = os.path.abspath(output_filename)
    
    # Write the sorted contacts to the new JSON file
    with open(output_file, 'w') as file:
        json.dump(sorted_contacts, file, indent=4)
# A4()import os

def A5(log_dir_path='/data/logs', output_file_path='/data/logs-recent.txt', num_files=10):
    # Convert log_dir_path to a Path object
    # log_dir = Path(log_dir_path).resolve()
    
    if log_dir_path.startswith("/"):
        log_dir_path = log_dir_path[1:]
    log_dir = os.path.abspath(log_dir_path)
    log_dir = Path(log_dir).resolve()
    # Ensure the log directory exists
    if not log_dir.exists():
        raise FileNotFoundError(f"Log directory does not exist: {log_dir}")

    # Get list of .log files sorted by modification time (most recent first)
    log_files = sorted(log_dir.glob('*.log'), key=lambda f: f.stat().st_mtime, reverse=True)[:num_files]
    
    if output_file_path.startswith("/"):
        output_file_path = output_file_path[1:]
    output_file = os.path.abspath(output_file_path)
    
    # Convert output file path to a Path object
    output_file = Path(output_file_path).resolve()

    # Ensure the parent directory for the output file exists
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Read the first line of each log file and write to the output file
    with output_file.open('w', encoding='utf-8') as f_out:
        for log_file in log_files:
            with log_file.open('r', encoding='utf-8') as f_in:
                first_line = f_in.readline().strip()
                f_out.write(f"{first_line}\n")

    print(f"✅ Successfully wrote first lines of {len(log_files)} log files to {output_file}")

#A5()

def A6(doc_dir_path='/data/docs', output_file_path='/data/docs/index.json'):
    # docs_dir = doc_dir_path
    output_filename = output_file_path
    index_data = {}

    if doc_dir_path.startswith("/"):
        doc_dir_path = doc_dir_path[1:]
    docs_dir = os.path.abspath(doc_dir_path)
    # Walk through all files in the docs directory
    for root, _, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md'):
                # print(file)
                file_path = os.path.join(root, file)
                # Read the file and find the first occurrence of an H1
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.startswith('# '):
                            # Extract the title text after '# '
                            title = line[2:].strip()
                            # Get the relative path without the prefix
                            relative_path = os.path.relpath(file_path, docs_dir).replace('\\', '/')
                            index_data[relative_path] = title
                            break  # Stop after the first H1
    # Write the index data to index.json
    # print(index_data)
    
    if output_filename.startswith("/"):
        output_filename = output_filename[1:]
    output_file = os.path.abspath(output_filename)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, indent=4)
# A6()
def A7(filename='/data/email.txt', output_filename='/data/email-sender.txt'):
    # Read the content of the email
    if filename.startswith("/"):
            filename = filename[1:]
    input_file = os.path.abspath(filename)
    
    # sender_email = None
    email_pattern = re.compile(r'[\w\.-]+@[\w\.-]+\.\w+')

    with open(input_file, 'r') as file:
        print(file.read())  
        for line in input_file:
            if line.lower().startswith("from"):
                matches = email_pattern.findall(line)
                if matches:
                    sender_email = matches[-1]  # Extract the last found email
                break  # Stop after finding the first occurrence

    # Get the extracted email address
    if output_filename.startswith("/"):
        output_filename = output_filename[1:]
    output_file = os.path.abspath(output_filename)

    # Write the email address to the output file
    with open(output_file, 'w') as file:
        file.write(sender_email)
    print(f"✅ Extracted sender email: {sender_email} and saved to {output_file}")
# A7()
import base64
def png_to_base64(image_path):
    output_filename = image_path
    # Get the extracted email address
    if output_filename.startswith("/"):
        output_filename = output_filename[1:]
    output_file = os.path.abspath(output_filename)

    with open(output_file, "rb") as image_file:
        base64_string = base64.b64encode(image_file.read()).decode('utf-8')
    return base64_string

# def A8():
#     input_image = "data/credit_card.png"
#     output_file = "data/credit-card.txt"

#     # Step 1: Extract text using OCR
#     try:
#         image = Image.open(input_image)
#         extracted_text = pytesseract.image_to_string(image)
#         print(f"Extracted text:\n{extracted_text}")
#     except Exception as e:
#         print(f"❌ Error reading or processing {input_image}: {e}")
#         return

#     # Step 2: Pass the extracted text to the LLM to validate and extract card number
#     prompt = f"""Extract the credit card number from the following text. Respond with only the card number, without spaces:

#     {extracted_text}
#     """
#     try:
#         card_number = ask_llm(prompt).strip()
#         print(f"Card number extracted by LLM: {card_number}")
#     except Exception as e:
#         print(f"❌ Error processing with LLM: {e}")
#         return

#     # Step 3: Save the extracted card number to a text file
#     try:
#         with open(output_file, "w", encoding="utf-8") as file:
#             file.write(card_number + "\n")
#         print(f"✅ Credit card number saved to: {output_file}")
#     except Exception as e:
#         print(f"❌ Error writing {output_file}: {e}")

def A8(filename='/data/credit_card.txt', image_path='/data/credit_card.png'):
    # Construct the request body for the AIProxy call
    body = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "There is 8 or more digit number is there in this image, with space after every 4 digit, only extract the those digit number without spaces and return just the number without any other characters"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{png_to_base64(image_path)}"
                        }
                    }
                ]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AIPROXY_TOKEN}"
    }

    # Make the request to the AIProxy service
    response = requests.post("http://aiproxy.sanand.workers.dev/openai/v1/chat/completions",
                             headers=headers, data=json.dumps(body))
    # response.raise_for_status()

    # Extract the credit card number from the response
    result = response.json()
    # print(result); return None
    card_number = result['choices'][0]['message']['content'].replace(" ", "")
    if filename.startswith("/"):
            filename = filename[1:]
    output_file = os.path.abspath( filename)

    # Write the extracted card number to the output file
    with open(output_file, 'w') as file:
        file.write(card_number)
# A8()


def get_embedding(text):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AIPROXY_TOKEN}"
    }
    data = {
        "model": "text-embedding-3-small",
        "input": [text]
    }
    response = requests.post("http://aiproxy.sanand.workers.dev/openai/v1/embeddings", headers=headers, data=json.dumps(data))
    response.raise_for_status()
    return response.json()["data"][0]["embedding"]

def A9(filename='/data/comments.txt', output_filename='/data/comments-similar.txt'):
    # Read comments
    if filename.startswith("/"):
        filename = filename[1:]
    input_file = os.path.abspath( filename)

    with open(input_file, 'r') as f:
        comments = [line.strip() for line in f.readlines()]

    # Get embeddings for all comments
    embeddings = [get_embedding(comment) for comment in comments]

    # Find the most similar pair
    min_distance = float('inf')
    most_similar = (None, None)

    for i in range(len(comments)):
        for j in range(i + 1, len(comments)):
            distance = cosine(embeddings[i], embeddings[j])
            if distance < min_distance:
                min_distance = distance
                most_similar = (comments[i], comments[j])
    if output_filename.startswith("/"):
            output_filename = output_filename[1:]
    output_file = os.path.abspath(output_filename)
    # Write the most similar pair to file
    with open(output_file, 'w') as f:
        f.write(most_similar[0] + '\n')
        f.write(most_similar[1] + '\n')
# A9()
def A10(filename='/data/ticket-sales.db', output_filename='/data/ticket-sales-gold.txt', query="SELECT SUM(units * price) FROM tickets WHERE type = 'Gold'"):
    # Connect to the SQLite database
    
    if filename.startswith("/"):
        filename = filename[1:]
    filename = os.path.abspath(filename)
    
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()

    # Calculate the total sales for the "Gold" ticket type
    cursor.execute(query)
    total_sales = cursor.fetchone()[0]

    # If there are no sales, set total_sales to 0
    total_sales = total_sales if total_sales else 0

    if output_filename.startswith("/"):
        output_filename = output_filename[1:]
    output_file = os.path.abspath(output_filename)
 
    # Write the total sales to the file
    with open(output_file, 'w') as file:
        file.write(str(total_sales))

    # Close the database connection
    conn.close()
# A10()