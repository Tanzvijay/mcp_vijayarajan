from fastmcp import FastMCP


import smtplib
from email.mime.text import MIMEText



mcp = FastMCP()


  
SENDER_EMAIL = "vijaytanz12@gmail.com"
RECEIVER_EMAIL = "manvitharajeev@gmail.com"
SENDER_PASSWORD = "mbpt vayd zyrf oeww" 


operation = []





import pandas as pd
import io
from contextlib import redirect_stdout

df = pd.read_excel("C:/Users/vijay/Downloads/All Vouchers (7).xlsx")

@mcp.tool()
def info() -> str:
    """get info dataframes"""

    buffer = io.StringIO()
    with redirect_stdout(buffer):
        df.info()

    result = buffer.getvalue()
    operation.append(result)
    print("info__results")
    return result


def send_mail(subject: str, message: str):
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("✅ Email Sent Successfully!")
        return True
    except Exception as e:
        print(f"❌ Email Failed: {e}")
        return False


# Register ALL tools - make sure they're all decorated
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together"""
    result = a + b*100
    operation.append(f"Addition: {a} + {b} = {result}")
    print(f"✅ Add tool called: {a} + {b} = {result}")
    return result


@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract b from a"""
    result = a - b
    operation.append(f"Subtraction: {a} - {b} = {result}")
    print(f"✅ Subtract tool called: {a} - {b} = {result}")
    return result


@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers together"""
    result = a * b
    operation.append(f"Multiplication: {a} × {b} = {result}")
    print(f"✅ Multiply tool called: {a} × {b} = {result}")
    return result


@mcp.tool()
def send_all_results() -> str:
    """Send all accumulated operation results via email"""
    if not operation:
        return "❌ No operations performed yet."

    message = "\n".join(operation)
    print(f"📧 Sending email with {len(operation)} operations...")
    
    if send_mail("Combined Operation Results", message):
        count = len(operation)
        operation.clear()
        return f"✅ Email sent successfully with {count} operations!"
    else:
        return "❌ Failed to send email. Check your email configuration."





# Run the server
 