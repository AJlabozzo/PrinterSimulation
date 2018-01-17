from Queue import Queue
import random


# Input file is assigned to config and output assigned to fileOut
fileOut = open("sim_out.txt",'w')
config = open("sim_config.txt")


# Printer class  and definitions was created by the proffesor for use in assignment as well as the Task class 
class Printer:
    def __init__(self, ppm):
        self.pagerate = ppm
        self.currentTask = None
        self.timeRemaining = 0

    def tick(self):
        if self.currentTask != None:
            self.timeRemaining = self.timeRemaining - 1
            if self.timeRemaining <= 0:
                self.currentTask = None

    def busy(self):
        if self.currentTask != None:
            return True
        else:
            return False

    def startNext(self,newtask):
        self.currentTask = newtask
        self.timeRemaining = newtask.getPages() * 60/self.pagerate

class Task:
    def __init__(self,time,minTask,maxTask):
        self.timestamp = time
        self.pages = random.randrange(minTask,maxTask+1)

    def getStamp(self):
        return self.timestamp

    def getPages(self):
        return self.pages

    def waitTime(self, currenttime):
        return currenttime - self.timestamp

def newPrintTask():
    num = random.randrange(1,181)
    if num == 180:
        return True
    else:
        return False

def fileclose():   # A function to close the files
    config.close() 
    fileOut.close()

def Simulaton(Duration,PPM1,PPM2,numberOfSimulations,minTask,maxTask,printerNum):

    averageWaitList = []
    
    # first forloop runs for the number of simulations specified
    for i in range(numberOfSimulations):

        # Declares printer objects, waitingtimes list, and printQueue for each simulation 
        labprinter = Printer(PPM1)
        labprinter2 = Printer(PPM2)
        waitingtimes = []
        printQueue = Queue()
            
        # This loop will be for the individual simulation and runs for the number of Seconds Specified
        for currentSecond in range(Duration):
                    
            # If the number of printers is 1, printer 1 is free, and there is a task in the queue
            # Printer 1 will be given the next task in the queue then printer calls tick method
            if  printerNum == 1:
    
                if newPrintTask(): 
                    task = Task(currentSecond,minTask,maxTask)
                    printQueue.enqueue(task)

                if (not labprinter.busy()) and (not printQueue.is_empty()):
                    nexttask = printQueue.dequeue()
                    waitingtimes.append(nexttask.waitTime(currentSecond))
                    labprinter.startNext(nexttask)

                labprinter.tick() 

            # Else If the number of printers is two
            # the program will run a series of if statements to decided which printer to run
            # then both printers call tick method
            elif printerNum == 2:

                if newPrintTask(): 
                    task = Task(currentSecond,minTask,maxTask)
                    printQueue.enqueue(task)
                
                # If both printers are free the task goes to the printer with the higher Page Per Minute value
                if (not labprinter2.busy()) and (not labprinter.busy()) and (not printQueue.is_empty()):
                    nexttask = printQueue.dequeue()
                    waitingtimes.append(nexttask.waitTime(currentSecond))
                    if PPM1 >= PPM2:
                        labprinter.startNext(nexttask)
                    else:
                        labprinter2.startNext(nexttask)
                        
                # Else if labprinter 1 is free the next task goes to printer 1
                elif (not labprinter.busy()) and labprinter2.busy() and (not printQueue.is_empty()):
                    nexttask = printQueue.dequeue()
                    waitingtimes.append(nexttask.waitTime(currentSecond))
                    labprinter.startNext(nexttask)
                    
                # Else if labprinter2 is free the next task goes to printer 2
                elif (not labprinter2.busy()) and labprinter.busy() and (not printQueue.is_empty()):
                    nexttask = printQueue.dequeue()
                    waitingtimes.append(nexttask.waitTime(currentSecond))
                    labprinter2.startNext(nexttask)

                # if both printers are busy then the task should remain in printer Q
                # both printers will tick and if one frees up then it will be processed
                                       
                labprinter.tick()
                labprinter2.tick()

        # as we calculate the averageWait of each simulation append that averageWait to a list
        averageWait = abs(sum(waitingtimes)/len(waitingtimes))
        averageWaitList.append(averageWait)
        
        fileOut.write("\nAverage Wait %6.2f secs %3d tasks remaining." \
                         %(averageWait,printQueue.size()))
        
    # once the simulations are finished we calculate the average by
    # the sum of all averageWaits divided that by the number of simulations
    overalAverage = sum(averageWaitList)/numberOfSimulations
    fileOut.write("\nOverall average wait time: %6.2f secs"  %(overalAverage))


def main():
    configList = []

    #for loop to iterate through the input file and appends each line to configList
    for line in config:
       try:
           configList.append(int(line)) # try statement catches anything out of integer format in sim_config thats being appended to configList
       except:   
          return print('Format error sim_config value: '+ line[:-1] +', Exiting')

    configsize = len(configList)

    # all elements from sim_config being assigned to variables
    Duration = configList[0]  # Duration is the time in seconds
    numberOfSimulations = configList[1]
    minTask = configList[2] # the minimum and maximum task sizes
    maxTask = configList[3]
    printerNum = configList[4] # printerNum = number of printers
    PPM1 = configList[5]                
    if printerNum == 2: #PPM = Page Per Minute
        PPM2 = configList[6]
    else:
        PPM2 = -1

    # if statements to catch invalid inputs from sim_config.txt
    # if a condition is met then a error message is writen to file out and the files are closed.
    if printerNum == 1 and configsize == 7:
        fileOut.write("sim_config size error: When there is only one printer, do not assign a page per minute value to a second printer")
        fileclose()
  
    elif configsize > 7 or configsize < 6:
        fileOut.write("sim_config size error must have 6 or 7 integers")
        fileclose()
    
    elif Duration < 3600 or Duration > 36000 :
        fileOut.write("Invalid Duration: Valid range is 3600-36000 seconds")
        fileclose()
    
    elif numberOfSimulations < 1 or numberOfSimulations > 100:
        fileOut.write("Invalid Number of Simulations: Valid range is 1-100")
        fileclose()
            
    elif minTask < 1 or minTask > 100:
        fileOut.write("Invalid Minimum Task Size: Valid range is 1-100")
        fileclose()
            
    elif maxTask < 1 or maxTask > 100:
        fileOut.write("Invalid Maximum Task Size: Valid range is 1-100")
        fileclose()

    elif maxTask < minTask:
        fileOut.write("Invalid Task value: Maximum task must greater than minimum task's value")
        fileclose()
        
    elif printerNum < 1 or printerNum > 2: 
        fileOut.write("Invalid Number of Printers: Please input 1 or 2 printers")
        fileclose()
        
    elif printerNum == 2 and configsize <= 6:
        fileOut.write("Error: Missing Page Rate value for Printer 2")
        fileclose()

    elif PPM1 > 50 or PPM1 < 1 :
        fileOut.write("Invalid Page Per Minute value for printer one: Valid range is 1-50")
        fileclose()

    elif PPM2 > 50 or PPM2 < 1 and printerNum == 2:
        fileOut.write("Invalid Page Per Minute value for printer two: Valid range is 1-50")
        fileclose()
    
    else: #If all the variables are valid run Simulation.
        Simulaton(Duration,PPM1,PPM2,numberOfSimulations,minTask,maxTask,printerNum)
        fileclose()
          
if __name__ == "__main__":
    main()
