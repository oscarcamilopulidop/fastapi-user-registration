from config.database import CursorFromConnectionPool
from schemas.user import User
from config.database import Database
from fastapi import HTTPException, status
import datetime

# Parametrized SQL queries
INSERT_USER_QUERY = "INSERT INTO users (email, password, verification_code, verification_code_expiry, is_verified) VALUES (%(email)s, %(password)s, %(verification_code)s, %(verification_code_expiry)s, %(is_verified)s)"
GET_USER_BY_EMAIL_QUERY = "SELECT * FROM users WHERE email = %(email)s"
UPDATE_VERIFICATION_CODE_QUERY = "UPDATE users SET verification_code = %(verification_code)s, verification_code_expiry = %(expiry_date)s WHERE email = %(email)s"
UPDATE_VERIFIED_USER_QUERY = (
    "UPDATE users SET is_verified = %(is_verified)s WHERE email = %(email)s"
)
DELETE_USER_QUERY = "DELETE FROM users WHERE email = %(email)s"
UPDATE_VERIFICATION_CODE_EXPIRY_QUERY = "UPDATE users SET verification_code_expiry = %(expiry_date)s WHERE email = %(email)s"


class UserRepository:
    def __init__(self, db: Database):
        self.db = db

    def register_new_user(self, user: User) -> None:
        with CursorFromConnectionPool() as cursor:
            cursor.execute(INSERT_USER_QUERY, vars(user))

    def get_user_by_email(self, email: str) -> User:
        with CursorFromConnectionPool() as cursor:
            cursor.execute(GET_USER_BY_EMAIL_QUERY, {"email": email})
            user_record = cursor.fetchone()
            if user_record:
                user_dict = {
                    "email": user_record[1],
                    "password": user_record[2],
                    "verification_code": user_record[3],
                    "created_at": user_record[4],
                    "verification_code_expiry": user_record[5],
                    "is_verified": user_record[6],
                }
                return User(**user_dict)
            else:
                return None

    def get_user_by_email_or_404(self, email: str):
        user = self.get_user_by_email(email)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user

    def user_exists(self, email: str) -> bool:
        user = self.get_user_by_email(email)
        if user is None:
            return False
        return True

    def is_user_verified(self, email: str) -> bool:
        user = self.get_user_by_email(email)
        if user is None:
            return False
        return user.is_verified

    def update_verification_code(
        self, hashed_verification_code: str, user: User
    ) -> None:
        expiry_date = datetime.datetime.now() + datetime.timedelta(minutes=1)
        with CursorFromConnectionPool() as cursor:
            cursor.execute(
                UPDATE_VERIFICATION_CODE_QUERY,
                {
                    "verification_code": hashed_verification_code,
                    "expiry_date": expiry_date,
                    "email": user.email,
                },
            )

    def update_verified_user(self, user: User) -> None:
        with CursorFromConnectionPool() as cursor:
            cursor.execute(
                UPDATE_VERIFIED_USER_QUERY,
                {"is_verified": user.is_verified, "email": user.email},
            )

    def delete_user(self, email: str) -> None:
        with CursorFromConnectionPool() as cursor:
            cursor.execute(DELETE_USER_QUERY, {"email": email})

    def update_verification_code_expiry(
        self, expiry_date: datetime, user: User
    ) -> None:
        with CursorFromConnectionPool() as cursor:
            cursor.execute(
                UPDATE_VERIFICATION_CODE_EXPIRY_QUERY,
                {
                    "expiry_date": expiry_date,
                    "email": user.email,
                },
            )
