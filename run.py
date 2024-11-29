from avatarVideoGeneration import *

file_name="your_file_name"
video_path="video\\"+file_name+".mp4"
audio_path="audio\\"+file_name+".wav"
final_output_path="output_video\\"+file_name+".mp4"
image_list_path="image_list.txt"

script = '''Artificial intelligence is a field of science concerned with building computers and machines that can reason, learn, and act in such a way that would normally require human intelligence or that involves data whose scale exceeds what humans can analyze. 

AI is a broad field that encompasses many different disciplines, including computer science, data analytics and statistics, hardware and software engineering, linguistics, neuroscience, and even philosophy and psychology.

On an operational level for business use, AI is a set of technologies that are based primarily on machine learning and deep learning, used for data analytics, predictions and forecasting, object categorization, natural language processing, recommendations, intelligent data retrieval, and more.
'''

generate_audio(script,audio_path)
word_durations=word_durations(audio_path)
create_image_list(image_list_path,word_durations)
generate_video(video_path,image_list_path)
combine_audio_video(video_path,audio_path,final_output_path)
git clone https://github.com/omjadhav007/VideoGeneration
