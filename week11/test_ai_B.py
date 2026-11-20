from pathlib import Path

import pytest

from week11.load_scores import load_scores


def _assert_file_error_is_reported(result):
    assert isinstance(result, tuple)
    assert len(result) == 2
    kept, skipped = result
    assert kept == []
    assert skipped
    assert all(len(record) == 3 for record in skipped)
    assert all(isinstance(record[2], str) and record[2] for record in skipped)


def test_loads_trimmed_names_and_inclusive_score_boundaries(tmp_path):
    path = tmp_path / "scores.csv"
    path.write_text("이름,점수\n 민지 , 0 \n준호,100\n", encoding="utf-8")

    kept, skipped = load_scores(path)

    assert kept == [("민지", 0), ("준호", 100)]
    assert skipped == []


def test_parses_quoted_name_containing_comma(tmp_path):
    path = tmp_path / "scores.csv"
    path.write_text('이름,점수\n"최, 네번",90\n', encoding="utf-8")

    kept, skipped = load_scores(path)

    assert kept == [("최, 네번", 90)]
    assert skipped == []


def test_skips_later_duplicate_name_and_records_reason(tmp_path):
    path = tmp_path / "scores.csv"
    path.write_text("이름,점수\n민지,80\n민지,95\n", encoding="utf-8")

    kept, skipped = load_scores(path)

    assert kept == [("민지", 80)]
    assert len(skipped) == 1
    assert skipped[0][0] == 3
    assert skipped[0][1] == "민지,95"
    assert "중복" in skipped[0][2]


@pytest.mark.parametrize(
    ("row", "reason"),
    [
        ("민지", "열 개수"),
        ("민지,80,추가", "열 개수"),
        (" ,80", "이름"),
        ("민지,   ", "점수"),
        ("민지,팔십", "점수"),
        ("민지,-1", "점수"),
        ("민지,101", "점수"),
    ],
)
def test_skips_invalid_rows_with_line_number_original_and_reason(
    tmp_path, row, reason
):
    path = tmp_path / "scores.csv"
    path.write_text(f"이름,점수\n{row}\n", encoding="utf-8")

    kept, skipped = load_scores(path)

    assert kept == []
    assert len(skipped) == 1
    assert skipped[0][0] == 2
    assert skipped[0][1] == row
    assert reason in skipped[0][2]


def test_empty_file_is_reported_as_missing_header(tmp_path):
    path = tmp_path / "empty.csv"
    path.write_text("", encoding="utf-8")

    kept, skipped = load_scores(path)

    assert kept == []
    assert skipped
    assert any("헤더" in record[2] for record in skipped)


def test_invalid_header_is_reported_and_rows_are_not_loaded(tmp_path):
    path = tmp_path / "scores.csv"
    path.write_text("학생,점수\n민지,80\n", encoding="utf-8")

    kept, skipped = load_scores(path)

    assert kept == []
    assert any(record[0] == 1 and "헤더" in record[2] for record in skipped)


def test_missing_file_is_reported_without_raising(tmp_path):
    path = tmp_path / "missing.csv"

    result = load_scores(path)

    _assert_file_error_is_reported(result)


def test_unreadable_file_is_reported_without_raising(tmp_path, monkeypatch):
    path = tmp_path / "unreadable.csv"
    path.write_text("이름,점수\n민지,80\n", encoding="utf-8")
    original_open = open

    def deny_read(target, *args, **kwargs):
        if Path(target) == path:
            raise PermissionError("읽기 권한이 없습니다")
        return original_open(target, *args, **kwargs)

    monkeypatch.setattr("builtins.open", deny_read)

    result = load_scores(path)

    _assert_file_error_is_reported(result)


def test_invalid_utf8_is_reported_without_raising(tmp_path):
    path = tmp_path / "invalid_encoding.csv"
    path.write_bytes(b"\xff\xfe\xfa")

    result = load_scores(path)

    _assert_file_error_is_reported(result)
