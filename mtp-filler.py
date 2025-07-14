#!/usr/bin/env python3
import os
import subprocess
import time
import sys
import argparse

BASE = os.path.dirname(__file__)

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def create_dummy_file(path, size):
    with open(path, 'wb') as f:
        f.seek(size-1)
        f.write(b'\0')

def detect_kindle_device():
    try:
        result = subprocess.run(['mtp-detect'],
                              capture_output=True, text=True, timeout=10)

        if 'Amazon' in result.stdout or 'Kindle' in result.stdout:
            print("Kindle device detected!")
            return True
        else:
            print("No Kindle device found")
            return False
    except subprocess.TimeoutExpired:
        print("Timeout detecting device")
        return False
    except Exception as e:
        print(f"Error detecting device: {e}")
        return False

def wait_for_kindle():
    print("Waiting for Kindle device to be connected...")
    print("Please connect your Kindle via USB and enable MTP mode")

    while True:
        if detect_kindle_device():
            print("Kindle found and ready!")
            return True

        print("Kindle not detected. Please:")
        print("1. Connect Kindle via USB")
        print("2. Enable MTP mode on Kindle")
        print("3. Wait for device to be recognized")

        time.sleep(5)

def send_file_to_kindle(local_path):
    try:
        filename = os.path.basename(local_path)
        print(f"Sending {filename} to Kindle...")

        process = subprocess.Popen([
            'mtp-sendfile',
            local_path,
            filename
        ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, universal_newlines=True)

        for line in process.stdout:
            line = line.rstrip()
            if line.startswith('Progress:'):
                print(f"\r{line}", end='', flush=True)
            else:
                print(f"\n{line}")

        print()
        process.wait()

        if process.returncode == 0:
            print(f"Successfully sent {filename} to Kindle")
            return True
        else:
            print(f"Error sending file {filename} to Kindle (return code: {process.returncode})")
            return False
    except Exception as e:
        print(f"Error sending file to Kindle: {e}")
        return False

def list_kindle_files():
    try:
        result = subprocess.run(['mtp-files'],
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("Files on Kindle:")
            print(result.stdout)
        else:
            print("Could not list Kindle files")
    except Exception as e:
        print(f"Error listing Kindle files: {e}")

def parse_size(size_str):
    size_str = size_str.lower().strip()

    if size_str.endswith('gb'):
        return int(float(size_str[:-2]) * 1024**3)
    elif size_str.endswith('mb'):
        return int(float(size_str[:-2]) * 1024**2)
    elif size_str.endswith('kb'):
        return int(float(size_str[:-2]) * 1024)
    else:
        return int(float(size_str))

def cleanup_file(filepath):
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"Cleaned up {os.path.basename(filepath)}")
        else:
            print(f"Warning: {os.path.basename(filepath)} not found for cleanup")
    except Exception as e:
        print(f"Error cleaning up {os.path.basename(filepath)}: {e}")

def main():
    parser = argparse.ArgumentParser(description='Create and send filler files to Kindle')
    parser.add_argument('sizes', nargs='+', help='File sizes to create (e.g., 4.78gb 1.5gb 100mb)')
    parser.add_argument('--prefix', default='filler', help='Prefix for file names (default: filler)')
    parser.add_argument('--no-send', action='store_true', help='Create files but don\'t send to Kindle')

    args = parser.parse_args()

    if not args.no_send:
        if not wait_for_kindle():
            print("Failed to detect Kindle. Exiting.")
            return

    ensure_dir(BASE)

    for i, size_str in enumerate(args.sizes):
        filepath = None
        try:
            size_bytes = parse_size(size_str)
            filename = f"{args.prefix}_{size_str}_{i+1}"
            filepath = os.path.join(BASE, filename)

            print(f"Creating {filename} ({size_str})...")
            create_dummy_file(filepath, size_bytes)

            if not args.no_send:
                if send_file_to_kindle(filepath):
                    print(f"Successfully transferred {filename} to Kindle")
                else:
                    print(f"Failed to transfer {filename} to Kindle")
            else:
                print(f"Created {filename} locally")

        except ValueError as e:
            print(f"Error parsing size '{size_str}': {e}")
            continue
        finally:
            # Always cleanup the file if it was created and we're not in no-send mode
            if filepath and not args.no_send:
                cleanup_file(filepath)

    if not args.no_send:
        print("\nVerifying files on Kindle...")
        list_kindle_files()
    else:
        print(f"\nFiles created in {BASE}")

if __name__ == '__main__':
    main()
