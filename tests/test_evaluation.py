from pathlib import Path

import jsonlines
import yaml

from qa_eval import (
    stats_for_series,
    run_evaluation,
    compute_aggregations,
    compute_answer_score,
)


def test_stats_for_series():
    assert stats_for_series([]) == {"sum": 0, "mean": 0, "median": 0, "min": 0, "max": 0}
    assert stats_for_series([1]) == {"sum": 1, "mean": 1, "median": 1, "min": 1, "max": 1}
    assert stats_for_series([1.5]) == {"sum": 1.5, "mean": 1.5, "median": 1.5, "min": 1.5, "max": 1.5}
    assert stats_for_series([1, 2]) == {"sum": 3, "mean": 1.5, "median": 1.5, "min": 1, "max": 2}
    assert stats_for_series([i for i in reversed(range(10))]) == {
        "sum": 45, "mean": 4.5, "median": 4.5, "min": 0, "max": 9
    }


def test_run_evaluation_and_compute_aggregations():
    def get_chat_responses(path: Path) -> dict:
        responses = dict()
        with jsonlines.open(path, "r") as reader:
            for obj in reader:
                responses[obj["question_id"]] = obj
        return responses

    sample_gold_standard = yaml.safe_load(
        (Path(__file__).parent / "test_data" / "sample_gold_standard_corpus_1.yaml").read_text(encoding="utf-8")
    )
    sample_chat_responses_path = Path(__file__).parent / "test_data" / "sample_chat_responses_1.jsonl"

    evaluation_results = run_evaluation(sample_gold_standard, get_chat_responses(sample_chat_responses_path))
    aggregates = compute_aggregations(evaluation_results)
    expected_evaluation_results = yaml.safe_load(
        (Path(__file__).parent / "test_data" / "sample_evaluation_per_question_1.yaml").read_text(encoding="utf-8")
    )
    assert expected_evaluation_results == evaluation_results
    expected_aggregates = yaml.safe_load(
        (Path(__file__).parent / "test_data" / "sample_evaluation_summary_1.yaml").read_text(encoding="utf-8")
    )
    assert expected_aggregates == aggregates


def test_run_evaluation_and_compute_aggregations_all_errors():
    def get_chat_responses(path: Path) -> dict:
        responses = dict()
        with jsonlines.open(path, "r") as reader:
            for obj in reader:
                responses[obj["question_id"]] = obj
        return responses

    sample_gold_standard = yaml.safe_load(
        (Path(__file__).parent / "test_data" / "sample_gold_standard_corpus_1.yaml").read_text(encoding="utf-8")
    )
    sample_chat_responses_path = Path(__file__).parent / "test_data" / "sample_chat_responses_2.jsonl"

    evaluation_results = run_evaluation(sample_gold_standard, get_chat_responses(sample_chat_responses_path))
    aggregates = compute_aggregations(evaluation_results)
    expected_evaluation_results = yaml.safe_load(
        (Path(__file__).parent / "test_data" / "sample_evaluation_per_question_2.yaml").read_text(encoding="utf-8")
    )
    assert expected_evaluation_results == evaluation_results
    expected_aggregates = yaml.safe_load(
        (Path(__file__).parent / "test_data" / "sample_evaluation_summary_2.yaml").read_text(encoding="utf-8")
    )
    assert expected_aggregates == aggregates


