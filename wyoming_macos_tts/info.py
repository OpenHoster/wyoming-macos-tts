import asyncio
import logging
import re

from wyoming.info import Attribution, Info, TtsProgram, TtsVoice

from . import __version__

_LOGGER = logging.getLogger("wyoming-macos-tts")


async def get_wyoming_info(args):
    command = "say -v '?'"
    proc = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode == 0:
        text = stdout.decode()
        pattern = re.compile(r"^(.*?)\s+([a-z]{2}_[A-Z]{2})", re.MULTILINE)
        results = []
        for match in pattern.finditer(text):
            voice_name, country_code = match.groups()
            results.append((voice_name, country_code))
    else:
        _LOGGER.error(stderr.decode())
        raise RuntimeError("Failed to get voices list. Return code {proc.returncode}")

    voices = [
        TtsVoice(
            name=voice_name,
            description="",
            attribution=Attribution(name="Apple", url="https://apple.com"),
            installed=True,
            version=None,
            languages=[country_code],
        )
        for (voice_name, country_code) in results
    ]

    return Info(
        tts=[
            TtsProgram(
                name=args.service_name,
                description="macos-tts",
                attribution=Attribution(name="Apple", url="https://apple.com"),
                installed=True,
                voices=sorted(voices, key=lambda v: v.name),
                version=__version__,
                supports_synthesize_streaming=args.streaming,
            )
        ],
    )
