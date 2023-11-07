from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
import random
import hashlib

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def generate_and_hash_verification_code():
    # Generate a 4-digit verification code
    verification_code = "{:04}".format(random.randint(0, 9999))

    # Hash the verification code
    hashed_verification_code = hashlib.sha256(verification_code.encode()).hexdigest()

    return verification_code, hashed_verification_code
