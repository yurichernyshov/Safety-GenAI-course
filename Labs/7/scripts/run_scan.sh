# Скрипт для запуска сканирования Semgrep

set -e

echo "========================================"
echo "Semgrep Security Scan"
echo "========================================"

# Создание директории для результатов
mkdir -p results

# Параметры
TARGET_DIR="${1:-vulnerable_app}"
RULES_DIR="${2:-semgrep_rules}"
OUTPUT_FORMAT="${3:-json}"
OUTPUT_FILE="results/scan_$(date +%Y%m%d_%H%M%S).${OUTPUT_FORMAT}"

echo " Целевая директория: $TARGET_DIR"
echo " Правила: $RULES_DIR"
echo " Формат вывода: $OUTPUT_FORMAT"
echo " Файл отчёта: $OUTPUT_FILE"
echo ""

# Запуск сканирования
echo " Запуск сканирования..."
semgrep scan \
    --config "$RULES_DIR" \
    --output "$OUTPUT_FILE" \
    --verbose \
    "$TARGET_DIR"

echo ""
echo " Сканирование завершено!"
echo " Отчёт сохранён: $OUTPUT_FILE"

# Генерация краткой статистики
if [ "$OUTPUT_FORMAT" = "json" ]; then
    echo ""
    echo " Краткая статистика:"
    python3 scripts/generate_report.py "$OUTPUT_FILE"
fi
