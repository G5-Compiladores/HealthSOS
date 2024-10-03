import bcrypt

def get_password_hash(password):
    # Genera un salt y hash la contraseña
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def check_password(hashed_password, user_password):
    # Verifica la contraseña ingresada con la contraseña hasheada
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password.encode('utf-8'))
