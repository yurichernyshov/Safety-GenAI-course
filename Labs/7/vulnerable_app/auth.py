#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Модуль аутентификации с уязвимостями
"""

import hashlib
import random

# Уязвимость: Hardcoded Credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

def verify_password(input_password, stored_hash):
    """Уязвимость: Weak Cryptography"""
    # Использование MD5 для хеширования паролей
    input_hash = hashlib.md5(input_password.encode()).hexdigest()
    return input_hash == stored_hash

def generate_token():
    """Уязвимость: Weak Random Number Generator"""
    # Использование random вместо secrets для криптографических целей
    return str(random.random())

def check_auth(username, password):
    """Уязвимость: Hardcoded Credentials"""
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        return True
    return False