def test_get_tools_calls_matches():
    expected_calls = [
        [
            {"name": "tool_a", "output": "result_a_1", "status": "success"},
            {"name": "tool_a", "output": "result_a_2", "status": "success"},
        ],
        [
            {"name": "tool_b", "output": "result_b_2", "status": "success"},
        ]
    ]
    actual_calls = [
        {"name": "tool_a", "output": "result_a_1", "status": "success", "id": "1"},
        {"name": "tool_b", "output": "error", "status": "error", "id": "2"},
        {"name": "tool_b", "output": "error", "status": "error", "id": "3"},
        {"name": "tool_a", "output": "result_a", "status": "success", "id": "4"},
        {"name": "tool_b", "output": "error", "status": "error", "id": "5"},
    ]
    assert compute_answer_score(expected_calls, actual_calls) == 0
    assert "matches" not in expected_calls[-1][0]

    expected_calls = [
        [
            {"name": "tool_a", "output": "result_a_1", "status": "success"},
            {"name": "tool_a", "output": "result_a_2", "status": "success"},
        ],
        [
            {"name": "tool_b", "output": "result_b_2", "status": "success"},
        ]
    ]
    actual_calls = [
        {"name": "tool_a", "output": "result_a_1", "status": "success", "id": "1"},
        {"name": "tool_b", "output": "result_b_2", "status": "success", "id": "2"},
        {"name": "tool_b", "output": "error", "status": "error", "id": "3"},
        {"name": "tool_a", "output": "result_a", "status": "success", "id": "4"},
        {"name": "tool_b", "output": "result_b_1", "status": "success", "id": "5"},
    ]
    assert compute_answer_score(expected_calls, actual_calls) == 1
    assert expected_calls[-1][0]["matches"] == "2"

    expected_calls = [
        [
            {"name": "tool_a", "output": "result_a_1", "status": "success"},
            {"name": "tool_a", "output": "result_a_2", "status": "success"},
        ],
        [
            {"name": "tool_b", "output": "result_b_1", "status": "success"},
            {"name": "tool_b", "output": "result_b_2", "status": "success"},
        ]
    ]
    actual_calls = [
        {"name": "tool_b", "output": "result_b_2", "status": "success", "id": "1"},
        {"name": "tool_b", "output": "error", "status": "error", "id": "2"},
        {"name": "tool_a", "output": "result_a", "status": "success", "id": "3"},
        {"name": "tool_b", "output": "result_b_1", "status": "success", "id": "4"},
    ]
    assert compute_answer_score(expected_calls, actual_calls) == 1
    assert expected_calls[-1][0]["matches"] == "4"
    assert expected_calls[-1][1]["matches"] == "1"

    expected_calls = [
        [
            {"name": "tool_a", "output": "result_a_1", "status": "success"},
            {"name": "tool_a", "output": "result_a_2", "status": "success"},
        ],
        [
            {"name": "tool_b", "output": "result_b_1", "status": "success"},
            {"name": "tool_b", "output": "result_b_2", "status": "success"},
        ]
    ]
    actual_calls = [
        {"name": "tool_b", "output": "result_b_24", "status": "success", "id": "1"},
        {"name": "tool_b", "output": "error", "status": "error", "id": "2"},
        {"name": "tool_a", "output": "result_a", "status": "success", "id": "3"},
        {"name": "tool_b", "output": "result_b_1", "status": "success", "id": "4"},
    ]
    assert compute_answer_score(expected_calls, actual_calls) == 0.5
    assert expected_calls[-1][0]["matches"] == "4"
    assert "matches" not in expected_calls[-1][1]


def test_compute_answer_score_expected_select_actual_ask():
    expected_calls = yaml.safe_load(
        (Path(__file__).parent / "test_data" / "expected_tools_calls_1.yaml").read_text(encoding="utf-8")
    )
    actual_calls = yaml.safe_load(
        (Path(__file__).parent / "test_data" / "actual_tools_calls_1.yaml").read_text(encoding="utf-8")
    )
    assert compute_answer_score(expected_calls, actual_calls) == 0
    assert "matches" not in expected_calls[-1][0]

    expected_calls = yaml.safe_load(
        (Path(__file__).parent / "test_data" / "expected_tools_calls_2.yaml").read_text(encoding="utf-8")
    )
    actual_calls = yaml.safe_load(
        (Path(__file__).parent / "test_data" / "actual_tools_calls_2.yaml").read_text(encoding="utf-8")
    )
    assert compute_answer_score(expected_calls, actual_calls) == 0
    assert "matches" not in expected_calls[-1][0]


def test_compute_answer_score_expected_select_actual_describe():
    expected_calls = yaml.safe_load(
        (Path(__file__).parent / "test_data" / "expected_tools_calls_3.yaml").read_text(encoding="utf-8")
    )
    actual_calls = yaml.safe_load(
        (Path(__file__).parent / "test_data" / "actual_tools_calls_3.yaml").read_text(encoding="utf-8")
    )
    assert compute_answer_score(expected_calls, actual_calls) == 0
    assert "matches" not in expected_calls[-1][0]


def test_compute_answer_score_expected_select_actual_ask_and_then_select():
    expected_calls = yaml.safe_load(
        (Path(__file__).parent / "test_data" / "expected_tools_calls_4.yaml").read_text(encoding="utf-8")
    )
    actual_calls = yaml.safe_load(
        (Path(__file__).parent / "test_data" / "actual_tools_calls_4.yaml").read_text(encoding="utf-8")
    )
    assert compute_answer_score(expected_calls, actual_calls) == 1
    assert "matches" in expected_calls[-1][0]
    assert expected_calls[-1][0]["matches"] == "call_3qJK186HZj1twnr6x976slHN"
