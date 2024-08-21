from PyQt6.QtWidgets import QMainWindow,QApplication,QFileDialog,QMessageBox,QFontDialog,QColorDialog
from notepad import Ui_MainWindow
from PyQt6.QtGui import QIcon,QFont
from PyQt6.QtCore import QSize,QFileInfo,Qt
from PyQt6.QtPrintSupport import QPrinter,QPrintDialog,QPrintPreviewDialog
import sys
class NotePadWindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.setWindowIcon(QIcon('Notepad/images/notepad.png'))
        self.setStyleSheet("background-color:#eacf80")
        self.textEdit.setStyleSheet("color:#0b605e")


        self.actionSave.triggered.connect(self.save_file)
        self.actionNew.triggered.connect(self.file_new)
        self.actionOpen.triggered.connect(self.file_open)
        self.actionPrint.triggered.connect(self.file_print)
        self.actionPrint_Prewiew.triggered.connect(self.preview_dialog)
        self.actionExport_PDF.triggered.connect(self.file_export)
        self.actionQuir.triggered.connect(self.file_quite)
        self.actionUndo.triggered.connect(self.textEdit.undo)
        self.actionRedo.triggered.connect(self.textEdit.redo)
        self.actionCopy.triggered.connect(self.textEdit.copy)
        self.actionCut.triggered.connect(self.textEdit.cut)
        self.actionPaste.triggered.connect(self.textEdit.paste)
        self.actionBold.triggered.connect(self.text_bold)
        self.actionItalic.triggered.connect(self.text_italic)
        self.actionUnderline.triggered.connect(self.text_underline)
        self.actionLeft.triggered.connect(self.align_left)
        self.actionRight.triggered.connect(self.align_right)
        self.actionCenter.triggered.connect(self.align_center)
        self.actionJustify.triggered.connect(self.align_justify)
        self.actionFont.triggered.connect(self.font_dialog)
        self.actionColor.triggered.connect(self.color_dialog)
        self.actionAbout_App.triggered.connect(self.about_app)

    def maybe_save(self):
        if not self.textEdit.document().isModified():
            return True
        ret =QMessageBox.warning(self,"Application","The document has been modified.\n Do you want to save your changes ?"
                                 ,QMessageBox.StandardButton.Save|QMessageBox.StandardButton.Discard|QMessageBox.StandardButton.Cancel)
        if ret ==QMessageBox.StandardButton.Save:
            return self.save_file()
        if ret == QMessageBox.StandardButton.Cancel:
            return False
        return True
    def save_file(self):
        filename = QFileDialog.getSaveFileName(self,"Save File")
        if filename[0]:
            f=open(filename[0],'w')

            with f:
                text = self.textEdit.toPlainText()
                f.write(text)

                QMessageBox.about(self,"Save File","File has been saved")
    
    def file_new(self):
        if self.maybe_save():
            self.textEdit.clear()

    def file_open(self):
        fname = QFileDialog.getOpenFileName(self,"Open File",'/home')
        if fname[0]:
            f =open(fname[0],'r')
            with f:
                data = f.read()
                self.textEdit.setText(data)
    def file_print(self):
        printer=QPrinter(QPrinter.PrinterMode.HighResolution)
        dialog=QPrintDialog(printer)

        if dialog.exec() == QPrintDialog.DialogCode.Accepted:
            self.textEdit.print(printer)

    def preview_dialog(self):
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        preview = QPrintPreviewDialog(printer,self)
        preview.paintRequested.connect(self.file_printPreview)
        preview.exec()

    def file_printPreview(self,printer):
        self.textEdit.print(printer)

    def file_export(self):
        fn, _ =QFileDialog.getSaveFileName(self,"Export PDF","PDF File(.pdf) ;; All File()")
        if fn!="":
            if QFileInfo(fn).suffix()=="":fn+='.pdf'
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
            printer.setOutputFileName(fn)
            self.textEdit.document().print(printer)
    def file_quite(self):
        self.close()
    def text_bold(self):
        font = QFont()
        font.setBold(True)
        self.textEdit.setFont(font)
    def text_italic(self):
        font = QFont()
        font.setItalic(True)
        self.textEdit.setFont(font)
    def text_underline(self):
        font = QFont()
        font.setUnderline(True)
        self.textEdit.setFont(font)
    def align_left(self):
        self.textEdit.setAlignment(Qt.AlignmentFlag.AlignLeft)
    def align_right(self):
        self.textEdit.setAlignment(Qt.AlignmentFlag.AlignRight)
    def align_center(self):
        self.textEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
    def align_justify(self):
        self.textEdit.setAlignment(Qt.AlignmentFlag.AlignJustify)
    def font_dialog(self):
        font,ok=QFontDialog.getFont()
        if ok:
            self.textEdit.setFont(font)
    def color_dialog(self):
        color = QColorDialog.getColor()
        self.textEdit.setTextColor(color)
    def about_app(self):
        QMessageBox.about(self,"About App","This is a simple Notepad application with PyQt6.\n Expire end of day: 21/8/2024")

app =QApplication(sys.argv)
note=NotePadWindow()
sys.exit(app.exec())

