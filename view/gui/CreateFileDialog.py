from PyQt5.QtWidgets import QFileDialog
from qt_material import apply_stylesheet

class CreateFileDialog(QFileDialog):
    """
        Class to open a custom dialog and change its names to brazilian portuguese
    """
    def __init__(self):
        super().__init__()
        apply_stylesheet(self, theme='dark_teal.xml')
        self.setDefaultSuffix('json')
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, extensions = QFileDialog.getSaveFileName(self, "Salvar ou abrir arquivo inicial", "", "JSON Files (*.json)",
                                                           options=options)
        self.file = fileName