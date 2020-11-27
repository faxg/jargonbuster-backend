from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from extractor.base_extractor import BaseExtractor


# import parser object from tike 
from tika import parser   

class TikaExtractor(BaseExtractor):
    _parsed_pdf = None
    _file = None

    def __init__(self, file):
         self._filename = file.name


    def extractText (self):
        try:
            self._parsed_pdf = parser.from_file(self._filename)
            # you can also bring text only, by parsed_pdf['text']  
            # parsed_pdf['content'] returns string 
            text = self._parsed_pdf['content']
        except Exception as e:
            text = f'Error extracting text ${e}'
        finally:
            return text

    
    def extractInfo (self):
        try:
            if (not self._parsed_pdf):
                self._parsed_pdf = parser.from_file(self._filename)
            info  = { key: val for key, val in self._parsed_pdf['metadata'].items() }
        except Exception as e:
            console.log (e)
            info = {}
        finally:
            return info

