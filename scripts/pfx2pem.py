import sys
from OpenSSL import crypto


def pfx2pem(input_file, output_file, passphrase=None):
    """Converts a PFX file to PEM using OpenSSL, using passpharse if provided"""
    pfx = open(input_file, 'rb').read()
    p12 = crypto.load_pkcs12(pfx, passphrase)
    pem = crypto.dump_certificate(crypto.FILETYPE_PEM, p12.get_certificate())
    pem += crypto.dump_privatekey(crypto.FILETYPE_PEM, p12.get_privatekey())
    open(output_file, 'wb').write(pem)


def pfx2pem_memmory(input_file):
    """Converts a PFX file into a PEM file using OpenSSL into memory and returns file strem"""
    pfx = open(input_file, 'rb').read()
    p12 = crypto.load_pkcs12(pfx)
    pem = crypto.dump_certificate(crypto.FILETYPE_PEM, p12.get_certificate())
    pem += crypto.dump_privatekey(crypto.FILETYPE_PEM, p12.get_privatekey())
    return pem

# Running as a script, receives input_file, output_file and passphrase as argument and call pfx2pem function
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: pfx2pem.py input_file output_file [passphrase]")
        sys.exit(-1)
    pfx2pem(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)