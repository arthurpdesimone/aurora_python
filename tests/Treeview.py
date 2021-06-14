import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QWidget, QTreeView, QVBoxLayout, QMenu, QMainWindow, QTreeWidget, \
    QAbstractItemView, QShortcut, QInputDialog, QTreeWidgetItem


class MyMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.tree = QTreeWidget(self)

        self.tree.setSelectionMode(QAbstractItemView.SingleSelection)

        insertKey = QShortcut(QKeySequence(Qt.Key_Insert), self.tree)
        insertKey.activated.connect(self.itemInsert)
        editKey = QShortcut(QKeySequence(Qt.Key_Return), self.tree)
        editKey.activated.connect(self.itemEdit)
        self.setCentralWidget(self.tree)
        self.tree.setHeaderLabel('Tree')
        i = QTreeWidgetItem(self.tree, ['Parent'])
        self.tree.addTopLevelItem(i)
        for x in range(5):
            QTreeWidgetItem(i, ['Child {}'.format(x)])

    def itemInsert(self):
        text, ok = QInputDialog.getText(self, "Add Child", "Enter child name:")
        if ok and text != "":
            if len(self.tree.selectedItems()) > 0:
                QTreeWidgetItem(self.tree.selectedItems()[0], [text])
            else:
                QTreeWidgetItem(self.tree, [text])

    def itemEdit(self):
        if self.tree.selectedItems():
            item = self.tree.selectedItems()[0]
            text, ok = QInputDialog.getText(self, "Edit Child", "Modify name:", QLineEdit.Normal, item.text(0))
            if ok and text != "":
                item.setText(0, text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = MyMainWindow()
    ui.show()
    sys.exit(app.exec_())