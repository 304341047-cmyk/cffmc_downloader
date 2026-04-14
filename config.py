from pathlib import Path

# 登录地址
LOGIN_URL = "https://investorservice.cfmmc.com/login.do"

# 下载根目录
DOWNLOAD_ROOT = Path("./downloads")

# 默认账户
DEFAULT_ACCOUNT = "acc1"

# 节假日清单
# 先手工维护，后面可以再升级
# HOLIDAYS = {
#     # "2026-01-01",
#     # "2026-02-17",
# }

# 多账户配置,不直接写死在这里，而是去环境变量里取
ACCOUNTS = {
    "acc1": {
        "username_env": "CFMMC_USER_ACC1",
        "password_env": "CFMMC_PASS_ACC1",
        "display_name": "默认账户",
    },
    "acc2": {
        "username_env": "CFMMC_USER_ACC2",
        "password_env": "CFMMC_PASS_ACC2",
        "display_name": "备用账户",
    },
}