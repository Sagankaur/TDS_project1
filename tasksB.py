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
    if not B12(save_path):
        return ("outside DATA")
    import requests
    response = requests.get(url)

    if save_path.startswith("/"):
        save_path = output_filename[1:]
    full_save_path = os.path.abspath(save_path)
    
    with open(full_save_path, 'w') as file:
        file.write(response.text)

#B4: Clone a Git Repo and Make a Commit
def clone_git_repo(repo_url, commit_message):
    import subprocess
    subprocess.run(["git", "clone", repo_url, "/data/repo"])
    subprocess.run(["git", "-C", "/data/repo", "commit", "-m", commit_message])

# B5: Run SQL Query
def B5(db_path, query, output_filename):
    if not B12(output_filename):
        return None
    import sqlite3, duckdb
    if db_path.startswith("/"):
        db_path = db_path[1:]
    db_path = os.path.abspath(db_path)
    
    conn = sqlite3.connect(db_path) if db_path.endswith('.db') else duckdb.connect(db_path)
    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchall()
    conn.close()

    if output_filename.startswith("/"):
        output_filename = output_filename[1:]
    output_file = os.path.abspath(output_filename)
    
    with open(output_file, 'w') as file:
        file.write(str(result))
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
    # if not B12(image_path):
    #     return None
    if not B12(output_path):
        return None
    
    img = Image.open(image_path)
    if resize:
        img = img.resize(resize)
    
    if output_path.startswith("/"):
        output_path = output_filename[1:]
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
        output_path = output_filename[1:]
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
                output_path = output_filename[1:]
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
        if B12(output_path) :
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
