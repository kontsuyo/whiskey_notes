import logging

import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

logger = logging.getLogger(__name__)
User = get_user_model()


@pytest.mark.django_db
def test_user_id_auto_added(user):
    logger.info(f"ID: {user.id}")
    assert user.id


@pytest.mark.django_db
def test_user_name_is_duplicate_at_update(user):
    create_user = User.objects.create_user(
        username="create_user",
        password="password",
        email="sladjfkjf@example.com",
    )
    create_user.username = user.username

    with pytest.raises(ValidationError) as e:
        create_user.full_clean()

    assert "そのユーザー名はすでに存在します。" in str(e.value)


@pytest.mark.django_db
def test_user_name_is_duplicate_at_create(user):
    with pytest.raises(IntegrityError) as e:
        User.objects.create_user(
            username=user.username,
            password="password",
            email="sladjfkjf@example.com",
        )

    assert "duplicate key value violates unique constraint " in str(e.value)


@pytest.mark.django_db
def test_email_address_is_duplicate_at_update(user):
    create_user = User.objects.create_user(
        username="create_user",
        password="password",
        email="sladjfkjf@example.com",
    )
    create_user.email = user.email

    with pytest.raises(ValidationError) as e:
        create_user.full_clean()

    assert "この Email address を持った ユーザー が既に存在します。" in str(e.value)


@pytest.mark.django_db
def test_email_address_is_duplicate_at_create(user):
    with pytest.raises(IntegrityError) as e:
        User.objects.create_user(
            username="hoge",
            password="password",
            email=user.email
        )

    assert "duplicate key value violates unique constraint " in str(e.value)


@pytest.mark.django_db
def test_user_name_character_counts(user):
    user.username = "a" * 31

    with pytest.raises(ValidationError) as e:
        user.full_clean()

    error_message = "この値は 30 文字以下でなければなりません( 31 文字になっています"
    assert error_message in str(e.value)


@pytest.mark.django_db
def test_user_password_character_counts(user):
    user.password = "a" * 129

    with pytest.raises(ValidationError) as e:
        user.full_clean()

    error_message = "この値は 128 文字以下でなければなりません( 129 文字になっています"
    assert error_message in str(e.value)


@pytest.mark.django_db
def test_user_email_character_counts(user):
    user.email = "a" * 255

    with pytest.raises(ValidationError) as e:
        user.full_clean()

    error_message = "この値は 254 文字以下でなければなりません( 255 文字になっています"
    assert error_message in str(e.value)


@pytest.mark.django_db
def test_user_email_is_duplicate(user):
    create_user = User.objects.create_user(
        username="create_user",
        password="password",
        email="create@sample.com",
    )
    create_user.email = user.email

    with pytest.raises(ValidationError) as e:
        create_user.full_clean()

    assert "この Email address を持った ユーザー が既に存在します。" in str(e.value)


@pytest.mark.django_db
def test_user_str_method_returns_username(user):
    assert str(user) == "testuser"
