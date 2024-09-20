import os
import threading
import speech_recognition as sr
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter

# Initialize recognizer and stopwords
recognizer = sr.Recognizer()
stop_words = set(stopwords.words('english'))

# Path to store the text file
text_file_path = "transcribed_text.txt"

def record_audio_chunk(chunk_index):
    with sr.Microphone() as source:
        print(f"Recording chunk {chunk_index}...")
        audio = recognizer.listen(source)
        
        try:
            # Convert audio to text
            text = recognizer.recognize_google(audio)
            print(f"Chunk {chunk_index} recognized: {text}")
            
            # Append the transcribed text to a file
            with open(text_file_path, "a") as file:
                file.write(text + " ")
            
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

def continuous_recording():
    chunk_index = 0
    while True:
        record_audio_chunk(chunk_index)
        chunk_index += 1

def process_transcribed_text(question_paper_text):
    # Read the transcribed text from the file
    with open(text_file_path, "r") as file:
        transcribed_text = file.read()
    
    # Tokenize and remove stopwords
    transcribed_words = [word for word in word_tokenize(transcribed_text.lower()) if word.isalnum() and word not in stop_words]
    question_words = [word for word in word_tokenize(question_paper_text.lower()) if word.isalnum() and word not in stop_words]
    
    # Count word frequencies
    transcribed_word_counts = Counter(transcribed_words)
    question_word_counts = Counter(question_words)
    
    # Find common words and their frequencies
    common_words = transcribed_word_counts & question_word_counts
    
    # Display the results
    print("Common words and frequencies:")
    for word, frequency in common_words.items():
        print(f"{word}: {frequency}")
    
def main():
    # Start the continuous recording in a separate thread
    recording_thread = threading.Thread(target=continuous_recording)
    recording_thread.daemon = True
    recording_thread.start()
    
    # Simulate the process running (e.g., for the duration of an exam)
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Recording stopped.")

    # After the recording is done, process the text
    question_paper_text = "Your question paper text here"  # Replace with actual question paper text
    process_transcribed_text(question_paper_text)

if __name__ == "__main__":
    main()
