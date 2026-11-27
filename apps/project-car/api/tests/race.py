"""Release n workers into fn together, each with its own session."""

from __future__ import annotations

import threading
from collections.abc import Callable

from sqlalchemy.orm import Session


def race(
    n: int,
    fn: Callable[[Session], object],
    session_factory: Callable[[], Session],
) -> tuple[list[object | None], list[BaseException | None]]:
    """Run fn(session) on n threads released together by one barrier.

    Each thread calls session_factory(), waits on a shared Barrier(n), then
    calls fn(session). The session is closed afterward when it has close.
    Returns (results, exceptions) in thread start order. exceptions[i] is
    None on success. results[i] is None when that thread raised.
    """
    barrier = threading.Barrier(n)
    results: list[object | None] = [None] * n
    exceptions: list[BaseException | None] = [None] * n

    def _worker(index: int) -> None:
        session: Session | None = None
        entered = False
        try:
            session = session_factory()
            barrier.wait()
            entered = True
            results[index] = fn(session)
        except BaseException as exc:
            exceptions[index] = exc
            if not entered:
                try:
                    barrier.abort()
                except Exception:
                    pass
        finally:
            if session is not None and callable(getattr(session, "close", None)):
                session.close()

    threads = [threading.Thread(target=_worker, args=(i,)) for i in range(n)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return results, exceptions
