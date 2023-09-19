from passlib.context import CryptContext

# Create a CryptContext instance
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(plain_password):
    hashed_password = pwd_context.hash(plain_password)
    return hashed_password

hashed = hash_password('ioioi')
# Verify a password against the hash
is_verified = pwd_context.verify('1234678', '$2b$12$Y.VJlB2c2Dm4V4Ie.DoQmOyo94mJcVAkRM5Ts0AIJ8ldrC4qVFkAC')

print(is_verified)
