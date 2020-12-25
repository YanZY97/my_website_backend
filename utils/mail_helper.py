from utils.string_helper import gen_captcha_code
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

import smtplib


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def gen_captcha_code_msg(code, from_addr, to_addr):
    text = '感谢注册！ 您的验证码是：{}，有效期为10分钟。'
    msg = MIMEText(text.format(code), 'plain', 'utf-8')
    msg['From'] = _format_addr('Y<%s>' % from_addr)
    msg['To'] = _format_addr('<%s>' % to_addr)
    msg['Subject'] = Header('注册验证码', 'utf-8').encode()
    return msg


def send_captcha_code(smtp_server, from_addr, password, to_addr):
    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)

    server.login(from_addr, password)
    code = gen_captcha_code()
    msg = gen_captcha_code_msg(code, from_addr, to_addr)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()
    return code


if __name__ == '__main__':
    from_addr = '1835752347@qq.com'
    to_addr = '1835752347@qq.com'
    password = 'yksxrkfmldojdadb'
    smtp_server = 'smtp.qq.com'
    send_captcha_code(smtp_server, from_addr, password, to_addr)
