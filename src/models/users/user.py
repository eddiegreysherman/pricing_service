import uuid

from src.common.database import Database
import src.models.users.errors as UserErrors
from src.common.utils import Utils
from src.models.alerts.alert import Alert
import src.models.users.constants as UserConstants


class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<User {}>".format(self.email)

    @staticmethod
    def is_login_valid(email, password):
        """
        This method verifies the email/password combo is valid
        Checks that the email exists, and password matches
        :param email: The users email
        :param password: A sha512 hashed password
        :return: true if valid, false otherwise
        """
        user_data = Database.find_one(UserConstants.COLLECTION, {"email": email})
        if user_data is None:
            # Tell user the email does not exist.
            raise UserErrors.UserNotExistsError("Your user does not exist.")

        if not Utils.check_hashed_password(password, user_data['password']):
            # Tell the user wrong password
            raise UserErrors.IncorrectPasswordError("Incorrect password.")

        return True

    @staticmethod
    def register_user(email, password):
        '''
        This method registers a user using email and password
        password is
        :param email: email
        :param password: sha512 hashed password
        :return: True if successfully registered, False otherwise
        '''
        user_data = Database.find_one(UserConstants.COLLECTION, {"email": email})

        if user_data is not None:
            raise UserErrors.UserAlreadyRegisteredError("User email used to register already exists.")
        if not Utils.email_is_valid(email):
            raise UserErrors.InvalidEmailError("You entered an invalid email address.")

        User(email, Utils.hash_password(password)).save_to_db()

        return True

    def save_to_db(self):
        Database.insert(UserConstants.COLLECTION, self.json())

    def json(self):
        return {
            "_id": self._id,
            "email": self.email,
            "password": self.password
        }

    @classmethod
    def find_by_email(cls, email):
        return cls(**Database.find_one(UserConstants.COLLECTION, {"email" : email}))

    def get_alerts(self):
        return Alert.find_by_user_email(self.email)