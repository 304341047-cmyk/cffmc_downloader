from config import DEFAULT_ACCOUNT
from date_utils import resolve_default_trade_date
from downloader import run_download_for_account_and_range

#WINDOWS 定时任务
def main():
    # 自动算出今天应该下载哪个交易日
    trade_date = resolve_default_trade_date()

    # 只下载这一天
    run_download_for_account_and_range(
        account_name=DEFAULT_ACCOUNT,
        start_date=trade_date,
        end_date=trade_date,
    )


if __name__ == "__main__":
    main()