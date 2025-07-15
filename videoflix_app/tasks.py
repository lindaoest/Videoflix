import subprocess
import os
from django.conf import settings

def convert1080p(instance, source):
    base_path, ext = os.path.splitext(source)
    new_file_name = base_path + '_1080p.mp4'
    thumbnail_name = base_path + '_thumb.jpg'

    # 1. MP4 in 1080p rendern
    cmd = [
        'ffmpeg',
        '-i', source,
        '-s', 'hd1080',
        '-c:v', 'libx264',
        '-crf', '23',
        '-c:a', 'aac',
        '-strict', '-2',
        new_file_name
    ]
    subprocess.run(cmd, capture_output=True)

    # 2. Thumbnail erzeugen
    thumbnail_cmd = [
        'ffmpeg',
        '-ss', '00:00:01',
        '-i', new_file_name,
        '-frames:v', '1',
        '-q:v', '2',
        thumbnail_name
    ]
    subprocess.run(thumbnail_cmd, capture_output=True)

    rel_thumb_path = os.path.relpath(thumbnail_name, settings.MEDIA_ROOT)
    instance.thumbnail_url.name = rel_thumb_path

    # 3. Convert in HLS
    source = instance.video_file.path
    output_base = os.path.join(settings.MEDIA_ROOT, 'hls', str(instance.id), '1080p')
    segment_dir = os.path.join(output_base, 'segments')
    playlist_dir = output_base

    os.makedirs(segment_dir, exist_ok=True)

    cmd = [
        'ffmpeg',
        '-i', source,
        '-vf', 'scale=854:1080',
        '-b:v', '5000k',
        '-c:v', 'h264',
        '-c:a', 'aac',
        '-strict', '-2',
        '-f', 'hls',
        '-hls_time', '4',
        '-hls_playlist_type', 'vod',
        '-hls_segment_filename', os.path.join(segment_dir, 'index_%03d.ts'),
        os.path.join(playlist_dir, 'index.m3u8'),
        '-map', '0:v', '-map', '0:a'
    ]
    subprocess.run(cmd, check=True)

    instance.save()

def convert720p(instance, source):
    base_path, ext = os.path.splitext(source)
    new_file_name = base_path + '_720p.mp4'
    thumbnail_name = base_path + '_thumb.jpg'

    # 1. MP4 in 720p rendern
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
    subprocess.run(cmd, capture_output=True)

    # 2. Thumbnail erzeugen
    thumbnail_cmd = [
        'ffmpeg',
        '-ss', '00:00:01',
        '-i', new_file_name,
        '-frames:v', '1',
        '-q:v', '2',
        thumbnail_name
    ]
    subprocess.run(thumbnail_cmd, capture_output=True)

    rel_thumb_path = os.path.relpath(thumbnail_name, settings.MEDIA_ROOT)
    instance.thumbnail_url.name = rel_thumb_path

    # 3. Convert in HLS
    source = instance.video_file.path
    output_base = os.path.join(settings.MEDIA_ROOT, 'hls', str(instance.id), '720p')
    segment_dir = os.path.join(output_base, 'segments')
    playlist_dir = output_base

    os.makedirs(segment_dir, exist_ok=True)

    cmd = [
        'ffmpeg',
        '-i', source,
        '-vf', 'scale=1280:720',
        '-b:v', '2000k',
        '-c:v', 'h264',
        '-c:a', 'aac',
        '-strict', '-2',
        '-f', 'hls',
        '-hls_time', '4',
        '-hls_playlist_type', 'vod',
        '-hls_segment_filename', os.path.join(segment_dir, 'index_%03d.ts'),
        os.path.join(playlist_dir, 'index.m3u8'),
        '-map', '0:v', '-map', '0:a'
    ]
    subprocess.run(cmd, check=True)

    instance.save()

def convert480p(instance, source):
    base_path, ext = os.path.splitext(source)
    new_file_name = base_path + '_480p.mp4'
    thumbnail_name = base_path + '_thumb.jpg'

    # 1. MP4 in 480p rendern
    cmd = [
        'ffmpeg',
        '-i', source,
        '-s', 'hd480',
        '-c:v', 'libx264',
        '-crf', '23',
        '-c:a', 'aac',
        '-strict', '-2',
        new_file_name
    ]
    subprocess.run(cmd, capture_output=True)

    # 2. Thumbnail erzeugen
    thumbnail_cmd = [
        'ffmpeg',
        '-ss', '00:00:01',
        '-i', new_file_name,
        '-frames:v', '1',
        '-q:v', '2',
        thumbnail_name
    ]
    subprocess.run(thumbnail_cmd, capture_output=True)

    rel_thumb_path = os.path.relpath(thumbnail_name, settings.MEDIA_ROOT)
    instance.thumbnail_url.name = rel_thumb_path

    # 3. Convert in HLS
    source = instance.video_file.path
    output_base = os.path.join(settings.MEDIA_ROOT, 'hls', str(instance.id), '480p')
    segment_dir = os.path.join(output_base, 'segments')
    playlist_dir = output_base

    os.makedirs(segment_dir, exist_ok=True)

    cmd = [
        'ffmpeg',
        '-i', source,
        '-vf', 'scale=854:480',
        '-b:v', '1000k',
        '-c:v', 'h264',
        '-c:a', 'aac',
        '-strict', '-2',
        '-f', 'hls',
        '-hls_time', '4',
        '-hls_playlist_type', 'vod',
        '-hls_segment_filename', os.path.join(segment_dir, 'index_%03d.ts'),
        os.path.join(playlist_dir, 'index.m3u8'),
        '-map', '0:v', '-map', '0:a'
    ]
    subprocess.run(cmd, check=True)

    instance.save()