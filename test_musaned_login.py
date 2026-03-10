from app.musaned.login import login_to_musaned

if __name__ == "__main__":
    result = login_to_musaned(headless=False)
    print("RESULT =", result)