class RequestManager:
    def __init__(self):
        self.saved_requests = []

    def save_request(self, name, method, url, headers, content_type, body):
        saved_request = {
            "name": name,
            "method": method,
            "url": url,
            "headers": headers,
            "content_type": content_type,
            "body": body
        }
        self.saved_requests.append(saved_request)

    def load_requests(self):
        return self.saved_requests
