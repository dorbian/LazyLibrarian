#Name: Processor.py
#Function: Processes a file name to figure out the writer, title of the book, and possibly the type and quality

#Script stuff
from lazylibrarian import logger

__author__ = 'dorbian'
__version__ = "1.0"

#Imports
import sys
import os
import getopt

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
        logger.log("Processing file: {0}".format(os.path.abspath(filen)), 'info')
        head, tail = (os.path.split(filen))
        p = re.match('(?x)(?P<TITLE>.+?) (?P<EXT>\.[^.]*$|$)', tail)
        self.filetitle = p.group('TITLE')
        self.fileext = str(p.group('EXT')).split('.')[1]
        logger.log("Filename found: {0}".format(self.filetitle), 'debug')
        logger.log("Type found: {0}".format(self.fileext), 'debug')
        if self.fileext.lower() == "mobi":
            self.mobiparser()
            logger.log("Processing file as a {0} file".format(self.fileext.lower()), 'debug')
        elif self.fileext.lower() == "epub":
            self.epubparser()
            logger.log("Processing file as a {0} file".format(self.fileext.lower()), 'debug')
        # elif self.fileext.lower() == "pdf":
        #     self.pdfparser()
        #     Logger.log("Processing file as a {0} file".format(self.fileext.lower()), 'debug')

    def mobiparser(self):
        import lib.mobi
        book = lib.mobi.Mobi(self.filepath)
        book.parse()
        self.bookauthor = book.author()
        self.booktitle = book.title()
        logger.log("Author found: {0}".format(self.bookauthor), 'debug')
        logger.log("Title found: {0}".format(self.booktitle), 'debug')

    def epubparser(self):
        import lib.epub
        book = lib.epub.open_epub(self.filepath, mode=None)
        self.bookauthor = book.opf.metadata.creators[0][0]
        self.booktitle = book.opf.metadata.titles[0][0]
        logger.log("Author found: {0}".format(self.bookauthor), 'debug')
        logger.log("Title found: {0}".format(self.booktitle), 'debug')

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
        sys.exit(0)

    def arguments():
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hf:dt", ["help", "file=", "debug", "trace"])
        except getopt.GetoptError as e:
            print("Error in arguments")
            sys.exit(0)
        else:
            if len(args) != 1:
                logger.log("No arguments passed!", 'trace')
                usage()
            for opt, arg in opts:
                logger.log("Args: {0}".format(arg), 'trace')
                if opt in ("-h", "--help"):
                    logger.log("Showing help", 'trace')
                    usage()
                elif opt == ('-d', "--debug"):
                    logger.log("Debug enabled", 'trace')
                    global _debug
                    _debug = True
                elif opt == ("-t", "--trace"):
                    logger.log("Trace enabled", 'trace')
                    global _trace
                    _trace = True
                elif opt in ("-f", "--file"):
                    logger.log("Loading file: {0}".format(arg), 'trace')
                    global filename
                    filename = arg
                else:
                    usage()

    logger.log("Parsing Arguments", 'debug')
    logger.log("Checking for arguments", 'trace')
    arguments()
    logger.log("Starting post processor", 'trace')
    processor = PostProcessor()
    logger.log("Starting Name Resolver", 'trace')
    processor.nameresolver(filename)
    Author = processor.bookauthor
    Title = processor.booktitle
    Type = str(processor.fileext).upper()
    print("Author: {0}\nTitle: {1}\nFormat: {2}".format(Author, Title, Type))