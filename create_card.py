import os
import sys
import argparse
from pprint import pprint
from album import Album
from pdf_generator import PdfGenerator


parser = argparse.ArgumentParser(description='')
parser.add_argument('album_paths', help='Paths of the album folder', nargs='*')
args = parser.parse_args()


def process(album_path):
    album = Album(album_path)
    album.print()
    PdfGenerator(album).generate()

for album_path in args.album_paths:
    process(album_path)