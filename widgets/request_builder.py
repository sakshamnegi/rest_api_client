# request_builder.py

import json
from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QLineEdit, QTextEdit, QVBoxLayout, QPushButton, QCheckBox,QMessageBox,QFileDialog


class RequestBuilderWidget(QWidget):
    def __init__(self):
        super().__init__() 
        # Create layout for the RequestBuilderWidget
        layout = QVBoxLayout()

        self.method_label = QLabel("HTTP Method:")
        self.method_combo = QComboBox()
        self.method_combo.addItems(["GET", "POST", "PUT", "DELETE"])

        # Content Type Label and Combo Box for POST and PUT requests
        self.content_type_label = QLabel("Content Type:")
        self.content_type_combo = QComboBox()
        self.content_type_combo.addItems(
            ["application/json", "application/xml", "multipart/form-data"])  # Add other options as needed
        self.content_type_combo.setCurrentText(
            "application/json")  # Default to JSON

        self.url_label = QLabel("URL:")
        self.url_input = QLineEdit()

        self.headers_label = QLabel("Headers:")
        self.headers_input = QTextEdit()

        self.body_label = QLabel("Request Body:")
        self.body_input = QTextEdit()

        # Checkbox to Include/Exclude Content-Type Header for POST and PUT
        self.include_content_type_checkbox = QCheckBox(
            "Include Content-Type Header")

        self.send_button = QPushButton("Send Request")
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_request)

        layout.addWidget(self.save_button)

        layout = QVBoxLayout()
        layout.addWidget(self.method_label)
        layout.addWidget(self.method_combo)

        # Add the Content Type UI for POST and PUT requests
        layout.addWidget(self.content_type_label)
        layout.addWidget(self.content_type_combo)

        layout.addWidget(self.url_label)
        layout.addWidget(self.url_input)
        layout.addWidget(self.headers_label)
        layout.addWidget(self.headers_input)
        layout.addWidget(self.body_label)
        layout.addWidget(self.body_input)

        # Add the Include Content-Type Header Checkbox for POST and PUT requests
        layout.addWidget(self.include_content_type_checkbox)

        layout.addWidget(self.send_button)

        self.setLayout(layout)

    def save_request(self):
        # Capture request details (HTTP method, URL, headers, body, and user-provided name)
        http_method = self.method_combo.currentText()
        url = self.url_input.text()
        headers = self.headers_input.toPlainText()
        body = self.body_input.toPlainText()

        # Prompt the user to choose a location and provide a name for the saved request
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Request", "", "JSON Files (*.json);;All Files (*)", options=options)

        if file_name:
            # Create a JSON structure to store the request details
            request_data = {
                "HTTP Method": http_method,
                "URL": url,
                "Headers": headers,
                "Body": body,
                "Name": file_name  # Use the provided name as the file name
            }

            # Save the JSON structure to the chosen file
            with open(file_name, "w") as file:
                json.dump(request_data, file, indent=4)

            # Inform the user that the request has been saved
            QMessageBox.information(self, "Request Saved", "The request has been saved successfully.")
