import time
from langfuse import Langfuse

langfuse = Langfuse()

def complex_workflow(query):
    trace = langfuse.trace(name="research-agent", user_id="student_01")
    
    # Шаг 1: Поиск (имитация задержки)
    with trace.span(name="search-knowledge-base") as search_span:
        time.sleep(1) 
        context = "Langfuse - это инструмент для мониторинга LLM."
        search_span.end(output={"context_found": True})
    
    # Шаг 2: Генерация ответа
    with trace.span(name="llm-generation") as gen_span:
        # В реальном проекте здесь был бы вызов OpenAI
        time.sleep(1.5)
        response = f"На основе данных: {context}, отвечаю на {query}"
        gen_span.end(output=response)
        
    # Шаг 3: Пост-обработка
    with trace.span(name="formatting") as fmt_span:
        time.sleep(0.5)
        fmt_span.end(output="Formatted")
        
    return response

complex_workflow("Как работает Langfuse?")
