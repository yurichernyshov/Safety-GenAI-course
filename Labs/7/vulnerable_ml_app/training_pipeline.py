"""
Пайплайн обучения с уязвимостями
"""

import pandas as pd
import numpy as np

def load_training_data(source_url):
    """Уязвимость: SSRF / Untrusted Data Source"""
    # Загрузка данных из непроверенного источника
    df = pd.read_csv(source_url)
    return df

def train_model(data):
    """Уязвимость: Lack of Data Validation (риск Data Poisoning)"""
    # Отсутствие проверки на выбросы или аномалии в данных
    # Злоумышленник может внедрить отравленные примеры
    X = data.drop('label', axis=1)
    y = data['label']
    # ... обучение ...
    return "Model trained"
