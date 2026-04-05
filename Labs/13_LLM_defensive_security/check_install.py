from llm_guard.input_scanners import PromptInjection
from llm_guard.input_scanners.prompt_injection import MatchType

try:
    scanner = PromptInjection(threshold=0.5, match_type=MatchType.FULL)
    prompt = "Hello, how are you?"
    sanitized_prompt, is_valid, risk_score = scanner.scan(prompt)
except Exceptionion as e:
    print(f"ERROR: Initialization problem {e}")

