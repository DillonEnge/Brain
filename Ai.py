import random

class Node():
    nodeCount = 1
    nodeChain = []

    def __init__(self, outputValue = 0):
        self.id = Node.nodeCount
        self.outputValue = outputValue
        self.threshold = 0
        self.activated = False
        Node.nodeCount += 1

    def __str__(self):
        return "Thresh: " + "{0:.3f}".format(self.threshold)

    def update(self):
        if self.activated:
            self.activated = False

    def initialize(self, rowSize):
        self.threshold = float(1) / rowSize

    def tryActivate(self):
        if random.random() <= self.threshold:
            self.activated = True
            Node().nodeChain.append(self)

class Network():
    def __init__(self, nodesPerLayer, middleLayers):
        self.net = []
        self.nodes = self.populateNodes(nodesPerLayer)
        self.resultNodes = self.populateOutputNodes(nodesPerLayer)
        self.net.append(self.nodes)
        for i in range(0, middleLayers):
            self.net.append(self.populateNodes(nodesPerLayer))
        self.net.append(self.resultNodes)
        self.initialize()

    def initialize(self):
         for row in self.net:
             for node in row:
                 node.threshold = float(1) / len(row)

    def update(self):
        for row in self.net:
            for node in row:
                node.update()

    def populateNodes(self, count):
        returnNodes = []
        for i in range(0,count):
            returnNodes.append(Node())
        return returnNodes

    def populateOutputNodes(self, count):
        returnNodes = []
        for i in range(0,count):
            returnNodes.append(Node(i + 1))
        return returnNodes

        
class Brain():
    def __init__(self, nodesPerLayer, layers):
        self.createNet(nodesPerLayer, layers)
        self.initialized = True

    def __str__(self):
        returnString = ""
        for line in self.network.net:
            returnString += "\n"
            for node in line:
                returnString += str(node) + ","
        return returnString

    def createNet(self, nodesPerLayer, layers):
        self.network = Network(nodesPerLayer, layers - 2)

    def startTraining(self, iterations):
        if not hasattr(self, 'initialized'):
            print "Network must be initialized before training can begin."
            raise SystemExit
        for i in range(0,iterations):
            self.runTrainingCycle((i == 0), i)
            print "Training cycle " + str((i + 1)) + " completed."

    def runTrainingCycle(self, initialRun, iteration):
        rowCount = 0
        nodeActivated = False
        for row in self.network.net:
            rowCount += 1
            while not nodeActivated:
                for node in row:
                    node.tryActivate()
                    if node == row[len(row)-1]:
                        if len(Node().nodeChain) >= rowCount:
                            if len(Node().nodeChain) == rowCount:
                                nodeActivated = True
                                for node in row:
                                    if node == Node().nodeChain[rowCount - 1]:
                                        node.threshold += (.01 * (len(row) - 1) / ((iteration + float(1))/2))
                                        print "Node " + str(node.id) + "s thresh is now " + "{0:.3f}".format(node.threshold)
                                    else:
                                        node.threshold -= (.01 / ((iteration + float(1))/2))
                                        print "Node " + str(node.id) + "'s thresh is now " + "{0:.3f}".format(node.threshold)
                            else:
                                difference = len(Node().nodeChain) - rowCount + 1
                                del Node().nodeChain[(len(Node().nodeChain)-difference):(len(Node().nodeChain)-1)]
                self.network.update()
            nodeActivated = False

mainBrain = Brain(5,10)
mainBrain.startTraining(5)
print mainBrain















              
