# -*- coding:utf-8 -*-
import os
import random
import string
import hashlib
import socketserver
from secret import *
import uuid
import gmpy2
from Crypto.Util.number import isPrime, long_to_bytes, getStrongPrime, bytes_to_long


def get_flag(head):
    table = string.printable
    name = ''.join([random.choice(table) for i in range(10)])
    return head + '{' + str(uuid.uuid5(uuid.NAMESPACE_OID, name)) + '}'


def relation():
    a, b = 0, 0
    for i in range(x - (2**2 - 1)):
        a += pow(e1, i)
    for j in range(3):
        b += pow(e2, j)
    if a == b:
        return True
    return False


def get_pqr():
    while True:
        p = getStrongPrime(1024)
        q = getStrongPrime(1024)
        if p % 4 == 3 and q % 4 == 3:
            break
    r = 2
    while True:
        r = r * x
        if r.bit_length() > 1024 and isPrime(r - 1):
            r = r - 1
            break
    return p, q, r


def encrypt():
    # if relation():
    #     print('success')
    # else:
    #     print('false')
    
    flag = 'D0g3{82309bce-9db6-5340-a9e4-a67a9ba15345}'  # get_flag('D0g3')

    m1 = ''.join([random.choice(string.ascii_letters) for _ in range(234)]) + ' ' + flag[:21]
    m2 = flag[21:] + ' ' + ''.join([random.choice(string.ascii_letters) for _ in range(234)])

    p, q, r = get_pqr()
    phi = (p - 1) * (q - 1) * (q - 1)
    while True:
        try:
            d = gmpy2.invert(e2, phi)
            break
        except Exception as e:
            p, q, r = get_pqr()

    n = p * q * r
    inv_p = gmpy2.invert(p, q)
    inv_q = gmpy2.invert(q, p)

    # print(e1, e2)
    c1 = pow(bytes_to_long(m1.encode()), e1, n)
    c2 = pow(bytes_to_long(m2.encode()), e2, n)

    return n, inv_p, inv_q, c1, c2
    # print("n = %d" % n)
    # print("ip = %d" % inv_p)
    # print("iq = %d" % inv_q)
    # print("c1 = %d" % c1)
    # print("c2 = %d" % c2)


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
        n, inv_p, inv_q, c1, c2 = encrypt()
        self.request.sendall('Press 1 to get ciphertext\n'.encode())
        number = self.request.recv(512).strip().decode()
        if number == '1':
            self.request.sendall(("n = %d\n" % n).encode())
            self.request.sendall(("inv_p = %d\n" % inv_p).encode())
            self.request.sendall(("inv_q = %d\n" % inv_q).encode())
            self.request.sendall(("c1 = %d\n" % c1).encode())
            self.request.sendall(("c2 = %d\n" % c2).encode())
        else:
            self.request.sendall('Incorrect input!\n'.encode())
        return


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == '__main__':
    sever = socketserver.ThreadingTCPServer(('0.0.0.0', 10100), MyServer)
    ThreadedTCPServer.allow_reuse_address = True
    ThreadedTCPServer.allow_reuse_port = True
    sever.serve_forever()