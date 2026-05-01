# Применение DVC для управления данными и обнаружения отравления обучающего набора

Тема: Обеспечение целостности данных в ML-пайплайне с помощью DVC (Data Version Control) и выявление признаков атаки типа Data Poisoning.

DVC — это инструмент целостности (Integrity), а не конфиденциальности. Для защиты от подмены самих файлов версий (.dvc) необходимо использовать подписанные Git-коммиты и строгий контроль доступа к репозиторию.

Цель работы
•	Освоить базовые принципы работы DVC для версионирования данных.
•	Понять роль хеширования в обеспечении целостности данных (Data Integrity).
•	Смоделировать атаку «Отравление данных» (Data Poisoning) путем несанкционированного изменения датасета.
•	Научиться использовать инструменты DVC для обнаружения изменений в данных перед обучением модели.
•	Отработать процедуру восстановления «чистой» версии данных.

Необходимые инструменты
ОС: Linux, macOS или Windows (с Git Bash/WSL).
ПО: Python 3.8+ (рекомендуется 3.12), Git, DVC (pip install dvc), Pandas, Scikit-learn.
Хранилище: Локальное (.dvc/cache), удаленное хранилище не требуется (для упрощения).

Инициализация проекта
Создание виртуального окружения
mkdir ml-security-lab
cd ml-security-lab
python3 -m venv venv
pip install -r requirements.txt
Рекомендуется использовать общий файл requirements.txt курса

Установка и настройка dvc
pip install dvc
git init
dvc init
# Сохраняем состояние DVC в Git
git add .
git commit -m "Init DVC project"

Генерация данных
import pandas as pd
import numpy as np

def generate_clean_data(filename="data/train.csv"):
    np.random.seed(42)
    # 1000 сэмплов, 5 признаков
    X = np.random.rand(1000, 5)
    # Простая логика: если сумма признаков > 2.5, класс 1, иначе 0
    y = (X.sum(axis=1) > 2.5).astype(int)
    
    df = pd.DataFrame(X, columns=[f"feat_{i}" for i in range(5)])
    df['label'] = y
    
    df.to_csv(filename, index=False)
    print(f"Датасет создан: {filename}, строк: {len(df)}")

if __name__ == "__main__":
    import os
    os.makedirs("data", exist_ok=True)
    generate_clean_data()


python generate_data.py
dvc add data/train.csv
git add data/train.csv.dvc .gitignore
git commit -m "Add clean training data v1.0"


Пояснение: Файл data/train.csv.dvc содержит мета-данные, включая MD5/SHA хеш файла. Это «якорь» целостности.


Обучение базовой модели

Train.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib

def train():
    df = pd.read_csv("data/train.csv")
    X = df.drop('label', axis=1)
    y = df['label']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LogisticRegression()
    model.fit(X_train, y_train)
    
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    
    print(f"Accuracy: {acc:.4f}")
    joblib.dump(model, "model.pkl")
    return acc

if __name__ == "__main__":
    train()

python train.py
# Запишите точность (Accuracy) в отчет. Ожидаемая: ~0.95-1.0

Симуляция атаки «Отравление данных» (Data Poisoning)
Симуляция ситуации: злоумышленник получил доступ к файловой системе или скомпрометировал пайплайн загрузки данных. Он меняет метки у части данных, чтобы ухудшить работу модели.

Attack_poisoning.py

import pandas as pd
import numpy as np

def poison_data(filename="data/train.csv"):
    df = pd.read_csv(filename)
    # Атака: Инвертируем метки (label) у первых 200 записей
    # Это имитирует внесение шумов или целевое отравление
    df.loc[:200, 'label'] = 1 - df.loc[:200, 'label']
    
    df.to_csv(filename, index=False)
    print("АТАКА ВЫПОЛНЕНА: Данные изменены локально!")

if __name__ == "__main__":
    poison_data()

Важно: Запустите атаку, но НЕ делайте коммит в Git/DVC. В реальном сценарии злоумышленник часто скрывает следы или меняет данные в промежуточном хранилище перед обучением.

Обнаружение изменения (Integrity Check)
Перед запуском переобучения инженер по ML должен убедиться, что данные не изменились. Проверить статус репозитория dvc
dvc status
Ожидаемый результат: DVC покажет, что data/train.csv изменен (modified).

что именно изменилось (DVC не показывает контент, но показывает факт изменения):
dvc diff

Примечание: Так как мы не коммитили изменения, dvc diff может показать разницу между рабочей директорией и HEAD (если настроено), но основной инструмент здесь — dvc status.

Ручная проверка хеша (для понимания механики):
Откройте файл data/train.csv.dvc в текстовом редакторе. Найдите поле md5 или sha256. Вычислите хеш текущего файла вручную и сравните:
md5sum data/train.csv
Сравните хеш в .dvc файле и хеш текущего файла. 

Запуск обучения на отравленных данных
Зафиксировать новую точность (Accuracy). Она должна значительно упасть из-за неверных меток.

Реагирование и восстановление (Mitigation)
Обнаружив расхождение хешей, система безопасности (или инженер) блокирует пайплайн и восстанавливает данные.
Восстановите оригинальную версию данных из кеша DVC:
dvc checkout data/train.csv
Проверить, что статус не изменялся
dvc status
Проверьте хеш вручную еще раз. Он должен совпадать с записью в data/train.csv.dvc.
Переобучите модель на восстановленных данных, точность должна вернуться к исходной.

Аудит истории коммитов в git и dvc и исправление
Представим, что злоумышленник успел сделать коммит «плохих» данных (например, подменив ключи доступа). Как найти, когда это произошло?
Внесите изменения в файл снова (симуляция коммита атаки):
python attack_poison.py
dvc add data/train.csv
git add data/train.csv.dvc
git commit -m "Update data (SUSPICIOUS)"

Сравнить текущую версию с предыдущей (HEAD~1)
dvc diff HEAD~1 HEAD
Тут можно использовать инструменты для валидации данных. Например, для анализа распределения меток.

Откат к чистой версии
git checkout HEAD~1 -- data/train.csv.dvc
dvc checkout data/train.csv


Дополнительные задания (со звездочкой *)
•	Валидация схемы: Добавьте библиотеку Great Expectations или Pandera. Настройте проверку, чтобы пайплайн останавливался, если распределение меток label отклоняется от ожидаемого (например, соотношение 0/1 стало 50/50 вместо 90/10).
•	Удаленное хранилище: Настройте удаленное хранилище DVC (например, через S3 совместимый MinIO или SSH). Покажите, как dvc push и dvc pull помогают синхронизировать доверенные данные между командами.
•	Pre-commit хуки: Настройте pre-commit хук, который запрещает коммит, если dvc status показывает изменения в данных, но не обновлен файл .dvc.
Вопросы для проверки
Почему хранение данных в Git без DVC не защищает от отравления? (Подсказка: размер файлов, бинарные форматы, отсутствие хеширования контента в трекинге).
Что произойдет, если злоумышленник изменит данные и пересчитает хеш вручную, обновив .dvc файл? Как защититься от этого? (Подсказка: подписанные коммиты GPG, защита веток, CI/CD проверки).
Сценарий защиты:
Опишите, как интегрировать проверку dvc status в CI/CD пайплайн (например, GitHub Actions), чтобы сборка падала при изменении данных без согласования.
