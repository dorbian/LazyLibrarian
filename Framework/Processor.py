#Name: Processor.py
#Function: Processes a file name to figure out the writer, title of the book, and possibly the type and quality

#Script stuffings
__author__ = 'dorbian'
__version__ = "1.0"

#Globals
global filename
global _debug

#Variables

#Imports
import sys
import os
import getopt


#Main class
class PostProcessor(object):

    filepath = ""
    fileext = ""
    filetitle = ""
    def __init__(self):
        nonet = ""

    def nameresolver(self,filen):
        import re
        self.filepath = os.path.abspath(filen)
        print("Path to file: {0}".format(os.path.dirname(filen)))
        print("Full Path to file: {0}".format(os.path.abspath(filen)))
        head, tail = (os.path.split(filen))
        print("Filename: {0}".format(tail))
        p = re.match('(?x)(?P<TITLE>.+?) (?P<EXT>\.[^.]*$|$)', tail)
        self.filetitle = p.group('TITLE')
        self.fileext = p.group('EXT')
        print("Filename found: {0} \n Extension found: {1}" .format(self.filetitle, self.fileext))
        if self.fileext.lower() == ".mobi":
            self.mobiparser()
        elif self.fileext.lower() == ".epub":
            self.epubparser()

    def mobiparser(self):
        import lib.mobi
        book = lib.mobi.Mobi(self.filepath)
        book.parse()
        print ("Author: {0}".format(book.author()))
        print ("Title: {0}".format(book.title()))

    def epubparser(self):
        import lib.epub
        book = lib.epub.open_epub(self.filepath,mode=None)
        for item in book.opf.manifest.values():
        # read the content
            data = book.read_item(item)
            print(data)


#Want to test out if a hit comes up, run the script directly
if __name__ == "__main__":
    def usage():
        print ("Please specify the filename you would like to parse with -f")

    def arguments(argv):
        try:
            opts, args = getopt.getopt(argv, "hf:d", ["help", "file="])
        except getopt.GetoptError:
            usage()
            sys.exit(2)
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                usage()
                sys.exit()
            elif opt == '-d':
                global _debug
                _debug = 1
            elif opt in ("-f", "--file"):
                global filename
                filename = arg

    processor = PostProcessor()
    arguments(sys.argv[1:])
    processor.nameresolver(filename)