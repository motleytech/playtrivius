from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pprint import pprint as pp

import time
import random
import json
import os

qaMap = {}
driver = None
qaFileName = 'qadata.json'

datafile = None
try:
    datafile = open(qaFileName)
    qaMap = json.loads(datafile.read())
    datafile.close()
except:
    pass
finally:
    if datafile is not None:
        datafile.close()

def startBrowser(url):
    global driver
    options = webdriver.ChromeOptions()
    this_folder = os.path.dirname(os.path.abspath(__file__))
    profile_folder = os.path.join(this_folder, 'profile')
    options.add_argument("user-data-dir={}".format(profile_folder))

    driver = webdriver.Chrome(chrome_options=options)
    driver.get(url)

def waitForPlayNow():
    while True:
        elem = driver.find_elements_by_css_selector('a.btn-sm')
        el = [x for x in elem if x.text == "Play Now"]
        if len(el) > 0:
            return el[0]
        time.sleep(0.3)
    return None

def clickPlayNow(el):
    el.click()
    time.sleep(3)

def waitForQuestion(num):
    print "Starting wait for question {}".format(num)
    while True:
        elem = driver.find_elements_by_css_selector('h5.question-number')
        question_title = "Question #{} of 5".format(num)
        el = [x for x in elem if x.text == question_title]
        if len(el) == 1:
            time.sleep(0.2)
            elem = driver.find_elements_by_css_selector('h3.question')
            if len(elem) == 1:
                return elem[0].text
            else:
                print "Found too many question elements"
                pp([x.text for x in elem])

        elif len(el) > 1:
            print "Found too many question title elements"
            pp([x.text for x in el])
        print "Trying to find question {}. Looping.".format(num)
        time.sleep(0.5)
    return None

def getAnswer(question):
    return qaMap.get(question, None)

def waitForAnswerChoices():
    while True:
        elems = driver.find_elements_by_css_selector('div.answer')
        answers = [x.find_elements_by_tag_name('a')[0] for x in elems]
        visibleAnswers = [x for x in answers if "ng-hide" not in x.get_attribute('class')]
        if len(visibleAnswers) == 4:
            return visibleAnswers
        time.sleep(0.3)
    return None

def clickOnAnswer(answer):
    answerDivs = driver.find_elements_by_css_selector('div.answer')
    answers = [x.find_elements_by_tag_name('a')[0] for x in answerDivs]
    pRight = 0.75
    randNum = random.random()
    if (answer is None) or (randNum > pRight):
        if answer is None:
            print "Don't know answer. Guessing"
        else:
            print "Taking a guess this time"
        ch = random.choice(range(4))
        ansCh = answers[ch]
        ansCh.click()
        print "Clicking {}".format(ansCh.text)
    else:
        print "Know answer..."
        ansCh = [ans for ans in answers if ans.text == answer][0]
        ansCh.click()
        print "Clicking {}".format(ansCh.text)

    return None

def waitForResults():
    print "waiting for result",
    while True:
        print ".",
        answers = driver.find_elements_by_css_selector('a.correct')
        if len(answers) == 1:
            result = answers[0].text
            print "  Returning answer: {}".format(result)
            return result
        time.sleep(0.3)
    return None


def saveAnswer(question, answer):
    if question not in qaMap:
        qaMap[question] = answer

        data = json.dumps(qaMap)
        dataFile = open(qaFileName, 'w')
        dataFile.write(data)
        dataFile.close()


def playGame():
    for x in range(0, 5):
        question = waitForQuestion(x+1)
        answer = getAnswer(question)

        time.sleep(4)

        waitForAnswerChoices()
        time.sleep(1 + 2.5*random.random())
        clickOnAnswer(answer)
        correctAnswer = waitForResults()
        saveAnswer(question, correctAnswer)

def waitForPlayAgain():
    while True:
        elems = driver.find_elements_by_css_selector('a.btn-md')
        if len(elems) > 0:
            els = [x for x in elems if x.text == "Play again"]
            if len(els) > 0:
                el = els[0]
                return el
        time.sleep(0.3)
    return None

def clickPlayAgain(el):
    el.click()
    time.sleep(1)

def main():
    startBrowser("https://triviusgame.com/topic/technology/python")

    time.sleep(2)

    el = waitForPlayNow()
    if el is None:
        print "could not find play now button"
        return

    time.sleep(1)
    clickPlayNow(el)

    numGames = 99999

    for x in range(numGames):
        time.sleep(2)
        playGame()
        el = waitForPlayAgain()
        time.sleep(2)
        clickPlayAgain(el)

if __name__ == '__main__':
    main()
