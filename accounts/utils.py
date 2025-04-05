import random

OTP_STORE = {}

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp(phone, email):
    otp = generate_otp()
    OTP_STORE[phone] = otp
    print(f"Sending OTP to {phone} and {email}: {otp}")
    return otp

def verify_otp(phone, otp):
    return OTP_STORE.get(phone) == otp
