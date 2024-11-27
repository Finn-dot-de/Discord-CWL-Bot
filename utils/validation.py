# utils/validation.py

def validate_townhall(townhall):
    """Überprüft, ob das Rathaus-Level eine Zahl zwischen 10 und 16 ist."""
    return townhall.isdigit() and 10 <= int(townhall) <= 16  # Max Rathaus-Level ist jetzt 16

def validate_username(username):
    """Überprüft, ob der Benutzername mindestens 3 Zeichen lang ist und nur alphanumerische Zeichen enthält."""
    return len(username) >= 3 and username.isalnum()
