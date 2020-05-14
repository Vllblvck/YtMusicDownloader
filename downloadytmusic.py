try:
    import sys
    import os
    import ffmpeg
    from pytube import YouTube, Playlist
except ImportError:
    print("You are lacking dependecies for the script")


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
    print("Removing mp4 file...")
    os.remove(DOWNLOADS_PATH + songname_mp4)
    print("Done")


def download_song(song_url):
    download_complete = False
    while not download_complete: 
        try:
            print("Trying to download: " + song_url)
            song = YouTube(song_url)
            stream = song.streams.filter(
                adaptive=True,
                mime_type="audio/mp4"
            ).first()
    
            songname_mp4 = stream.default_filename
            songname_mp3 = songname_mp4.replace(".mp4", ".mp3")
            if os.path.exists(DOWNLOADS_PATH + songname_mp3):
                print("Ommitting becaue it exists in given directory")
                return

            print("Downloading:" + songname_mp4)
            stream.download(DOWNLOADS_PATH)
            mp3_to_mp4(songname_mp4, songname_mp3)
            download_complete = True

        except KeyError:
            print("Something went wrong because pytube is buggy :(")
            print("Redoing the operation...")
            continue


def download_playlist(playlist_url):
    print("Gathering urls from playlist...")
    playlist = Playlist(playlist_url)
    song_urls = playlist.video_urls
    download_complete = False
    curr_idx = 0

    while not download_complete: 
        try:
            for idx, song_url in enumerate(song_urls[curr_idx:], start=curr_idx):
                print("[" + str(curr_idx) + "]Trying to download: " + song_url)
                song = YouTube(song_url)
                stream = song.streams.filter(
                    adaptive=True,
                    mime_type="audio/mp4"
                ).first()
                            
                songname_mp4 = stream.default_filename
                songname_mp3 = songname_mp4.replace(".mp4", ".mp3")
                if os.path.exists(DOWNLOADS_PATH + songname_mp3):
                    print("Ommitting becaue it exists in given directory")
                    curr_idx = idx + 1
                    continue
        
                print("Downloading:" + songname_mp4)
                stream.download(DOWNLOADS_PATH)
                mp3_to_mp4(songname_mp4, songname_mp3)
                curr_idx = idx + 1

            download_complete = True

        except KeyError:
            print("Something went wrong because pytube is buggy :(")
            print("Redoing the operation...")
            curr_idx = idx
            continue


def main():
    args = sys.argv
    args_len = len(args)
    if (args_len == 3):
        if args[1] == 'v':
            download_song(args[2])
        elif args[1] == 'p':
            download_playlist(args[2])
        else:
            print("Correct syntax is:")
            print("{v for video download or p for playlist download} {video/playlist url}")
            sys.exit()
    else:
        print("Correct syntax is:")
        print("{v for video download or p for playlist download} {video/playlist url}")
        sys.exit()


if __name__ == "__main__":
    main()