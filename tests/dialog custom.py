import sys

from PyQt5 import QtCore, QtWidgets


class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        button = QtWidgets.QPushButton("Press me")
        button.clicked.connect(self.on_clicked)

        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(button)

    @QtCore.pyqtSlot()
    def on_clicked(self):
        dialog = QtWidgets.QFileDialog(
            self,
            "Remove File",
            "path",
            "*.pdf",
            supportedSchemes=["file"],
            options=QtWidgets.QFileDialog.DontUseNativeDialog,
        )
        self.change_button_name(dialog)
        dialog.findChild(QtWidgets.QTreeView).selectionModel().currentChanged.connect(
            lambda: self.change_button_name(dialog)
        )
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            filename = dialog.selectedUrls()[0]
            print(filename)

    def change_button_name(self, dialog):
        for btn in dialog.findChildren(QtWidgets.QPushButton):
            if btn.text() == self.tr("&Open"):
                QtCore.QTimer.singleShot(0, lambda btn=btn: btn.setText("Remove"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    w = Widget()
    w.show()

    sys.exit(app.exec_())