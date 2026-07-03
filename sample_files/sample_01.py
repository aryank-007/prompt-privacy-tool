# Sample 01: Hardcoded API key in a simple assignment
api_key = "sk-abc123XYZsupersecret9999"

def fetch_data(endpoint):
    import urllib.request
    req = urllib.request.Request(endpoint)
    req.add_header("Authorization", f"Bearer {api_key}")
    return urllib.request.urlopen(req).read()
