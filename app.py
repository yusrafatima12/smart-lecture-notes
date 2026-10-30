
import os
import tempfile

import streamlit as st
from dotenv import load_dotenv
from faster_whisper import WhisperModel
from google import genai
from google.genai import errors


# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="MY SMART NOTES",
    page_icon="📚",
    layout="centered"
)

st.title("📚 MY SMART NOTES")
st.write("Turn your lecture audio into clear, exam-ready notes.")


# Load Whisper model only once
@st.cache_resource
def load_model():
    return WhisperModel(
        "small",
        device="cpu",
        compute_type="int8"
    )


# Upload audio
audio_file = st.file_uploader(
    "Upload your lecture audio",
    type=["mp3", "wav", "m4a", "ogg", "aac", "acc"]
)


if audio_file:

    st.audio(audio_file)

    if st.button("GENERATE MY NOTES", type="primary"):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            st.error("GEMINI_API_KEY missing. Check your .env file.")
            st.stop()

        temp_path = None

        try:

            # Save uploaded audio temporarily
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=os.path.splitext(audio_file.name)[1]
            ) as temp_audio:

                temp_audio.write(audio_file.getbuffer())
                temp_path = temp_audio.name


            # Step 1: Audio transcription
            with st.spinner("Step 1/2: Understanding your lecture audio..."):

                model = load_model()

                segments, info = model.transcribe(
                    temp_path,
                    language=None,
                    beam_size=5,
                    condition_on_previous_text=False,
                    vad_filter=True
                )

                transcript = " ".join(
                    segment.text.strip()
                    for segment in segments
                ).strip()


            # Check transcription
            if not transcript or len(transcript.split()) < 5:

                st.warning(
                    "Not enough clear speech was detected. "
                    "Please upload a longer or clearer recording."
                )
                st.stop()


            # Step 2: Generate notes
            with st.spinner("Step 2/2: Creating your study notes..."):

                client = genai.Client(api_key=api_key)

                response = client.models.generate_content(
                    model="gemini-3.8-flash",

                    contents=f"""
You are an expert university study-notes assistant.

Your task is to create useful and accurate study notes
from the lecture text provided below.

IMPORTANT RULES:

1. Write all notes in simple, clear English.
2. Organize notes using headings and subheadings.
3. Explain important concepts and definitions.
4. Include examples when supported by the lecture.
5. Highlight important exam points.
6. Add a short summary.
7. Add five revision questions with answers.
8. Never invent information and present it as lecture content.
9. If the transcript is unclear, mention the limitation.
10. Do not display the raw transcript.

LECTURE TEXT:

{transcript}
"""
                )

                notes = response.text

                if not notes:
                    st.error("AI returned empty notes. Please try again.")
                    st.stop()


            # Display notes
            st.success("Your study notes are ready!")

            st.markdown(notes)


            # Download notes
            st.download_button(
                label="📥 DOWNLOAD NOTES",
                data=notes,
                file_name="my_lecture_notes.md",
                mime="text/markdown"
            )


        except errors.APIError as e:

            st.error(
                "Gemini API is currently unavailable. "
                "Please try again later."
            )

            st.caption(str(e)[:500])


        except Exception as e:

            st.error("Something went wrong during processing.")

            st.caption(str(e)[:500])


        finally:

            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)


else:

    st.info("Upload a lecture recording to get started.")

import os
import tempfile
import streamlit as st
from dotenv import load_dotenv
from faster_whisper import WhisperModel
from google.genai import errors

from audio_processing import clean_audio
from audio_quality import check_audio_quality
from notes_generator import generate_notes
import database


load_dotenv()

st.set_page_config(
    page_title="MY SMART NOTES",
    page_icon="📚",
    layout="wide"
)

database.create_table()

st.title("📚 MY SMART NOTES")
st.write("Turn your lecture audio into clear, exam-ready notes.")


@st.cache_resource
def load_model():
    return WhisperModel(
        "small",
        device="cpu",
        compute_type="int8"
    )


# ---------------- AUDIO UPLOAD ----------------

st.header("Upload Your Lecture")

audio_file = st.file_uploader(
    "Choose your lecture recording",
    type=["mp3", "wav", "m4a", "ogg", "aac", "acc"]
)

