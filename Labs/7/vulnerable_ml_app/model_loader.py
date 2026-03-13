#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Загрузка моделей с уязвимостями
"""

import torch
import pickle
import joblib

def load_pytorch_model(model_path):
    """Уязвимость: Insecure Model Loading (pickle внутри torch.load)"""
    # По умолчанию torch.load использует pickle, что опасно для непроверенных файлов
    model = torch.load(model_path)
    return model

def load_sklearn_model(model_path):
    """Уязвимость: Insecure Deserialization (pickle)"""
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    return model

def load_joblib_model(model_path):
    """Уязвимость: Insecure Deserialization (joblib)"""
    model = joblib.load(model_path)
    return model

def load_safe_model(model_path):
    """Безопасно: Использование weights_only=True"""
    model = torch.load(model_path, weights_only=True)
    return model
