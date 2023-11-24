from faster_whisper import WhisperModel
import datetime
import subprocess
from dop_fun import time_of_function, profile
import os
from pydub import AudioSegment

class Sound_to_text:
    def __init__(self):
        # self.model = WhisperModel("large-v2", )
        self.model = WhisperModel("medium", )


    def convert_video_to_audio_ffmpeg(self, video_file, output_ext="mp3"):
        """Converts video to audio directly using `ffmpeg` command
        with the help of subprocess module"""
        filename, ext = os.path.splitext(video_file)
        subprocess.call(["ffmpeg", "-y", "-i", video_file, f"{filename}.{output_ext}"],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.STDOUT)
        return f"{filename}.{output_ext}"

    @profile
    def audio_segment(self, audio):
        sound = AudioSegment.from_mp3(audio)

        # len() and slicing are in milliseconds
        point = 120000  # len(sound) / 2
        # print(halfway_point)
        nom = 0
        for i in [sound[i:i + point] for i in range(0, len(sound), point)]:
            i.export(f"./audio_segment/seg_{nom}.mp3", format="mp3")
            nom += 1

        return os.listdir('./audio_segment')

    @profile
    def sound_to_text(self, file):
        if 'mp4' in file:
            audio = self.convert_video_to_audio_ffmpeg(file)
        else:
            audio = file
        seg_audio = self.audio_segment(audio)
        print(len(seg_audio))
        with open("test.txt", "a") as output:
            n=0
            for i in seg_audio:
                segments, info = self.model.transcribe(f'./audio_segment/{i}', language='ru')
                # print(segments.text)
                add_time = 120*n
                for segment in segments:
                    # print(segment.start)
                    z = str([str(datetime.timedelta(seconds=int(segment.start)+add_time)),'-->',  str(datetime.timedelta(seconds=int(segment.end)+add_time)),': ', segment.text])
                    print(z)
                    output.write(z +'\n')
                    z=''
                n+=1