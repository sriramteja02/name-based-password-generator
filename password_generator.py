import random
import secrets
import string
import re
import os

confusing_chars = "O0oIl1"

leet_map={
    'a':'@','s':'$','i':'1',
    'o':'0','e':'3','l':'!'
}

safe_symbols="!@#$%^&*()-_=+[]{}<>?"

all_chars=string.ascii_letter + string.digits+ safe_symbols

def random_case(word):
    return ''.join(
        c.upper() if secrets.randbelow(2) else c.lower()
        for c in word
    )

def leet_transform(word):
    return ''.join(
        leet_map.get(c.lower(),c)for c in word
    )

def remove_confusing(text):
    return ''.join(c for c in text if c not in confusing_chars)

def password_strength(pwd):
    score=0

    if len(pwd)>=12:
        score+=2
    elif len(pwd)>=8:
        score+=2
    
    if re.search(r"[A_Z]",pwd):score+=1
    if re.search(r"[a-z]",pwd):score+=1
    if re.search(r"\d",pwd):score+=1
    if re.search(rf"[{re.escape(safe_symbols)}]",pwd):score+=1

    if score<=2:
        return "Weak"
    elif score<=4:
        return "Medium"
    return "strong"

def generate_password(base_words,digits,symbols,min_length):
    if not base_words:
        raise ValueError("At least one base word is required")
    
    if digits<0 or symbols<0:
        raise ValueError("Digits and symbols count cannot be negative")
    
    if min_length<0:
        raise ValueError("Minimum length cannot be negative")
    
    parts=[]

    for word in base_words:
        word=random_case(word)
        word=leet_transform(word)
        word=remove_confusing(word)

        if word:
            parts.append(word)

    parts+=[secrets.choice(string.digits)for _ in range(digits)]
    parts+=[secrets.choice(safe_symbols)for _ in range(symbols)]

    secrets.SystemRandom().shuffle(parts)
    password=''.join(parts)

    while len(password)<min_length:
        password+=secrets.choice(all_chars)

    return password

if __name__=="__main__":
    print("----Smart Customised Password Generator----")

    while True:
        base_words=[]