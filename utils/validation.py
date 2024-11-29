# utils/validation.py

def validate_townhall(townhall):
    """Überprüft, ob das Rathaus-Level eine Zahl zwischen 10 und 17 ist."""
    return townhall.isdigit() and 10 <= int(townhall) <= 17  # Max Rathaus-Level ist jetzt 17

def validate_username(username):
    """Überprüft, ob der Benutzername mindestens 3 Zeichen lang ist und nur alphanumerische Zeichen enthält."""
    return len(username) >= 3 and username.isalnum()
