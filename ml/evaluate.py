import os
import json
import sys

# Seuil de qualité (90% par défaut)
ACCURACY_THRESHOLD = float(os.getenv("ACCURACY_THRESHOLD", "0.90"))

def main():
    # Lecture de l'input (soit pipe stdin, soit argument)
    if not sys.stdin.isatty():
        payload = sys.stdin.read().strip()
    else:
        # Fallback si testé manuellement sans pipe
        payload = sys.argv[1]

    data = json.loads(payload)
    acc = float(data["accuracy"])
    
    passed = acc >= ACCURACY_THRESHOLD

    result = {
        "passed": passed,
        "accuracy": acc,
        "threshold": ACCURACY_THRESHOLD,
        "model_version": data.get("model_version"),
        "run_id": data.get("run_id"),
    }
    
    print(json.dumps(result))
    
    # Code de sortie : 0 si succès, 2 si échec (pour faire échouer la CI)
    if not passed:
        sys.exit(2)

if __name__ == "__main__":
    main()