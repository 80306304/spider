import imaplib
import email
from email.header import decode_header
from email.utils import parsedate_to_datetime


def get_qq_email(username, password, folder='INBOX', num=5):
    """
    获取QQ邮箱指定文件夹的最新邮件
    :param username: QQ邮箱地址（如：xxx@qq.com）
    :param password: QQ邮箱IMAP授权码（非登录密码）
    :param folder: 邮箱文件夹（默认收件箱）
    :param num: 获取最新邮件数量（默认5封）
    :return: 邮件列表（包含主题、发件人、时间、正文）
    """
    # 连接QQ邮箱IMAP服务器（SSL加密）
    try:
        mail = imaplib.IMAP4_SSL('imap.qq.com', 993)
    except Exception as e:
        print(f"连接服务器失败: {str(e)}")
        return []

    # 登录邮箱
    try:
        mail.login(username, password)
    except imaplib.IMAP4.error as e:
        print(f"登录失败: {str(e)}。请检查授权码是否正确")
        mail.logout()
        return []

    # 选择邮箱文件夹
    try:
        mail.select(folder)
    except imaplib.IMAP4.error as e:
        print(f"选择文件夹失败: {str(e)}")
        mail.logout()
        return []

    # 搜索最新的num封邮件（按接收时间倒序）
    try:
        _, data = mail.search(None, 'ALL')
        mail_ids = data[0].split()[-num:]  # 取最后num个邮件ID（最新）
    except Exception as e:
        print(f"搜索邮件失败: {str(e)}")
        mail.logout()
        return []

    emails = []
    # 遍历获取邮件内容
    for mail_id in reversed(mail_ids):  # 反转顺序保持时间正序
        try:
            _, data = mail.fetch(mail_id, '(RFC822)')
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)
        except Exception as e:
            print(f"获取邮件{mail_id}失败: {str(e)}")
            continue

        # 解析邮件主题
        subject, encoding = decode_header(msg['Subject'])[0]
        if encoding:
            subject = subject.decode(encoding)

        # 解析发件人
        from_addr = msg['From']
        if '>' in from_addr:
            from_addr = from_addr.split('>')[1].strip().strip('<')

        # 解析时间（转换为北京时间）
        try:
            mail_time = parsedate_to_datetime(msg['Date']).astimezone()
        except:
            mail_time = '未知时间'

        # 解析正文内容
        body = ''
        if msg.is_multipart():
            for part in msg.get_payload():
                if part.get_content_type() == 'text/plain':
                    charset = part.get_charset() or 'utf-8'
                    body += part.get_payload(decode=True).decode(charset, 'ignore')
        else:
            charset = msg.get_charset() or 'utf-8'
            body = msg.get_payload(decode=True).decode(charset, 'ignore')

        emails.append({
            'subject': subject,
            'from': from_addr,
            'time': str(mail_time),
            'body': body.strip()[:500]  # 取前500字
        })

    mail.logout()
    return emails


if __name__ == "__main__":
    # 请替换为你的QQ邮箱信息
    QQ_EMAIL = "80306304@qq.com"  # 你的QQ邮箱地址
    AUTH_CODE = "yaugwzlqvaivbgij"  # 你的IMAP授权码

    # 获取最新5封收件箱邮件
    latest_emails = get_qq_email(QQ_EMAIL, AUTH_CODE)

    # 打印结果
    for idx, email_info in enumerate(latest_emails, 1):
        print(f"\n=== 第{idx}封邮件 ===")
        print(f"主题: {email_info['subject']}")
        print(f"发件人: {email_info['from']}")
        print(f"时间: {email_info['time']}")
        print(f"正文: {email_info['body']}...")
