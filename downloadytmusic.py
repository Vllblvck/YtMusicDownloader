import argparse
import os
import sys
import ffmpeg
from pytube import YouTube, Playlist
from pytube.exceptions import RegexMatchError


DOWNLOADS_PATH = '/path/to/music/directory/'

class YtMusicDownloader:
    
    def __init__(self, downloads_path):
        self.downloads_path = downloads_path


    def mp3_to_mp4(self, songname_mp4, songname_mp3):
        print('Converting from mp4 to mp3...')
        try:
            (
                ffmpeg
                .input(self.downloads_path + songname_mp4)
                .output(self.downloads_path + songname_mp3)
                .global_args('-loglevel', 'error')
                .run() 
            )
            print('Removing mp4 file...')
            os.remove(self.downloads_path + songname_mp4)
            print('Done')
        except ffmpeg.Error as e:
            print('There was an error during file conversion')
            print(e)
            sys.exit()


    def download_song(self, song_url):
        download_complete = False
        while not download_complete: 
            try:
                print('Trying to download: ' + song_url)
                song = YouTube(song_url)
                stream = song.streams.filter(
                    adaptive=True,
                    mime_type='audio/mp4'
                ).first()
    
                songname_mp4 = stream.default_filename
                songname_mp3 = songname_mp4.replace('.mp4', '.mp3')
                if os.path.exists(self.downloads_path + songname_mp3):
                    print('Ommitting becaue song exists in given directory')
                    return

                print('Downloading:' + songname_mp4)
                stream.download(self.downloads_path)
                self.mp3_to_mp4(songname_mp4, songname_mp3)
                download_complete = True

            except KeyError:
                print('Something went wrong with pytube module :(')
                print('Redoing the operation...')
                continue
            except RegexMatchError:
                print('Provided url is wrong')
                sys.exit()


    def download_playlist(self, playlist_url):
        print('Gathering urls from playlist...')
        playlist = Playlist(playlist_url)
        song_urls = playlist.video_urls
        download_complete = False
        curr_idx = 0

        while not download_complete: 
            try:
                for idx, song_url in enumerate(song_urls[curr_idx:], start=curr_idx):
                    print('[' + str(curr_idx) + ']Trying to download: ' + song_url)
                    song = YouTube(song_url)
                    stream = song.streams.filter(
                        adaptive=True,
                        mime_type='audio/mp4'
                    ).first()
                            
                    songname_mp4 = stream.default_filename
                    songname_mp3 = songname_mp4.replace('.mp4', '.mp3')
                    if os.path.exists(self.downloads_path + songname_mp3):
                        print('Ommitting becaue song exists in given directory')
                        curr_idx = idx + 1
                        continue
        
                    print('Downloading:' + songname_mp4)
                    stream.download(self.downloads_path)
                    self.mp3_to_mp4(songname_mp4, songname_mp3)
                    curr_idx = idx + 1

                download_complete = True

            except KeyError:
                print('Something went wrong with pytube module :(')
                print('Redoing the operation...')
                curr_idx = idx
                continue
            except RegexMatchError:
                print('Provided url is wrong')
                sys.exit()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'download_type',
        choices=['song', 'playlist']
    )
    parser.add_argument(
        'url',
        help='Url to song or playlist'
    )
    args = parser.parse_args()

    yt = YtMusicDownloader(DOWNLOADS_PATH)
    
    if args.download_type == 'song':
        yt.download_song(args.url)
    elif args.download_type == 'playlist':
        yt.download_playlist(args.url)
     

if __name__ == '__main__':
    main()