#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор отчётов по результатам сканирования Semgrep
"""

import json
import sys
from collections import Counter
from datetime import datetime

def generate_report(json_file):
    """Генерирует текстовый отчёт из JSON файла Semgrep"""
    
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    results = data.get('results', [])
    errors = data.get('errors', [])
    
    print("=" * 70)
    print("ОТЧЁТ ПО БЕЗОПАСНОСТИ КОДА")
    print("=" * 70)
    print(f"Дата генерации: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Всего найдено уязвимостей: {len(results)}")
    print(f"Ошибок сканирования: {len(errors)}")
    print()
    
    # Статистика по уровням серьёзности
    severity_counts = Counter(r.get('severity', 'UNKNOWN') for r in results)
    print(" Распределение по серьёзности:")
    for severity, count in severity_counts.items():
        print(f"   {severity}: {count}")
    print()
    
    # Статистика по типам уязвимостей
    rule_counts = Counter(r.get('check_id', 'UNKNOWN') for r in results)
    print(" Распределение по типам уязвимостей:")
    for rule_id, count in rule_counts.most_common(10):
        print(f"   {rule_id}: {count}")
    print()
    
    # Детальный список уязвимостей
    print(" Детальный список уязвимостей:")
    print("-" * 70)
    
    for i, result in enumerate(results, 1):
        print(f"\n[{i}] {result.get('check_id', 'UNKNOWN')}")
        print(f"    Серьёзность: {result.get('severity', 'UNKNOWN')}")
        print(f"    Сообщение: {result.get('message', 'N/A')}")
        print(f"    Файл: {result.get('path', 'N/A')}:{result.get('start', {}).get('line', 'N/A')}")
        print(f"    CWE: {result.get('extra', {}).get('metadata', {}).get('cwe', 'N/A')}")
        print(f"    OWASP: {result.get('extra', {}).get('metadata', {}).get('owasp', 'N/A')}")
        
        # Пример кода
        if 'extra' in result and 'lines' in result['extra']:
            print(f"    Код: {result['extra']['lines'].strip()}")
    
    print("\n" + "=" * 70)
    print("РЕКОМЕНДАЦИИ ПО УСТРАНЕНИЮ")
    print("=" * 70)
    
    recommendations = {
        'python-sql-injection': 'Используйте параметризованные запросы вместо интерполяции строк',
        'python-command-injection': 'Избегайте shell=True, используйте subprocess.run с списком аргументов',
        'python-hardcoded': 'Используйте переменные окружения или secure vault для секретов',
        'python-weak-hash': 'Используйте bcrypt, argon2 или pbkdf2 для хеширования паролей',
        'python-weak-random': 'Используйте модуль secrets вместо random для криптографии',
        'python-insecure-deserialization': 'Используйте JSON вместо pickle для ненадёжных данных',
        'python-code-injection': 'Избегайте eval/exec, используйте безопасные альтернативы',
        'python-debug-mode': 'Отключите debug mode в production окружении',
        'python-path-traversal': 'Валидируйте и санируйте пути файлов',
        'python-ssrf': 'Валидируйте URL и используйте whitelist для внешних запросов'
    }
    
    found_categories = set()
    for result in results:
        check_id = result.get('check_id', '')
        for category, rec in recommendations.items():
            if category in check_id.lower():
                found_categories.add(category)
    
    for category in found_categories:
        print(f"• {recommendations[category]}")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python3 generate_report.py <json_file>")
        sys.exit(1)
    
    generate_report(sys.argv[1])
