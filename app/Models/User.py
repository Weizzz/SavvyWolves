class User():
    def __init__(self, userObj):
        self.user = userObj

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.user

    @staticmethod
    def validate_login(password_hash, password):
        return password == password_hash
        # return check_password_hash(password_hash, password)