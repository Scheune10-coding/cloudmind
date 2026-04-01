from src.llm.token_tracker import TokenTracker
import pytest


def test_add_tokens_accumulates():
  tracker = TokenTracker()
  tracker.add("session_1", 100, 50)
  tracker.add("session_1", 200, 100)
  assert tracker.total_prompt == 300
  assert tracker.total_completion == 150


def test_multiple_sessions_tracked_separately():
  tracker = TokenTracker()
  tracker.add("session_1", 100, 50)
  tracker.add("session_2", 200, 100)
  assert tracker.sessions["session_1"]["prompt"] == 100
  assert tracker.sessions["session_2"]["prompt"] == 200
  assert tracker.total_prompt == 300


def test_get_cost():
  tracker = TokenTracker()
  tracker.add("session_1", 1_000_000, 1_000_000)
  assert tracker.get_cost() == 0.75


def test_get_cost_partial():
  tracker = TokenTracker()
  tracker.add("session_1", 500_000, 0)
  assert tracker.get_cost() == pytest.approx(0.075)