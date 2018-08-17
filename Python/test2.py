import re

pattern = re.compile(r'(<dt>.+</dt>)')

pattern = re.compile(r'<a\s+href="(.+)">(.+)</a>')

string = '<dt><dt>9.4 <a href="ch09s04.html#e94">use dict</a></dt>'
find = pattern.search(string)

print find.group(1)
print find.group(2)



