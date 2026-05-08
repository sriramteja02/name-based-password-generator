import secrets
import string
import random
import re
import os


CONFUSING_CHARS = "O0oIl1"
LEET_MAP = {
    'a': '@', 's': '$', 'i': '1',
    'o': '0', 'e': '3', 'l': '!'
}

SAFE_SYMBOLS = "!@#$%^&*()-_=+[]{}<>?"

# ---- UTILS ----
def random_case(word):
    return ''.join(
        c.upper() if secrets.randbelow(2) else c.lower()
        for c in word
    )

def leet_transform(word):
    return ''.join(
        LEET_MAP.get(c.lower(), c) for c in word
    )

def remove_confusing(text):
    return ''.join(c for c in text if c not in CONFUSING_CHARS)

def password_strength(pwd):
    score = 0
    if len(pwd) >= 12: score += 2
    if re.search(r"[A-Z]", pwd): score += 1
    if re.search(r"[a-z]", pwd): score += 1
    if re.search(r"\d", pwd): score += 1
    if re.search(rf"[{re.escape(SAFE_SYMBOLS)}]", pwd): score += 1

    if score <= 2: return "Weak"
    if score <= 4: return "Medium"
    return "Strong"

# ---- CORE ----
def generate_password(base_words, digits, symbols, min_length):
    if not base_words:
        raise ValueError("At least one base word is required")

    parts = []

    for word in base_words:
        word = random_case(word)
        word = leet_transform(word)
        word = remove_confusing(word)
        parts.append(word)

    parts += [secrets.choice(string.digits) for _ in range(digits)]
    parts += [secrets.choice(SAFE_SYMBOLS) for _ in range(symbols)]

    random.shuffle(parts)
    password = ''.join(parts)

    
    if len(password) < min_length:
        raise ValueError("Password too short after processing")

    return password

# ---- MAIN LOOP ----
if __name__ == "__main__":
    print("=== Smart Password Generator ===")

    while True:
        base_words = []
        while True:
            word = input("Enter a base word (or press Enter to stop): ").strip()
            if not word:
                break
            base_words.append(word)

        try:
            digits = int(input("How many digits to add: "))
            symbols = int(input("How many symbols to add: "))
            min_length = int(input("Minimum password length (>=8): "))

            if min_length < 8:
                raise ValueError

        except ValueError:
            print("Invalid input. Numbers only. Min length >= 8.")
            continue

        password = generate_password(base_words, digits, symbols, min_length)
        strength = password_strength(password)

        print("\nGenerated Password:", password)
        print("Strength:", strength)

        save = input("\nSave password? (y/n): ").lower()
        if save == 'y':
            path = input("Enter full file path (e.g. /home/user/passwords.txt): ").strip()

            if not path:
                print("Invalid path. Skipping save.")
            else:
                os.makedirs(os.path.dirname(path), exist_ok=True) if os.path.dirname(path) else None
                with open(path, "a") as f:
                    f.write(password + "\n")
                print(f"Saved to {path}")

        again = input("\nGenerate another password? (y/n): ").lower()
        if again != 'y':
            print("Exiting. Don’t be stupid with your passwords.")
            break
