#!/usr/bin/python
from pymeta.grammar import OMeta2Grammar, OMetaBase
from pymeta.builder import TreeBuilder, moduleFromGrammar
import json
import pprint
class OMeta():
    def __init__(self, key):
        gkey = ''.join(["'" + x + "'" for x in list(key)])

        grammar = r"""
start = (gettext:x | anything -> None)+:xs -> [x for x in xs if x != None]
gettext = '(' gettext_key space+ string:s ')' -> s
string  = space* '"' ('\\' '"' | ~'"' :x)*:xs '"' -> ''.join(xs)
gettext_key = """+gkey+"""
space = anything:c ?(c.isspace())  -> c
"""
        G = OMeta2Grammar(grammar)
        tree = G.parseGrammar('evaluator', TreeBuilder)
        self.Parser = moduleFromGrammar(tree, 'evaluator', OMetaBase, {})

    def parse(self, code):
        parser = self.Parser(code)
        res = parser.apply("start")[0]
        #pprint.pprint(res)
        return res

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
    o = OMeta("__")
    matches = [json.dumps(s) for s in o.parse(fulltext)]

    #print filename + " matched: " + str(len(matches))
#    print fulltext

#    print str(len(matches))
#    print matches
    return (filename, matches)

def writeOutput(matches, outputfileName):
    outputfile = file(outputfileName, "w")
    outputfile.write(header)
    outputfile.write("\n\n")

    #to avoid duplicates
    allMatches = []
    
    for fileAndMatches in matches:
        filename = fileAndMatches[0]
        fileMatches = fileAndMatches[1]
        for match in fileMatches: 
            if (match not in allMatches):
                outputfile.write("#: "+filename+":0\n")
                outputfile.write('msgid '+match+'\n')
                outputfile.write('msgstr ""\n\n')
                allMatches.append(match)
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

