import random, pylab

def sampleQuizzes():
    midterm1 = []
    midterm2 = []
    finaltest = []
    finalGrade = []
    rangeList = []
    
    for i in range(10000):
        midterm1.append(round(random.uniform(0.5,0.8)*100))
        midterm2.append(round(random.uniform(0.6,0.9)*100))
        finaltest.append(round(random.uniform(0.55,0.95)*100))

    for n in range(10000):
        finalGrade.append((.25 * midterm1[n]) + (.25 * midterm2[n]) + (.5 * finaltest[n]))

    for j in finalGrade:
        if j >= 70 and j <= 75:
            rangeList.append(j)

    return (len(rangeList) + 0.0) / len(finalGrade)