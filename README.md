# Smart Lecture Notes

Smart Lecture Notes is an AI-powered application that converts university lecture recordings into structured and exam-ready study notes.

It helps students save time, understand important concepts, and prepare for exams more easily.

## Features

- Upload university lecture audio.
- Convert speech into text using Whisper AI.
- Generate exam-ready notes using Gemini AI.
- Get explanations, definitions, and key points.
- Generate summaries and revision questions.
- Edit and download notes.
- Save and access previous lectures.
- Reduce background noise before transcription.

## Technologies Used

- Python
- Streamlit
- Faster-Whisper
- Google Gemini API
- SQLite
- FFmpeg
- Python-dotenv

## Installation

1. Clone the repository:

   git clone https://github.com/yusrafatima12/smart-lecture-notes.git

2. Open the project folder:

   cd smart-lecture-notes

3. Create a virtual environment:

   python -m venv env

4. Activate the environment:

   env\Scripts\activate

5. Install the required packages:

   pip install -r requirements.txt

## API Configuration

Create a `.env` file in the project folder and add your Gemini API key:

GEMINI_API_KEY=your_api_key_here

Replace `your_api_key_here` with your own API key.

## Audio Processing Requirement

FFmpeg must be installed on your system for audio processing and noise reduction.

## Run the Application

Start the application using:

streamlit run app.py

## Developer

**Yusra Fatima**

GitHub: [yusrafatima12](https://github.com/yusrafatima12)

