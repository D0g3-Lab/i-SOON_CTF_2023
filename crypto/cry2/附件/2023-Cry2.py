# -*- coding:utf-8 -*-
from Crypto.Util.number import isPrime, long_to_bytes, getStrongPrime, bytes_to_long
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os
import binascii
import random
import string
import hashlib
import socketserver

FLAG = '**********'
KEY = b'****************'
IV = b'****************'


def cbc_decrypt(c, iv):
    aes = AES.new(KEY, AES.MODE_CBC, iv=iv)
    return aes.decrypt(c)


def encrypt():
    plain_text = ''.join([random.choice(string.ascii_letters) for _ in range(2)]) + FLAG
    aes = AES.new(KEY, AES.MODE_CBC, iv=IV)
    plain_text = pad(plain_text.encode(), AES.block_size)
    cipher = aes.encrypt(plain_text)
    return IV.hex() + cipher.hex()


def asserts(pt: bytes):
    num = pt[-1]
    if len(pt) == 16:
        result = pt[::-1]
        count = 0
        for i in result:
            if i == num:
                count += 1
            else:
                break
        if count == num:
            return True
        else:
            return False
    else:
        return False


def decrypt(c):
    iv = c[:32]
    cipher = c[32:]
    plain_text = cbc_decrypt(binascii.unhexlify(cipher), binascii.unhexlify(iv))
    if asserts(plain_text):
        return True
    else:
        return False


class MyServer(socketserver.BaseRequestHandler):
    def proof(self):
        random.seed(os.urandom(8))
        random_str = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(20)])
        str_sha256 = hashlib.sha256(random_str.encode()).hexdigest()
        self.request.sendall(('SHA256(XXXX + %s):%s\n' % (random_str[4:], str_sha256)).encode())
        self.request.sendall('Give Me XXXX:\n'.encode())
        XXXX = self.request.recv(2048).strip()

        if hashlib.sha256((XXXX + random_str[4:].encode())).hexdigest() != str_sha256:
            return False

        return True

    def handle(self):
        if not self.proof():
            self.request.sendall(b'Error Hash!')
            return
        cipher = encrypt()
        self.request.sendall('Welcome to AES System, please choose the following options:\n1. encrypt the flag\n2. decrypt the flag\n'.encode())
        n = 0
        while n < 65536:
            options = self.request.recv(512).strip().decode()
            if options == '1':
                self.request.sendall(('This is your flag: %s\n' % cipher).encode())
            elif options == '2':
                self.request.sendall('Please enter ciphertext:\n'.encode())
                recv_cipher = self.request.recv(512).strip().decode()
                if decrypt(recv_cipher):
                    self.request.sendall('True\n'.encode())
                else:
                    self.request.sendall('False\n'.encode())
            else:
                self.request.sendall('Input wrong! Please re-enter\n'.encode())
            n += 1
        return


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == '__main__':
    sever = socketserver.ThreadingTCPServer(('0.0.0.0', 10010), MyServer)
    ThreadedTCPServer.allow_reuse_address = True
    ThreadedTCPServer.allow_reuse_port = True
    sever.serve_forever()