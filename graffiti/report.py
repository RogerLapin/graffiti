import fileinput
import shutil
import base64
import os
import datetime


class Report(object):

    def __init__(self):
        self.charts = ''

    def write(self, html):
        dirname = os.path.dirname(os.path.abspath(__file__))
        src = os.path.join(dirname, 'template.html')
        shutil.copyfile(src, html)

        with fileinput.FileInput(html, inplace=True, backup='.bak') as file:
            for line in file:
                tag_date = '{{GRAFFITI_DATE}}'

                if tag_date in line:
                    date =  str(datetime.datetime.now())
                    print(line.replace(tag_date, date), end='')
                    continue

                tag_charts = '{{GRAFFITI_CHARTS}}'
                if tag_charts in line:
                    print(line.replace(tag_charts, self.charts), end='')
                    continue

                print(line)

    def add(self, graph):
        chart =  ('<hr>\n'
                  '<h2><a>{}</a></h2>\n'
                  '{}\n'
                  '<br/><br/>\n').format(graph.req.cfg.request, graph.req.cfg.description)

        for img in graph.imgs:
            i = base64.b64encode(open(img,'rb').read()).decode('utf-8')
            tag = ('<img src="data:image/png;base64,{}" align="center"/>\n'
                   '<br/><br/>\n'
                    .format(i))
            chart += tag

        self.charts += chart