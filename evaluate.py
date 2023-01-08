import sys
from string import punctuation
from sklearn import metrics
import postagger

y_predict = []
y_actual = []
with open(sys.argv[1]) as file:
    counter = 0
    twiLine = []
    for line in file:
        if counter == 0: # get Twi
            twiLine = line.translate(str.maketrans('', '', punctuation)).split()
        elif counter == 1: # check
            pos = line.split()
            assert len(pos) == len(twiLine)
            y_actual += pos # update the true values
            for word in twiLine:
                possibilities = postagger.tag(word)
                if pos in possibilities:
                    y_predict.append(pos)
                else: # TODO: pick the highest ranked pos option 
                    y_predict.append(possibilities[0])
        elif counter == 2: # new line
            pass
        counter = (counter+1)%3

confusion_matrix = metrics.confusion_matrix(y_actual, y_predict)
print(confusion_matrix)