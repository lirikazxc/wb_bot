import requests

class WildberriesAPI:
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key
        self.headers = {
            "Authorization": f"{self.api_key}",
            "Content-Type": "application/json"
        }

    def ping(self):
        url = f"{self.api_url}/ping"
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Ошибка: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса: {e}")
            return None

    def get_sales_data(self, start_date: str, end_date: str):
        params = {
            "dateFrom": start_date,
            "dateTo": end_date
        }

        try:
            response = requests.get(self.api_url + "/sales", headers=self.headers, params=params)
            print("URL запроса:", response.url)
            print("Параметры запроса:", params)
            print("Ответ сервера:", response.text)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Ошибка: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса: {e}")
            return None

    def get_stocks_data(self, start_date: str, end_date: str):
        params = {
            "dateFrom": start_date,
            "dateTo": end_date
        }

        try:
            response = requests.get(self.api_url + "/stocks", headers=self.headers, params=params)
            print("URL запроса:", response.url)
            print("Параметры запроса:", params)
            print("Ответ сервера:", response.text)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Ошибка: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса: {e}")
            return None

    def get_incomes_data(self, start_date: str, end_date: str):
        params = {
            "dateFrom": start_date,
            "dateTo": end_date
        }

        try:
            response = requests.get(self.api_url + "/incomes", headers=self.headers, params=params)
            print("URL запроса:", response.url)
            print("Параметры запроса:", params)
            print("Ответ сервера:", response.text)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Ошибка: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса: {e}")
            return None

    def get_orders_data(self, start_date: str, end_date: str):
        params = {
            "dateFrom": start_date,
            "dateTo": end_date
        }

        try:
            response = requests.get(self.api_url + "/orders", headers=self.headers, params=params)
            print("URL запроса:", response.url)
            print("Параметры запроса:", params)
            print("Ответ сервера:", response.text)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Ошибка: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса: {e}")
            return None

    def get_reportDetailByPeriod_data(self, start_date: str, end_date: str):
        params = {
            "dateFrom": start_date,
            "dateTo": end_date
        }

        try:
            response = requests.get(self.api_url + "/reportDetailByPeriod", headers=self.headers, params=params)
            print("URL запроса:", response.url)
            print("Параметры запроса:", params)
            print("Ответ сервера:", response.text)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Ошибка: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса: {e}")
            return None
