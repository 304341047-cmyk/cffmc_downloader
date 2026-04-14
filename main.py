from datetime import date

from config import DEFAULT_ACCOUNT
from downloader import run_download_for_account_and_range


def main():
    """
    最小调用版本：
    - 默认账户：acc1
    - 日期区间：2026-04-09 到 2026-04-10
    - 整个区间只登录一次
    """
    account_name = DEFAULT_ACCOUNT
    start_date = date(2026, 4, 9)
    end_date = date(2026, 4, 10)

    print("开始执行最小调用示例...")
    print(f"账户: {account_name}")
    print(f"日期区间: {start_date.isoformat()} ~ {end_date.isoformat()}")

    run_download_for_account_and_range(
        account_name=account_name,
        start_date=start_date,
        end_date=end_date,
    )


if __name__ == "__main__":
    main()