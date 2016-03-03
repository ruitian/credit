# -*- coding: utf-8 -*-
import urllib
import urllib2
import re


class Gpa():
    NUM = 0
    TABLE = None
    INFO = {}
    RET = {}

    def __init__(self, num):
        self.NUM = num

    def crawl(self):
        request_url = 'http://210.44.176.116/cjcx/zcjcx_list.php'

        postData = {
            'post_xuehao': self.NUM,
            'Submit': '提交'
        }

        data = urllib.urlencode(postData)

        req = urllib2.Request(request_url, data)
        rep = urllib2.urlopen(req)
        page = rep.read()
        return page

    def get_table(self):
        page = self.crawl()
        pattern = re.compile(
            '<td scope="col" align=".*" valign="middle" nowrap>&nbsp;(.*)</td>')
        self.TABLE = pattern.findall(page)
        return 0

    def get_user_info(self):
        self.INFO['id'] = self.TABLE[0]
        self.INFO['name'] = self.TABLE[1]
        self.INFO['sex'] = self.TABLE[2]
        self.INFO['grade'] = self.TABLE[3]
        self.INFO['acachemy'] = self.TABLE[4]
        self.INFO['major'] = self.TABLE[5]
        self.INFO['class'] = self.TABLE[6]
        self.INFO['stream'] = self.TABLE[7]
        self.INFO['level'] = self.TABLE[8]
        self.INFO['length'] = self.TABLE[9]
        self.INFO['teacher-training'] = self.TABLE[10]
        self.INFO['foreign'] = self.TABLE[11]

    def get_score(self):
        type = []
        course = []
        credit = []
        old_score = []
        new_score = []
        i = 13
        all = len(self.TABLE)
        while(i+16 <= all):
            type.append(self.TABLE[i+3].replace(' ', ''))
            course.append(self.TABLE[i+5].replace(' ', ''))
            credit.append(self.TABLE[i+7].replace(' ', ''))
            old_score.append(self.TABLE[i+10].replace(' ', ''))
            new_score.append(self.TABLE[i+11].replace(' ', ''))
            i += 16
        Gpa.RET['type'] = type
        Gpa.RET['course'] = course
        Gpa.RET['credit'] = credit
        Gpa.RET['old_score'] = old_score
        Gpa.RET['new_score'] = new_score

    def score_to_number(self, text):
        '''将二级和五级成绩转换成数字成绩,或者将成绩转换成浮点型'''
        sc_dict = {
            '合格': 70,
            '不合格': 0,
            '优秀': 95,
            '良好': 84,
            '中等': 73,
            '及格': 62,
            '不及格': 0,
            '缺考': 0,
            '禁考': 0,
            '退学': 0,
            '缓考（时': 0,
            '缓考': 0,
            '休学': 0,
            '未选': 0,
            '作弊': 0,
            '取消': 0,
            '免修': 60,
            '-': 0,
            '': 0
        }
        try:
            num = sc_dict[text]
            return num
        except:
            try:
                num = float(text)
                return num
            except:
                return -1

    def get_credit(self):
        not_accept = []
        totle_credit = 0
        totle_score = 0
        ave_score = 0
        type = self.RET['type']
        course = self.RET['course']
        credit = self.RET['credit']
        old_score = self.RET['old_score']
        new_score = self.RET['new_score']

        set_course = []
        set_score = []
        set_credit = []

        print new_score
        i = 0
        all = len(type)
        while(i < all):
            if type[i] == '公选课':
                i += 1
                continue

            if credit[i] == '':
                credit[i] = '0'

            s = self.score_to_number(old_score[i])
            s2 = self.score_to_number(new_score[i])

            if s > s2:
                max = s
            else:
                max = s2
            #  判断重修
            if course[i] in set_course:
                position = set_course.index(course[i])
                if max < 60:
                    i += 1
                    continue
                if max > float(set_score[position]):
                    totle_credit -= float(set_credit[position])
                    totle_score -= float(set_score[position]) * float(
                        set_credit[position])
                    set_score[position] = max
                else:
                    i += 1
                    continue
            else:
                set_course.append(course[i])
                set_score.append(max)
                set_credit.append(credit[i])
            totle_credit += float(credit[i])
            if s < 60:
                if s2 >= 60:
                    totle_score += 60 * float(credit[i])
                else:
                    not_accept.append(course[i])
            else:
                totle_score += float(credit[i]) * s
            i += 1
        if totle_credit == 0:
            ave_score = 0
        else:
            ave_score = totle_score / totle_credit
        print ave_score


if __name__ == '__main__':
    num = raw_input('输入学号:')
    gpa = Gpa(num)
    gpa.get_table()
    gpa.get_user_info()
    gpa.get_score()
    gpa.get_credit()
