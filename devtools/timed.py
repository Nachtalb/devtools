import io
import json
import time
from collections import defaultdict
from functools import wraps
from typing import Any, Callable, List, Tuple

from tabulate import tabulate

log_buffer = io.StringIO()  # shared across all decorated functions


def timed(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator for timing asynchronous functions.

    Args:
        func (Callable[..., Any]): Function to be timed.

    Returns:
        Callable[..., Any]: Wrapped function with timing logic.
    """

    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.monotonic_ns()
        result = await func(*args, **kwargs)
        end_time = time.monotonic_ns()
        elapsed_time = end_time - start_time  # keep as nanoseconds
        log_entry = json.dumps({"function": func.__module__ + "." + func.__qualname__, "time_ns": elapsed_time})
        log_buffer.write(f"{log_entry}\n")
        return result

    return wrapper


def process_logs() -> None:
    """Processes the logs and prints a tabulated summary of function timings.

    The summary includes the function's name, and its total execution time in seconds,
    milliseconds, and nanoseconds. Functions are sorted by execution time in descending order.
    """

    log_buffer.seek(0)  # reset cursor to start of buffer
    log_lines = log_buffer.readlines()

    # Dictionary to hold the cumulative time for each function
    times_dict: defaultdict[str, int] = defaultdict(int)

    for line in log_lines:
        log = json.loads(line)
        times_dict[log["function"]] += log["time_ns"]

    # Prepare data for tabulation
    data: List[Tuple[str, float, float, int]] = []
    for function, total_time_ns in times_dict.items():
        total_time_s = total_time_ns / 1e9
        total_time_ms = total_time_ns / 1e6
        data.append((function, total_time_s, total_time_ms, total_time_ns))

    # Sort data by total time (ns), in descending order
    data.sort(key=lambda x: x[3], reverse=True)

    print(tabulate(data, headers=["Function", "Time (s)", "Time (ms)", "Time (ns)"], tablefmt="grid"))
