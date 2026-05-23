import json
import os
from datetime import datetime


def log_attack(username, attack_text, attack_type):

    try:

        attack = {
            "username": username,
            "attack": attack_text,
            "type": attack_type,
            "risk": "High",
            "time": str(datetime.now())
        }

        # Get project root
        project_root = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                ".."
            )
        )

        file_path = os.path.join(
            project_root,
            "data",
            "attacks.json"
        )

        print("\n===== LOGGER DEBUG =====")
        print("PROJECT ROOT:")
        print(project_root)

        print("ATTACK FILE:")
        print(file_path)

        # Ensure data folder exists
        os.makedirs(
            os.path.dirname(file_path),
            exist_ok=True
        )

        # Create file if missing
        if not os.path.exists(file_path):

            print("Creating attacks.json")

            with open(file_path, "w") as f:
                json.dump([], f)

        # Read file
        with open(file_path, "r") as f:

            try:
                data = json.load(f)

            except:

                data=[]

        print("OLD DATA:")
        print(data)

        data.append(attack)

        # Write back
        with open(file_path, "w") as f:

            json.dump(
                data,
                f,
                indent=4
            )

        print("NEW ENTRY SAVED")
        print(attack)

        print("====================\n")

    except Exception as e:

        print("\nLOGGER ERROR:")
        print(str(e))
print("JSON WRITE COMPLETE")