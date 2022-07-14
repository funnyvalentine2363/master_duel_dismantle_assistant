from PyQt6.QtWidgets import QApplication, QMainWindow, QLineEdit, QVBoxLayout, QWidget, QScrollArea, QTextEdit
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


import sys
import json

from card_info import *


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
        with open('deck_type.txt', 'r', encoding='gbk') as r:
            for line in r.readlines():
                line = line.strip().split(":")

                if len(line) > 1:
                    self.eng_to_cn_dic[line[0]] = line[0]+"("+line[-1]+")"
                else:
                    self.eng_to_cn_dic[line[0]] = line[0]

        self._create_database()

        for key in id_to_all.keys():
            deck_info = CardInfo(id_to_all[key]["rarity"], id_to_all[key]
                                 ["deck_used"], id_to_all[key]["deck_types_info"])
            if not deck_info.valid():
                continue

            for language in ["en-US", "ja-JP", "zh-CN", "zh-TW", "ko-KR"]:
                if language+"_name" in id_to_all[key].keys():
                    db = self._rarity2database(deck_info.rarity)
                    db.insert(id_to_all[key][language+"_name"], deck_info)

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

    def _create_database(self):
        self.databaseUR = CardInfoDB()
        self.databaseSR = CardInfoDB()
        self.databaseN = CardInfoDB()
        self.databaseR = CardInfoDB()
        self.databaseList = [
            self.databaseUR,
            self.databaseSR,
            self.databaseR,
            self.databaseN,
        ]

        self.database = CardInfoDBGroup(self.databaseList)

        self.rarity_id = {
            'UR': 0,
            'SR': 1,
            'R': 2,
            'N': 3,
        }

    def _rarity2database(self, rarity: str):
        return self.databaseList[self.rarity_id[rarity]]

    def text_changed(self):
        html = ''
        results = self.database.search(
            self.input.text(), [True, True, False, False])
        for name, card_info in results:
            if name is None:
                return
            if card_info.rarity is None:
                rarity = "无"
            prefix = self._card_info_to_prefix(name, card_info)
            html += self.to_html(prefix)
        self.label.setText(html)

    def _card_info_to_prefix(self, name: str, card_info: CardInfo):
        prefix = {"卡名: " + name: {},
                  "稀有度: " + card_info.rarity: {}}

        if card_info.deck_info is None:
            prefix["携带此卡的卡组: 无"] = None

        else:
            for deck in card_info.deck_used:
                deck_name = deck.strip()
                if deck_name in self.eng_to_cn_dic:
                    deck_name = self.eng_to_cn_dic[deck_name]

                if deck in card_info.deck_info:
                    #prefix[deck] = {"3×": deck_info[deck][0], "2×": deck_info[deck][1], "1×": deck_info[deck][2], "0×":deck_info[deck][3],"平均携带":deck_info[deck][4]}
                    prefix[deck_name] = card_info.deck_info[deck]
                else:
                    prefix[deck_name] = ['?']*5
        return prefix

    def to_html(self, dic):
        html = "<thead><tr style='text-align: center;'><th></th><th>3×</th><th>2×</th><th>1×</th><th>0×</th><th>平均携带</th></tr></thead>"
        html += "<tbody>"
        for key in dic.keys():
            html += "<tr>"
            html += "<th>"+key+"</th>"
            if dic[key]:
                for str in dic[key]:
                    html += "<td>"+str+"</td>"
            else:
                for _ in range(5):
                    html += "<td>" + "</td>"
        html += "</tbody>"
        return "<table border='1'>" + html+"</table>\n"


app = QApplication(sys.argv)
QApplication.setFont(QFont('微软雅黑', 10), "QTextEdit")

window = MainWindow()
window.resize(400, 600)
window.show()

app.exec()
