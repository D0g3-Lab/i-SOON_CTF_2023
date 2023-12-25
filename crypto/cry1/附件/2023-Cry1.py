# -*- coding:utf-8 -*-
import os
import random
import string
import hashlib
import socketserver
from Crypto.Util.number import isPrime, long_to_bytes, getStrongPrime, bytes_to_long

flag = b"D0g3{******************************************}"

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

    def getPQN(self):
        while True:
            p = getStrongPrime(2048)
            q = getStrongPrime(2048)
            n = p * q
            if p.bit_length() == 2048 and q.bit_length() == 2048 and n.bit_length() == 4096:
                return p, q, n

    def encrypt(self):
        p, q, n = self.getPQN()
        m = bytes_to_long(flag)
        e = 0x10001
        c = pow(m, e, n)
        p = bin(p)[2:]
        p1 = list(p[:1024])
        p2 = list(p[1024:])
        p1[random.choice([i for i, c in enumerate(p1) if c == '1'])] = '0'
        p2[random.choice([i for i, c in enumerate(p1) if c == '0'])] = '1'
        return n, ''.join(p1) + ''.join(p2), c

    def handle(self):
        if not self.proof():
            self.request.sendall(b'Error Hash!')
            return
        n, p, c = self.encrypt()
        self.request.sendall('Press 1 to get ciphertext\n'.encode())
        number = self.request.recv(512).strip().decode()
        if number == '1':
            self.request.sendall((str(n) + '\n').encode())
            self.request.sendall((str(p) + '\n').encode())
            self.request.sendall((str(c) + '\n').encode())
        else:
            self.request.sendall('Incorrect input!\n'.encode())
        return


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == '__main__':
    sever = socketserver.ThreadingTCPServer(('0.0.0.0', 10001), MyServer)
    ThreadedTCPServer.allow_reuse_address = True
    ThreadedTCPServer.allow_reuse_port = True
    sever.serve_forever()