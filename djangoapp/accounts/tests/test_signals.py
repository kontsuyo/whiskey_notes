import pytest
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()


@pytest.mark.django_db
def test_token_created_on_user_creation():
    user = User.objects.create_user(username="testuser", password="password")

    token = Token.objects.filter(user=user).first()
    assert token is not None, "ユーザー作成時にトークンが作成されていません。"
    assert isinstance(token.key, str) and len(token.key) > 0
