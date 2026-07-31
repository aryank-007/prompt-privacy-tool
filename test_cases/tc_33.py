# Secret embedded inside an f-string — AST sees it as a joined string, not a plain value
token = "ghp_AbCdEfGhIjKlMnOpQrStUvWxYz123456"
url = f"https://api.github.com?access_token={token}"
