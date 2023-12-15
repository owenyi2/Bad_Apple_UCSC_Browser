# mv bad_apple/bad_apple.wav bad_apple/bad_apple.mp3
# ffmpeg -framerate 29.97 -pattern_type glob -i 'bad_apple_output/*.png' -shortest -c:v libx264 bad_apple_output_no_audio.mp4
ffmpeg -i bad_apple_output_no_audio.mp4 -i bad_apple/bad_apple.wav -c:v copy -c:a aac bad_apple_output.mp4