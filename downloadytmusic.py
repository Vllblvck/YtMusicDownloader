try:
    import sys
    import os
    import ffmpeg
    from pytube import YouTube, Playlist
except ImportError:
    print("You are lacking dependecies for the script")
    print("Check README file for more instructions")


DOWNLOADS_PATH = "/home/vllblvck/Music/"


def mp3_to_mp4(songname_mp4, songname_mp3):
    print("Converting from mp4 to mp3...")
    (
        ffmpeg
        .input(DOWNLOADS_PATH + songname_mp4)
        .output(DOWNLOADS_PATH + songname_mp3)
        .global_args('-loglevel', 'error')
        .run() 
    )
    os.remove(DOWNLOADS_PATH + songname_mp4)


def download_song(link):
    print("Connecting to youtube...")
    
    try:
        yt = YouTube(link)
    except KeyError:
        print("Provided link seems to be bad.")
        print("Make sure it leads to a video")
        sys.exit()

    stream = yt.streams.filter(
        adaptive=True,
        mime_type="audio/mp4"
    ).first()
    
    songname_mp4 = stream.default_filename
    songname_mp3 = songname_mp4.replace(".mp4", ".mp3")
    if os.path.exists(DOWNLOADS_PATH + songname_mp3):
        print("Song already exists in given directory")
        return

    print("Downloading:" + songname_mp4)
    stream.download(DOWNLOADS_PATH)
    mp3_to_mp4(songname_mp4, songname_mp3)


def download_playlist(link):
    print("Connecting to youtube...")

    try:
        playlist = Playlist(link)
    except KeyError:
        print("Provided link seems to be bad")
        print("Make sure it leads to a playlist")
        sys.exit()
    
    for video in playlist.videos:
        stream = video.streams.filter(
            adaptive=True,
            mime_type="audio/mp4"
        ).first()

        songname_mp4 = stream.default_filename
        songname_mp3 = songname_mp4.replace(".mp4", ".mp3")
        if os.path.exists(DOWNLOADS_PATH + songname_mp3):
            print("Ommitting " + songname_mp4)
            continue
        
        print("Downloading:" + songname_mp4)
        stream.download(DOWNLOADS_PATH)
        mp3_to_mp4(songname_mp4, songname_mp3)


if sys.argv[1] == "v" and sys.argv[2] is not None:
    link = sys.argv[2]
    download_song(link)
elif sys.argv[1] == "p" and sys.argv[2] is not None:
    link = sys.argv[2]
    download_playlist(link)
else:
    print("You need to provide link and download type")
    print("Correct syntax is:")
    print("{v for video download or p for playlist download} {video/playlist link}")
    sys.exit()