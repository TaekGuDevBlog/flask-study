import hashlib
import bcrypt
import jwt

#hashlib
m = hashlib.sha256()
m.update(b"test password")
print(m.hexdigest())

#bcrypt
print(bcrypt.hashpw(b"secrete password", bcrypt.gensalt()))
print(bcrypt.hashpw(b"secrete password", bcrypt.gensalt()).hex())

#pyjwt
data_to_encode = {'some':'payload'}
encryption_secret = 'secrete'
algorithm = 'HS256'
encoded = jwt.encode(data_to_encode, encryption_secret, algorithm=algorithm)
print(bytes(encoded))
print(type(encoded))
decoded = jwt.decode(encoded, encryption_secret, algorithms=[algorithm])
print(decoded)

