import json
import os

# Adjust this path to point to your actual cowrie.json location
LOG_PATH = "../log/cowrie.json"

def main():
    # Dictionaries for stats
    ip_count = {}
    credentials_count = {}
    commands_count = {}

    # Additional counters
    total_lines = 0       # how many non-empty lines in cowrie.json
    total_events = 0      # how many lines were valid JSON events
    login_attempts = 0    # how many times we saw login.failed/login.success

    if not os.path.isfile(LOG_PATH):
        print(f"No log file found at {LOG_PATH}")
        return

    with open(LOG_PATH, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            total_lines += 1

            # Attempt to parse JSON
            try:
                data = json.loads(line)
                total_events += 1
            except json.JSONDecodeError:
                continue

            eventid = data.get("eventid", "")
            src_ip = data.get("src_ip", "")

            # Track login attempts
            if eventid in ["cowrie.login.failed", "cowrie.login.success"]:
                login_attempts += 1

                username = data.get("username", "")
                password = data.get("password", "")

                # Update IP dictionary
                ip_count[src_ip] = ip_count.get(src_ip, 0) + 1

                # Update credentials dictionary
                creds_key = f"{username}:{password}"
                credentials_count[creds_key] = credentials_count.get(creds_key, 0) + 1

            # Track commands
            if eventid == "cowrie.command.input":
                cmd = data.get("input", "")
                commands_count[cmd] = commands_count.get(cmd, 0) + 1

    # Print a summary
    print("=== SUMMARY ===")
    print(f"Total lines (non-empty) in the log file: {total_lines}")
    print(f"Total valid JSON events: {total_events}")
    print(f"Total login attempts detected: {login_attempts}")
    print(f"Number of unique IPs involved: {len(ip_count)}")

    # Print top 10 IP
    print("\n=== TOP 10 IP (by number of login attempts) ===")
    sorted_ip = sorted(ip_count.items(), key=lambda x: x[1], reverse=True)[:10]
    for ip, count in sorted_ip:
        print(f"{ip} -> {count} attempts")

    # Print top 10 credentials
    print("\n=== TOP 10 CREDENTIALS USED ===")
    sorted_creds = sorted(credentials_count.items(), key=lambda x: x[1], reverse=True)[:10]
    for creds, num in sorted_creds:
        print(f"{creds} -> {num} times")

    # Print top 10 commands
    print("\n=== TOP 10 COMMANDS ENTERED ===")
    sorted_cmds = sorted(commands_count.items(), key=lambda x: x[1], reverse=True)[:10]
    for cmd, num in sorted_cmds:
        print(f"{cmd} -> {num} times")

if __name__ == "__main__":
    main()
