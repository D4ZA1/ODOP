
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15


# Generate RSA keys (public and private)
def generate_keys():

    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

# Sign data using the private key
def sign_data(private_key, data):
    private_key_obj = RSA.import_key(private_key)
    h = SHA256.new(data.encode())
    signature = pkcs1_15.new(private_key_obj).sign(h)
    return signature

# Verify data using the public key
def verify_signature(public_key, data, signature):
    public_key_obj = RSA.import_key(public_key)
    h = SHA256.new(data.encode())
    try:
        pkcs1_15.new(public_key_obj).verify(h, signature)
        return True
    except (ValueError, TypeError):
        return False

