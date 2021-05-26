from framework import smoothingFramework as sf
import sys, os

def printException(ex, types):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    sf.Output.printBash("Catched exception for '{}'. \nException type: {}\nFile name: {}:{}".format(
        types, exc_type, exc_tb.tb_frame.f_code.co_filename, exc_tb.tb_lineno
        ), 'err')