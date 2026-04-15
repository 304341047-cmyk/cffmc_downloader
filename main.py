import argparse
from datetime import date

from config import DEFAULT_ACCOUNT, ACCOUNTS
from date_utils import parse_date_str, resolve_default_trade_date
from downloader import run_download_for_account_and_range

def build_parser():
    parser = argparse.ArgumentParser(description="CFMMC 结算日报自动下载工具")

    parser.add_argument(
        "--account",
        type=str,
        default=DEFAULT_ACCOUNT,
        help=f"指定账户，例如 acc1 / acc2，默认为 {DEFAULT_ACCOUNT}"
    )

    parser.add_argument(
        "--date",
        type=str,
        help="指定单个日期，例如 2026-04-10，优先级高于 --start/--end"
    )

    parser.add_argument(
        "--start",
        type=str,
        help="指定开始日期，例如 2026-04-09",
    )

    parser.add_argument(
        "--end",
        type=str,
        help="指定结束日期，例如 2026-04-10",
    )

    return parser

def resolve_date_range(args) -> tuple[date, date]:
    """
    根据命令行参数决定下载日期范围。

    支持三种模式：
    1. python main.py
       -> 默认下载 1 天（自动判断默认交易日）

    2. python main.py --date 2026-04-10
       -> 下载单日

    3. python main.py --start 2026-04-09 --end 2026-04-10
       -> 下载区间
    """

    if args.date:
        target_date = parse_date_str(args.date)
        return target_date, target_date
    
    if args.start and args.end:
        start_date = parse_date_str(args.start)
        end_date = parse_date_str(args.end)
        if start_date > end_date:
            raise ValueError("开始日期不能晚于结束日期")
        return start_date, end_date

    default_date = resolve_default_trade_date()
    return default_date, default_date

def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.account not in ACCOUNTS:
        raise ValueError(
            f"账户 {args.account} 不存在，可选账户:{','.join(ACCOUNTS.keys())}"
            )
    
    account_name = args.account
    start_date, end_date = resolve_date_range(args)

    run_download_for_account_and_range(
        account_name=account_name,
        start_date=start_date,
        end_date=end_date,
    )


if __name__ == "__main__":
    main()