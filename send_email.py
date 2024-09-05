## sendmail
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from loguru import logger

# EMAIL
EMAIL_HOST='smtp.vertumap.com'
EMAIL_PORT=465
EMAIL_USERNAME='admin@vertumap.com'
EMAIL_PASSWORD='vertu@123'

async def send_email(to_email, subject, context):
    from_email=EMAIL_USERNAME

    # 创建MIME文本对象
    message = MIMEText(context, "plain", 'utf-8')
    # 设置邮件头
    message["Subject"] = Header(subject, 'utf-8')
    message['From'] = f"GAEA Mail Service <{from_email}>"    # 设置发送者信息
    # message["From"] = from_email  #Header(from_addr, 'utf-8')
    message["To"] = to_email      #Header(to_email, 'utf-8')

    # 创建SMTP连接
    try:
        if EMAIL_PORT == 25:
            # 使用非加密方式连接
            smtpObj = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        elif EMAIL_PORT == 465:
            # 使用SSL方式连接,
            smtpObj = smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT)
        elif EMAIL_PORT == 587:
            # 使用TLS方式连接
            smtpObj = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
            # smtpObj.ehlo()
            smtpObj.starttls()
        # debug日志
        # smtpObj.set_debuglevel(1)
        # 登录发送邮件服务器
        smtpObj.login(from_email, EMAIL_PASSWORD)
        # 发送邮件
        smtpObj.sendmail(from_email, to_email, message.as_string())

        logger.success(f"{subject} {from_email} => {to_email} Email sent successfully")
    except Exception as e:
        logger.error(f"{subject} {from_email} => {to_email} Email sent failed: {e}")
    # 关闭SMTP连接
    smtpObj.quit()


if __name__ == "__main__":
    send_email("370887876@qq.com", "Account Creation Notification", f"This is the registration email, please open the link to continue.")
