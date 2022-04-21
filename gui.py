from PyQt6.QtWidgets import QApplication, QMainWindow, QLineEdit, QVBoxLayout, QWidget,QScrollArea,QTextEdit
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


import sys
import json
class trie():
    def __init__(self):
        self.dic = {}
        self.end = False

    def insert(self,s,rarity,deck,deck_info):
        d = self
        s = s.lower()
        for char in s:
            d = d.dic
            if char not in d.keys():
               d[char] = trie()
            d = d[char]
        d.end = True
        d.rarity = rarity
        d.deck = deck
        d.name = s
        d.deck_info = deck_info

    def search(self,s):
        if not s:
            return None,None,None,None
        s = s.lower()
        d = self
        i = 0
        while not d.end:
            d = d.dic
            if i<len(s):
                if s[i] not in d.keys():
                    return None,None,None,None
                else:
                    d = d[s[i]]
                    i+=1
            else:
                if d:
                    for key in d.keys():
                        d = d[key]
                        break
                else:
                    return None,None,None,None
        return d.name,d.rarity,d.deck,d.deck_info


# id_to_all = json.load(open("data.json", "r"))
# t = trie()
# for key in id_to_all.keys():
#     for language in ["en-US","ja-JP","zh-CN","zh-TW","ko-KR"]:
#         if language+"_name" in id_to_all[key].keys():
#             t.insert(id_to_all[key][language+"_name"],id_to_all[key]["rarity"],id_to_all[key]["deck_used"],id_to_all[key]["deck_types_info"])
#
# name,rarity,deck,deck_info = t.search("幻")
# print(name,rarity,deck,deck_info)

class ScrollLabel(QScrollArea):

    # constructor
    def __init__(self, *args, **kwargs):
        QScrollArea.__init__(self, *args, **kwargs)

        # making widget resizable
        self.setWidgetResizable(True)

        # making qwidget object
        content = QWidget(self)
        self.setWidget(content)

        # vertical box layout
        lay = QVBoxLayout(content)

        # creating label
        self.label = QTextEdit(content)

        # setting alignment to the text
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # making label multi-line

        # adding label to the layout
        lay.addWidget(self.label)

    # the setText method
    def setText(self, text):
        # setting text to the label
        self.label.setText(text)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        id_to_all = json.load(open("data.json", "r"))
        self.eng_to_cn_dic = {}
        with open('deck_type.txt', 'r') as r:
            for line in r.readlines():
                line = line.strip().split(":")
                if len(line) > 1:
                    self.eng_to_cn_dic[line[0]] = line[0]+"("+line[-1]+")"
                else:
                    self.eng_to_cn_dic[line[0]] = line[0]
        self.trie = trie()
        for key in id_to_all.keys():
            for language in ["en-US","ja-JP","zh-CN","zh-TW","ko-KR"]:
                if language+"_name" in id_to_all[key].keys():
                    self.trie.insert(id_to_all[key][language+"_name"],id_to_all[key]["rarity"],id_to_all[key]["deck_used"],id_to_all[key]["deck_types_info"])

        self.setWindowTitle("dismantle Assistant")
        self.label = ScrollLabel()
        self.input = QLineEdit()
        self.input.textChanged.connect(self.text_changed)

        layout = QVBoxLayout()
        layout.addWidget(self.input)
        layout.addWidget(self.label)

        container = QWidget()
        container.setLayout(layout)

        # Set the central widget of the Window.
        self.setCentralWidget(container)

    def text_changed(self):
        name,rarity,decks,deck_info = self.trie.search(self.input.text())
        if name is None:
            return
        if rarity is None:
            rarity = "无"
        #"3×": [], "2×": [], "1×": [], "0×:[]"
        prefix = {"卡名: "+name:{},
                  "稀有度: "+rarity:{}}
        if not decks:
            prefix["携带此卡的卡组: 无"] = {}
        else:
            for deck in decks:
                if deck_info and deck in deck_info.keys():
                    #prefix[deck] = {"3×": deck_info[deck][0], "2×": deck_info[deck][1], "1×": deck_info[deck][2], "0×":deck_info[deck][3],"平均携带":deck_info[deck][4]}
                    try:
                        prefix[self.eng_to_cn_dic[deck.strip()]] = deck_info[deck]
                    except:
                        print(deck)
                        continue
                else:
                    prefix[self.eng_to_cn_dic[deck]] = ['?']*5
                    #prefix[deck] = {"3×": "?", "2×": "?", "1×": "?","0×": "?", "平均携带": "?"}
        # import pandas as pd
        # df = pd.DataFrame(data=prefix)
        # df = df.fillna(' ').T
        # print(df.to_html())
        # print(self.to_html(prefix))
        self.label.setText(self.to_html(prefix))

    def to_html(self,dic):
        html = "<thead><tr style='text-align: center;'><th></th><th>3×</th><th>2×</th><th>1×</th><th>0×</th><th>平均携带</th></tr></thead>"
        html+="<tbody>"
        for key in dic.keys():
            html+="<tr>"
            html+="<th>"+key+"</th>"
            if dic[key]:
                for str in dic[key]:
                    html+="<td>"+str+"</td>"
            else:
                for _ in range(5):
                    html += "<td>" + "</td>"
        html +="</tbody>"
        return "<table border='1'>" + html+"</table>"

app = QApplication(sys.argv)
QApplication.setFont(QFont('微软雅黑', 10), "QTextEdit")

window = MainWindow()
window.resize(400,600)
window.show()

app.exec()
