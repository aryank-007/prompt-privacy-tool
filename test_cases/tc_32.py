# Secret passed as a positional argument — tool only checks keyword args and variable names
def connect(host, port, password):
    print("connecting...")

connect("localhost", 5432, "SuperSecretPass99!")