if audio_file:

    st.audio(audio_file)

    lecture_title = st.text_input(
        "Lecture title",
        value=os.path.splitext(audio_file.name)[0]
    )

    if st.button("GENERATE MY NOTES", type="primary"):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            st.error("GEMINI_API_KEY is missing. Check your .env file.")

        else:
            original_path = None
            cleaned_path = None

            try:
                # Save uploaded audio temporarily
                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=os.path.splitext(audio_file.name)[1]
                ) as temp_audio:

                    temp_audio.write(audio_file.getbuffer())
                    original_path = temp_audio.name

                # Step 1: Clean audio
                with st.spinner("Step 1: Cleaning lecture audio..."):
                    cleaned_path = clean_audio(original_path)

                # Step 2: Transcribe audio
                with st.spinner("Step 2: Understanding your lecture..."):

                    model = load_model()

                    segments, info = model.transcribe(
                        cleaned_path,
                        language=None,
                        beam_size=5,
                        condition_on_previous_text=False,
                        vad_filter=True
                    )

                    segments = list(segments)

                    transcript = " ".join(
                        segment.text.strip()
                        for segment in segments
                    ).strip()

                # Step 3: Check transcription quality
                quality = check_audio_quality(
                    segments,
                    transcript
                )

                st.write(
                    f"Audio understanding score: {quality['score']}/100"
                )

                if quality["status"] == "poor":
                    st.error(quality["message"])

                elif quality["status"] == "medium":
                    st.warning(quality["message"])

                if quality["status"] != "poor" and len(transcript.split()) >= 5:

                    # Step 4: Generate notes
                    with st.spinner("Step 3: Creating your study notes..."):

                        notes = generate_notes(
                            transcript,
                            api_key
                        )

                    st.session_state["current_notes"] = notes
                    st.session_state["current_transcript"] = transcript
                    st.session_state["current_title"] = lecture_title

                    st.success("Your study notes are ready!")

                elif quality["status"] != "poor":
                    st.warning("Not enough speech was detected.")

            except errors.APIError as e:
                st.error("Gemini API is currently unavailable.")
                st.caption(str(e)[:500])

            except Exception as e:
                st.error("Something went wrong during processing.")
                st.caption(str(e)[:500])

            finally:
                # Remove temporary audio files
                if original_path and os.path.exists(original_path):
                    os.remove(original_path)

                if (
                    cleaned_path
                    and cleaned_path != original_path
                    and os.path.exists(cleaned_path)
                ):
                    os.remove(cleaned_path)


# ---------------- EDIT AND SAVE NOTES ----------------

if "current_notes" in st.session_state:

    st.header("Your Study Notes")

    edited_notes = st.text_area(
        "Edit your notes",
        value=st.session_state["current_notes"],
        height=450
    )

    st.download_button(
        "📥 DOWNLOAD NOTES",
        data=edited_notes,
        file_name="my_lecture_notes.md",
        mime="text/markdown"
    )

    if st.button("SAVE LECTURE TO HISTORY"):

        database.save_lecture(
            st.session_state["current_title"],
            st.session_state["current_transcript"],
            edited_notes
        )

        del st.session_state["current_notes"]
        del st.session_state["current_transcript"]
        del st.session_state["current_title"]

        st.success("Lecture saved successfully!")
        st.rerun()


# ---------------- PREVIOUS LECTURES ----------------

st.divider()
st.header("📚 Previous Lectures")

lectures = database.get_all_lectures()

if lectures:

    lecture_options = {
        f"{lecture[1]} — {lecture[2]}": lecture[0]
        for lecture in lectures
    }

    selected_title = st.selectbox(
        "Select a saved lecture",
        options=list(lecture_options.keys())
    )

    if selected_title:

        lecture_id = lecture_options[selected_title]
        lecture = database.get_lecture(lecture_id)

        if lecture:
            st.subheader(lecture[1])
            st.markdown(lecture[3])

            st.download_button(
                "📥 DOWNLOAD THIS LECTURE",
                data=lecture[3],
                file_name="saved_lecture_notes.md",
                mime="text/markdown",
                key=f"download_{lecture_id}"
            )

            if st.button(
                "DELETE THIS LECTURE",
                key=f"delete_{lecture_id}"
            ):
                database.delete_lecture(lecture_id)
                st.success("Lecture deleted.")
                st.rerun()

else:
    st.info("No saved lectures yet. Generate and save your first notes!")

