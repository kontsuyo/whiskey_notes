import pytest

from .models import CustomUser


@pytest.mark.django_db
class TestCustomUser:
    def setup_method(self):
        self.username = "testuser"
        self.password = "password"
        self.email = ""

    def test_create_user(self):
        user = CustomUser.objects.create_user(
            username=self.username,
            password=self.password,
            email=self.email,
        )
        assert CustomUser.objects.filter(id=user.id).exists()  # type: ignore

    def test_create_super_user(self):
        super_user = CustomUser.objects.create_superuser(
            username=self.username,
            password=self.password,
            email=self.email,
        )
        assert CustomUser.objects.filter(id=super_user.id).exists()  # type: ignore
