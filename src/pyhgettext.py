#!/usr/bin/python

import re

header = "\n".join(["# Translation file",
                               "",
                               "msgid \"\"",
                               "msgstr \"\"",
                               "",
                               "\"Project-Id-Version: PACKAGE VERSION\\n\"",
                               "\"Report-Msgid-Bugs-To: \\n\"",
                               "\"POT-Creation-Date: 2009-01-13 06:05-0800\\n\"",
                               "\"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\\n\"",
                               "\"Last-Translator: FULL NAME <EMAIL@ADDRESS>\\n\"",
                               "\"Language-Team: LANGUAGE <LL@li.org>\\n\"",
                               "\"MIME-Version: 1.0\\n\"",
                               "\"Content-Type: text/plain; charset=UTF-8\\n\"",
                               "\"Content-Transfer-Encoding: 8bit\\n\"",
                               ""])


def getMatches(filename, keyword):
    inputfile = file(filename,"rU")
    lines = inputfile.readlines()
    inputfile.close()
    fulltext = "".join(lines)
    # when not using U (universal newline support), search for keyword+" \r?\n?.*\"(.*)\""
    matches = re.findall(keyword+" \n?.*\"(.*)\"", fulltext)
#    print fulltext

#    print str(len(matches))
#    print matches
    return (filename, matches)

def writeOutput(matches, outputfileName):
    outputfile = file(outputfileName, "w")
    outputfile.write(header)
    outputfile.write("\n\n")
    
    for fileAndMatches in matches:
        filename = fileAndMatches[0]
        fileMatches = fileAndMatches[1]
        for match in fileMatches: 
            outputfile.write("#: "+filename+":0\n")
            outputfile.write('msgid "'+match+'"\n')
            outputfile.write('msgstr ""\n\n')
    outputfile.flush()
    outputfile.close()


if __name__ == "__main__":
    import sys
    args = sys.argv[1:]

#    print args
    cmdOutput = 'messages.pot'
    cmdKeyword = '__'
    try: 
        outputFlagIndex = args.index('-o')
        args.remove('-o')
        cmdOutput = args[outputFlagIndex]
        args.remove(cmdOutput)
    except:
        print 'Error finding flag -o: '+str(args)

    try:
        keywordFlagIndex = args.index('-k')
        args.remove('-k')
        cmdKeyword = args[keywordFlagIndex]
        args.remove(cmdKeyword)
    except:
        print 'Error finding flag -k: '+str(args)
    
    fileMatches = map((lambda filename: getMatches(filename,cmdKeyword)), args)
    writeOutput(fileMatches, cmdOutput)

