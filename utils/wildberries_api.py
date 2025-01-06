import requests


class WildberriesAPI:
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
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
        body = {
            "period": {
                "begin": start_date,
                "end": end_date
            },
            "page": 1
        }

        try:
            print(f"Отправляем запрос с телом: {body}")

            response = requests.post(self.api_url, headers=self.headers, json=body)
            print(self.headers)

            if response.status_code == 200:
                print("Запрос выполнен успешно")
                return response.json()
            else:
                print(f"Ошибка: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса: {e}")
            return None