
from google import genai


def generate_notes(transcript, api_key):

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are an expert university study assistant.

Convert the following lecture transcript into
clear, detailed and exam-ready English notes.

Follow this structure:

# Lecture Notes

## 1. Main Topics
List the important topics discussed.

## 2. Detailed Explanations
Explain each topic in simple English.
Use headings and subheadings.

## 3. Important Definitions
Include important definitions.

## 4. Examples
Include examples mentioned in the lecture.

## 5. Key Points
List the most important points.

## 6. Summary
Give a short summary of the lecture.

## 7. Revision Questions
Create 5 important questions with answers.

IMPORTANT RULES:
- Use simple and clear English.
- Do not invent information.
- Do not add unrelated topics.
- If something is unclear in the transcript,
  mention that it is unclear.
- Preserve important technical terms.
- Make notes useful for university exams.

LECTURE TRANSCRIPT:
{transcript}
"""

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )

    if not response.text:
        raise ValueError("AI could not generate notes.")

    return response.text
