import subprocess

def convert720p(source):
	# source.pop('.mp4')
	new_file_name = source + '_720p.mp4'
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