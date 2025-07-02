import subprocess
import os
from django.conf import settings

def convert720p(instance, source):
    # source.pop('.mp4')
    new_file_name = source + '_720p.mp4'
    thumbnail_name = source + '_thumb.jpg'
	# cmd = 'ffmpeg -i "{}" -s hd720 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, new_file_name)
    cmd = [
        'ffmpeg',
        '-i', source,
        '-s', 'hd720',
        '-c:v', 'libx264',
        '-crf', '23',
        '-c:a', 'aac',
        '-strict', '-2',
        new_file_name
    ]
    run = subprocess.run(cmd, capture_output=True)

    thumbnail_cmd = [
        'ffmpeg',
        '-ss', '00:00:01',
        '-i', new_file_name,
        '-frames:v', '1',
        '-q:v', '2',
        thumbnail_name
    ]

    run = subprocess.run(thumbnail_cmd, capture_output=True)

    rel_thumb_path = os.path.relpath(thumbnail_name, settings.MEDIA_ROOT)
    instance.thumbnail.name = rel_thumb_path
    instance.save()