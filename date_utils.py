from datetime import date, datetime, timedelta


def is_weekend(d: date) -> bool:
    """
    判断是否是周末。
    周六=5，周日=6
    """
    return d.weekday() >= 5


def previous_weekday(d: date) -> date:
    """
    返回前一个工作日。
    这里只按周末处理，先不处理法定节假日。
    """
    d = d - timedelta(days=1)
    while is_weekend(d):
        d = d - timedelta(days=1)
    return d


def resolve_default_trade_date(today: date | None = None) -> date:
    """
    计算默认交易日。

    当前规则：
    - 周一到周五：默认今天
    - 周六、周日：默认前一个工作日（通常是周五）

    注意：
    这还不是严格的中国交易日历，暂时不处理法定节假日。
    """
    if today is None:
        today = date.today()

    if is_weekend(today):
        return previous_weekday(today)

    return today


def parse_date_str(s: str) -> date:
    """
    把 '2026-04-10' 这种字符串转换成 date 对象。
    """
    return datetime.strptime(s, "%Y-%m-%d").date()

def iter_weekdays(start_date: date, end_date: date):
    """
    生成从 start_date 到 end_date 的工作日序列。
    返回区间内的所有工作日（仅过滤周末）。
    暂不处理法定节假日。
    """
    current = start_date
    while current <= end_date:
        if not is_weekend(current):
            yield current
        current += timedelta(days=1)