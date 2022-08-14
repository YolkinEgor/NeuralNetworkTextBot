import re

print(
    re.findall(r'[А-Яа-я]+',
               'Один, два, три!\n'
               'hello, world!')
)
