import pytest

from week11.load_scores import load_scores


def test_loads_valid_rows_strips_fields_and_keeps_duplicate_names(tmp_path):
    path = tmp_path / "scores.csv"
    path.write_text(
        "\ufeff이름,점수\n 민지 , 0 \n준호,100\n민지,50\n",
        encoding="utf-8",
    )

    kept, skipped = load_scores(path)

    assert kept == [("민지", 0), ("준호", 100), ("민지", 50)]
    assert skipped == []


def test_header_only_file_returns_empty_lists(tmp_path):
    path = tmp_path / "scores.csv"
    path.write_text("이름,점수\n", encoding="utf-8")

    assert load_scores(path) == ([], [])


def test_skips_invalid_rows_with_line_number_original_and_reason(tmp_path):
    path = tmp_path / "scores.csv"
    path.write_text(
        "이름,점수\n"
        " ,90\n"
        "가,\n"
        "나,abc\n"
        "다,1.5\n"
        "라,-1\n"
        "마,101\n"
        "바\n"
        "사,10,extra\n"
        "\n",
        encoding="utf-8",
    )

    kept, skipped = load_scores(path)

    assert kept == []
    assert skipped == [
        (2, " ,90", "이름이 비어 있음"),
        (3, "가,", "점수가 비어 있음"),
        (4, "나,abc", "점수가 정수가 아님"),
        (5, "다,1.5", "점수가 정수가 아님"),
        (6, "라,-1", "점수가 0~100 밖"),
        (7, "마,101", "점수가 0~100 밖"),
        (8, "바", "열 개수가 2가 아님"),
        (9, "사,10,extra", "열 개수가 2가 아님"),
    ]


def test_missing_file_raises_file_not_found_error(tmp_path):
    path = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError):
        load_scores(path)