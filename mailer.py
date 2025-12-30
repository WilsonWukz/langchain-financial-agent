import os
import smtplib
import markdown
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from dotenv import load_dotenv

load_dotenv()


def send_email(content: str, subject: str = "今日金价银价分析简报"):
    sender = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASSWORD")

    receivers_str = os.getenv("EMAIL_TO")

    if not all([sender, password, receivers_str]):
        print("Error: please enter EMAIL_USER, EMAIL_PASSWORD and EMAIL_TO in .env file.")
        return

    receivers_list = [email.strip() for email in receivers_str.split(',')]

    html_content = markdown.markdown(content)
    styled_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: 'Georgia', 'Times New Roman', serif;
                    background-color: #f0f2f5;
                    margin: 0;
                    padding: 0;
                    -webkit-font-smoothing: antialiased;
                }}

                .container {{
                    max_width: 700px;
                    margin: 30px auto;
                    background: #ffffff;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
                    border-top: 5px solid #003366;
                }}

                .header {{
                    background-color: #ffffff;
                    padding: 30px 40px;
                    text-align: center;
                    border-bottom: 1px solid #eaeaea;
                }}
                .header h1 {{
                    margin: 0;
                    color: #003366;
                    font-size: 24px;
                    letter-spacing: 1px;
                    text-transform: uppercase;
                }}
                .header .date {{
                    color: #888;
                    font-size: 14px;
                    margin-top: 10px;
                    font-family: 'Arial', sans-serif;
                }}

                .content {{
                    padding: 40px;
                    color: #333333;
                    line-height: 1.8;
                    font-size: 16px;
                }}

                h1, h2, h3 {{
                    color: #003366;
                    margin-top: 25px;
                    margin-bottom: 15px;
                }}
                h2 {{
                    font-size: 20px;
                    border-bottom: 2px solid #C5A059;
                    padding-bottom: 8px;
                    display: inline-block;
                }}

                strong {{
                    color: #b30000;
                    font-weight: 600;
                }}

                ul {{
                    padding-left: 20px;
                    margin-bottom: 20px;
                }}
                li {{
                    margin-bottom: 10px;
                }}

                .footer {{
                    background-color: #f8f9fa;
                    padding: 20px;
                    text-align: center;
                    font-size: 12px;
                    color: #999;
                    font-family: 'Arial', sans-serif;
                    border-top: 1px solid #eaeaea;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Gold & Silver Daily Insight</h1>
                    <div class="date">AI 驱动 · 每日市场深度分析</div>
                </div>

                <div class="content">
                    {html_content}
                </div>

                <div class="footer">
                    <p>此报告由 Multi - Agent 查找分析，数据仅供参考，不构成投资建议。</p>
                    <p>© 2025 Gold Market Agent | Powered by Gemini </p>
                </div>
            </div>
        </body>
        </html>
        """
    message = MIMEMultipart()
    message['From'] = Header("Gold Agent 🤖", 'utf-8')

    message['To'] = Header("Gold Subscribers", 'utf-8')

    message['Subject'] = Header(subject, 'utf-8')

    message.attach(MIMEText(styled_html, 'html', 'utf-8'))

    try:
        print(f"Sending email to: {receivers_list} ...")

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)

        server.sendmail(sender, receivers_list, message.as_string())

        print("Emails sent successfully.")
        server.quit()

    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    sample_text = """
## 测试标题
* **加粗测试**: 12345
* 列表项测试
    """
    send_email(sample_text, "HTML 样式测试")