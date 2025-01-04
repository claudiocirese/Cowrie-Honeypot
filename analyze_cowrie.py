import json
import os

# Path to the Cowrie JSON logfile. Adjust as needed.
LOG_PATH = "../log/cowrie.json"

def main():
    """
    This script processes Cowrie's JSON log (cowrie.json) line by line
    and extracts some statistics about:
      - IP addresses (which IP attempted to log in)
      - Credentials (username:password pairs)
      - Commands typed by attackers

    It then prints top-10 rankings for each category.
    """

    # Dictionaries to keep counters for different data points
    ip_count = {}           # Tracks how many times each IP address appears
    credentials_count = {}  # Tracks how many times each (username:password) combo appears
    commands_count = {}     # Tracks how many times each command is used

    # Check if the logfile actually exists
    if not os.path.isfile(LOG_PATH):
        print(f"Log file not found: {LOG_PATH}")
        return

    # Open the JSON log, read line by line
    with open(LOG_PATH, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Each line should be a valid JSON object
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                # If it fails to parse, skip this line
                continue

            # We examine the 'eventid' field to determine the event type
            eventid = data.get("eventid", "")
            src_ip = data.get("src_ip", "")

            # Process login events (failed or successful)
            if eventid in ["cowrie.login.failed", "cowrie.login.success"]:
                username = data.get("username", "")
                password = data.get("password", "")

                # Increment IP counter
                ip_count[src_ip] = ip_count.get(src_ip, 0) + 1

                # Increment credentials counter
                creds = f"{username}:{password}"
                credentials_count[creds] = credentials_count.get(creds, 0) + 1

            # Process command input events
            if eventid == "cowrie.command.input":
                cmd = data.get("input", "")
                commands_count[cmd] = commands_count.get(cmd, 0) + 1

    # Now we display the top 10 for each category

    # Top 10 IPs by login attempts
    print("=== TOP 10 IP ADDRESSES (by number of login attempts) ===")
    sorted_ips = sorted(ip_count.items(), key=lambda x: x[1], reverse=True)[:10]
    for ip, count in sorted_ips:
        print(f"{ip}: {count} attempts")

    # Top 10 credentials
    print("\n=== TOP 10 CREDENTIALS (username:password) ===")
    sorted_creds = sorted(credentials_count.items(), key=lambda x: x[1], reverse=True)[:10]
    for creds, count in sorted_creds:
        print(f"{creds} -> {count} times")

    # Top 10 commands
    print("\n=== TOP 10 COMMANDS ENTERED ===")
    sorted_cmds = sorted(commands_count.items(), key=lambda x: x[1], reverse=True)[:10]
    for cmd, count in sorted_cmds:
        print(f"{cmd} -> {count} times")


if __name__ == "__main__":
    main()
