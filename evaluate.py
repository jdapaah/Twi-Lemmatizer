#!python3
# import sys
from sklearn import metrics
import matplotlib.pyplot as plt
import postagger

y_predict = []
y_actual = []
# with open(sys.argv[1]) as file:
with open('corpora/small.txt') as file:
    counter = 0
    twiLine = []
    for line in file:
        if counter == 0: # get Twi
            twiLine = line.translate(str.maketrans('', '', '!,.?')).split()
        elif counter == 1: # check
            allPos = [x.upper() for x in line.split()]
            allPos = [postagger.simpleTag.get(x, x) for x in allPos]
            assert len(allPos) == len(twiLine)
            y_actual += allPos # update the true values
            for i, word in enumerate(twiLine):
                print("-- {} ---".format(word))
                pos = allPos[i]
                pos = postagger.simpleTag.get(pos, pos)
                print(pos)
                possibilities = postagger.tag(word)
                print(possibilities)
                if pos in possibilities:
                    print(pos)
                    y_predict.append(pos)
                else: # if incorrect, assign it to whoever is the strongest
                    falsePos = postagger.get_highest_ranked(possibilities)
                    print(falsePos)
                    y_predict.append(falsePos)
        counter = (counter+1)%3

confusion_matrix = metrics.confusion_matrix(y_actual, y_predict)
print(confusion_matrix)
cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix, display_labels=sorted(set(y_actual)|set(y_predict)))
cm_display.plot()
plt.show()