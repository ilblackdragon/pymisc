from random import randint

DEFAULT_TOKEN_LENGTH=32

def generate_token(token_length=DEFAULT_TOKEN_LENGTH):
    return '%.5x' % randint(0, 16 ** token_length)
