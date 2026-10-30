def check_audio_quality(segments, transcript):
    """
    Check Whisper transcription quality.
    """

    if not segments or not transcript.strip():
        return {
            "status": "poor",
            "score": 0,
            "message": "No clear speech detected."
        }

    total_segments = len(segments)

    avg_logprob = sum(
        segment.avg_logprob for segment in segments
    ) / total_segments

    avg_no_speech = sum(
        segment.no_speech_prob for segment in segments
    ) / total_segments

    avg_compression = sum(
        segment.compression_ratio for segment in segments
    ) / total_segments

    word_count = len(transcript.split())

    score = 100

    if avg_logprob < -1:
        score -= 30

    if avg_no_speech > 0.6:
        score -= 30

    if avg_compression > 2.4:
        score -= 20

    if word_count < 10:
        score -= 20

    score = max(0, score)

    if score >= 70:
        status = "good"
        message = "Audio transcription looks reliable."

    elif score >= 40:
        status = "medium"
        message = "Audio quality is uncertain. Notes may miss details."

    else:
        status = "poor"
        message = "Audio is unclear. Please upload a better recording."

    return {
        "status": status,
        "score": score,
        "message": message
    }