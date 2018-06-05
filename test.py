# __author: Lambert
# __date: 2018/6/5 17:44
import os

with open(os.path.join(os.path.dirname(__file__), 'massage_manager/settings.py'), encoding='utf8') as readme:
    README = readme.read()
    print(README)
