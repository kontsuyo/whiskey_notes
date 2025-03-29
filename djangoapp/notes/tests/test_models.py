import pytest
from django.core.exceptions import ValidationError


@pytest.mark.django_db
def test_whisky_name_exceed_200_character(whisky):
    whisky.name = "A" * 201

    with pytest.raises(ValidationError) as e:
        whisky.full_clean()

    assert (
        "この値は 200 文字以下でなければなりません( 201 文字になっています)。"
        in str(e.value)
    )


@pytest.mark.django_db
def test_whisky_name_is_empty(whisky):
    whisky.name = ""

    with pytest.raises(ValidationError) as e:
        whisky.full_clean()

    assert "このフィールドは空ではいけません。" in str(e.value)


@pytest.mark.django_db
def test_whisky_str_representation(whisky):
    assert str(whisky) == "Sample Whisky"


@pytest.mark.django_db
def test_tastingnote_note_is_empty(note):
    note.note = ""

    with pytest.raises(ValidationError) as e:
        note.full_clean()

    assert "このフィールドは空ではいけません。" in str(e.value)


@pytest.mark.django_db
def test_tastingnote_str_representation(note):
    assert str(note) == "good!"
