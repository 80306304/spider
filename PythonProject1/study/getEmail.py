import poplib
from email.parser import BytesParser
from email.header import decode_header
from typing import List


def decode_email_header(header: str) -> str:
    """解码邮件头中的乱码（如中文）"""
    decoded = decode_header(header)
    result = []
    for part, charset in decoded:
        if charset:
            part = part.decode(charset) if isinstance(part, bytes) else part
        result.append(str(part))
    return ''.join(result)


def fetch_emails(
        pop_server: str,
        pop_port: int,
        email_addr: str,
        password: str,
        count: int = 3  # 获取最近3封邮件
) -> List[dict]:
    """
    使用POP3协议获取邮件

    :param pop_server: POP3服务器地址（如pop.qq.com）
    :param pop_port: POP3端口（如995/SSL）
    :param email_addr: 邮箱地址
    :param password: 邮箱授权码（非登录密码）
    :param count: 获取最近的邮件数量
    :return: 邮件信息列表（包含主题、发件人、正文等）
    """
    emails = []
    try:
        # 连接到POP3服务器（SSL加密）
        with poplib.POP3_SSL(pop_server, pop_port) as server:
            # 登录
            server.user(email_addr)
            server.pass_(password)

            # 获取邮件数量和总大小
            msg_count, msg_total_size = server.stat()
            print(f"📮 服务器共有 {msg_count} 封邮件，总大小 {msg_total_size} bytes")

            # 获取最近的N封邮件（索引从1开始，倒序取最后count封）
            start_idx = max(1, msg_count - count + 1)
            for idx in range(start_idx, msg_count + 1):
                # 获取邮件原始字节数据
                resp, lines, octets = server.retr(idx)
                raw_email = b'\r\n'.join(lines)

                # 解析邮件内容
                parser = BytesParser()
                msg = parser.parsebytes(raw_email)

                # 提取关键信息
                email_info = {
                    "id": idx,
                    "subject": decode_email_header(msg["Subject"]),
                    "from": decode_email_header(msg["From"]),
                    "to": decode_email_header(msg["To"]),
                    "date": msg["Date"],
                    "body": ""
                }

                # 解析正文（处理纯文本或HTML）
                if msg.is_multipart():
                    for part in msg.get_payload():
                        if part.get_content_type() == 'text/plain':
                            charset = part.get_content_charset() or 'utf-8'
                            email_info["body"] += part.get_payload(decode=True).decode(charset, 'ignore')
                else:
                    charset = msg.get_content_charset() or 'utf-8'
                    email_info["body"] = msg.get_payload(decode=True).decode(charset, 'ignore')

                emails.append(email_info)
                print(f"✅ 已获取第 {idx} 封邮件：{email_info['subject']}")

            return emails

    except poplib.error_proto as e:
        print(f"\n⚠️ POP3协议错误: {str(e)}")
    except Exception as e:
        print(f"\n⚠️ 发生未预期错误: {str(e)}")
    return emails


if __name__ == "__main__":
    # 配置信息（请替换成你自己的信息）
    config = {
        "pop_server": "pop.qq.com",  # QQ邮箱POP3服务器
        "pop_port": 995,  # QQ邮箱POP3-SSL端口
        "email_addr": "80306304@qq.com",  # 你的邮箱
        "password": "yaugwzlqvaivbgij",  # 邮箱授权码（非登录密码）
        "count": 3  # 获取最近3封邮件
    }

    print("=== 开始接收邮件 ===")
    received_emails = fetch_emails(**config)

    if received_emails:
        print("\n=== 邮件列表 ===")
        for idx, email in enumerate(received_emails, 1):
            print(f"\n邮件 {idx}:")
            print(f"主题: {email['subject']}")
            print(f"发件人: {email['from']}")
            print(f"时间: {email['date']}")
            print(f"正文: {email['body'][:100]}...（截断显示）")
    else:
        print("\nℹ️ 未获取到邮件")
