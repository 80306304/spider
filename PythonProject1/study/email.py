import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

def send_email():
    # 配置信息（请替换成你自己的信息）
    smtp_server = "smtp.qq.com"  # SMTP服务器地址
    smtp_port = 587                   # 端口（常用：587/TLS，465/SSL）
    sender_email = "80306304@qq.com"  # 发件邮箱
    sender_name = "发件人名称"               # 发件人显示名称
    password = "yaugwzlqvaivbgij"  # 安全获取密码
    receiver_email = "320920643@qq.com"  # 收件邮箱
    subject = "乌龟说话"                    # 邮件主题
    body = "乌龟说话"         # 邮件正文

    try:
        # 创建MIME对象
        print("\n1. 正在创建邮件内容...")
        msg = MIMEText(body, 'plain', 'utf-8')
        msg['From'] = formataddr((sender_name, sender_email))
        msg['To'] = receiver_email
        msg['Subject'] = subject
        print("✅ 邮件内容创建成功")
        print(f"   发件人: {sender_name} <{sender_email}>")
        print(f"   收件人: {receiver_email}")
        print(f"   邮件大小: {len(msg.as_string())} bytes")

        # 创建SMTP连接
        print("\n2. 正在连接邮件服务器...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        print(f"✅ 已连接到 {smtp_server}:{smtp_port}")

        # 建立加密连接
        print("\n3. 启动加密连接...")
        server.starttls()
        print("✅ TLS加密已启用")

        # 登录邮箱
        print("\n4. 正在登录邮箱...")
        server.login(sender_email, password)
        print("✅ 登录成功")

        # 发送邮件
        print("\n5. 正在发送邮件...")
        server.sendmail(sender_email, [receiver_email], msg.as_string())
        print("✅ 邮件已成功发送到服务器")

        # 退出连接
        print("\n6. 正在断开连接...")
        server.quit()
        print("✅ 连接已安全关闭")

    # except smtplib.SMTPException as e:
    #     print(f"\n⚠️ SMTP协议错误: {str(e)}")
    except Exception as e:
        # print(f"\n⚠️ 发生未预期错误: {str(e)}")
        print("有错误")

if __name__ == "__main__":
    print("=== 邮件发送程序开始 ===")
    for i in range(3):
        send_email()
    print("\n=== 程序执行结束 ===")