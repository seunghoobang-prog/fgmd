from __future__ import annotations

REGIONS: dict[str, dict] = {
    "서울": {"lat": 37.5665, "lng": 126.9780},
    "오산": {"lat": 37.1498, "lng": 127.0772},
    "전라": {"lat": 35.1595, "lng": 126.8526},
    "경상": {"lat": 35.8714, "lng": 128.6014},
    "충청": {"lat": 36.3504, "lng": 127.3845},
}

REGION_ORDER = ["서울", "오산", "전라", "경상", "충청"]

MAP_CENTER = [36.5, 127.5]
MAP_ZOOM = 7

BOXES_PER_ICON = 10
ICON_SIZE_MIN = 18
ICON_SIZE_MAX = 72
ICON_SIZE_PER_UNIT = 14

ORDER_EMAIL_TO = "240027@samchully.co.kr"