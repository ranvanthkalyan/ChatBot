from flask import Flask, request, jsonify
import random
import smtplib

app = Flask(__name__)

# Fake database for storing verification codes
verification_data = {}

# Email Configuration (Use real email credentials)
EMAIL_ADDRESS = "your-email@gmail.com"
EMAIL_PASSWORD = "your-password"

def send_email(to_email, code):
    subject = "Your Verification Code"
    message = f"Your verification code is: {code}"
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    server.sendmail(EMAIL_ADDRESS, to_email, f"Subject: {subject}\n\n{message}")
    server.quit()

@app.route('/send-verification', methods=['POST'])
def send_verification():
    data = request.json
    email = data.get("email")
    if not email:
        return jsonify({"success": False, "error": "Email required"}), 400
    
    code = str(random.randint(100000, 999999))  # Generate 6-digit code
    verification_data[email] = code
    send_email(email, code)
    
    return jsonify({"success": True})

@app.route('/verify-code', methods=['POST'])
def verify_code():
    data = request.json
    email = data.get("email")
    code = data.get("code")

    if email in verification_data and verification_data[email] == code:
        return jsonify({"success": True})
    return jsonify({"success": False, "error": "Invalid code"}), 400

if __name__ == '__main__':
    app.run(debug=True)
