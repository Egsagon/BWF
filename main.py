'''
    main.py
'''

import os
import hashlib
import base64 as b64
from time import sleep
from cryptography.fernet import Fernet as Encryptor

# ---------------- #

BACKENDS = ['Fernet', 'Base16', 'Base64', 'Light']

class Bar:
    def __init__(self) -> None: self.value = 0
    
    configure = lambda self, *a, **k: print(k)
    
    def __getitem__(self, item): return self.value
    
    def __setitem__(self, item, value):
        print(item, '->', value)
        self.value = value
    
    def start(self):
        print('started bar')

class Msg: configure = lambda *a, **k: print(k)

to_sha256 = lambda text: hashlib.sha256(text).hexdigest()
encode_pwd = lambda pwd: b64.b64encode(bytes(pwd + '0' * abs((32 - len(pwd))), 'utf-8'))

# --- Backends --- #
class Backends:
    class FernetBackend:
        def encrypt(encryptor, rawbytes) -> bytes: return encryptor.encrypt(rawbytes)
        def decrypt(encryptor, rawbytes) -> bytes: return encryptor.decrypt(rawbytes)

    class Base16Backend:
        def encrypt(encryptor, rawbytes) -> bytes: return b64.b16encode(rawbytes)
        def decrypt(encryptor, rawbytes) -> bytes: return b64.b16decode(rawbytes)

    class Base64Backend:
        def encrypt(encryptor, rawbytes) -> bytes: return b64.b64encode(rawbytes)
        def decrypt(encryptor, rawbytes) -> bytes: return b64.b64decode(rawbytes)

    class LightBackend:
        encrypt = decrypt = lambda encryptor, rawbytes: rawbytes

# --- Methods ---- #
def encrypt_to_rtf(encryptor: Encryptor,
                           source: str, target: str,
                           backend: object,
                           seps: tuple = ('@', '$'),
                           bar = None, msg = None) -> dict:
    
    '''
    Encrypt the files of a folder to a rtf archive.
    '''
    
    bar = bar # or Bar()
    msg = msg # or Msg()
    
    # get absolute path
    source = os.path.abspath(source) + '/'
    target = os.path.abspath(target)
    files = os.listdir(source)
    
    bar.configure(length = len(files))
    msg.configure(text = 'Starting ...')
    
    sleep(1)
    
    unit = 100 / len(files)
    
    # Encrypt source files
    output = []
    for f in files:
        
        bar['value'] += unit
        msg.configure(text = f'Encrypting {os.path.basename(f)} ...')
        sleep(1)
        output += [(f.split('.')[-1],
                    backend.encrypt(encryptor, open(os.path.abspath(source + f), 'rb').read()).decode())]
    
    sleep(1)
    
    # Write to target
    msg.configure(text = 'Writing to archive ...')
    open(target, 'w').write(seps[0].join(map(seps[1].join, output)))
    
    sleep(1)
    
    msg.configure(text = 'Finished process.')
    
    return {'files': len(files), 'names': files, 'rtfsize': os.path.getsize(target)}
    
def decrypt_to_folder(encryptor: Encryptor,
                        source: str, target: str,
                        backend: object,
                        seps: tuple = ('@', '$'),
                        bar = None, msg = None) -> dict:
    
    '''
    Decrypt the files from a rtf archive to a folder.
    '''
    
    bar = bar # or Bar()
    msg = msg # or Msg()
    
    # get absolute path
    source = os.path.abspath(source)
    target = os.path.abspath(target) + '/'
    
    bar.configure(mode = 'indeterminate')
    # bar.start()
    
    sleep(1)
    
    # Parse source file
    # input = [f.split(seps[1]) for f in open(source, 'r').read().split(seps[0])]
    input = []
    for i, f in enumerate(open(source, 'r').read().split(seps[0])):
        
        bar['value'] += 20
        
        sleep(1)
        
        msg.configure(text = f'Parsing {i} files ...')
        input += [f.split(seps[1])]
    
    bar.configure(mode = 'determinate', length = len(input) * 2)
    
    # Decrypt input
    # input = [(ext, encryptor.decrypt(raw)) for ext, raw in input]
    
    unit = 100 / (len(input) * 2)
    
    decrypted = []
    for i, (ext, raw) in enumerate(input):
        
        sleep(1)
        
        msg.configure(text = f'Decrypting {i} files ({ext=}) ...')
        bar['value'] += unit
        
        decrypted += [(ext, backend.decrypt(encryptor, raw))]
    
    msg.configure(text = 'Wrinting to target...')
    
    for i, (ext, raw) in enumerate(decrypted):
        sleep(1)
        
        bar['value'] += unit
        msg.configure(text = f'Writing {i}.{ext}')
        open(target + str(i) + '.' + ext, 'wb').write(raw)
    
    sleep(1)
    
    files = os.listdir(target)
    msg.configure(text = f'Wrote {len(files)} files.')
    
    return {'files': len(files), 'names': files, 'sizes': [os.path.getsize(target + f) for f in files]}
