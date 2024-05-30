from app.config import Config


def get_json_and_response_code_from_response(response):
    if Config.TEST_CLIENT == "httpx":
        return response.json(), response.status_code
    elif Config.TEST_CLIENT == "flask":
        return response.json, response.status_code
