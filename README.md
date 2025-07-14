# Kindle MTP Filler

A Python script to create and transfer filler files to your (latest) Kindle device via MTP.

## Features

- Create filler files of any size (GB, MB, KB)
- Automatic Kindle device detection
- Real-time transfer progress

## Installation (macOS)

### Prerequisites

1. **Homebrew**
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Python 3**
   ```bash
   brew install python3
   ```

3. **libmtp**:
   ```bash
   brew install libmtp
   ```

## Usage

### Basic Usage

You will need sudo permissions.

```bash
# Create and transfer a single 4.78GB file
./mtp-filler.py 4.78gb

# Create and transfer multiple files
./mtp-filler.py 4.78gb 1.5gb 100mb

# Create files with custom prefix
./mtp-filler.py 2gb 500mb --prefix myfiller
```

### Advanced Usage

```bash
# Create files locally without sending to Kindle
./mtp-filler.py 1gb 500mb --no-send

# Create multiple files with custom naming
./mtp-filler.py 2.5gb 1gb 750mb --prefix kindle_filler
```

### Size Format Examples

- `4.78gb` - 4.78 gigabytes
- `1.5gb` - 1.5 gigabytes
- `500mb` - 500 megabytes
- `100mb` - 100 megabytes
- `50kb` - 50 kilobytes
- `1000` - 1000 bytes

## Kindle Setup

1. **Connect your Kindle** to your Mac via USB cable
3. **Wait for device recognition** - your Mac should detect the Kindle as an MTP device

## Troubleshooting

### Kindle Not Detected

1. **Check USB connection** - try a different cable or USB port
2. **Check sudo** - Make sure you are using sudo or su
3. **Check libmtp installation**:
   ```bash
   which mtp-detect
   which mtp-sendfile
   which mtp-files
   ```
