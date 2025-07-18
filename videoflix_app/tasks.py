import subprocess
import os
from django.conf import settings

def saveOriginalVideo(instance, source):
    # Render MP4 in 1080p
    videos_dir = os.path.join(settings.MEDIA_ROOT, 'videos')
    os.makedirs(videos_dir, exist_ok=True)

    base_name = f"{instance.id}.mp4"
    new_file_path = os.path.join(videos_dir, base_name)

    cmd = [
        'ffmpeg',
        '-i', source,
        '-s', 'hd1080',
        '-c:v', 'libx264',
        '-crf', '23',
        '-c:a', 'aac',
        '-strict', '-2',
        new_file_path
    ]
    subprocess.run(cmd, capture_output=True)

    # Generate Thumbnail
    thumbnail_dir = os.path.join(settings.MEDIA_ROOT, 'thumbnails')
    os.makedirs(thumbnail_dir, exist_ok=True)

    base_name_thumbnail = f"{instance.id}_thumb.jpg"
    thumbnail_path = os.path.join(thumbnail_dir, base_name_thumbnail)

    thumbnail_cmd = [
        'ffmpeg',
        '-ss', '00:00:01',
        '-i', new_file_path,
        '-frames:v', '1',
        '-q:v', '2',
        thumbnail_path
    ]
    subprocess.run(thumbnail_cmd, capture_output=True)

    # Delete Original MP4 video
    if os.path.isfile(instance.video_file.path):
        os.remove(instance.video_file.path)

    instance.thumbnail_url.name = os.path.join('thumbnails', base_name_thumbnail)
    instance.video_file.name = os.path.join('videos', base_name)
    instance.save()

def convert1080p(instance, source):
    # Convert in HLS
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

def convert720p(instance, source):
    # Convert in HLS
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

def convert480p(instance, source):
    # Convert in HLS
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