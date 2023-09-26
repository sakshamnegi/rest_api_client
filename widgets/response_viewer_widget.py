from PyQt5.QtWidgets import QWidget, QLabel, QTextEdit, QVBoxLayout

class ResponseViewerWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.response_label = QLabel("API Response:")
        self.response_text = QTextEdit()
        self.response_text.setReadOnly(True)  # Make the text area read-only

        layout = QVBoxLayout()
        layout.addWidget(self.response_label)
        layout.addWidget(self.response_text)

        self.setLayout(layout)

    def display_response(self, response_text):
        self.response_text.setPlainText(response_text)
