from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtGui import QPen, QPixmap, QPainter
from PyQt5.QtCore import QPoint, Qt, QRect


class ConfigureMonitor(QWidget):
    def __init__(self, file_path: str, partition: str, param: str, parent=None) -> None:
        super().__init__()
        
        # Gets file path of img
        self.file_path = file_path
        
        # Gets config partition
        self.partition = partition

        # Gets config param 
        self.param = param

        # Gets parent class
        self.parent = parent
        
        # Init gui
        self.init_gui()
        
    def init_gui(self):
        # Gets size of recived img
        self.img_size = QPixmap(self.file_path)
        self.img_width, self.img_height = self.img_size.width(), self.img_size.height()
        
        # Sets reduced by 2 times pixmap
        self.pixmap = None
        self.load_pixmap()
                
        # Gets resolutin of pixmap
        self.pxm_width, self.pxm_height = self.pixmap.width(), self.pixmap.height()
        
        # Start and end pos() of cursor
        self.begin = QPoint()
        self.end = QPoint()
        
        # Gets rectangle of drawRect() object
        self.rectangle_rect = None
        
        self.setFixedSize(self.pxm_width, self.pxm_height)
        self.setWindowTitle("Configure Window")
        
        # Set pixmap onto the label widget
        self.img_label = QLabel(self)
        self.img_label.setPixmap(self.pixmap)
        self.img_label.show()
        
    def load_pixmap(self):
        # Load / Reload pixmap (img)
        self.pixmap = QPixmap(self.file_path).scaled(int(self.img_width / 1.5),
                                                    int(self.img_height / 1.5), 
                                                    Qt.KeepAspectRatio)
        
    def paintEvent(self, event):
        # create painter instance with pixmap
        self.qp = QPainter(self.pixmap)

        # set rectangle color and thickness
        self.pen = QPen(Qt.red)
        self.pen.setWidth(1)
        
        # Sets rect of rectangle
        self.rectangle_rect = QRect(self.begin, self.end)
        
        # draw rectangle on painter
        self.qp.setPen(self.pen)
        self.qp.drawRect(self.rectangle_rect)
        self.img_label.setPixmap(self.pixmap)
        self.img_label.update()
        self.qp.end()
        
    def mousePressEvent(self, event) -> None:
        self.begin = event.pos()
        self.end = event.pos()
        self.load_pixmap()
        self.img_label.update()
        
    def mouseMoveEvent(self, event) -> None:
        self.end = event.pos()
        self.load_pixmap()
        self.img_label.update()

    def mouseReleaseEvent(self, event) -> None:
        self.end = event.pos()
        self.img_label.update()
        
    def closeEvent(self, event) -> None:
        monitor = {"'top'": int(self.rectangle_rect.top() * 1.5), #screenshot capture area
                    "'left'": int(self.rectangle_rect.left() * 1.5), 
                    "'width'": int(self.rectangle_rect.width() * 1.5),
                    "'height'": int(self.rectangle_rect.height() * 1.5)}
        try:
            if ((monitor["'top'"] or monitor["'left'"]) == 0 or
                (monitor["'width'"] or monitor["'height'"]) < 1):
                
                self.parent.update_config(self.partition,
                                        self.param,
                                        "default")
            else:
                self.parent.update_config(self.partition,
                                            self.param,
                                            monitor)
        except:
            print("Can't change monitor")
        finally:
            self.close()