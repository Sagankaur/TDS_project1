# Phase B: LLM-based Automation Agent for DataWorks Solutions

# B1 & B2: Security Checks
import os

# import csv d
# import sqlite3 
# import duckdb d
# import speech_recognition as sr d
# import markdown d
# import json d
# from fastapi import HTTPException d
# import requests
# from PIL import Image
# import ffmpeg d

def B12(filepath):
    # if filepath.startswith("/"):
    #     filepath = filepath[1:]
    # filepath_full = os.path.abspath(filepath)
    
    if filepath.startswith('/data'):
        # raise PermissionError("Access outside /data is not allowed.")
        return True
    else:
        return False
        print("Access outside /data is not allowed.")
    


# B3: Fetch Data from an API
def B3(url, save_path):
    import requests
    if not B12(save_path):
        return "outside DATA"
    
    response = requests.get(url)
    
    # Fix the variable name issue
    if save_path.startswith("/"):
        save_path = save_path[1:]
    
    full_save_path = os.path.abspath(save_path)
    
    with open(full_save_path, 'w') as file:
        file.write(response.text)
    
    print(f"✅ Data saved to {full_save_path}")

#B4: Clone a Git Repo and Make a Commit
def clone_git_repo(repo_url, commit_message):
    repo_path = "/data/repo"

    # Check if repo already exists
    if os.path.exists(repo_path):
        print("⚠️ Repo already exists at /data/repo. Skipping clone.")
    else:
        subprocess.run(["git", "clone", repo_url, repo_path])
    
    # Make a commit
    subprocess.run(["git", "-C", repo_path, "commit", "--allow-empty", "-m", commit_message])
    print(f"✅ Commit made with message: {commit_message}")

# B5: Run SQL Query
def B5(db_path, query, output_filename):
    import sqlite3
    if not B12(output_filename):
        return None
    
    if db_path.startswith("/"):
        db_path = db_path[1:]
    
    db_path = os.path.abspath(db_path)

    # Handle SQLite and DuckDB connections
    if db_path.endswith('.db'):
        conn = sqlite3.connect(db_path)
    else:
        conn = duckdb.connect(db_path)
    
    # Use conn.execute instead of cursor for DuckDB
    cur = conn.execute(query)
    result = cur.fetchall()
    conn.close()
    
    # Fix the file path handling
    if output_filename.startswith("/"):
        output_filename = output_filename[1:]
    
    output_file = os.path.abspath(output_filename)
    
    with open(output_file, 'w') as file:
        file.write(str(result))
    
    print(f"✅ Query results saved to {output_file}")
    return result

# B6: Web Scraping
def B6(url, output_filename):
    import requests
    result = requests.get(url).text
    
    if not B12(output_filename):
        return None
    
    if output_filename.startswith("/"):
        output_filename = output_filename[1:]
    output_file = os.path.abspath(output_filename)
    
    with open(output_file, 'w') as file:
        file.write(str(result))

# B7: Image Processing
def B7(image_path, output_path, resize=None):
    from PIL import Image
    if not B12(image_path):
        return None
    if image_path.startswith("/"):
        image_path = image_path[1:]
    image_path = os.path.abspath(image_path)
    
    if not B12(output_path):
        return None
    
    img = Image.open(image_path)
    if resize:
        img = img.resize(resize)
    
    if output_path.startswith("/"):
        output_path = output_path[1:]
    output_path_full = os.path.abspath(output_path)
    
    img.save(output_path_full)

# B8: Audio Transcription
# def B8(audio_path):
#     import openai
#     if not B12(audio_path):
#         return None
#     with open(audio_path, 'rb') as audio_file:
#         return openai.Audio.transcribe("whisper-1", audio_file)

# B9: Markdown to HTML Conversion
def B9(md_path, output_path):
    import markdown
    # if not B12(md_path):
    #     return None
    if not B12(output_path):
        return None
    if md_path.startswith("/"):
        md_path = md_path[1:]
    md_path_full = os.path.abspath(md_path)
    
    with open(md_path_full, 'r') as file:
        html = markdown.markdown(file.read())
        
    if output_path.startswith("/"):
        output_path = output_path[1:]
    output_path_full = os.path.abspath(output_path)
    
    with open(output_path_full, 'w') as file:
        file.write(html)

# B10: API Endpoint for CSV Filtering
# from flask import Flask, request, jsonify
# app = Flask(__name__)
# @app.route('/filter_csv', methods=['POST'])
# def filter_csv():
#     import pandas as pd
#     data = request.json
#     csv_path, filter_column, filter_value = data['csv_path'], data['filter_column'], data['filter_value']
#     B12(csv_path)
#     df = pd.read_csv(csv_path)
#     filtered = df[df[filter_column] == filter_value]
#     return jsonify(filtered.to_dict(orient='records'))
def transcribe_audio(mp3_file, output_path):
    """
    Transcribes an MP3 audio file to text.

    Args:
        mp3_file (str): The name of the MP3 file to transcribe.

    Returns:
        str: The transcribed text.

    Raises:
        HTTPException: If there are issues with transcription.
    """
    try:
        from fastapi import HTTPException
        # Validate and construct file paths
        if B12(output_path):
            import speech_recognition as sr
            import ffmpeg
            
            if mp3_file.startswith("/"):
                mp3_file = mp3_file[1:]
            input_path = os.path.abspath(mp3_file)
            
            # Ensure paths are safe
            if not os.path.exists(input_path):
                raise HTTPException(status_code=400, detail="MP3 file not found.")

            # Convert MP3 to WAV using ffmpeg-python
            wav_file = input_path.replace(".mp3", ".wav")
            ffmpeg.input(input_path).output(wav_file, format="wav").run()

            # Transcribe WAV using SpeechRecognition
            recognizer = sr.Recognizer()
            with sr.AudioFile(wav_file) as source:
                audio_data = recognizer.record(source)
                transcription = recognizer.recognize_google(audio_data)
           
            if output_path.startswith("/"):
                output_path = output_path[1:]
            output_path_full = os.path.abspath(output_path)
            
            with open(output_path_full, "w") as f:
                f.write(transcription)

            return f"Transcription of {input_path} saved successfully to {output_path}."
        else:
            return ("Path outside DATA dir")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error transcribing audio: {str(e)}")  


