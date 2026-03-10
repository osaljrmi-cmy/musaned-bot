from app.musaned.service import ensure_musaned_session

if __name__ == "__main__":
    result = ensure_musaned_session(headless=False)
    print("RESULT =", result)