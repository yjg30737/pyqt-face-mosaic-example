import os, sys

from findPathWidget import FindPathWidget
from imageView import SplittedImageView
from script import apply_mosaic_to_face, apply_mosaic_to_pedestrain

# Get the absolute path of the current script file
script_path = os.path.abspath(__file__)

# Get the root directory by going up one level from the script directory
project_root = os.path.dirname(os.path.dirname(script_path))

sys.path.insert(0, project_root)
sys.path.insert(0, os.getcwd())  # Add the current directory as well

from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QVBoxLayout, QWidget, QMessageBox, QListWidget, \
    QSplitter, QSizePolicy, QComboBox, QHBoxLayout
from PyQt5.QtCore import Qt, QCoreApplication, QThread, pyqtSignal
from PyQt5.QtGui import QFont

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)  # HighDPI support

QApplication.setFont(QFont('Arial', 12))


class Thread(QThread):
    generateFinished = pyqtSignal(str)

    def __init__(self, filename, cur_type):
        super(Thread, self).__init__()
        self.__filename = filename
        self.__cur_type = cur_type

    def run(self):
        try:
            dst_filename = os.path.basename(self.__filename)+'_result'+os.path.splitext(self.__filename)[-1]
            if self.__cur_type == 'Face':
                apply_mosaic_to_face(self.__filename, dst_filename)
            else:
                apply_mosaic_to_pedestrain(self.__filename, dst_filename)
            self.generateFinished.emit(dst_filename)
        except Exception as e:
            raise Exception(e)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.__initVal()
        self.__initUi()

    def __initVal(self):
        self.__filename_dict = {}

    def __initUi(self):
        self.setWindowTitle('PyQt Face Mosaic Example')

        findPathWidget = FindPathWidget()
        findPathWidget.getLineEdit().setPlaceholderText('Select the Directory including images...')
        findPathWidget.added.connect(self.__addFiles)
        findPathWidget.setAsDirectory(True)

        self.__fileListWidget = QListWidget()
        self.__fileListWidget.itemActivated.connect(self.__itemActivated)
        self.__fileListWidget.currentItemChanged.connect(self.__itemActivated)

        self.__mosaicTypeCmbBox = QComboBox()
        self.__mosaicTypeCmbBox.addItems(['Face', 'Ped'])

        self.__runBtn = QPushButton('Run')
        self.__runBtn.clicked.connect(self.__run)

        lay = QHBoxLayout()
        lay.addWidget(self.__mosaicTypeCmbBox)
        lay.addWidget(self.__runBtn)

        navWidget = QWidget()
        navWidget.setLayout(lay)

        self.__view = SplittedImageView(self)

        lay = QVBoxLayout()
        lay.addWidget(navWidget)
        lay.addWidget(self.__view)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        splitterRightWidget = QWidget()
        splitterRightWidget.setLayout(lay)

        splitter = QSplitter()
        splitter.addWidget(self.__fileListWidget)
        splitter.addWidget(splitterRightWidget)
        splitter.setHandleWidth(1)
        splitter.setChildrenCollapsible(False)
        splitter.setSizes([400, 600])
        splitter.setStyleSheet(
            "QSplitterHandle {background-color: lightgray;}")
        splitter.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)

        lay = QVBoxLayout()
        lay.addWidget(findPathWidget)
        lay.addWidget(splitter)

        mainWidget = QWidget()
        mainWidget.setLayout(lay)

        self.setCentralWidget(mainWidget)

        self.__runBtn.setEnabled(False)

    def __addFiles(self, dirname):
        self.__filename_dict.clear()
        self.__fileListWidget.clear()
        filenames = [os.path.join(dirname, filename) for filename in os.listdir(dirname) if
                     os.path.splitext(filename)[-1] in ['.png', '.jpg']]
        self.__fileListWidget.addItems(filenames)
        self.__runBtn.setEnabled(len(filenames) > 0)
        self.__fileListWidget.setCurrentRow(0)

    def __setItemToEachView(self, item):
        filename = item.text()
        self.__cur_src_filename = filename
        if self.__filename_dict.get(self.__cur_src_filename, '') == '':
            self.__filename_dict[self.__cur_src_filename] = ''
            self.__view.removeItemOnTheRight()
        else:
            self.__view.setFilenameToRight(self.__filename_dict[self.__cur_src_filename])
        self.__view.setFilenameToLeft(self.__cur_src_filename)

    def __itemActivated(self, item):
        if item:
            self.__setItemToEachView(item)
        else:
            item = self.__fileListWidget.currentItem()
            if item:
                self.__setItemToEachView(item)
            else:
                print('there is no item what')

    def __run(self):
        item = self.__fileListWidget.currentItem()
        cur_type = self.__mosaicTypeCmbBox.currentText()
        if item:
            filename = item.text()
            self.__t = Thread(filename, cur_type)
            self.__t.generateFinished.connect(self.__generateFinished)
            self.__t.start()
        else:
            QMessageBox.information(self, 'Notification', 'Select the item in the list first.')

    def __generateFinished(self, filename):
        self.__filename_dict[self.__cur_src_filename] = filename
        self.__view.setFilenameToRight(filename)

    def __started(self):
        print('started')

    def __finished(self):
        print('finished')


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())