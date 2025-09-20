# reminder.py
# 课程提醒系统 - 自动发送邮件提醒明天有课的老师

import pandas as pd
import smtplib
import logging
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.header import Header
from config import MAIL_CONFIG, EXCEL_PATH, TEACHER_EMAILS, LOG_FILE


# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()  # 同时输出到控制台
    ]
)


def send_email(receiver_email, subject, body):
    """
    发送邮件，使用 SMTP 协议
    """
    sender = MAIL_CONFIG["sender_email"]
    sender_name = MAIL_CONFIG["sender_name"]
    smtp_server = MAIL_CONFIG["smtp_server"]
    port = MAIL_CONFIG["port"]
    password = MAIL_CONFIG["sender_password"]

    try:
        # 创建邮件对象
        msg = MIMEText(body, 'plain', 'utf-8')

        # ✅ 正确设置邮件头（符合 RFC 标准）
        from_header = Header(f"{sender_name}", 'utf-8')
        msg['From'] = f"{from_header.encode()} <{sender}>"
        msg['To'] = receiver_email
        msg['Subject'] = Header(subject, 'utf-8')

        # 连接 SMTP 服务器
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()  # 启用 TLS 加密
        server.login(sender, password)
        server.sendmail(sender, [receiver_email], msg.as_string())
        server.quit()

        logging.info(f"✅ 邮件已发送至 {receiver_email}")
        return True

    except Exception as e:
        logging.error(f"❌ 邮件发送失败给 {receiver_email}：{e}")
        return False


def load_schedule():
    """
    读取 Excel 课表，返回 DataFrame
    """
    try:
        df = pd.read_excel(EXCEL_PATH)
        # 重命名列以确保一致性（可选）
        df.columns = ['日期', '节次', '内容', '老师姓名']
        
        # 将 '日期' 列转换为标准日期格式
        df['日期'] = pd.to_datetime(df['日期'], format='%m/%d/%y', errors='coerce').dt.date
        
        logging.info(f"✅ 成功读取课表：共 {len(df)} 行数据")
        return df
    except Exception as e:
        logging.critical(f"❌ 读取课表失败：{e}")
        return None


def get_tomorrow_classes(df):
    """
    从课表中提取明天有课的老师
    """
    tomorrow = (datetime.now() + timedelta(days=1)).date()

    # 筛选明天有课的行
    tomorrow_classes = df[df['日期'] == tomorrow]

    if tomorrow_classes.empty:
        logging.info(f"ℹ️ {tomorrow.strftime('%m月%d日')} 没有课程安排")
        return {}

    # 按老师分组，收集课程信息
    teacher_courses = {}
    for _, row in tomorrow_classes.iterrows():
        teacher = row['老师姓名']
        course = row['内容']
        period = row['节次']

        if teacher not in teacher_courses:
            teacher_courses[teacher] = []
        teacher_courses[teacher].append({
            'course': course,
            'period': period
        })

    return teacher_courses, tomorrow.strftime('%m月%d日')


def main():
    """
    主函数
    """
    logging.info("🌟 开始执行课程提醒任务...")

    # 1. 读取课表
    df = load_schedule()
    if df is None:
        return

    # 2. 获取明天的课程
    result = get_tomorrow_classes(df)
    if not result:
        return
    teacher_courses, tomorrow_str = result

    # 3. 给每位老师发送邮件
    for teacher, courses in teacher_courses.items():
        if teacher not in TEACHER_EMAILS:
            logging.warning(f"⚠️ 未找到 {teacher} 的邮箱地址")
            continue

        email = TEACHER_EMAILS[teacher]
        subject = f" 上课提醒：{tomorrow_str} 课程安排"
        body = f"""尊敬的 {teacher} 老师，您好：

这是您明天（{tomorrow_str}）的课程安排，请提前准备：

"""
        for c in courses:
            body += f"🔹 课程：{c['course']}\n"
            body += f"   时间：第 {c['period']} 节\n\n"

        body += "祝教学顺利！\n\n"
        body += f"{MAIL_CONFIG['sender_name']}"

        send_email(email, subject, body)

    logging.info("🎉 课程提醒任务执行完毕！")


# 程序入口
if __name__ == "__main__":
    main()