from services.user_service import register_user
from services.auth_service import login,logout
from constants import SUCCESS, INVALID_PASSWORD, BLOCKED, USER_NOT_FOUND, NO_USER_LOGGED
from utils.session import set_current_user

def fake_data():
    return {
        "users": [],
        "logs": [],
        "session": {}
    }

def test_login_success():
    data = fake_data()

    register_user(data, "matheus", "1234")

    result, _ = login(data, "matheus", "1234")

    assert result == SUCCESS

def test_login_invalid_password():
    data = fake_data()

    register_user(data, "matheus", "1234")

    result, attempts = login(data, "matheus", "errada")

    assert result == INVALID_PASSWORD
    assert attempts == 1

def test_user_block_after_3_attempts():
    data = fake_data()

    register_user(data, "matheus", "1234")

    login(data, "matheus", "errada")
    login(data, "matheus", "errada")
    result, attempts = login(data, "matheus", "errada")

    assert result == BLOCKED
    assert attempts == 3
    assert data["users"][0]["blocked"] is True

def test_login_user_not_found():
    data = fake_data()

    result, attempts = login(data, "josiane", "1234")

    assert result == USER_NOT_FOUND
    assert attempts is None

def test_logout_without_user():
    data = fake_data()

    result,_ = logout(data)

    assert result == NO_USER_LOGGED

def test_login_with_invalid_password():
    data = fake_data()

    register_user(data, "matheus", "1234")

    result,attempts = login(data, "matheus", "errada")

    assert result == INVALID_PASSWORD
    assert attempts == 1
    assert data["users"][0]["blocked"] is False

def test_login_with_blocked_user():
    data = fake_data()

    register_user(data, "matheus", "1234")

    login(data, "matheus", "errada")
    login(data, "matheus", "errada")
    login(data, "matheus", "errada")

    result,_ = login(data, "matheus", "1234")

    assert result == BLOCKED

def test_current_user():
    data = fake_data()

    register_user(data, "matheus", "1234")

    result,_ = login(data, "matheus", "1234")

    assert result == SUCCESS
    assert data["session"]["current_user"]["username"] == "matheus"

def test_logout_with_user_logged():
    data = fake_data()

    register_user(data, "matheus", "1234")

    result,_ = login(data, "matheus", "1234")

    assert result == SUCCESS

    result,_ = logout(data)

    assert result == SUCCESS
    assert data["session"]["current_user"] is None

