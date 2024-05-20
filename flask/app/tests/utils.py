from app.config import Config


def get_response_json_status_code(response):
    if Config.TEST_CLIENT == "httpx":
        return response.json(), response.status_code
    elif Config.TEST_CLIENT == "flask":
        return response.json, response.status_code
