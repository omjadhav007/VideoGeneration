# Importing required Libraries
from moviepy.editor import VideoFileClip, AudioFileClip
from TTS.api import TTS
import os
from phonemizer import phonemize
import re
from phonemizer.backend.espeak.wrapper import EspeakWrapper
EspeakWrapper.set_library('C:\Program Files\eSpeak NG\libespeak-ng.dll')
import whisper
import ffmpeg

phoneme_to_visme = {
    # Set 1: A, E, I
    'ɐ': 'boy\\1.png',
    'æ': 'boy\\1.png',
    'e': 'boy\\1.png',
    'ɪ': 'boy\\1.png',
    'iː': 'boy\\1.png',
    'eɪ': 'boy\\1.png',
    'aɪ': 'boy\\1.png',
    'ɜː': 'boy\\1.png',
    'ɑː': 'boy\\1.png',
    'ə': 'boy\\1.png',
    'aʊ': 'boy\\1.png',
    'eə': 'boy\\1.png',
    'ɐ': 'boy\\1.png',
    'ɛ': 'boy\\1.png', 

    # Set 2: TH
    'θ': 'boy\\2.png',
    'ð': 'boy\\2.png',

    # Set 3: O
    'ɒ': 'boy\\3.png',
    'ɔː': 'boy\\3.png',
    'oʊ': 'boy\\3.png',
    'əʊ': 'boy\\3.png',
    'ʌ': 'boy\\3.png',
    'ɔɪ': 'boy\\3.png',
    'ɔ': 'boy\\3.png',

    # Set 4: EE
    'iː': 'boy\\4.png',
    'ɪə': 'boy\\4.png',

    # Set 5: U
    'uː': 'boy\\5.png',
    'juː': 'boy\\5.png',
    'ʊ': 'boy\\5.png',
    'ʊə': 'boy\\5.png',

    # Set 6: L
    'l': 'boy\\6.png',

    # Set 7: CH, J, SH
    'tʃ': 'boy\\7.png',
    'dʒ': 'boy\\7.png',
    'ʃ': 'boy\\7.png',
    'ʒ': 'boy\\7.png',

    # Set 8: B, M, P
    'b': 'boy\\8.png',
    'm': 'boy\\8.png',
    'p': 'boy\\8.png',

    # Set 9: F, V
    'f': 'boy\\9.png',
    'v': 'boy\\9.png',

    # Set 10: W, Q
    'w': 'boy\\10.png',
    'h': 'boy\\10.png',

    # Set 11: C, D, N, S, T, X, Y, Z
    'k': 'boy\\11.png',
    's': 'boy\\11.png',
    'd': 'boy\\11.png',
    'n': 'boy\\11.png',
    'ŋ': 'boy\\11.png',
    't': 'boy\\11.png',
    'ks': 'boy\\11.png',
    'j': 'boy\\11.png',
    'z': 'boy\\11.png',
    'ɹ': 'boy\\11.png',  # 'R' sound
    'r': 'boy\\11.png',
    'tɹ': 'boy\\11.png',  # "tr" cluster
    'ʔ': 'boy\\11.png',  # Glottal stop

    # Set 12: G, K
    'ɡ': 'boy\\12.png',
    'ɾ': 'boy\\12.png',  # Flap 'r'
}

def generate_audio(script, audio_path):
    # Using Tacotron 2 for TTS
    tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")
    tts.tts_to_file(text=script, file_path=audio_path,speed=0.85,speaker_id=2,emotion="happy")

def word_to_splited_phonemes(word):
    phonemized_text = phonemize(
        word, 
        backend='espeak', 
        language='en-us', 
        strip=True, 
        preserve_punctuation=True
    )
    # Define a pattern for IPA phonemes, prioritizing multi-character phonemes
    phoneme_pattern = r"(aɪ|eɪ|oʊ|ɔɪ|ʊə|iː|uː|ɜː|ɑː|əʊ|ɪə|æ|ɛ|ʌ|ɒ|ʃ|ʒ|θ|ð|ŋ|ɹ|ɾ|ɐ|ɑ|ɔ|ə|ɜ|ɛ|ɪ|ʊ|ʌ|p|b|t|d|k|g|f|v|s|z|m|n|l|r|h|w|j|tʃ|dʒ)"
    
    # If phonemized_text is a list, join it into a single string
    if isinstance(phonemized_text, list):
        phonemized_text = " ".join(phonemized_text)
    
    # Find and return phonemes
    return re.findall(phoneme_pattern, phonemized_text)

def word_durations(audio_path):
    # loading model
    model = whisper.load_model("small")

    # stroring transcriptions into result
    result=model.transcribe(audio_path, word_timestamps=True)['segments']

    duration=[]
    privious_end=0
    # printing sentence and word alignments
    for segment in result: # one segments has data one sentence
        # print(f"\n{segment['id']}) start : {segment['start']:.02f}, end : {segment['end']:.02f}, text : {segment['text']}")
        for shabd in segment['words']:
            # print(f"\tword : {shabd['word']}, start : {shabd['start']:.02f}, end : {shabd['end']:.02f}")
            word=shabd['word']
            silence_duration=shabd['start']-privious_end
            word_duration=shabd['end']-shabd['start']
            privious_end=shabd['end']
            duration.append([word,silence_duration,word_duration])
    return duration

def create_image_list(image_list_path,word_durations):
    # Create the text file listing images and durations
    with open(image_list_path, "w") as f: 
        for word,silence_duration,word_duration in word_durations:
            if silence_duration:
                f.write(f"file 'boy\close.png'\n")
                f.write(f"duration {silence_duration}\n")
                
            phoneme_list=word_to_splited_phonemes(word)
            phoneme_duration=word_duration/len(phoneme_list)

            for phoneme in phoneme_list:
                f.write(f"file '{phoneme_to_visme[phoneme]}'\n")
                f.write(f"duration {phoneme_duration}\n")

    # Add an extra file entry for the last image to avoid FFmpeg trimming it early
    last_image = 'boy\happy.png'
    with open(image_list_path, "a") as f:
        f.write(f"file '{last_image}'\n")
        f.write(f"duration 3.0\n")

def generate_video(video_path,image_list_path):
    # Use FFmpeg to create a video
    ffmpeg.input(image_list_path, format='concat', safe=0) \
        .output(video_path, vcodec='libx264', framerate=24, pix_fmt='yuv420p') \
        .run()

    print("Video created successfully as in "+video_path)

def combine_audio_video(video_path,audio_path,final_output_path):
    # Load the video
    video = VideoFileClip(video_path)

    # Load the audio
    audio = AudioFileClip(audio_path)

    # Sync durations (optional)
    # audio = audio.set_duration(video.duration)

    # Add audio to the video
    final_video = video.set_audio(audio)

    # Save the resulting video
    final_video.write_videofile(final_output_path, codec="libx264", audio_codec="aac",fps=24)

    print(f"Video with audio saved as {final_output_path}")
