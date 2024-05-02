from typing import Iterable, Any


def custom_cycle(items: Iterable[Any], count: int) -> Any:
    """Performs like itertools.cycle except yields each element count times."""

    saved = []
    for item in items:
        for _ in range(count):
            yield item
        saved.append(item)
    while saved:
        for item in saved:
            for _ in range(count):
                yield item