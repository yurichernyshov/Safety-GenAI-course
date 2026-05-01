# Практическое применение методов SHAP и LIME для интерпретации работы модели машинного обучения

Оглавление
Общее описание	1
Теоретические сведения	1
Описание практики	3
Дополнительные задания (повышенной сложности)	7
Ссылки	7

Общее описание
Цель работы: изучить методологию и освоить базовые практические навыки применения методов объяснимого искусственного интеллекта (Explainable Artificial Intelligence, XAI). В качестве методов объяснения применяются типовые инструменты SHAP и LIME, используемые для интерпретации предсказаний моделей машинного обучения.
Этапы практического занятия:
•	Изучить теоретические основы методов SHAP и LIME 
•	Научиться устанавливать и настраивать необходимые библиотеки
•	Построить модель машинного обучения на табличных данных
•	Применить LIME для локальной интерпретации отдельных предсказаний
•	Применить SHAP для локальной и глобальной интерпретации модели
•	Сравнить результаты и сделать выводы о применимости методов

Теоретические сведения
Метод LIME (Local Interpretable Model-agnostic Explanations)
Основная идея: LIME аппроксимирует поведение сложной закрытой (black-box) модели машинного обучения локально, в окрестности конкретного предсказания, с помощью простой интерпретируемой модели (например, линейной регрессии). 
Алгоритм работы:
•	Выбирается экземпляр данных, предсказание которого нужно объяснить
•	Генерируются выборки данных с отклонением от заданного экземпляра, с помощью случайного изменения признаков
•	Для каждой выборки с отклонением получаются предсказания исходной модели
•	Выборам назначается вес, учитывающий близость к исходному экземпляру
•	На взвешенных данных обучается простая интерпретируемая модель
•	Коэффициенты этой модели показывают вклад признаков в предсказание 

Преимущества LIME:
•	Не зависит от модели (model-agnostic)
•	Поддерживает табличные данные, текст и изображения 
•	Даёт интуитивно понятные локальные объяснения
•	Прост в использовании 
Ограничения:
•	Выбор размера окрестности для генерации выборки и назначения весов — нерешённая проблема 
•	Возможна нестабильность объяснений при повторных запусках
•	Игнорирует зависимости между признаками при сэмплировании

Метод SHAP (SHapley Additive exPlanations)
Основная идея: SHAP использует значения Шепли (Shapley Values) из теории кооперативных игр для справедливого распределения вклада каждого признака в предсказание модели. Применяется теория игр: каждый признак играет роль «игрока» и алгоритм должен определить вклад каждого игрока в общий результат.
Ключевые свойства SHAP:
•	Локальная точность: сумма вкладов признаков равна разнице между предсказанием и средним предсказанием
•	Отсутствие вклада для отсутствующих признаков: если признак не используется, его вклад = 0
•	Согласованность: если вклад признака в модели увеличивается, его SHAP-значение также не уменьшается 
Преимущества SHAP:
•	Теоретически обоснован (единственное решение, удовлетворяющее аксиомам Шепли) 
•	Согласованность локальных и глобальных объяснений
•	Быстрая реализация для деревьев (TreeSHAP) 
•	Богатая визуализация: force plots, summary plots, dependence plots 

Ограничения:
•	KernelSHAP вычислительно затратен для больших наборов данных
•	Игнорирует зависимости между признаками (при маргинальном сэмплировании)
•	Возможна интерпретационная неоднозначность при коррелированных признаках 




Описание практики

Шаг 1: Создание виртуального окружения и установка необходимых библиотек (если не установлены)
python3 -m venv venv
source ./venv/bin/activate
pip install shap lime scikit-learn pandas numpy matplotlib seaborn

# Импорт библиотек
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.datasets import load_breast_cancer, load_wine
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

import shap
import lime
from lime import lime_tabular

# Настройка визуализации
plt.style.use('seaborn-v0_8')
shap.initjs()


# Загрузка датасета (на выбор: breast_cancer или wine)
data = load_wine()
X = pd.DataFrame(data.data, columns=data.feature_names)
y = pd.Series(data.target, name='target')

print(f"Размер датасета: {X.shape}")
print(f"Классы: {dict(zip(range(len(data.target_names)), data.target_names))}")
print(X.head())

# Разделение на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

print(f"Обучающая выборка: {X_train.shape}, Тестовая: {X_test.shape}")

Обучение модели
# Обучение Random Forest классификатора
model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
model.fit(X_train, y_train)

# Оценка качества модели
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)

