# Wyoming macOS TTS

[Wyoming protocol](https://github.com/rhasspy/wyoming) server for Text-to-Speech on macOS, using the `say` built-in command to generate speech natively on Apple silicon for voice pipelines in Home Assistant.

## Features
- Single install command to run in the background and automatically on login
- Supports multiple languages and voices
- Supports streaming

For Speech-to-Text on macOS, check out [wyoming-macos-stt](https://github.com/openhoster/wyoming-macos-stt)

## Getting Started

### Requirements
- macOS 26
- [uv](https://github.com/astral-sh/uv)
- [ffmpeg](https://github.com/FFmpeg/FFmpeg)

> These can be installed using [Homebrew](https://brew.sh) - `brew install uv ffmpeg`

### Installing

1. Clone this repository and navigate into it:
    ```bash
    git clone https://github.com/openhoster/wyoming-macos-tts
    cd wyoming-macos-tts
    ```
2. Run the installer and follow the prompts:
    ```bash
    uv run script/install.py
    ```
    This will create a launcher file and optionally set it to run in the background and on login.
    
    By default the server will be available externally for devices on the local network. You can change this and other arguments by editing the launcher file `WyomingTTS`. 

    Streaming is disabled by default, to enable it add `--streaming` in the launcher file.
    
    > To see all the available arguments, run: `uv run -m wyoming_macos_tts --help`
3. Adding to Home Assistant:  
   Add a new Wyoming service with the Mac’s host/IP and port `10200`.

> Tip: Additional voices can be downloaded in the system settings under `Accessibility -> Live Speech -> Voice -> ℹ️`. 
>
> if new voices are not showing in Home Assistant, try reloading the Wyoming service in Home Assistant

### Uninstalling

Re-run the installer and, when prompted: `Run in the background and on login?` enter `n`

To completely remove all resources, delete the cloned repository folder.

### Development

- Install dev dependencies: 
    ```bash
    uv sync --extra dev
    ```
- Running in a terminal session:
    ```bash 
    uv run -m wyoming_macos_tts --help
    ```
- Running tests:
    ```bash 
    uv run -m pytest tests
    ```

---

If you find this usefull and want to support future projects:

<a href="https://www.buymeacoffee.com/openhoster" target="_blank">
  <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" height="50"/>
</a>
