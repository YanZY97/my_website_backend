from utils.string_helper import gen_captcha_code
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

import smtplib


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def gen_captcha_code_msg(code, from_addr, to_addr, hint):
    """创建邮件"""
    if hint == 'register':
        text = '感谢注册！ 您的验证码是：{}，有效期为10分钟。'
        header = '注册验证码'
    else:
        text = '您的验证码是：{}，有效期为10分钟。'
        header = 'captcha'
    msg = MIMEText(text.format(code), 'plain', 'utf-8')
    msg['From'] = _format_addr('Y<%s>' % from_addr)
    msg['To'] = _format_addr('<%s>' % to_addr)
    msg['Subject'] = Header(header, 'utf-8').encode()
    return msg


def send_captcha_code(smtp_server, from_addr, password, to_addr, hint):
    """发送验证码"""
    code = gen_captcha_code()
    msg = gen_captcha_code_msg(code, from_addr, to_addr, hint).as_string()

    send_email(smtp_server, from_addr, password, to_addr, msg)
    return code


def send_email(smtp_server, from_addr, password, to_addr, msg):
    """发送邮件"""
    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)

    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg)
    server.quit()


if __name__ == '__main__':
    from_addr = '1835752347@qq.com'
    to_addr = '1835752347@qq.com'
    password = 'yksxrkfmldojdadb'
    smtp_server = 'smtp.qq.com'
    send_captcha_code(smtp_server, from_addr, password, to_addr)
