import os
import platform
import redis
import subprocess

def ping(host):
    # Check the operating system to determine the appropriate ping command
    ping_str = "-n 1" if platform.system().lower() == "windows" else "-c 1"

    # Send a single ICMP echo request packet to the host
    command = ["ping", ping_str, host]
    return subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

# Redis connection
redis_host = "localhost"
redis_port = 6379
redis_db = 0
redis_ttl = 60  # 1 minute TTL

redis_client = redis.Redis(host=redis_host, port=redis_port, db=redis_db)

# Example usage
host_to_ping = "13.127.65.19"
if ping(host_to_ping):
    print(f"The host {host_to_ping} is reachable.")
else:
    print(f"The host {host_to_ping} is not reachable.")
    redis_client.setex(host_to_ping, redis_ttl, "unreachable")