def filter_csv_to_json(csv_file, filter_column, filter_value, output_path):
    """
    Filters a CSV file based on a column value and returns JSON data.

    Args:
        csv_file (str): The name of the CSV file to filter.
        filter_column (str): The column name to filter by.
        filter_value (str): The value to match in the column.

    Returns:
        list: A list of dictionaries representing filtered rows.

    Raises:
        HTTPException: If there are issues with filtering or reading the file.
    """
    try:
        import csv
        from fastapi import HTTPException
        import json
        # Validate and construct file paths
        if B12(output_path) and B12(csv_file):
            if csv_file.startswith("/"):
                csv_file = csv_file[1:]
            input_path = os.path.abspath(csv_file)
            
        # Read and filter CSV data
            filtered_rows = []
            with open(input_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get(filter_column) == filter_value:
                        filtered_rows.append(row)

            return filtered_rows
        else:
            return ("path outside DATA")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error filtering CSV data: {str(e)}")

#TESTING

# import os
# import sqlite3
# import csv
# from os.path import join
# import ffmpeg

# db_path = join(os.getcwd(), 'data/mydatabase.db')
# csv_path = join(os.getcwd(),'data/example.csv')
# md_path = join(os.getcwd(),'data/example.md')
# mp3_path = join(os.getcwd(),'data/audio_sample.mp3')
# image_path = join(os.getcwd(),'data/input_image.jpg')
# # Create SQLite database and table
# conn = sqlite3.connect(db_path)
# cur = conn.cursor()
# cur.execute('''CREATE TABLE IF NOT EXISTS my_table (id INTEGER PRIMARY KEY, name TEXT, status TEXT)''')
# cur.executemany('INSERT INTO my_table (name, status) VALUES (?, ?)', [
#     ('Alice', 'active'),
#     ('Bob', 'inactive'),
#     ('Charlie', 'active'),
#     ('Dave', 'inactive'),
# ])
# conn.commit()
# conn.close()

# # Create CSV file
# with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(['id', 'name', 'status'])
#     writer.writerow([1, 'Alice', 'active'])
#     writer.writerow([2, 'Bob', 'inactive'])
#     writer.writerow([3, 'Charlie', 'active'])
#     writer.writerow([4, 'Dave', 'inactive'])

# # Create Markdown file
# with open(md_path, 'w', encoding='utf-8') as mdfile:
#     mdfile.write("# Example Markdown\n\nThis is a sample markdown file.\n\n- Item 1\n- Item 2\n")

# # Create placeholder MP3 file (empty for now)
# with open(mp3_path, 'wb') as mp3file:
#     mp3file.write(b'\x00')

# # # Create placeholder image file (empty for now)
# # with open(image_path, 'wb') as imgfile:
# #     imgfile.write(b'\x00')
# from PIL import Image
# img = Image.new('RGB', (200, 200), color=(255, 0, 0))  # Red 200x200 image
# img.save(image_path)

# # Return paths to verify
# print(db_path, csv_path, md_path, mp3_path, image_path)

# print(B12("/data/myfile.txt"))  # Expected: True (inside /data)  
# print(B12("/etc/passwd"))       # Expected: False (outside /data)  
# print(B12("myfile.txt"))        # Expected: False (relative path, not /data)  
# B3("https://jsonplaceholder.typicode.com/todos/1", "/data/todo.json")  
# # Expected: File saved in /data/todo.json with JSON content.

# B3("https://jsonplaceholder.typicode.com/todos/1", "/etc/todo.json")  
# # Expected: "outside DATA" (since save_path isn’t in /data).

# # clone_git_repo("https://github.com/octocat/Hello-World.git", "Initial commit")  
# # # Expected: Clones the repo to /data/repo and makes a commit with the message.

# B5("/data/mydatabase.db", "SELECT * FROM my_table;", "/data/query_result.txt")  
# # Expected: File saved with query result.

# B5("/data/mydatabase.db", "SELECT * FROM my_table;", "/etc/query_result.txt")  
# # Expected: None (since output filename is outside /data).

# B6("https://jsonplaceholder.typicode.com/todos/1", "/data/todo.json")
# # Expected: File saved at /data/todo.json with JSON content.
# # If the output filename isn’t inside /data, it should return None.
# B7("/data/input_image.jpg", "/data/output_image.jpg", resize=(100, 100))
# # Expected: Resized image saved to /data/output_image.jpg.
# B9("/data/example.md", "/data/example.html")
# # Expected: Markdown from example.md converted to HTML and saved to /data/example.html.
# # If paths are outside /data, it should return None.
# # If output path is not in /data, it should return None.
# filter_csv_to_json("/data/example.csv", "status", "active", "/data/filtered_data.json")
# ffmpeg.input('anullsrc=r=44100:cl=stereo', f='lavfi').output(mp3_path, t=5).run()
# print(f"Silent audio created at: {mp3_path}")
# transcribe_audio("/data/audio_sample.mp3", "/data/transcription.txt")
# # clone_git_repo("https://github.com/octocat/Hello-World.git", "Initial commit")  
