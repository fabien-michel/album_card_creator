import os
import fpdf
from album import Album


class PdfGenerator(object):
    album = None
    PAGE_WIDTH = 190
    PAGE_HEIGHT = 92

    def __init__(self, album):
        self.album = album
    
    def generate(self):
        pdf = fpdf.FPDF(format=(self.PAGE_WIDTH, self.PAGE_HEIGHT))
        pdf.set_auto_page_break(False)

        pdf.add_page()
        pdf.add_font('DejaVu', '', 'font/DejaVuSans.ttf', uni=True)
        pdf.add_font('DejaVu Bold', '', 'font/DejaVuSans-Bold.ttf', uni=True)
        
        cover_width = 100
        cover_data, cover_ext = self.album.get_cover()
        cover_file = None
        if cover_data:
            cover_file = open(f'cover.{cover_ext}', 'wb')
            cover_file.write(cover_data)
            cover_file.close()
            pdf.image(cover_file.name, 0, 0, 0, 92)
        
        pdf.set_xy(cover_width + 5, 0)
        main_title = self.album.main_title
        pdf.set_font("DejaVu Bold", size=12)
        pdf.set_font_size(self.__reduce_font_to_fit(pdf, main_title, 12, 80 ))
        title_height = 10.5
        pdf.cell(self.PAGE_WIDTH-cover_width-3, 6, txt=main_title, align='C',)
        if self.album.sub_title: 
            pdf.set_xy(cover_width + 5, 6)
            pdf.set_font_size(self.__reduce_font_to_fit(pdf, main_title, 9, 80 ))
            pdf.cell(self.PAGE_WIDTH-cover_width-3, 3, txt=self.album.sub_title, align='C',)

        pdf.set_font("DejaVu", size=12)
        row_height = 6

        font_size, row_height = self.__get_track_name_size(len(self.album.tracks))
            
        for index, track in enumerate(self.album.tracks):
            print(track.title)
            pdf.set_xy(cover_width + 5, index * row_height + title_height)
            pdf.set_font_size(font_size)
            pdf.cell(10, row_height, txt=str(track.number), align='R')
            
            specific_font_size=self.__reduce_font_to_fit(pdf, track.title, font_size, 70)
            pdf.set_font_size(specific_font_size)
            # pdf.set_stretching(self.__stretching_of_text(pdf, track.title, 50))
            pdf.cell(self.PAGE_WIDTH-cover_width-3, row_height, txt=track.title)
            # pdf.set_font_size(font_size)
        
        pdf.output(f"{self.album.title}.pdf")

        if cover_file: 
            os.unlink(cover_file.name)

    def __get_track_name_size(self, tracks_count):
        if tracks_count > 29:
            return 7, 2.6
        elif tracks_count > 27:
            return 7, 2.8
        elif tracks_count > 25:
            return 8, 3.1
        elif tracks_count > 23:
            return 9, 3.2
        elif tracks_count > 20:
            return 10, 3.5
        elif tracks_count > 16:
            return 11, 4.1
        elif tracks_count > 13:
            return 11.5, 5
        else:
            return 12, 6
            

    def __reduce_font_to_fit(sefl, pdf, text, fs, max_width):
        text_width = pdf.get_string_width(text)
        while text_width>max_width:
            fs = fs - 0.1
            pdf.set_font_size(fs)
            text_width = pdf.get_string_width(text)
        return fs