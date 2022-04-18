from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget,QScrollArea
from PyQt6.QtCore import Qt
import sys
import json
class trie():
    def __init__(self):
        self.dic = {}
        self.end = False

    def insert(self,s,rarity,deck):
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

    def search(self,s):
        if not s:
            return None,None,None
        s = s.lower()
        d = self
        i = 0
        while not d.end:
            d = d.dic
            if i<len(s):
                if s[i] not in d.keys():
                    return None,None,None
                else:
                    d = d[s[i]]
                    i+=1
            else:
                if d:
                    for key in d.keys():
                        d = d[key]
                        break
                else:
                    return None,None,None
        return d.name,d.rarity,d.deck


# id_to_all = json.load(open("data.json", "r"))
# t = trie()
# for key in id_to_all.keys():
#     for language in ["en-US","ja-JP","zh-CN","zh-TW","ko-KR"]:
#         if language+"_name" in id_to_all[key].keys():
#             t.insert(id_to_all[key][language+"_name"],id_to_all[key]["rarity"],id_to_all[key]["deck_used"])
#
#
#
# name,rarity,deck = t.search("a")
# print(name,rarity,deck)

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
        self.label = QLabel(content)

        # setting alignment to the text
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        # making label multi-line
        self.label.setWordWrap(True)

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
        self.trie = trie()
        for key in id_to_all.keys():
            for language in ["en-US","ja-JP","zh-CN","zh-TW","ko-KR"]:
                if language+"_name" in id_to_all[key].keys():
                    self.trie.insert(id_to_all[key][language+"_name"],id_to_all[key]["rarity"],id_to_all[key]["deck_used"])
        self.setFixedWidth(200)
        self.setFixedHeight(400)
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
        name,rarity,deck = self.trie.search(self.input.text())
        if name is None:
            return
        if rarity is None:
            rarity = "无"
        if deck == []:
            deck = "无"
        else:
            deck = '\n'.join(deck)
        self.label.setText("卡名:"+name+'\n'+"稀有度:"+rarity+'\n'+"携带此卡的卡组:\n"+deck)


app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()
