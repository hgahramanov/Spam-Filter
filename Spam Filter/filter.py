import email
import math
import quality
import utils
import  os


SPAM = "SPAM"
HAM = "OK"
spamicityham = {}
spamicityspam={}


class MyFilter():
    def __init__(self):
        self.spamicityspam = {}
        self.spamicityham = {}




    def train(self, path):
        hamcounter = utils.makecounter(path, HAM)
        spamcounter = utils.makecounter(path, SPAM)

        numspam= utils.filenumber(path, SPAM)
        numham = utils.filenumber(path, HAM)
        #finding spamicity
        for word in spamcounter:
            self.spamicityspam[word] = spamcounter[word]/(spamcounter[word] + hamcounter[word]*numspam/numham)
        for word in hamcounter:
            self.spamicityham[word] = hamcounter[word] / (hamcounter[word] + spamcounter[word] * numham / numspam)



    def test(self, path):
        files = os.listdir(path)
        results = {}
        for fpath in files:
            if (fpath == "!truth.txt") | (fpath == "!prediction.txt"):
                continue
            with open(os.path.join(path, fpath), 'tr', encoding="latin1") as sth:
                b = email.message_from_string(sth.read())
                body = b.get_payload()
                if not isinstance(body, str):
                    body = utils.readmultimail(body)
                words = utils.getwords(body)
                probspam = 0.0
                probham = 0.0
                #calculating probability using spamicities by adding logarithms
                for word in words:
                    if word in self.spamicityspam:
                        probspam += math.log(self.spamicityspam[word])
                    if word in self.spamicityham:
                        probham += math.log(self.spamicityham[word])
                if (probspam > probham):
                    results[fpath] = SPAM
                else:
                    results[fpath] = HAM
        utils.write_classification_to_file(results, path + "/!prediction.txt")
        print(quality.compute_quality_for_corpus(path))



        
if __name__ == '__main__':

    b = MyFilter()
    b.train('C:\\Users\\123\\Desktop\\1')

    b.test('C:\\Users\\123\\Desktop\\2')


