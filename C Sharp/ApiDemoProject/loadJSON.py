import json
import csv
import codecs
import cStringIO


class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

target = open ("G:\\TestArea\\ApiDemoProject\\JSON.txt")
writtenCSV = open("G:\\TestArea\\ApiDemoProject\\decodedJSON.csv", "wb")

line = target.readline()
##writer = csv.writer(writtenCSV)
writer = UnicodeWriter(writtenCSV)

while line:
     paramList = []
     decoded = json.loads(line)
     if len(decoded) > 0:
          paramList.append(decoded["ManufacturerPartNumber"])
##          print decoded[0]["TechnicalDetails"]
          if decoded["TechnicalDetails"]!= None:
               for paramItem in decoded["TechnicalDetails"]:
                    paramStr =  paramItem["Name"] + ": " + paramItem["Value"].strip('\n')
                    paramList.append(paramStr)

          writer.writerow(paramList)

     line = target.readline()

target.close()
writtenCSV.close()

print "Finished"
