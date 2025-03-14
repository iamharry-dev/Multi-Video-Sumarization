
#!/bin/bash
frames_folder_path=./data
videos_folder_path=./videos
ext=mp4

mkdir "${frames_folder_path}"

for video_file_path in "${videos_folder_path}"/*."${ext}"; do
    slash_and_video_file_name="${video_file_path:${videos_folder_path}}"
    slash_and_video_file_name_without_extension="${slash_and_video_file_name%.${ext}}"
    video_frames_folder_path="${frames_folder_path}${slash_and_video_file_name_without_extension}";
    mkdir "${video_frames_folder_path}"
    ffmpeg -i "${video_file_path}" "${video_frames_folder_path}/%d.jpg"
done