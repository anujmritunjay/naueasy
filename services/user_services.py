import bcrypt
import jwt

JWT_SECRET="MRITUNJAY"

salt = bcrypt.gensalt() 
def hash_password(password):
    
    hashed_pass = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_pass.decode('utf-8')

def compare_password(password, db_pass):
    return bcrypt.checkpw(password.encode('utf-8'), db_pass.encode('utf-8'))

def generate_jwt(data):
    return jwt.encode(data, JWT_SECRET, algorithm = "HS256")

def decode_jwt(token):
    decoded_token = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    return decoded_token