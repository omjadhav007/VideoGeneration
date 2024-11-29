# VideoGeneration
Revolutionizing Video Production with AI: 3D  Avatars &amp; Human-like Voice  
• Problem Statement:  
  • Traditional video production is time-consuming and resource-intensive. 
  • Manual creation of videos requires human intervention for script reading, avatar animation,  and voiceover.

# Avatar Video Generator

This project allows you to create avatar videos from text input. It uses a combination of Python libraries to synthesize speech, generate phonemes, and produce a video with an animated avatar that lip-syncs to the speech.

## Features

- Generate a video of an avatar speaking synthesized speech.
- Customize the avatar using TTS (Text-to-Speech) and phoneme generation.
- Extract audio and create synchronized lip movements with speech.

## Requirements

Ensure you have the following Python libraries installed:

- `moviepy` – For video editing and creation.
- `TTS` – For text-to-speech synthesis.
- `phonemizer` – For converting text into phonemes.
- `whisper` – For transcription and speech recognition (optional).
- `ffmpeg-python` – For interacting with FFmpeg programmatically.
- `espeak-ng` – Required for phoneme generation (ensure the library is installed and accessible).

To install all required Python packages, use:

```bash
pip install -r requirements.txt

