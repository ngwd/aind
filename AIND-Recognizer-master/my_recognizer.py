import warnings
from asl_data import SinglesData
import arpa


def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       probabilities is a list of dictionaries where each key a word and value is Log Liklihood
           [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            ]
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    probabilities = []
    guesses = []

    for i in range(len(test_set.wordlist)):
        X, lengths = test_set.get_item_Xlengths(i)
        word = test_set.wordlist[i] 
        
        scores = {}
        for k in models.keys():
            logL = float("-inf") 
            try:
                logL = models[k].score(X, lengths)
            except:
                print("fail to score {} with model {}".format(word, k))
                continue
            scores[k] = logL

        probabilities.append(scores)

    for scores in probabilities:
        max_item = max((scores[s], s) for s in scores)
        guesses.append(max_item[1])
       
    return probabilities, guesses

def recognize_plus_slm(models: dict, test_set: SinglesData):

    lm_models = arpa.loadf("devel-lm-M3.sri.lm")
    #lm_models = arpa.loadf("ukn.3.lm")
    lm = lm_models[0]  # ARPA files may contain several models.

    """
    lm.p("in the end")
    lm.log_s("in the end")
    """

    warnings.filterwarnings("ignore", category=DeprecationWarning)
    warnings.filterwarnings("ignore", category=RuntimeWarning)

    probabilities = []
    guesses = []
    gi = 0
    for sn in test_set.sentences_index.keys():
        for si in range(len(test_set.sentences_index[sn])):
            X, lengths = test_set.get_item_Xlengths(test_set.sentences_index[sn][si])
            if si>1:
                prefix3 = guesses[gi-2]+ " " + guesses[gi-1]  
                prefix2 = guesses[gi-1]
            elif si==1:  
                prefix3 = "<s> " + guesses[gi-1]
                prefix2 = guesses[gi-1]
            else : # si==0
                prefix3 = ""
                prefix2 = "<s>"
            #print ("p2 and p3 are {}, {}".format(prefix2, prefix3))

            score = float("-inf")
            w = ""
            for k in models.keys():
                #logL, logS = 0., 0.
                logL, logS = float("-inf"), float("-inf") 
                try:
                    logL = models[k].score(X, lengths)
                except:
                    pass

                try:
                    if prefix3 != "":
                        logS = lm.log_s(prefix3 + " " + k)
                    if logS==float("-inf"):
                        logS = lm.log_s(prefix2+" "+k)
                    if logS==float("-inf"):
                        logS = lm.log_s(k)
                    if logS==float("-inf"):
                        logS = -99.
                except:
                    pass
                alpha = 1.
                if alpha*logL + logS > score:
                   score = alpha*logL + logS  
                   w = k
                #print("logL is {}, logS is {} ".format(logL, logS))
            guesses.append(w)
            gi += 1
        # end of the sentences_index loop
    # end of the keys loop
    return probabilities, guesses

