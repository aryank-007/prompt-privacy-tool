# Clean class with no sensitive data
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def greet(self):
        return "Hello, " + self.name
