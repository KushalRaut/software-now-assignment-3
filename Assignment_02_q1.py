# encrypt and decrypt text

def encrypt_letter(letter, s1, s2):
    # lowercase letters
    if letter.islower():
        if 'a' <= letter <= 'm':
            move = s1 * s2
            return chr((ord(letter) - ord('a') + move) % 26 + ord('a'))
        else:
            move = s1 + s2
            return chr((ord(letter) - ord('a') - move) % 26 + ord('a'))

    # uppercase letters
    elif letter.isupper():
        if 'A' <= letter <= 'M':
            return chr((ord(letter) - ord('A') - s1) % 26 + ord('A'))
        else:
            move = s2 * s2
            return chr((ord(letter) - ord('A') + move) % 26 + ord('A'))

    # everything else stays the same
    return letter


def decrypt_letter(letter, s1, s2):
    # reverse of encryption rules

    if letter.islower():
        if 'a' <= letter <= 'm':
            move = s1 * s2
            return chr((ord(letter) - ord('a') - move) % 26 + ord('a'))
        else:
            move = s1 + s2
            return chr((ord(letter) - ord('a') + move) % 26 + ord('a'))

    elif letter.isupper():
        if 'A' <= letter <= 'M':
            return chr((ord(letter) - ord('A') + s1) % 26 + ord('A'))
        else:
            move = s2 * s2
            return chr((ord(letter) - ord('A') - move) % 26 + ord('A'))

    return letter


def encrypt_file(s1, s2):
    # read raw text and write encrypted text
    raw_file = open("raw_text.txt", "r", encoding="utf-8")
    enc_file = open("encrypted_text.txt", "w", encoding="utf-8")

    for line in raw_file:
        new_line = ""
        for ch in line:
            new_line += encrypt_letter(ch, s1, s2)
        enc_file.write(new_line)

    raw_file.close()
    enc_file.close()


def decrypt_file(s1, s2):
    # read encrypted text and write decrypted text
    enc_file = open("encrypted_text.txt", "r", encoding="utf-8")
    dec_file = open("decrypted_text.txt", "w", encoding="utf-8")

    for line in enc_file:
        new_line = ""
        for ch in line:
            new_line += decrypt_letter(ch,
