from datetime import date,datetime
from trading_calendar.calendar import TradingCalendar
from config import DEFAULT_MARKET


def parse_date_str(s: str) -> date:
    return datetime.strptime(s, "%Y-%m-%d").date()

def resolve_default_trade_date(
        today: date | None = None,
        market: str = DEFAULT_MARKET) -> date:
    """
    返回默认交易日：
    - 若今天是交易日，则返回今天
    - 否则返回前一个交易日
    """
    if today is None:
        today = date.today()

    calendar = TradingCalendar(market)

    if calendar.is_trading_day(today):
        return today
    
    return calendar.previous_trading_day(today)