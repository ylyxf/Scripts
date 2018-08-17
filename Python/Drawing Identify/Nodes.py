__author__ = 'frank.qiu'
class node:
    def __init__(self, preNodeName, nextNodeNameList, nodeName):
        self.preNodeName = preNodeName
        self.nextNodeNameList = nextNodeNameList
        self.nodeName = nodeName

def findNextNodes(thisNode, tree):
    matchNodes = []
    for nextNode in thisNode.nextNodeNameList:
        for nodeToMatch in tree:
            if nextNode == nodeToMatch.nodeName:
                matchNodes.append(nodeToMatch)
                break

    return matchNodes

def findNodeByName(nodeName, tree):
    for nodeToMatch in tree:
        if nodeToMatch.nodeName == nodeName:
            return nodeToMatch

D = node("b", [], "d")
E = node("b", [], "e")
B = node("a", ["d", "e"], "b")
F = node("a", [], "f")
C = node("a", ["g"], "c")
A = node("", ["b", "f", "c"], "a")
G = node("c", [], "g")

someTree = [A, B, F,C,D,E, G]
startNode = A

#breadth first
# nextLevelNodes = findNextNodes(A, someTree)
# while nextLevelNodes:
#     currentLevelNodes = nextLevelNodes
#     nextLevelNodes = []
#     for currentNode in currentLevelNodes:
#         print currentNode.nodeName
#         for nextNodeName in currentNode.nextNodeNameList:
#             nextNode = findNodeByName(nextNodeName, someTree)
#             nextLevelNodes.append(nextNode)

#depth first
branchNodeList = []
branchRouteList = []
branchNodeList.append(startNode)
branchRouteList = []
while branchNodeList:
    currentNode = branchNodeList.pop()
    if branchRouteList:
        currentRoute = branchRouteList.pop()
    else:
        currentRoute = []
    currentRoute.append(currentNode.nodeName)
    # print currentNode.nodeName

    nextNodes = findNextNodes(currentNode, someTree)
    while nextNodes:
        for i in xrange(len(nextNodes)):
            if i == 0:
                nextNode = nextNodes[i]
                # print nextNode.nodeName
            else:
                branchNodeList.append(nextNodes[i])
                newRoute = []
                newRoute.extend(currentRoute)
                branchRouteList.append(newRoute)

        currentRoute.append(nextNode.nodeName)
        nextNodes = findNextNodes(nextNode, someTree)


    print currentRoute