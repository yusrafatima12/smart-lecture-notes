import os
import shutil
import subprocess
import tempfile


def clean_audio(input_path):
    """
    Reduce background noise and convert audio
    into Whisper-friendly WAV format.
    """

    ffmpeg_path = shutil.which("ffmpeg")

    if not ffmpeg_path:
        print("FFmpeg not found. Using original audio.")
        return input_path

    output_path = tempfile.mktemp(suffix=".wav")

    command = [
        ffmpeg_path,
        "-y",
        "-i", input_path,
        "-af", "highpass=f=100,lowpass=f=7500,afftdn=nf=-25",
        "-ar", "16000",
        "-ac", "1",
        "-acodec", "pcm_s16le",
        output_path
    ]

    try:
        subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True
        )

        return output_path

    except subprocess.CalledProcessError:
        print("Error processing audio.")

        if os.path.exists(output_path):
            os.remove(output_path)

        return input_path