print(f"Точность на тесте: {accuracy_score(y_test, y_pred):.3f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=data.target_names))

Интерпретация с помощью LIME
# Инициализация LIME explainer для табличных данных
lime_explainer = lime_tabular.LimeTabularExplainer(
    training_data=X_train.values,
    feature_names=X_train.columns.tolist(),
    class_names=data.target_names,
    mode='classification',
    random_state=42
)
# Выбор экземпляра для объяснения (например, первый из тестовой выборки)
idx = 0
instance = X_test.iloc[idx]
true_label = y_test.iloc[idx]
predicted_label = np.argmax(y_proba[idx])
predicted_proba = y_proba[idx][predicted_label]

print(f"Индекс: {idx}")
print(f"Истинный класс: {data.target_names[true_label]}")
print(f"Предсказанный класс: {data.target_names[predicted_label]} (вероятность: {predicted_proba:.3f})")

# Получение объяснения LIME
explanation = lime_explainer.explain_instance(
    data_row=instance.values,
    predict_fn=model.predict_proba,
    top_labels=3,  # количество классов для объяснения
    num_features=len(X.columns),  # показать все признаки
    num_samples=5000  # количество возмущённых выборок
)

# Визуализация объяснения
explanation.show_in_notebook()
# Или сохранить как HTML: explanation.save_to_file('lime_explanation.html')

# Анализ весов признаков для конкретного класса
print(f"\nВеса признаков для класса '{data.target_names[predicted_label]}':")
for feature, weight in explanation.as_list(label=predicted_label):
    print(f"{feature:30s} {weight:+.4f}")


Вопросы для анализа:
Какие признаки оказали наибольшее положительное/отрицательное влияние на предсказание?
Соответствуют ли объяснения LIME вашим ожиданиям, исходя из предметной области?
Как изменится объяснение, если выбрать другой экземпляр из тестовой выборки?

Интерпретация с помощью SHAP
# Инициализация SHAP explainer (TreeExplainer для деревьев)
shap_explainer = shap.TreeExplainer(model)

# Вычисление SHAP-значений для тестовой выборки
shap_values = shap_explainer.shap_values(X_test)

# Force plot для одного экземпляра (локальное объяснение)
idx = 0
shap.force_plot(
    shap_explainer.expected_value[predicted_label],
    shap_values[predicted_label][idx],
    X_test.iloc[idx],
    feature_names=X.columns.tolist(),
    matplotlib=True,
    show=False
)
plt.title(f"SHAP Force Plot — Предсказание: {data.target_names[predicted_label]}")
plt.tight_layout()
plt.show()

# Summary plot — глобальная важность признаков
shap.summary_plot(
    shap_values[predicted_label],
    X_test,
    feature_names=X.columns.tolist(),
    plot_type="dot",  # или "bar" для bar plot
    show=False
)
plt.title("SHAP Summary Plot — Важность признаков")
plt.tight_layout()
plt.show()

# Dependence plot — зависимость SHAP-значения от значения признака
shap.dependence_plot(
    index=0,  # индекс признака (например, первый признак)
    shap_values=shap_values[predicted_label],
    features=X_test,
    feature_names=X.columns.tolist(),
    interaction_index="auto",  # автоматический выбор признака для цвета
    show=False
)
plt.title(f"SHAP Dependence Plot — {X.columns[0]}")
plt.tight_layout()
plt.show()


Дополнительные задания (повышенной сложности)
Эксперимент с разными моделями: Примените SHAP/LIME к линейной модели, SVM и нейросети. Сравните качество и скорость объяснений.
Анализ стабильности LIME: Запустите объяснение одного экземпляра 10 раз с разными random_state. Оцените вариативность весов признаков (стандартное отклонение).
Работа с текстовыми данными: Используйте SHAP для интерпретации модели классификации текстов (например, тональности отзывов). Примените shap.Explainer с maskers.Text.
Исследование влияния корреляции признаков: Создайте синтетические данные с коррелированными признаками. Проанализируйте, как это влияет на SHAP-значения при маргинальном и условном сэмплировании.
Визуализация взаимодействий: Постройте heatmap SHAP interaction values для пары наиболее взаимодействующих признаков.

Ссылки
christophm.github.io
Официальная документация SHAP: https://shap.readthedocs.io 
shap.readthedocs.io
Книга «Interpretable Machine Learning» (Christoph Molnar): https://christophm.github.io/interpretable-ml-book/ 
Туториал по LIME: https://github.com/marcotcr/lime
Практический гайд по SHAP: https://www.kaggle.com/code/khusheekapoor/explainable-ai-intro-to-lime-shap 
Статья сравнение: «SHAP and LIME: Great ML Explainers with Pros and Cons» 
