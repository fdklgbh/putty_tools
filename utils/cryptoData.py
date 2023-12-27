# -*- coding: utf-8 -*-
# @Author  : fdklgbh
# @FileName: cryptoData.py
"""

"""
from config import CRYPTO_KEY

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64
import hashlib


# 创建 AES 加密对象
def create_aes_cipher(iv):
    key = hashlib.sha256(CRYPTO_KEY.encode('utf-8')).digest()  # 转换为 32 字节的密钥
    return AES.new(key, AES.MODE_CBC, iv)


# AES 加密函数
def encrypt(plaintext, useIv=True):
    if useIv:
        iv = get_random_bytes(AES.block_size)
    else:
        iv = b''
    cipher = create_aes_cipher(iv)
    ciphertext = cipher.encrypt(pad(plaintext.encode('utf-8'), AES.block_size))
    return base64.b64encode(iv + ciphertext).decode('utf-8')


# AES 解密函数
def decrypt(ciphertext):
    ciphertext = base64.b64decode(ciphertext.encode('utf-8'))
    iv = ciphertext[:AES.block_size]
    cipher = create_aes_cipher(iv)
    decrypted = unpad(cipher.decrypt(ciphertext[AES.block_size:]), AES.block_size)
    return decrypted.decode('utf-8')


__all__ = ['decrypt', 'encrypt']
