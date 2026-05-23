def detect_prompt_injection(prompt):

    print("\n========== PROMPT DETECTOR ==========")

    suspicious_patterns=[

        "ignore previous instructions",
        "ignore instructions",
        "reveal system prompt",
        "developer mode",
        "jailbreak",
        "forget your instructions",
        "bypass safety",
        "pretend to be",
        "you are now",
        "ignore all rules",
        "act as",
        "system prompt",
        "disable security"

    ]

    prompt=prompt.lower()

    print("User Prompt:",prompt)

    for pattern in suspicious_patterns:

        print("Checking:",pattern)

        if pattern in prompt:

            print("MATCH FOUND:",pattern)
            print("=================================\n")

            return True,pattern


    print("No attack detected")
    print("=================================\n")

    return False,None