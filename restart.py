#!/usr/bin/env python3
import subprocess
import time

command = ["python3", "app.py"]  
while True:
    try:
        process = subprocess.Popen(command)
        process.wait()
    except KeyboardInterrupt:
        print("\nScript dihentikan secara manual.")
        break
    except Exception as e:
        print(f"\nError: {e}")
        print("Melakukan restart dalam 1 detik...")
        time.sleep(1)