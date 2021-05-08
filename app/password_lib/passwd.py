import bcrypt


class PasswordLib(object):
    def __init__(self):
        pass

    @staticmethod
    def get_hashed_password(plain_text_password: str):
        # Hash a password for the first time
        #   (Using bcrypt, the salt is saved into the hash itself)
        return bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt()).decode()

    @staticmethod
    def check_password(plain_text_password: str, hashed_password):
        # Check hashed password. Using bcrypt, the salt is saved into the hash itself
        return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password.encode('utf-8'))
