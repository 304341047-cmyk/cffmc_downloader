import json
from datetime import date, timedelta
from pathlib import Path


class TradingCalendar:
    """
    交易日历类：
    - 判断是否为交易日
    - 获取前一交易日
    - 遍历交易日区间
    """

    def __init__(self, market="shfe"):
        self.market = market.lower()
        self.holiday_dir = Path(__file__).parent / "holidays"
        self._cache = {}

    def _load_holidays(self, year: int) -> set:
        """加载指定年份的节假日数据"""
        cache_key = f"{self.market}_{year}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        file_path = self.holiday_dir / f"{self.market}_{year}.json"
        if not file_path.exists():
            self._cache[cache_key] = set()
            return set()

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        holidays = set(data.get("holidays", []))
        self._cache[cache_key] = holidays
        return holidays

    def is_trading_day(self, d: date) -> bool:
        """判断是否为交易日"""
        if d.weekday() >= 5:  # 周末
            return False

        holidays = self._load_holidays(d.year)
        return d.isoformat() not in holidays

    def previous_trading_day(self, d: date) -> date:
        """获取前一个交易日"""
        d = d - timedelta(days=1)
        while not self.is_trading_day(d):
            d -= timedelta(days=1)
        return d

    def iter_trading_days(self, start_date: date, end_date: date):
        """遍历交易日"""
        current = start_date
        while current <= end_date:
            if self.is_trading_day(current):
                yield current
            current += timedelta(days=1)