#!python3
import sys
import numpy as np
from sklearn import metrics
import matplotlib.pyplot as plt
import postagger


def main():
    y_predict = []
    y_actual = []
    memo = dict()
    with open(sys.argv[1]) as file, open(sys.argv[2], 'w') as f:
    # with open('mf') as file, open('fefadsdfewa', 'w') as f:
        def fprint(*args):
            print(*args, file=f)
        counter = 0
        twiLine = []
        for line in file:
            if counter == 0: # get Twi
                twiLine = line.translate(str.maketrans('', '', '!,.?')).split()
            elif counter == 1: # get tags and compare
                allPos = [x.upper() for x in line.split()]
                allPos = [postagger.simpleTag.get(x, x) for x in allPos]
                assert len(allPos) == len(twiLine)
                y_actual += allPos # update the true values
                for i, word in enumerate(twiLine):
                    fprint("-- {} ---".format(word))
                    pos = allPos[i]
                    pos = postagger.simpleTag.get(pos, pos)
                    fprint(pos)
                    if word in memo:
                        possibilities = memo[word]
                    else:
                        possibilities = postagger.tag(word)
                        memo[word] = possibilities
                    fprint(possibilities)
                    if pos in possibilities:
                        fprint(pos)
                        y_predict.append(pos)
                    else: # if incorrect, assign it to whoever is the strongest
                        falsePos = postagger.get_highest_ranked(possibilities)
                        fprint(falsePos)
                        y_predict.append(falsePos)
            counter = (counter+1)%3
        confusion_matrix = metrics.confusion_matrix(y_actual, y_predict)
        fprint(confusion_matrix)

        total_accuracy = np.trace(confusion_matrix)/np.sum(confusion_matrix)
        fprint("Total accuracy:", total_accuracy)

        labels = sorted(set(y_actual)|set(y_predict))
        diag = np.diagonal(confusion_matrix)

        precision = dict(zip(labels, diag/np.sum(confusion_matrix, axis=0)))
        recall    = dict(zip(labels, diag/np.sum(confusion_matrix, axis=1)))
        fprint("TABLE")
        fprint("\tPOS & Precision & Recall\\\\\\hline")
        for k in precision:
            fprint("\t{} & {} & {}\\\\\\hline".format(k,round(precision[k], 3), round(recall[k], 3)))

    cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix, display_labels=labels)
    cm_display.plot()
    plt.show()
if __name__ == '__main__':
    main()