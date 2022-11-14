from os import walk
from bank_parser_kotaksavings import KotakSavingsParserOld
from bank_parser_kotaksavings import KotakSavingsParserNew
from bank_parser_kotakcc import KotakCCParser
from bank_parser_hdfcsavings import HDFCSavingsParser
from bank_parser_hdfccc import HDFCCCParser
from bank_parser_icicisavings import ICICISavingsParser

class Parser:

    data = set([])

    def __init__(self, directory):
        self.dir = directory
        _, _, filenames = next(walk(self.dir))
        for f in filenames:
            self.readfile(self.dir, f)

    def readfile(self, directory, filename):
        f = filename.lower()
        fn = directory + "/" + filename

        # TODO: This list below needs to be updated according to the format of 
        # your own exported report formats.

        if f.startswith("") and f.endswith("csv"):
            self.data.update(KotakSavingsParserNew(fn).parse())
        
        if f.startswith("report") and f.endswith("csv"):
            self.data.update(KotakSavingsParserOld(fn).parse())
        
        if f.startswith("") and f.endswith("xls"):
            self.data.update(HDFCSavingsParser(fn).parse())
        
        if f.startswith("xxxxx") and f.endswith("pdf"):
            self.data.update(KotakCCParser(fn).parse())

        if f.startswith("") and f.endswith("pdf"):
            self.data.update(HDFCCCParser(fn).parse())
        
        if f.startswith("optransactionhistory") and f.endswith("xls"):
            self.data.update(ICICISavingsParser(fn).parse())