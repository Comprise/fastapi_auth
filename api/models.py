from database.connect import Base

from passlib.context import CryptContext
from sqlalchemy import Column, Integer, Boolean, VARCHAR

pwd_context = CryptContext(["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(VARCHAR(255), unique=True)
    hashed_password = Column(VARCHAR(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, value):
        self.hashed_password = pwd_context.hash(value)

    def verify(self, value):
        return pwd_context.verify(value, self.hashed_password)
