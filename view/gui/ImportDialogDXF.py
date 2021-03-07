from PyQt5.QtWidgets import QFileDialog
from qt_material import apply_stylesheet

from dxf.DXF import DXF


class ImportDialogDXF(QFileDialog):
    """
        Class to open a custom dialog and change its names to brazilian portuguese
    """
    def __init__(self, showbase):
        super().__init__()
        apply_stylesheet(self, theme='dark_teal.xml')
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, extensions = QFileDialog.getOpenFileName(self, "Importar DXF", "", "DXF Files (*.dxf)",
                                                           options=options)
        if fileName:
            DXF(showbase).read_dxf(fileName)