

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from lib.config import get_email_info
import threading

email_info = get_email_info()

def send_email(subject, body):
    # 设置SMTP服务器
    smtp_server = email_info['host']
    smtp_port = 25  # 网易邮箱的SMTP端口

    # 创建邮件对象
    msg = MIMEMultipart()
    msg['From'] = email_info['user']
    msg['To'] = ','.join(email_info['to_email_list'])
    msg['Subject'] = subject

    # 添加邮件正文
    msg.attach(MIMEText(body, 'plain'))
    server = None  # 初始化 server 变量
    try:
        # 连接到SMTP服务器
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # 启动安全传输模式
        server.login(email_info['user'], email_info['token'])  # 登录邮箱

        # 发送邮件
        server.sendmail(email_info['user'], email_info['to_email_list'], msg.as_string())
        print("邮件发送成功！")

    except Exception as e:
        print(f"邮件发送失败: {e}")

    finally:
        if server:
            server.quit()  # 关闭连接


def send_email_for_trade(current_price, stop_loss_price, take_profit_price, side, symbol):
    sideText = "多" if side == "buy" else "空"
    subject = f"告警提示"
    body = f"官式针法触发开{sideText}\n\nsymbol：{symbol}\nprice：{current_price}\ntake_profit_price：{take_profit_price}\nstop_loss_price：{stop_loss_price}\nside：{side}"
    # 邮件发送使用单独的线程, 防止阻塞主进程. 
    threading.Thread(target=send_email, args=(subject, body)).start()
