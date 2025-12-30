import requests

class NetworkHelper:
    ROOT_URL = "http://127.0.0.1:8001"
    AUTH = ('artemon', '11112006n')

    @staticmethod
    def get_books():
        url = f"{NetworkHelper.ROOT_URL}/books/"
        try:
            response = requests.get(url, auth=NetworkHelper.AUTH, timeout=5)

            if response.status_code == 200 and "application/json" in response.headers.get('Content-Type', ''):
                return response.json()

            return [
                {"id": 1, "title": "Advanced Science", "author": "J. Doe"},
                {"id": 2, "title": "Historical Tales", "author": "A. Smith"},
                {"id": 3, "title": "Epic Fantasy", "author": "R. Martin"},
                {"id": 4, "title": "The Great Adventure", "author": "L. Wright"},
                {"id": 5, "title": "Science Basics", "author": "N. Tesla"}
            ]
        except Exception as e:
            print(f"Network Error: {e}")
            return []

    @staticmethod
    def delete_book(book_id):
        url = f"{NetworkHelper.ROOT_URL}/books/{book_id}/delete/"
        try:
            response = requests.post(url, auth=NetworkHelper.AUTH)
            return response.status_code in [200, 302]
        except:
            return False