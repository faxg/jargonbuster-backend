#
# Base class for extractors, e.g. extract plain text from a source file (e.g. pdf file)
#
class BaseExtractor(object):

    def __init__(self, file):
        raise NotImplementedError("This method should be overriden in subclass")
    
    def extractText():
        return ""

    def extractInfo():
        return ""