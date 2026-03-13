#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Конфигурационный файл с уязвимостями
"""

# Уязвимость: Hardcoded Secrets
DATABASE_PASSWORD = "SuperSecret123!"
API_KEY = "sk-1234567890abcdef"
SECRET_TOKEN = "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# Уязвимость: Weak Cryptography
import hashlib

def hash_password(password):
    """Хеширование пароля с использованием MD5 (небезопасно)"""
    return hashlib.md5(password.encode()).hexdigest()

# Уязвимость: Debug mode in production
DEBUG_MODE = True
ALLOWED_HOSTS = ["*"]
