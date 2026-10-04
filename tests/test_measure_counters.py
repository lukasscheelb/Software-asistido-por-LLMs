from types import SimpleNamespace
from tests.quality.measure import ResourceCounters


def test_initial_and_final_cpu_counters_cover_the_whole_workload():
    proc = SimpleNamespace(
        pid=1,
        memory_info=lambda: SimpleNamespace(rss=123),
        cpu_times=lambda: (2.0, 3.0),
    )
    counters = ResourceCounters([])
    counters.processes = lambda: {(1, 0.0): proc}
    counters.capture("initial")
    proc.cpu_times = lambda: (3.0, 5.0)
    counters.capture("final")
    assert counters.cpu_seconds() == 3.0
    assert counters.rss == [123, 123]
    assert counters.gaps["missing_at_final"] == []


def test_started_and_exited_process_counter_gaps_are_disclosed():
    proc = SimpleNamespace(
        pid=1,
        memory_info=lambda: SimpleNamespace(rss=123),
        cpu_times=lambda: (1.0, 0.0),
    )
    counters = ResourceCounters([])
    counters.processes = lambda: {}
    counters.capture("initial")
    counters.processes = lambda: {(1, 0.0): proc}
    counters.capture("sample")
    counters.processes = lambda: {}
    counters.capture("final")
    assert counters.gaps["started_after_initial"][0]["pid"] == 1
    assert counters.gaps["missing_at_final"][0]["pid"] == 1
