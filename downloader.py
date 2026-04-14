import os
from datetime import date
from pathlib import Path

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

from config import ACCOUNTS, DOWNLOAD_ROOT, LOGIN_URL
from date_utils import iter_weekdays


def get_account_credentials(account_name: str) -> tuple[str, str, str]:
    """
    根据账户名，从环境变量中读取用户名和密码。
    """
    if account_name not in ACCOUNTS:
        raise ValueError(f"账户 {account_name} 不存在，请检查 config.py")
    account_config = ACCOUNTS[account_name]

    username_env = account_config["username_env"]
    password_env = account_config["password_env"]
    display_name = account_config["display_name"]

    username = os.getenv(username_env)
    password = os.getenv(password_env)

    if not username or not password:
        raise ValueError(
            f"账户 {account_name} 缺少环境变量配置，请检查 {username_env} / {password_env}"
        )

    return username, password, display_name


def build_download_dir(account_name: str, trade_date: date) -> Path:
    """
    生成下载目录。
    目录结构：
        downloads/账户名/交易日/
    """
    target_dir = DOWNLOAD_ROOT / account_name / trade_date.isoformat()
    target_dir.mkdir(parents=True, exist_ok=True)
    return target_dir


def format_download_filename(account_name: str, suggested_name: str) -> str:
    """
    统一生成下载文件名。
    """
    return f"{account_name}_{suggested_name}"


def login_once(page,username: str, password: str):
    """
    只登录一次。
    """
    page.goto(LOGIN_URL, wait_until="domcontentloaded")
    page.locator('input[name="userID"]').fill(username)
    page.locator('input[name="password"]').fill(password)

    print("请手动输入验证码，并手动点击登录。")
    input("登录成功后，按回车继续...")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(1000)

def query_and_download_one_date(page, account_name: str, trade_date: date) -> Path:
    """
    在“已经登录成功”的前提下，下载某一天的结算日报。
    """
    target_date_str = trade_date.isoformat()
    save_dir = build_download_dir(account_name, trade_date)

    date_input = page.get_by_role("textbox")
    date_input.click()
    date_input.fill(target_date_str)

    page.get_by_role("combobox").select_option("date")
    page.get_by_role("button", name="提交").click()
    page.wait_for_timeout(1000)
    page.get_by_role("radio", name="xlsx").check()

    # 点击下载
    with page.expect_download(timeout=30000) as download_info:
        with page.expect_popup(timeout=30000) as popup_info:
            page.get_by_role("link", name="下载").click()
        popup_page = popup_info.value

    download = download_info.value

    final_name = format_download_filename(
        account_name=account_name,
        suggested_name=download.suggested_filename,
    )
    final_path = save_dir / final_name
    download.save_as(str(final_path))

    # 下载页面如果是弹窗，顺手关掉
    try:
        popup_page.close()
    except Exception:
        pass

    page.wait_for_timeout(800)
    return final_path

def run_download_for_account_and_range(account_name: str, start_date: date, end_date: date):
    """
    下载某个账户在一个日期区间内的日报。
    - 只登录一次
    - 在同一个浏览器会话里，循环下载多个日期
    """
    load_dotenv()
    username, password, display_name = get_account_credentials(account_name)
    target_dates = list(iter_weekdays(start_date, end_date))

    if not target_dates:
        print("指定区间内没有可下载的工作日。")
        return

    print("开始执行下载任务...")
    print(f"账户: {account_name}")
    print(f"日期区间: {start_date.isoformat()} ~ {end_date.isoformat()}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        login_once(page, username, password)

        # 登录成功后，循环下载每一天
        for trade_date in target_dates:
            try:
                final_path = query_and_download_one_date(page, account_name, trade_date)
                print(f"[完成] {trade_date.isoformat()} -> {final_path}")
            except Exception as e:
                print(f"[失败] {trade_date.isoformat()} -> {e}")
                print("继续处理下一天...")
        
        input("全部日期处理完成。按回车关闭浏览器...")
        browser.close()