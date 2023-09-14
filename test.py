from passlib.context import CryptContext

# Create a CryptContext instance
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Generate a salted hash
plain_password = "password123"
hashed_password = pwd_context.hash(plain_password)

# Verify a password against the hash
is_verified = pwd_context.verify(plain_password, hashed_password)

print(hashed_password)
print(is_verified)
