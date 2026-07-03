# Sample 04: Function that accepts sensitive parameters
def connect_to_service(host, port, password, api_key=None):
    print(f"Connecting to {host}:{port}")
    # authenticate here
    return True
