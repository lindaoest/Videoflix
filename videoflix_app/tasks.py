import subprocess
import os
from django.conf import settings
from videoflix_app.models import Video
import django_rq

def save_original_video(instance_pk, source):
    instance = Video.objects.get(pk=instance_pk)
    # Render MP4 in 1080p
    # Set path
    videos_dir = os.path.join(settings.MEDIA_ROOT, 'videos')
    # Create directory
    os.makedirs(videos_dir, exist_ok=True)

    # Rename instance
    base_name = f"{instance.id}.mp4"
    # Set new path
    new_file_path = os.path.join(videos_dir, base_name)

    # ffmpeg command to convert the video to 1080p using libx264 codec,
    # sets CRF quality to 23, encodes audio with AAC,
    # and saves the output to `new_file_path`
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

    # Run subprocess
    subprocess.run(cmd, capture_output=True)

    # Generate Thumbnail
    # Set path
    thumbnail_dir = os.path.join(settings.MEDIA_ROOT, 'thumbnails')
    # Create directory
    os.makedirs(thumbnail_dir, exist_ok=True)

    # Rename thumbnail
    base_name_thumbnail = f"{instance.id}_thumb.jpg"
    # Set new path
    thumbnail_path = os.path.join(thumbnail_dir, base_name_thumbnail)

    # ffmpeg command to capture a thumbnail image at 1 second
    # from the video file at `new_file_path`, saving it to `thumbnail_path`
    thumbnail_cmd = [
        'ffmpeg',
        '-ss', '00:00:01',
        '-i', new_file_path,
        '-frames:v', '1',
        '-q:v', '2',
        thumbnail_path
    ]

    # Run subprocess
    subprocess.run(thumbnail_cmd, capture_output=True)

    # Delete Original MP4 video
    if os.path.isfile(instance.video_file.path):
        os.remove(instance.video_file.path)

    # Set new names to thumbnail and video
    instance.thumbnail_url.name = os.path.join('thumbnails', base_name_thumbnail)
    instance.video_file.name = os.path.join('videos', base_name)

    instance.save()

    # Create a queue
    queue = django_rq.get_queue('default', autocommit=True)
    # Apply task convert_1080p to queue
    queue.enqueue(convert_1080p, instance.pk, instance.video_file.path)
    # Apply task convert_720p to queue
    queue.enqueue(convert_720p, instance.pk, instance.video_file.path)
    # Apply task convert_480p to queue
    queue.enqueue(convert_480p, instance.pk, instance.video_file.path)

def convert_1080p(instance_pk, source):
    instance = Video.objects.get(pk=instance_pk)

    # Convert in HLS
    # Base output directory for the HLS 1080p version of the video, organized by instance ID
    output_base = os.path.join(settings.MEDIA_ROOT, 'hls', str(instance.id), '1080p')
    # Directory where HLS video segments (.ts files) will be stored
    segment_dir = os.path.join(output_base, 'segments')
    # Directory where the HLS playlist (.m3u8 file) will be stored
    playlist_dir = output_base

    # Create directory
    os.makedirs(segment_dir, exist_ok=True)

    # ffmpeg command to convert the video to 1080p HLS stream:
    # scales video, sets codecs and bitrate, splits into 4s segments,
    # outputs .ts segments and .m3u8 playlist files
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

    # Run subprocess
    subprocess.run(cmd, check=True)

def convert_720p(instance_pk, source):
    instance = Video.objects.get(pk=instance_pk)

    # Convert in HLS
    # Base output directory for the HLS 720p version of the video, organized by instance ID
    output_base = os.path.join(settings.MEDIA_ROOT, 'hls', str(instance.id), '720p')
    # Directory where HLS video segments (.ts files) will be stored
    segment_dir = os.path.join(output_base, 'segments')
    # Directory where the HLS playlist (.m3u8 file) will be stored
    playlist_dir = output_base

    # Create directory
    os.makedirs(segment_dir, exist_ok=True)

    # ffmpeg command to convert the video to 720p HLS stream:
    # scales video, sets codecs and bitrate, splits into 4s segments,
    # outputs .ts segments and .m3u8 playlist files
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

    # Run subprocess
    subprocess.run(cmd, check=True)

def convert_480p(instance_pk, source):
    instance = Video.objects.get(pk=instance_pk)

    # Convert in HLS
    # Base output directory for the HLS 480p version of the video, organized by instance ID
    output_base = os.path.join(settings.MEDIA_ROOT, 'hls', str(instance.id), '480p')
    # Directory where HLS video segments (.ts files) will be stored
    segment_dir = os.path.join(output_base, 'segments')
    # Directory where the HLS playlist (.m3u8 file) will be stored
    playlist_dir = output_base

    # Create directory
    os.makedirs(segment_dir, exist_ok=True)

    # ffmpeg command to convert the video to 480p HLS stream:
    # scales video, sets codecs and bitrate, splits into 4s segments,
    # outputs .ts segments and .m3u8 playlist files
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

    # Run subprocess
    subprocess.run(cmd, check=True)