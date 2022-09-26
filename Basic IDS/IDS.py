#!/usr/bin/python

import sys
import statistics

eNames = []
eWeights = []
eBase = []
eTest = []
eAvg = []
eStdev = []
eDistances = []
threshold = 0 # Placeholder value

def main():
    task1()
    task2()
    task3()

def task3():
    testFile = open(sys.argv[3], 'r')
    lines = testFile.readlines();

    for line in lines:
        fillTest(line)

    distance = 0
    for i in eTest:
        for j in range(0, len(eNames)):
            distance = distance + (float(eWeights[j]) * float(abs(float(i[j]) - float(eAvg[j])) / float(eStdev[j])))
        eDistances.append(round(distance, 2))
        distance = 0

    print("\n\n")
    for i in range(0, len(eTest)):
        if eDistances[i] > threshold:
            alarm = "Yes"
        else:
            alarm =  "No"

        listLine  = ""
        listLine.join(eTest[i])
        print("Line " + str(i) + ":   ", end = "")
        for j in eTest[i]:
            print(str(j), end=" ")
        print("      Distance: " + str(eDistances[i]) + "     Alarm:" + alarm)

def fillTest(str):
    line = str.rstrip()[:-1].split(':')
    eTest.append(line)

def task1():
    eventFile = open(sys.argv[1], 'r')
    dataFile = open(sys.argv[2], 'r')

    # Fill lists with data from files
    # List indexes will corespond to specific elements in other lists
    lines = eventFile.readlines();
    fillEvents(lines[1])
    lines = dataFile.readlines();
    for line in lines:
        fillBase(line)
    fillAvg()
    fillStdev()

    # Output result of Task 1
    outputBaseInfo()

def task2():
    temp = 0
    for i in eWeights:
        temp = temp + float(i)
    global threshold
    threshold = 2 * temp

    print("\nThreshold = " + str(threshold))

def outputBaseInfo():
    print("\nOutput is formatted like so:\n")
    print("Event Name       Average -- Stdev -- Weight\n")

    for i in range(0, len(eNames)):
        line = eNames[i] + "       " + str(eAvg[i]) + " -- " + str(eStdev[i]) + " -- " + str(eWeights[i])

        print(line)


def fillEvents(str):
    line = str.rstrip()[:-1].split(':')
    i = 0

    while i < len(line):
        eNames.append(line[i])
        eWeights.append(line[i+1])
        i = i + 2

def fillBase(str):
    line = str.rstrip()[:-1].split(':')
    eBase.append(line)

def fillAvg():
    days = len(eBase)
    temp = 0

    for i in range(0, len(eNames)):
        for j in eBase:
            temp = temp + int(j[i])
        avg = temp / days
        eAvg.append(round(avg, 2))
        temp = 0

def fillStdev():
    temp = []
    for i in range(0, len(eNames)):
        for j in eBase:
            temp.append(int(j[i]))
        eStdev.append(round(statistics.stdev(temp), 2));
        temp.clear()


if __name__ == '__main__':
	main()