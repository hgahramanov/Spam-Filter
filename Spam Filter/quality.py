from collections import namedtuple
import utils
import os

def compute_confusion_matrix(truth_dict, pred_dict, pos_tag="SPAM", neg_tag="OK"):
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    for i in truth_dict:

        if pred_dict[i] == truth_dict[i]:
            if pred_dict[i] == pos_tag:
                tp = tp + 1
            elif pred_dict[i] == neg_tag:
                tn = tn + 1
        if pred_dict[i]!= truth_dict[i]:
            if pred_dict[i] == pos_tag:
                fp = fp + 1
            if pred_dict[i] == neg_tag:
                fn = fn + 1
    ConfMat = namedtuple("ConfMat", ["tp", "tn", "fp",  "fn"])
    mat = ConfMat(tp, tn, fp, fn)

    return mat

def quality_score(tp, tn, fp, fn):
    score = (tp+tn)/(tp+tn+fn+(10*fp))

    return score
def compute_quality_for_corpus(corpus_dir):

    truth = utils.read_classifications_from_file(os.path.join(corpus_dir, '!truth.txt'))
    prediction = utils.read_classifications_from_file(os.path.join(corpus_dir, '!prediction.txt'))
    CONFMAT =compute_confusion_matrix(truth, prediction,'SPAM', 'OK' )
    tp = CONFMAT.tp
    tn = CONFMAT.tn
    fp = CONFMAT.fp
    fn = CONFMAT.fn

    return (quality_score(tp, tn, fp, fn))

if __name__ == '__main__':

    truth_dict={'em1': 'SPAM', 'em2':'SPAM', 'em3':'OK', 'em4': 'OK'}
    pred_dict ={'em1': 'SPAM', 'em2':'OK', 'em3':'OK', 'em4': 'SPAM'}
    compute_confusion_matrix(truth_dict, pred_dict, pos_tag='SPAM', neg_tag='OK' )
    quality_score(2,2,0,0)
    print(compute_quality_for_corpus('C:\\Users\\123\\Desktop\\corpus'))


