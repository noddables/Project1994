'''
Created on Nov 24, 2018
@author: Charlie
'''
'''FUNCTIONS'''
def GetHeaders(ReadFilePath):
    "Takes ReadFilePath for a CSV file (e.g. C:\\FileName.csv) and returns the header row for that file"
    import csv
    with open(ReadFilePath,'rb') as ReadFile:
        Reader = csv.reader(ReadFile)
        Headers = Reader.next()
        return Headers
def GetRow(ReadFilePath,RowIndex):
    "Takes ReadFilePath for a CSV file (e.g. C:\\FileName.csv) and a RowIndex x and returns row occurence x for that file"
    import csv
    openFile = open(ReadFilePath,'rb')
    reader = csv.reader(openFile)
    TargetRow = [row for idx, row in enumerate(reader) if idx == RowIndex][0]
    return TargetRow
def CleanString(InputTerm):
    "Takes an InputTerm ( HelloWorlD   ) and returns it capitalized and stripped of leading and trailing spaces (HELLOWORLD)"
    OutputTerm = InputTerm
    OutputTerm = OutputTerm.strip()
    OutputTerm = OutputTerm.upper()
    return OutputTerm
def TheseMatch(SearchTerm,ResultTerm):
    "Takes, cleans, and compares two terms (SearchTerm and ResultTerm); returns True if they match, returns False if they don't"
    if CleanString(SearchTerm) ==  CleanString(ResultTerm):
        return True
    else:
        return False
'''  next three are typing shortcuts because they'll get used a lot, but you could give them more meaningful names'''
def U(InputTerm):
    "Takes an InputTerm (HelloWorlD) and returns it as a Unicode string (u'HelloWorlD')"
    OutputTerm = "u'" + InputTerm + "'"
    return OutputTerm
def Q(InputTerm):
    "Takes an InputTerm (HelloWorlD) and returns it as a single-quoted string ('HelloWorlD')"
    OutputTerm = "'" + InputTerm + "'"
    return OutputTerm
def P(InputTerm):
    "Takes and InputTerm >HelloWorlD< and wraps it in parens (HelloWorlD)"
    return "(" + InputTerm + ")"
def IsNumber(InputTerm):
    try:
        float(InputTerm)
        return True
    except ValueError:
        return False
def InsertValue(InputTerm):
    "Takes an InputTerm (4/HelloWorlD) and returns numbers unqualified (4) and strings qualified (u'HelloWorlD')"
    if IsNumber(InputTerm):
        return InputTerm
    else:
        return Q(InputTerm)
def CleanInt(InputTerm):
    "Takes an InputTerm ( 4   ) and returns it stripped of leading and trailing spaces and converted to an int (4)"
    OutputTerm = InputTerm
    OutputTerm = OutputTerm.strip()
    OutputTerm = int(OutputTerm)
    return OutputTerm
'''Tests'''
#print Q("HelloWorlD")
#print Value("HelloWorlD")