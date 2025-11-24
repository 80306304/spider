import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from typing import List


def send_email(
        smtp_server: str,
        smtp_port: int,
        sender_email: str,
        sender_name: str,
        password: str,
        receiver_emails: List[str],
        subject: str,
        body: str,
        is_html: bool = True  # 新增参数控制邮件格式
) -> bool:
    """
    发送邮件的通用函数（支持HTML/纯文本格式，多收件人）

    :param smtp_server: SMTP服务器地址（如smtp.qq.com）
    :param smtp_port: SMTP端口号（如587/TLS，465/SSL）
    :param sender_email: 发件人邮箱地址
    :param sender_name: 发件人显示名称
    :param password: 邮箱授权码（非登录密码）
    :param receiver_emails: 收件人邮箱地址列表（支持多个）
    :param subject: 邮件主题
    :param body: 邮件正文内容（HTML或纯文本）
    :param is_html: 是否为HTML格式（默认True）
    :return: 发送成功返回True，失败返回False
    """
    try:
        # 校验收件人列表
        if not receiver_emails:
            print("\n⚠️ 错误：收件人列表不能为空")
            return False

        # 创建MIME对象（根据格式选择类型）
        print("\n1. 正在创建邮件内容...")
        msg = MIMEText(body, 'html' if is_html else 'plain', 'utf-8')
        msg['From'] = formataddr((sender_name, sender_email))
        msg['To'] = ", ".join(receiver_emails)
        msg['Subject'] = subject
        print("✅ 邮件内容创建成功")
        print(f"   发件人: {sender_name} <{sender_email}>")
        print(f"   收件人: {', '.join(receiver_emails)}（共{len(receiver_emails)}人）")
        print(f"   邮件格式: {'HTML' if is_html else '纯文本'}")
        print(f"   邮件大小: {len(msg.as_string())} bytes")

        # 创建SMTP连接（自动判断SSL/TLS）
        print("\n2. 正在连接邮件服务器...")
        server = smtplib.SMTP_SSL(smtp_server, smtp_port) if smtp_port == 465 else smtplib.SMTP(smtp_server, smtp_port)
        print(f"✅ 已连接到 {smtp_server}:{smtp_port}")

        # 启动TLS加密（非465端口需要）
        if smtp_port != 465:
            print("\n3. 启动TLS加密连接...")
            server.starttls()
            print("✅ TLS加密已启用")

        # 登录邮箱
        print("\n4. 正在登录邮箱...")
        server.login(sender_email, password)
        print("✅ 登录成功")

        # 发送邮件
        print("\n5. 正在发送邮件...")
        server.sendmail(sender_email, receiver_emails, msg.as_string())
        print(f"✅ 邮件已成功发送到 {len(receiver_emails)} 个收件人")

        return True

    except smtplib.SMTPConnectError as e:
        print(f"\n⚠️ 服务器连接失败: 无法连接到 {smtp_server}:{smtp_port}")
        print(f"   错误详情: {str(e)}")
    except smtplib.SMTPAuthenticationError as e:
        print(f"\n⚠️ 认证失败: 发件人邮箱或授权码错误")
        print(f"   错误详情: {str(e)}")
    except smtplib.SMTPRecipientsRefused as e:
        print(f"\n⚠️ 部分/全部收件人被拒绝: {e.recipients}")
        print(f"   错误详情: {str(e)}")
    except smtplib.SMTPException as e:
        print(f"\n⚠️ SMTP协议错误: {str(e)}")
    except Exception as e:
        print(f"\n⚠️ 发生未预期错误: {str(e)}")
    finally:
        # 确保关闭连接
        try:
            if 'server' in locals():
                print("\n6. 正在断开连接...")
                server.quit()
                print("✅ 连接已安全关闭")
        except Exception as e:
            print(f"\n⚠️ 连接关闭异常: {str(e)}")

    return False


if __name__ == "__main__":
    print("=== 邮件发送程序开始 ===")

    # 配置信息（请替换成你自己的信息）
    config = {
        "smtp_server": "smtp.qq.com",
        "smtp_port": 587,
        "sender_email": "80306304@qq.com",
        "sender_name": "大鳖速速回话",
        "password": "yaugwzlqvaivbgij",
        "receiver_emails": [
            "320920643@qq.com",
            "2446809427@qq.com"
        ],
        "subject": "HTML格式邮件测试",
        "body": """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>HTML邮件示例</title>
        </head>
        <body>
            <h1 style="color: #2c3e50;">这是一封HTML格式的邮件</h1>
            <p style="font-size: 16px; line-height: 1.6;">
                乌龟您好！<br>
                这是邮件的正文内容，支持：<br>
                <ul>
                    <li>Best Regards,</li>
                    <li>YUXing Li</li>
                    <li>Test Engineer</li>
                    <li>6F, Building B8, Guanggu Biology City, No. 666 Gaoxin Blvd, Wuhan</li>
                    <li>430063, P.R. China</li>
                    <li>Tel:86-13972683760</li>
                    <li><a href="https://example.com" style="color: #3498db;">超链接</a></li>
                </ul>
            </p>
            <p style="color: #7f8c8d; font-size: 14px;">发送时间：2025-05-12</p>
        </body>
        </html>
        """,  # HTML格式正文
        "is_html": True  # 显式指定为HTML格式（可省略，默认True）
    }

    success = send_email(**config)
    print(f"\n=== 程序执行结束 {'(发送成功)' if success else '(发送失败)'} ===")
