#Name: Processor.py
#Function: Processes a file name to figure out the writer, title of the book, and possibly the type and quality

#Script stuff
__author__ = 'dorbian'
__version__ = "1.0"

#Imports
import sys
import os
import getopt
import Logger

#Main class
class PostProcessor(object):

    filepath = ""
    fileext = ""
    filetitle = ""
    bookauthor = ""
    booktitle = ""

    def __init__(self):
        nonet = ""

    def nameresolver(self, filen):
        import re
        self.filepath = os.path.abspath(filen)
        Logger.log("Processing file: {0}".format(os.path.abspath(filen)), 'info')
        head, tail = (os.path.split(filen))
        p = re.match('(?x)(?P<TITLE>.+?) (?P<EXT>\.[^.]*$|$)', tail)
        self.filetitle = p.group('TITLE')
        self.fileext = str(p.group('EXT')).split('.')[1]
        Logger.log("Filename found: {0}".format(self.filetitle), 'debug')
        Logger.log("Type found: {0}".format(self.fileext), 'debug')
        if self.fileext.lower() == "mobi":
            self.mobiparser()
            Logger.log("Processing file as a {0} file".format(self.fileext.lower()), 'debug')
        elif self.fileext.lower() == "epub":
            self.epubparser()
            Logger.log("Processing file as a {0} file".format(self.fileext.lower()), 'debug')
        # elif self.fileext.lower() == "pdf":
        #     self.pdfparser()
        #     Logger.log("Processing file as a {0} file".format(self.fileext.lower()), 'debug')

    def mobiparser(self):
        import lib.mobi
        book = lib.mobi.Mobi(self.filepath)
        book.parse()
        self.bookauthor = book.author()
        self.booktitle = book.title()
        Logger.log("Author found: {0}".format(self.bookauthor), 'debug')
        Logger.log("Title found: {0}".format(self.booktitle), 'debug')

    def epubparser(self):
        import lib.epub
        book = lib.epub.open_epub(self.filepath, mode=None)
        self.bookauthor = book.opf.metadata.creators[0][0]
        self.booktitle = book.opf.metadata.titles[0][0]
        Logger.log("Author found: {0}".format(self.bookauthor), 'debug')
        Logger.log("Title found: {0}".format(self.booktitle), 'debug')

    # def pdfparser(self):
    #     from lib.pdfminer.pdfparser import PDFParser
    #     from lib.pdfminer.pdfdocument import PDFDocument
    #     book = open(self.filepath, 'rb')
    #     parser = PDFParser(book)
    #     docs = PDFDocument(parser)
    #     outlines = docs.get_outlines()_
    #     for (level, title, dest, a, se) in outlines
    #         print (level, title)


#Want to test out if a hit comes up, run the script directly with the -f and full file path
if __name__ == "__main__":
    global filename
    filename = ""

    def usage():
        print ("Please specify the filename you would like to parse with -f")
        sys.exit(2)

    def arguments():
        opts, args = getopt.getopt(sys.argv[1:], "hf:d", ["help", "file="])
        if len(args) != 1:
            Logger.log("No arguments passed!", 'trace')
            usage()
        for opt, arg in opts:
            Logger.log("Args: {0}".format(arg), 'trace')
            if opt in ("-h", "--help"):
                usage()
            elif opt == '-d':
                global _debug
                _debug = 1
            elif opt in ("-f", "--file"):
                global filename
                filename = arg
            else:
                usage()

    Logger.log("Parsing Arguments", 'debug')
    arguments()
    processor = PostProcessor()
    processor.nameresolver(filename)
    Author = processor.bookauthor
    Title = processor.booktitle
    Type = str(processor.fileext).upper()
    print("Author: {0}\nTitle: {1}\nFormat: {2}".format(Author, Title, Type))