from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import pdfminer.high_level
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument

from extractor.base_extractor import BaseExtractor

class PDFMinerExtractor(BaseExtractor):
    _document = ""
    _parser = ""

    def __init__(self, file):
        parser = PDFParser(file)
        self._document = PDFDocument(parser)
        self._filename = file.name
        

    def extractText (self):
        try:
            text = pdfminer.high_level.extract_text (self._filename)
        except e as Exception:
            text = f'Error extracting text: ${e}'
        finally:
            return text

    
    def extractInfo (self):
        info  = { key: val.decode() for key, val in self._document.info[0].items() }
        return info
