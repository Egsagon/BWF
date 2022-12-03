'''
    main.py
'''

import os
import hashlib
import base64 as b64
from cryptography.fernet import Fernet as Encryptor

# ---------------- #

BACKENDS = [
    'fernet',
    'Base16',
    'Base64',
    'Light'
]

to_sha256 = lambda text: hashlib.sha256(text).hexdigest()

def encode_pwd(pwd: str) -> bytes:
    '''
    Encode a password string to a Fernet key 
    '''
    
    return b64.b64encode(bytes(pwd + '0' * abs((32 - len(pwd))), 'utf-8'))

# --- Backends --- #

class Backend:
    def encrypt_to_rtf(encryptor: Encryptor, source: str, target: str, seps: tuple = ('@', '$')) -> dict:
        '''
        Encrypt the files of a folder to a rtf archive.
        folder -> rtf
        '''
        
        pass

    def decrypt_to_folder(encryptor: Encryptor, source: str, target: str, seps: tuple = ('@', '$')) -> dict:
        '''
        Decrypt the files from a rtf archive to a folder.
        '''
        
        pass

class fernet:
    def encrypt_to_rtf(encryptor: Encryptor, source: str, target: str, seps: tuple = ('@', '$')) -> dict:
        '''
        Encrypt the files of a folder to a rtf archive.
        folder -> rtf
        '''
        
        # get absolute path
        source = os.path.abspath(source) + '/'
        target = os.path.abspath(target)
        files = os.listdir(source)
        
        # Encrypt source files
        output = [(f.split('.')[-1], # TODO - to b64
                encryptor.encrypt(open(os.path.abspath(source + f), 'rb').read()).decode())
                for f in files]
        
        # Write to target
        open(target, 'w').write(seps[0].join(map(seps[1].join, output)))
        
        return {'files': len(files), 'names': files, 'rtfsize': os.path.getsize(target)}

    def decrypt_to_folder(encryptor: Encryptor, source: str, target: str, seps: tuple = ('@', '$')) -> dict:
        '''
        Decrypt the files from a rtf archive to a folder.
        '''
        
        # get absolute path
        source = os.path.abspath(source)
        target = os.path.abspath(target) + '/'
        
        # Parse source file
        input = [f.split(seps[1]) for f in open(source, 'r').read().split(seps[0])]
        
        # Decrypt input
        input = [(ext, encryptor.decrypt(raw)) for ext, raw in input]
        
        for i, (ext, raw) in enumerate(input):
            open(target + str(i) + '.' + ext, 'wb').write(raw)
        
        files = os.listdir(target)
        
        return {'files': len(files), 'names': files, 'sizes': [os.path.getsize(target + f) for f in files]}

class Base16:
    def encrypt_to_rtf(encryptor: Encryptor, source: str, target: str, seps: tuple = ('@', '$')) -> dict:
        '''
        Encrypt the files of a folder to a rtf archive.
        folder -> rtf
        '''
        
        # get absolute path
        source = os.path.abspath(source) + '/'
        target = os.path.abspath(target)
        files = os.listdir(source)
        
        # Encrypt source files
        output = [(f.split('.')[-1], # TODO - to b64
                b64.b16encode(open(os.path.abspath(source + f), 'rb').read()).decode())
                for f in files]
        
        # Write to target
        open(target, 'w').write(seps[0].join(map(seps[1].join, output)))
        
        return {'files': len(files), 'names': files, 'rtfsize': os.path.getsize(target)}

    def decrypt_to_folder(encryptor: Encryptor, source: str, target: str, seps: tuple = ('@', '$')) -> dict:
        '''
        Decrypt the files from a rtf archive to a folder.
        '''
        
        # get absolute path
        source = os.path.abspath(os.path.normpath(source))
        target = os.path.abspath(os.path.normpath(target)) + '/'
        
        # Parse source file
        input = [f.split(seps[1]) for f in open(source, 'r').read().split(seps[0])]
        
        # Decrypt input
        input = [(ext, b64.b16decode(raw)) for ext, raw in input]
        
        for i, (ext, raw) in enumerate(input):
            open(target + str(i) + '.' + ext, 'wb').write(raw)
        
        files = os.listdir(target)
        
        return {'files': len(files), 'names': files, 'sizes': [os.path.getsize(target + f) for f in files]}

class Base64:
    def encrypt_to_rtf(encryptor: Encryptor, source: str, target: str, seps: tuple = ('@', '$')) -> dict:
        '''
        Encrypt the files of a folder to a rtf archive.
        folder -> rtf
        '''
        
        # get absolute path
        source = os.path.abspath(source) + '/'
        target = os.path.abspath(target)
        files = os.listdir(source)
        
        # Encrypt source files
        output = [(f.split('.')[-1], # TODO - to b64
                b64.b64encode(open(os.path.abspath(source + f), 'rb').read()).decode())
                for f in files]
        
        # Write to target
        open(target, 'w').write(seps[0].join(map(seps[1].join, output)))
        
        return {'files': len(files), 'names': files, 'rtfsize': os.path.getsize(target)}

    def decrypt_to_folder(encryptor: Encryptor, source: str, target: str, seps: tuple = ('@', '$')) -> dict:
        '''
        Decrypt the files from a rtf archive to a folder.
        '''
        
        # get absolute path
        source = os.path.abspath(source)
        target = os.path.abspath(target) + '/'
        
        # Parse source file
        input = [f.split(seps[1]) for f in open(source, 'r').read().split(seps[0])]
        
        # Decrypt input
        input = [(ext, b64.b64decode(raw)) for ext, raw in input]
        
        for i, (ext, raw) in enumerate(input):
            open(target + str(i) + '.' + ext, 'wb').write(raw)
        
        files = os.listdir(target)
        
        return {'files': len(files), 'names': files, 'sizes': [os.path.getsize(target + f) for f in files]}

class Light: # TODO
    def encrypt_to_rtf(encryptor: Encryptor, source: str, target: str, seps: tuple = ('@', '$')) -> dict:
        '''
        Encrypt the files of a folder to a rtf archive.
        folder -> rtf
        '''
        
        # get absolute path
        source = os.path.abspath(source) + '/'
        target = os.path.abspath(target)
        files = os.listdir(source)
        
        # Encrypt source files
        output = [(f.split('.')[-1], # TODO - to b64
                open(os.path.abspath(source + f), 'rb').read().decode())
                for f in files]
        
        # Write to target
        open(target, 'w').write(seps[0].join(map(seps[1].join, output)))
        
        return {'files': len(files), 'names': files, 'rtfsize': os.path.getsize(target)}

    def decrypt_to_folder(encryptor: Encryptor, source: str, target: str, seps: tuple = ('@', '$')) -> dict:
        '''
        Decrypt the files from a rtf archive to a folder.
        '''
        
        # get absolute path
        source = os.path.abspath(source)
        target = os.path.abspath(target) + '/'
        
        # Parse source file
        input = [f.split(seps[1]) for f in open(source, 'r').read().split(seps[0])]
        
        for i, (ext, raw) in enumerate(input):
            open(target + str(i) + '.' + ext, 'wb').write(raw)
        
        files = os.listdir(target)
        
        return {'files': len(files), 'names': files, 'sizes': [os.path.getsize(target + f) for f in files]}

# ---------------- #

if __name__ == '__main__':
    
    PASSWORD = 'password1234'
    enc = Encryptor(encode_pwd(PASSWORD))

    backend: Backend = Base16

    # res = backend.encrypt_to_rtf(enc, 'source', 'archive.rtf')
    # res = backend.decrypt_to_folder(enc, 'archive.rtf', 'out')
    # print(res)