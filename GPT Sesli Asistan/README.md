# GPT Voice Chat
## Project Description
This is a Python program for a voice-based chatbot. You can talk to the GPT-3.5 Turbo model using your microphone. The program records your voice, converts it to text, gets a response from the AI, and shows you the answer.

## How It Works
The program follows these steps:

Record Audio: It records your voice from the microphone for a set time (5 seconds by default).

Speech to Text: It uses the OpenAI Whisper model to convert the audio file into text.

Content Filtering: It checks the transcribed text for any banned words.

Get AI Response: It sends the filtered text to the OpenAI GPT-3.5 Turbo model to generate an answer.

Logging: It logs all steps and the conversation to a file and the console.

Cleanup: It deletes the temporary audio file after processing.

## Technologies Used
OpenAI API: For speech-to-text (Whisper-1) and text generation (GPT-3.5 Turbo).

SoundDevice & SciPy: For recording audio from the microphone and saving it as a WAV file.

Python-dotenv: For managing the OpenAI API key securely.

Logging Module: For keeping a detailed record of the program's activity.

Regular Expressions (Re): For simple, rule-based filtering of unwanted words.


## Setup Instructions
### 1. Install the required libraries:

Before running the script, you need to install the necessary packages. You can do this using pip:

```bash
pip install openai python-dotenv sounddevice scipy
```

### 2. Set up your OpenAI API Key:

Get an API key from OpenAI.

Create a file named .env in the same folder as the Python script.

Add your API key to this file like this:

OPENAI_API_KEY="your-api-key-here"

## How to Run the Program
Make sure you have completed the setup steps.

Run the Python script from your terminal or command prompt:

```bash
python gpt_voice_chat.py
```
When the program starts, it will begin recording audio immediately. Speak your question clearly.

After 5 seconds, it will process your speech and print the AI's response in the console.

The program will then finish. (To have a continuous conversation, you can uncomment the while True: loop in the code).

## Important Notes
Security: The program includes a basic word filter. You can add words to the BANNED_WORDS list in the script to filter them out.

Logs: The program creates a logs/ folder and saves a detailed log file for every session. This is useful for checking errors or reviewing the conversation.

Current Mode: The code is set up for a single question/answer interaction. For a continuous chat, you need to uncomment the main while True: loop and comment out or remove the single test section at the bottom.

Performance: The program uses OpenAI's servers, so you need an internet connection. The speed of the response depends on your connection and OpenAI's API performance.