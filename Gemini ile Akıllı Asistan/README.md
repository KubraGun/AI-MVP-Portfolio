# Smart Assistant with Gemini

This project is a command-line smart assistant that helps you manage notes and events through natural language. It uses Google's Gemini AI to understand your requests and a local SQLite database to store your information.

## What It Does
The assistant lets you:

Add and view notes

Add and view calendar events

Chat naturally with the AI

Get summaries of your notes or events

Ask questions about your stored information

When you chat with the assistant, it automatically detects whether you're asking for note summaries, event summaries, or just having a regular conversation.

## How It Works
The system consists of three main components:

### Assistant (assistant.py)

Communicates with Google's Gemini AI API

Detects what kind of request you're making (notes, events, or general chat)

Processes natural language queries

### Database (database.py)

Stores your notes and events in a SQLite database

Handles adding and retrieving information

Automatically creates the database file when you first run the application

### Main Application (main.py)

Provides the user interface

Coordinates between the AI assistant and database

Processes your commands

## Setup Instructions
Install required packages:

```bash
pip install requests python-dotenv
```
Get a Gemini API key:

Visit https://aistudio.google.com/app/apikey

Create a new API key

Create a .env file in the project directory and add:

```text
GEMINI_API_KEY=your_api_key_here
```
Run the application:

```bash
python main.py
```
## How to Use
When you start the application, you'll see these available commands:

not ekle - Add a new note

etkinlik ekle - Add a new event

notları göster - Show all notes

etkinlikleri göster - Show all events

sohbet et - Chat with the AI assistant

çıkış - Exit the application

### Examples of Natural Language Queries
In chat mode, you can ask things like:

"What notes do I have?" (Automatically detects you want note summaries)

"Tell me about my upcoming events" (Automatically detects you want event summaries)

"What's the weather like?" (General conversation)

"Summarize my notes from last week"

The AI will understand your intent and provide appropriate responses, whether you need information from your database or just want to have a conversation.

## Technical Details
Uses Google Gemini 2.0 Flash model for AI responses

SQLite database stored in data/assistant.db

Automatic intent detection for note and event queries

Error handling for API issues and database operations

The application creates the database and necessary tables automatically when first run, so no manual setup is required.