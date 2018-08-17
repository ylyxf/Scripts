__author__ = 'frank.qiu'

with open("G:\\test.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content]

Date2File = {}
for line in content:
    if "Date:" in line:
        fileList = []
        date = line
        Date2File[date] = fileList

    if "Modified :" in line:
        if Date2File.has_key(date):
            Date2File[date].append(line)

        else:
            Date2File[date] = [line]

file2Date = {}
for date in Date2File:
    for action in Date2File[date]:
        if file2Date.has_key(action):
            file2Date[action].append(date)

        else:
            file2Date[action] = [date]

for action in file2Date:
    print action + " " + str(file2Date[action])


