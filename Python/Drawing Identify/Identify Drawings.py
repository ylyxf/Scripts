__author__ = 'frank.qiu'
import matplotlib.pyplot as plt
class cLine():
    def __init__(self, start, end, label):
        self.start = start
        self.end = end
        self.label = label

    # def joint(self, 2ndLine):

A = cLine("a", "d", "A")
B = cLine("a", "b", "B")
C = cLine("b", "c", "C")
D = cLine("c", "d", "D")
E = cLine("a", "c", "E")

drawing = [A,B,C,D,E]
nodeList = []
for track in drawing:
    if track.start not in nodeList:
        nodeList.append(track.start)
    if track.end not in nodeList:
        nodeList.append(track.end)

print nodeList


# class line:
#     def __init__(self, start, end, label):
#         self.start = start
#         self.end = end
#         self.label = label
#
#     def equal(self, aLine):
#         if aLine.start == self.start:
#             if aLine.end == self.end:
#                 return 1
#
#         elif aLine.start == self.end:
#             if aLine.end == self.start:
#                 return 1
#
#         else:
#             return 0
#
#     def joint(self, aLine):
#         if not self.equal(aLine):
#             if self.start == aLine.start or self.start == aLine.end:
#                 return self.start
#             elif self.end == aLine.start or self.end == aLine.end:
#                 return self.end
#             else:
#                 return ""
#
#         else:
#             return ""
#
#     def duplicate(self):
#         newLine = line(self.start, self.end,self.lable)
#
#         return newLine
#
# class drawing():
#     def __init__(self, lines):
#         self.tracks = lines
#
#     def findConnectedTracks(self, aTrack):
#         connectedTrackList = []
#         for track in self.tracks:
#             if not track.equal(aTrack):
#                 if aTrack.joint(track):
#                     connectedTrackList.append(track)
#
#         return connectedTrackList
#
#     def findNextTrack(self, currentTrack, previousTrack):
#         connectedTracks = self.findConnectedTracks(currentTrack)
#         for connectedTrack in connectedTracks:
#             if not connectedTrack.equal(previousTrack):
#                 return connectedTrack
#
#     def isClosed(self):
#         if self.tracks:
#             startTrack = self.tracks[0]
#             connectedTracks = self.findConnectedTracks(startTrack)
#             if connectedTracks:
#                 currentTrack = connectedTracks[0]
#                 lastTrack = startTrack
#
#                 i = 0
#                 while i < len(self.tracks):
#                     nextTrack = self.findNextTrack(currentTrack, lastTrack)
#                     if nextTrack:
#                         lastTrack = currentTrack
#                         currentTrack = nextTrack
#                     else:
#                         return 0
#
#                     i += 1
#
#                 if nextTrack.joint(startTrack):
#                     return 1
#                 else:
#                     return 0
#
#     def equal(self, aDrawing):
#         if len(aDrawing.tracks)!= len(self.tracks):
#             return 0
#         else:
#             for trackToMatch in self.tracks:
#                 matchTrack = 0
#                 for trackMatched in aDrawing.tracks:
#                     if trackMatched.equal(trackToMatch):
#                         matchTrack = 1
#
#                 if not matchTrack:
#                     return 0
#
#             return 1
#
#     def drawThis(self):
#         ax = plt.subplot()
#         for track in self.tracks:
#             (xs,ys) = zip(*[track.start, track.end])
#             ax.plot(xs,ys,color = "blue")
#
#         ax.set_axis_off()
#         plt.show()
#
#     def duplicate(self):
#         newDrawing = drawing([])
#         for aTrack in self.tracks:
#             newTrack = aTrack.duplicate()
#             newDrawing.tracks.append(newTrack)
#
#         return newDrawing
#
#     def findNextTracksNotInDrawing(self, currentTrack):
#         connectedTracks = self.findConnectedTracks(currentTrack)
#         result = []
#         for connectedTrack in connectedTracks:
#             trackInDrawing = 0
#             for drawingTrack in self.tracks:
#                 if drawingTrack.equal(connectedTrack):
#                     trackInDrawing = 1
#                     break
#
#             if not trackInDrawing:
#                 result.append(connectedTrack)
#
#         return result
#
#     def findNextTracks(self, currentTrack, previousTrack):
#         connectedTracks = self.findConnectedTracks(currentTrack)
#         result = []
#         for connectedTrack in connectedTracks:
#             if not connectedTrack.equal(previousTrack):
#                 result.append(connectedTrack)
#
#         return result
#
#
# class route(drawing):
#     drawingList = []
#
#     def insertDrawing(self, newDrawing):
#         newDrawingFound = 1
#
#         for drawingToMatch in self.drawingList:
#             if newDrawing.equal((drawingToMatch)):
#                 newDrawingFound = 0
#                 break
#
#         if newDrawingFound:
#             self.drawingList.append(newDrawing.duplicate())
#
#
#     def findDrawings(self):
#         for startTrack in self.tracks:
#             connectedTracks = self.findConnectedTracks(startTrack)
#             for connectedTrack in connectedTracks:
#                 branchTrackList = [connectedTrack]
#                 newDrawingList = []
#
#                 while branchTrackList:
#                     currentTrack = branchTrackList.pop()
#                     if newDrawingList:
#                         newDrawing = newDrawingList.pop()
#                     else:
#                         newDrawing = drawing([startTrack])
#
#                     nextTracks = self.findNextTracks(currentTrack, newDrawing.tracks[-1])
#                     newDrawing.tracks.append(currentTrack)
#
#                     while nextTracks:
#                         for i in xrange(len(nextTracks)):
#                             if nextTracks[i].equal(startTrack):
#                                 self.insertDrawing(newDrawing.duplicate())
#                                 newDrawing.drawThis()
#                             else:
#                                 if i == 0:
#                                     nextTrack = nextTracks[i]
#
#                                 else:
#                                     branchTrackList.append((nextTracks[i]))
#                                     newDrawingList.append(newDrawing.duplicate())
#
#                             nextTracks = self.findNextTracks(nextTrack, newDrawing.tracks[-1])
#                             newDrawing.tracks.append(nextTrack.duplicate())
#
#
#
#     def drawAll(self):
#         for i in xrange(len(self.drawingList)):
#             ax = plt.subplot(1,i + 1,1)
#             ax.set_axis_off()
#             for track in self.drawingList[i].tracks:
#                 (xs,ys) = zip(*[track.start, track.end])
#                 ax.plot(xs,ys,color = "blue")
#         plt.show()
#
# a = line([0,0], [3,0], "a")
# b = line([3,0], [3,3], "b")
# c = line([3,3], [0,3], "c")
# d = line([0,3], [3,0], "d")
# e = line([0,3], [0,0], "e")
#
# # testDrawing = drawing([d,e,a])
# # testDrawing.drawThis()
# # print testDrawing.isClosed()
# testRoute = route([a,b,c,d,e])
# testRoute.findDrawings()
# # testRoute.drawAll()
# for someDrawing in testRoute.drawingList:
#     someDrawing.drawThis()
#
# # print "is closed " + str(testDrawing.isClosed())