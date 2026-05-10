#!/usr/bin/env python
"""
Script test gửi email xác nhận đăng ký
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl

def send_email(email):
    """
    Gửi email xác nhận đăng ký thành công sử dụng Mailtrap SMTP
    """
    # Cấu hình SMTP Mailtrap
    smtp_server = 'sandbox.smtp.mailtrap.io'
    smtp_port = 2525
    smtp_username = 'api'
    smtp_password = 'dc90f147efdfbcabbffe4daf14f2e69d'
    
    # Tạo message
    msg = MIMEMultipart()
    msg['From'] = 'noreply@logisticsgis.com'
    msg['To'] = email
    msg['Subject'] = 'Đăng ký thành công'
    
    # Nội dung HTML
    html = """
    <html>
    <body>
        <h2>Đăng ký thành công!</h2>
        <p>Chào mừng bạn đến với Logistics GIS.</p>
        <p>Tài khoản của bạn đã được tạo thành công.</p>
        <p>Bạn có thể đăng nhập và sử dụng dịch vụ của chúng tôi.</p>
    </body>
    </html>
    """
    
    msg.attach(MIMEText(html, 'html'))
    
    try:
        # Kết nối SMTP
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Bật TLS
        server.login(smtp_username, smtp_password)
        
        # Gửi email
        text = msg.as_string()
        server.sendmail(msg['From'], email, text)
        
        # Đóng kết nối
        server.quit()
        
        print(f"Email sent successfully to {email}")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

if __name__ == "__main__":
    # Test với email ví dụ
    test_email = "1250080158@sv.hcmunre.edu.vn"
    send_email(test_email)