from __future__ import annotations

import math


def calc_boxes(visitor_count: int) -> int:
    if visitor_count < 300:
        return 1
    return math.ceil(visitor_count / 300)