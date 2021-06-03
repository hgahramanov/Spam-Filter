import email
import re
import os
from collections import Counter

def read_classifications_from_file(path):
    lst = []
    with open(path, 'r+') as sth:
       a = sth.readlines()

    for i in range  (len(a)):
        lst.append(a[i].rstrip('\t\n').replace('\n', ' ').split(' '))

    dict = {t[0]:t[1] for t in lst}


    return dict



def write_classification_to_file(cls_dict, fpath):
    with open(fpath, 'a') as sth:
       for key, value in cls_dict.items():
           sth.write(key)
           sth.write(" ")
           sth.write(value)
           sth.write("\n")


            
def filenumber(path, label):
    dict = read_classifications_from_file(os.path.join(path, "!truth.txt"))
    filelist = ([k for k, v in dict.items() if v == label])
    return len(filelist)


def makecounter(fpath, label):
    dict = read_classifications_from_file(os.path.join(fpath, "!truth.txt"))
    filelist =([k for k, v in dict.items() if v == label])
    counts = Counter()
    for i in filelist:
        with open(os.path.join(fpath, i), 'tr', encoding="latin1") as sth:
            b = email.message_from_string(sth.read())
            body = b.get_payload()
            if not isinstance(body, str):
                body = readmultimail(body)



            counts.update(list(set(getwords(body))))

    return counts

def getwords(text):
    #separating html junk, symbols and many more
    pat = r"<[^>]*>|\-|&[a-zA-Z0-9]*|['|`][A-Za-z]+|\n"
    text = re.sub(pat, '', str(text.lower()))
    #getting rid of hyperlinks
    pat = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    text = re.sub(pat, '', str(text))
    #getting rid of email adresses
    pat = r'[\w\.-]+@[\w\.-]+'
    text = re.sub(pat, '', str(text))
    #dividing into words
    pat = r'[a-z]+'
    compiledre = re.compile(pat)
    tokens = compiledre.findall(text)
    return tokens

#if email is multipart the following function is used
def readmultimail(mail):
    payload = ""
    for m in mail:
        p = m.get_payload()
        if isinstance(p, str):
            payload += p
        else:
            payload += readmultimail(p)
    return payload


