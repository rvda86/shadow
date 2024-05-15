from app.tests.user_routes.UserRequester import UserRequester


def create_user(requester: UserRequester, email: str, password: str, username: str) -> tuple[str, dict]:
    user_data, status_code = requester.create_user(email, password, username)
    data, status_code = requester.get_token(email, password)
    token = data["accessToken"]
    return token, user_data
