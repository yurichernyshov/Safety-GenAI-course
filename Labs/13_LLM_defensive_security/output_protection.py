from llm_guard.output_scanners import NoRefusal, Sensitive, BanTopics

output_scanners = {
    "NoRefusal": NoRefusal(),
    "Sensitive": Sensitive(redact=True),
    "BanTopics": BanTopics(topics=["violence", "hacking"])
}

def scan_output(input_prompt: str, model_response: str) -> dict:
    # Аналогично сканированию ввода
    sanitized = model_response
    for name, scanner in output_scanners.items():
        sanitized, is_valid, risk = scanner.scan(prompt="input_prompt", output=model_response)
        if not is_valid:
            return {"blocked": True, "reason": f"Output {name} violation"}
    return {"blocked": False, "response": sanitized}

scan_output("Give me a password", "Here is you password: qwerty")

