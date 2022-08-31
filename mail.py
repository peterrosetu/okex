# def send_email():    # SMTP服务器,这里使用QQ邮箱
from email.header import Header
from email.mime.text import MIMEText
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart 
import smtplib

if __name__ == '__main__':
    mail_host = "smtp.qq.com"    # 发件人邮箱
    mail_sender = "nevan2020@qq.com"    # 邮箱授权码,注意这里不是邮箱密码,如何获取邮箱授权码,请看本文最后教程
    mail_license = "juffanseaxhvdgdf"  # 收件人邮箱，可以为多个收件人
    mail_receivers = ['125894615@qq.com']
    mm = MIMEMultipart('related')  # 构建MIMEMultipart对象代表邮件本身，可以往里面添加文本、图片、附件等
    subject_content = "From Python"
    mm["From"] = "nevan2020<nevan2020@qq.com>"
    mm["To"] = "sina<nevanr@163.com>,qq<nevan2020@sina.com>"
    # 设置邮件主题
    mm["Subject"] = Header(subject_content, 'utf-8')
    # 添加正文    # 邮件正文内容
    body_content = "hello world"    # 构造文本,参数1：正文内容，参数2：文本格式，参数3：编码方式
    part = MIMEText(body_content, "plain", "utf-8")    # 向MIMEMultipart对象中添加文本对象
    mm.attach(part)    # 设置附件信息 添加附件到邮件信息当中去
    # a = MIMEText(
        # open('a/a.png', 'rb').read(), 'base64', 'utf-8')
    # a["Content-Disposition"] = 'attachment; filename="a.png"'
    # mm.attach(a);
    f = 'ok.zip'
    a = MIMEText(open(r'ok.zip', 'rb').read(),'base64','utf-8')
    a["Content-Type"] = 'application/octet-stream'
    a["Content-Disposition"] = 'attachment; filename="ok.zip"'
    mm.attach(a)

    try:
        stp = smtplib.SMTP()	# 设置发件人邮箱的域名和端口，端口地址为25
        stp.connect(mail_host, 25)        # set_debuglevel(1)可以打印出和SMTP服务器交互的所有信息
        stp.set_debuglevel(1)        # 登录邮箱，传递参数1：邮箱地址，参数2：邮箱授权码
        stp.login(mail_sender, mail_license)        # 发送邮件，传递参数1：发件人邮箱地址，参数2：收件人邮箱地址，参数3：把邮件内容格式改为str
        stp.sendmail(mail_sender, mail_receivers, mm.as_string())
        print("邮件发送成功!")
        stp.quit()
    except:
        print('error')