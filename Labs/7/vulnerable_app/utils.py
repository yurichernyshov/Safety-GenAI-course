#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Утилиты с уязвимостями
"""

import os
import tempfile

def save_uploaded_file(file_content, filename):
    """Уязвимость: Path Traversal"""
    # ОПАСНО: Нет проверки пути файла
    filepath = f"/uploads/{filename}"
    
    with open(filepath, 'w') as f:
        f.write(file_content)
    
    return filepath

def read_file(filename):
    """Уязвимость: Path Traversal"""
    # ОПАСНО: Нет проверки пути файла
    filepath = f"/data/{filename}"
    
    with open(filepath, 'r') as f:
        return f.read()

def download_file(url):
    """ Уязвимость: SSRF (Server-Side Request Forgery)"""
    import urllib.request
    
    # ОПАСНО: Нет проверки URL
    response = urllib.request.urlopen(url)
    return response.read()
