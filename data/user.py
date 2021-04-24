import sqlalchemy
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash


class User(SqlAlchemyBase):
    __tablename__ = 'usersdata'

    ID = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    mail = sqlalchemy.Column(sqlalchemy.String, unique=True,
                             index=True, nullable=True)
    nickname = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=True)
    money = sqlalchemy.Column(sqlalchemy.Integer)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
