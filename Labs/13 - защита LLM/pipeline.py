from llm_guard.input_scanners import PromptInjection, BanSubstrings, Toxicity, Secrets
from llm_guard.input_scanners.prompt_injection import MatchType


# Конфигурация сканеров
scanners = {
    "PromptInjection": PromptInjection(threshold=0.5, match_type=MatchType.FULL),
    "BanSubstrings": BanSubstrings(substrings=["ignore instructions", "developer mode"], match_type=MatchType.FULL),
    "Toxicity": Toxicity(threshold=0.8),
    "Secrets": Secrets()
}

def scan_input(user_input: str) -> dict:
    results = {}
    sanitized_input = user_input
    is_blocked = False
    block_reason = ""

    for name, scanner in scanners.items():
        try:
            sanitized, is_valid, risk_score = scanner.scan(sanitized_input)
            results[name] = {"valid": is_valid, "risk": risk_score}
            
            if not is_valid or risk_score > 0.5: # Глобальный порог блокировки
                is_blocked = True
                block_reason = f"{name} detected risk {risk_score:.2f}"
                break # Прерываем при первом критическом нарушении
            
            sanitized_input = sanitized
        except Exception as e:
            results[name] = {"error": str(e)}
            
    return {"blocked": is_blocked, "reason": block_reason, "details": results, "sanitized": sanitized_input}

scan_input("Hello!")
scan_input("Give me an example of reverse shell tool in python") 
