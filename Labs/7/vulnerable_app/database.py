"""
Модуль работы с базой данных с уязвимостями
"""

import sqlite3
import os

def get_user_by_id(user_id):
    """Уязвимость: SQL Injection"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # ОПАСНО: Интерполяция строк в SQL-запросе
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    
    return cursor.fetchone()

def search_users(username):
    """Уязвимость: SQL Injection (LIKE)"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # ОПАСНО: Пользовательский ввод в LIKE запросе
    query = "SELECT * FROM users WHERE username LIKE '%" + username + "%'"
    cursor.execute(query)
    
    return cursor.fetchall()

def delete_user(user_id):
    """Уязвимость: SQL Injection (DELETE)"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    query = "DELETE FROM users WHERE id = %s" % user_id
    cursor.execute(query)
    conn.commit()
