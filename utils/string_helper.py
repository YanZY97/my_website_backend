import random


def gen_captcha_code(length=6):
    return ''.join(random.choices('0123456789', k=length))


if __name__ == '__main__':
    print(gen_captcha_code())
