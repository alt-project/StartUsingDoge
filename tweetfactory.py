import random
import re
import math

class TweetFactory:
    def __init__(self,template_file):
        self.template_file = template_file

    def get_random_line_from_txt(self,filename):
        file = open(filename, 'r')
        line = self.random_line(file).strip()
        return line

    def random_line(self,file):
        line = next(file)
        for num, aline in enumerate(file):
            if random.randrange(num + 2): continue
            line = aline
        return line

    def spin(self,s):
        r = re.compile('{([^{}]*)}')
        while True:
            s, n = r.subn(self.spinner_select, s)
            if n == 0: break
        return s.strip()

    def spinner_select(self,wordList):
        words = wordList.group(0).replace("{", "").replace("}", "").split("|")
        randomNumber = int(math.ceil(random.random() * len(words))) - 1
        return words[randomNumber]

    def build_tweet(self):
        template = self.get_random_line_from_txt(self.template_file)
        return self.spin(template)