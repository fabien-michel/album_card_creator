import os
import base64
import tempfile
import mutagen
import imghdr
from mutagen.flac import Picture, error as FLACError
from natsort import natsorted

class Track(object):
    path=None
    tags=None

    def __init__(self, track_path):
        self.path = track_path
        self.tags = mutagen.File(self.path, easy=True)
    
    @property
    def title(self):
        return ' | '.join(self.tags.get('title'))

    @property
    def number(self):
        track_number = self.tags.get('tracknumber')
        if type(track_number) is list:
            track_number = track_number[0]
        else:
            track_number = ''
        if "/" in track_number:
            track_number = track_number.split("/")[0]
        try:
            return int(track_number)
        except ValueError:
            return track_number
    
    def get_cover(self):
        tags = mutagen.File(self.path, easy=False)
        
        if 'APIC:' in tags:
            cover_data = tags.get('APIC:').data
        elif 'metadata_block_picture' in tags:
            cover_data = base64.b64decode(tags.get('metadata_block_picture')[0])
        else:
            return None, None
        
        # extensions = {
        #     "image/jpeg": "jpg",
        #     "image/png": "png",
        #     "image/gif": "gif",
        # }
        # try:
        #     cover_picture = Picture(cover_data)
        #     ext = extensions.get(cover_picture.mime, "jpg")
        #     cover_data = cover_picture.data
        # except FLACError:
        #     ext = "jpg"
        ext = imghdr.what('', cover_data)
        
        return cover_data, ext
        # cover_file = tempfile.NamedTemporaryFile(delete=False, dir='/Users/fmichel/Dev/album_card_creator/', suffix=f'.{ext}')
        # cover_file.write(cover_data)
        # return cover_file
        

class Album(object):
    path=None
    tracks=[]

    def __init__(self, album_path):
        self.path = album_path
        self.__load_tracks()

    def __load_tracks(self):
        tracks = []
        for track_path in os.listdir(self.path):
            track = Track(os.path.join(self.path, track_path))
            tracks.append(track)

        self.tracks = natsorted(tracks, key=lambda kv: kv.number)
    

    @property
    def title(self): 
        return ' | '.join(self.tracks[0].tags.get('album'))
    @property
    def main_title(self):
        return self.title.split(': ')[0]
    @property
    def sub_title(self):
        parts = self.title.split(': ')
        return self.title.split(': ')[1] if len(parts)>1 else ''
    @property
    def total_tracks(self):
        return len(self.tracks)

    def print_tracks(self):
        for track in self.tracks:
            print(f'{track.number}. {track.title}')
    
    def print(self):
        print(self.title)
        print()
        self.print_tracks

    def get_cover(self):
        track = self.tracks[0]
        return track.get_cover()
        # self.cover_file = track.cover_to_file()
        # return self.cover_file.name
    

