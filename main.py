import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QComboBox, QLineEdit, QTextEdit, QPushButton, QVBoxLayout, QCheckBox
import requests
from services.request_manager import RequestManager
from widgets.request_builder import RequestBuilderWidget

from widgets.response_viewer_widget import ResponseViewerWidget
import logging


class APIClientApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize the RequestManager
        self.request_manager = RequestManager()

        # Create an instance of the RequestBuilderWidget
        self.request_builder_widget = RequestBuilderWidget()

        # Create an instance of the ResponseViewerWidget and assign it to self.response_viewer
        self.response_viewer = ResponseViewerWidget()

        # Create buttons for Save and Load
        self.save_request_button = QPushButton("Save Request")
        self.load_request_button = QPushButton("Load Request")

        # Connect the buttons to functions
        self.save_request_button.clicked.connect(self.save_request)
        self.load_request_button.clicked.connect(self.load_requests)

        # Create a layout for the main window
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.request_builder_widget)
        main_layout.addWidget(self.response_viewer)  # Updated to use self.response_viewer
        main_layout.addWidget(self.save_request_button)
        main_layout.addWidget(self.load_request_button)

        main_widget = QWidget()
        main_widget.setLayout(main_layout)

        self.setCentralWidget(main_widget)

        # Connect the "Send" button to the send_request function
        self.request_builder_widget.send_button.clicked.connect(self.send_request)

    def save_request(self):
        # Get data from the RequestBuilderWidget and call save_request on the RequestManager
        pass

    def load_requests(self):
        # Call load_requests on the RequestManager and display saved requests in the UI
        pass

    def initUI(self):
        self.setWindowTitle("API Client")
        self.setGeometry(100, 100, 800, 600)

    def setup_request_builder(self):
        self.request_builder_widget = QWidget()

        self.method_label = QLabel("HTTP Method:")
        self.method_combo = QComboBox()
        # Add other methods as needed
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

        self.request_builder_widget.setLayout(layout)

        # Connect the "Send" button to a function that sends the request (we'll implement this later).
        self.send_button.clicked.connect(self.send_request)

    def send_request(self):
        # Retrieve user inputs (HTTP method, URL, headers, body)
        http_method = self.request_builder_widget.method_combo.currentText()
        url = self.request_builder_widget.url_input.text()
        headers = self.request_builder_widget.headers_input.toPlainText()
        body = self.request_builder_widget.body_input.toPlainText()

        # Prepare headers as a dictionary
        headers_dict = {}
        for line in headers.split('\n'):
            if ':' in line:
                # Split at the first colon encountered
                key, value = line.split(':', 1)
                headers_dict[key.strip()] = value.strip()

        # Retrieve the selected content type (default to JSON)
        content_type = "application/json"  # Default
        if http_method in ["POST", "PUT"]:
            # Get the selected content type
            content_type = self.request_builder_widget.content_type_combo.currentText()
            
        # Retrieve the state of the "Include Content-Type Header" checkbox
        include_content_type_header = self.request_builder_widget.include_content_type_checkbox.isChecked()

        # Conditionally set the Content-Type header based on the checkbox state
        if http_method in ["POST", "PUT"] and include_content_type_header:
            headers_dict["Content-Type"] = content_type

        # Send the API request based on the selected HTTP method
        try:
            if http_method == "GET":
                response = requests.get(url, headers=headers_dict)
            elif http_method == "POST":
                response = requests.post(url, headers=headers_dict, data=body)
            elif http_method == "PUT":
                response = requests.put(url, headers=headers_dict, data=body)
            elif http_method == "DELETE":
                response = requests.delete(url, headers=headers_dict)
            else:
                print("Unsupported HTTP method")
                return

            # Handle the response (e.g., display it in the response viewer)
            response_text = response.text
            self.response_viewer.display_response(response_text)

        except requests.exceptions.RequestException as e:
            # Handle any request-related errors
            print(f"Request Error: {e}")


if __name__ == "__main__":
    app = QApplication([])
    window = APIClientApp()
    window.show()
    app.exec_()