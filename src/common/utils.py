from passlib.hash import pbkdf2_sha512
import re

class Utils(object):

    @staticmethod
    def hash_password(password):
        """
        hashes a password using pbkdf2_sha512
        :param password: sha512 password from login form
        :return: pbkdf2_sha512 password
        """
        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def check_hashed_password(password, hashed_password):
        """
        Password  submitted matches the encrypted database password
        :param password: sha512 hashed password
        :param hashed_password: pbkdf2_sha512 encrypted password
        :return: true if match, false otherwise
        """
        return pbkdf2_sha512.verify(password, hashed_password)

    @staticmethod
    def email_is_valid(email):
        email_address_matcher = re.compile('^[\w-]+@([\w-]+\.)+[\w]+$')

        return True if email_address_matcher.match(email) else False
