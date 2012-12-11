import random, pylab

numTrials = 10000

def generateScores(numTrials):
    scoreList = []
    for i in range(numTrials):
        scoreList.append(round(random.gauss(72.5, 7.5)))
    return scoreList

def plotQuizzes():
    scores = generateScores(numTrials)
    pylab.hist(scores, bins = 7)
    pylab.title('Distribution of Scores')
    pylab.xlabel('Final Score')
    pylab.ylabel('Number of Trials')
    pylab.show()

if __name__ == '__main__':
    plotQuizzes()
