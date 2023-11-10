#!/usr/bin/env python3

import argparse
from pytube import YouTube
from tqdm import tqdm
import requests
import os

yt = ""

def get_available_resolutions(youtube_url):
    global yt
    # yt = YouTube(youtube_url)
    resolutions = []
    seen_resolutions = set()

    for i, stream in enumerate(yt.streams):
        if stream.mime_type == "video/mp4" or stream.mime_type == "video/webm" and stream.resolution not in seen_resolutions:
            resolutions.append(f"{len(resolutions) + 1}. {stream.resolution}")
            seen_resolutions.add(stream.resolution)

    resolutions_list = sorted(seen_resolutions, key=lambda x: int(x[:-1]))
    return resolutions_list

def download_video(selected_resolution, video_name, download_location):
    global yt
    selected_stream = yt.streams.filter(res=selected_resolution).first()

    if selected_stream:
        print(f"Downloading video in {selected_resolution} resolution.")
        response = requests.get(selected_stream.url, stream=True)

        output_path = os.path.join(download_location, f'{video_name}.mp4')

        with open(output_path, 'wb') as video_file, tqdm(
                desc=f"Downloading {selected_resolution}",
                total=int(response.headers.get('content-length', 0)),
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
        ) as progress_bar:
            for data in response.iter_content(chunk_size=1024):
                video_file.write(data)
                progress_bar.update(len(data))

        print(f"Video downloaded successfully. Saved as: {output_path}")
    else:
        print(f"Could not find a stream with resolution: {selected_resolution}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download YouTube video.')
    parser.add_argument('--video_url', help='YouTube video URL')
    parser.add_argument('--resolution', help='Selected resolution')
    parser.add_argument('--video_name', help='Video name')
    parser.add_argument('--download_location', help='Download location')

    args = parser.parse_args()

    video_url = args.video_url
    resolution = args.resolution
    video_name = args.video_name
    download_location = args.download_location or 'downloads'

    if not video_url:
        video_url = input("Enter YouTube video URL: ")
    yt = YouTube(video_url) 

    if not resolution:
        # Get available video streams and display resolutions to the user
        c = 1
        available_resolutions = get_available_resolutions(video_url)
        print("\nAvailable resolutions:")
        for res in available_resolutions:
            print(f"{c}. {res}")
            c += 1

        # Prompt the user to select a resolution
        selected_option = input("\nEnter the number corresponding to the desired resolution: ")
        try:
            selected_option = int(selected_option)
            if 1 <= selected_option <= len(available_resolutions):
                resolution = available_resolutions[selected_option-1]
            else:
                print("Invalid option. Please enter a valid number.")
                exit()
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            exit()

           

    if not video_name:
        # Extract video name from the YouTube video
        # print("Change vid name ? Y/N : ")
        ch = input("Change vid name ? Y/N : ")
        if ch == "N" or ch == "n":
            video_name = yt.title.replace(" ", "_").lower()
        else:
            video_name = input("Enter new name : ")


        
        

    # if video_name:
    #     video_name = yt.title.replace(" ", "_").lower()




    download_video(resolution, video_name, download_location)
