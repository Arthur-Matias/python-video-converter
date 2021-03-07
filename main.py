"""
ffmpeg -i "ENTRADA" -i "LEGENDA" -c:v libx264 -crf 20 -preset veryslow -c:a aac -b:a 320k
-c:s srt -map v:0 -map a -map 1:0 "SAIDA"

-c --- codecs
-b --- bitrate

:a --- audio
:v --- video

"""

import os
import fnmatch
import sys

if sys.platform == 'linux':
    ffmpeg_command = 'ffmpeg'
else: 
    ffmpeg_command = r'ffmpeg\ffmpeg.exe'

video_codec = '-c:v libx264'
crf = '-crf 18'
preset = '-preset veryslow'
audio_codec = '-c:a aac'
audio_bitrate = '-b:a 320k'
debug = '-ss 00:00:00 -to 00:00:10'
curr_dir_path = os.path.dirname(os.path.realpath(__file__))
file_format_to_convert = str(input('Qual o formato desejado para conversão?\n'))

if not '.' in file_format_to_convert:
    file_format_to_convert = '.' + file_format_to_convert

origin_path = curr_dir_path + '/videos'
output_path = curr_dir_path + '/output'

for root, folders, files in os.walk(origin_path):
    for file in files:
        
        full_path = os.path.join(root, file)

        file_name, file_extension = os.path.splitext(full_path)
        subtitles_path = file_name + '.srt'

        if os.path.isfile(subtitles_path):
            print('Subtitles found!')
            subtitles_input = f'-i "{subtitles_path}"'
            subtitles_map = '-c:s srt -map v:0 -map a -map 1:0'
        else:
            subtitles_input = ''
            subtitles_map = ''

        file_name, file_extension = os.path.splitext(file)

        file_output = f'{output_path}/{file_name}_converted{file_format_to_convert}'

        command = f'{ffmpeg_command} -i "{full_path}" {subtitles_input} ' \
            f'{video_codec} {crf} {preset} {audio_codec} {audio_bitrate}' \
            f'{subtitles_map} "{file_output}"'

        os.system(command)