import sys
from PyQt6.QtWidgets import QApplication, QWidget

app = QApplication(sys.argv)

widget = QWidget()
widget.resize(640, 480)
widget.setWindowTitle("OCR Downloader")
widget.show()

exit(app.exec())
