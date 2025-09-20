# config.py
import os

# 邮箱配置（请修改为你自己的）
MAIL_CONFIG = {
    "smtp_server": "smtp.qq.com",   #按照你的邮箱填写smtp服务器
    "port": 587,   #按照你的邮箱填写正确的端口
    "sender_email": "此处改成你的邮箱",      # 你的邮箱号码
    "sender_password": "此处改成你的密码/授权码",      # 注意QQ邮箱要填SMTP授权码（不是登录密码！）
    "sender_name": "课程提醒系统"
}

# 课表文件路径
EXCEL_PATH = "课表.xlsx"

# 老师邮箱映射表（必须填写！）
TEACHER_EMAILS = {
    "老师1": "example@StellarKitty.top",
    "老师2": "example@StellarKitty.top",
    # 添加其他老师...
}

# 日志文件
LOG_FILE = "logs/reminder.log"

# 确保日志目录存在
os.makedirs("logs", exist_ok=True)