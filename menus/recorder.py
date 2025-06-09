#!/usr/bin/env python3
import subprocess
import os
from typing import List
from datetime import datetime

# Icons for recording options
system_record_icon = "󰍹  󰕾"  # Screen + system audio
silent_record_icon = "󰍹  󰖁"  # Screen + silent
mic_record_icon = "󰍹  󰍬"  # Screen + microphone
camera_mic_record_icon = "󰄀  󰍬"  # Camera + microphone
audio_only_record_icon = "󰍬"  # Microphone only
stop_record_icon = "󰓛"  # Stop/square icon
status_icon = "󰑊"  # Info icon

config_dir = os.environ.get("XDG_CONFIG_HOME", "") + "/rofi"


def is_recording() -> bool:
    """Check if wf-recorder or ffmpeg is currently running"""
    wf_result = subprocess.run(["pgrep", "wf-recorder"], capture_output=True)
    ffmpeg_result = subprocess.run(["pgrep", "ffmpeg"], capture_output=True)
    return wf_result.returncode == 0 or ffmpeg_result.returncode == 0


def get_recording_status() -> str:
    """Get current recording status"""
    if is_recording():
        return "Recording in progress..."
    else:
        return "No active recording"


def main_menu() -> str:
    options: List[str] = []

    if is_recording():
        options = [stop_record_icon]
    else:
        options = [
            system_record_icon,
            silent_record_icon,
            mic_record_icon,
            camera_mic_record_icon,
            audio_only_record_icon,
        ]

    menu: str = "\n".join([f"{item}" for item in options])
    status = get_recording_status()

    result = subprocess.run(
        [
            "rofi",
            "-dmenu",
            "-p",
            "Screen Recorder",
            "-mesg",
            f"{status}",
            "-theme",
            f"{config_dir}/power.rasi",
        ],
        input=menu,
        capture_output=True,
        text=True,
    ).stdout.strip()

    return result.split("\n")[0]


def start_system_recording():
    """Start recording with system audio"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"{os.path.expanduser('~/Videos')}/recording_{timestamp}.mp4"

    subprocess.Popen(
        [
            "wf-recorder",
            "--audio=alsa_output.pci-0000_00_1f.3.analog-stereo.monitor",
            "-f",
            output_file,
        ]
    )


def start_silent_recording():
    """Start recording without audio"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"{os.path.expanduser('~/Videos')}/recording_{timestamp}.mp4"

    subprocess.Popen(["wf-recorder", "-f", output_file])


def start_microphone_recording():
    """Start recording with microphone audio"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"{os.path.expanduser('~/Videos')}/recording_{timestamp}.mp4"

    subprocess.Popen(
        [
            "wf-recorder",
            "--audio=alsa_input.pci-0000_00_1f.3.analog-stereo",
            "-f",
            output_file,
        ]
    )


def start_camera_microphone_recording():
    """Start recording camera with microphone audio"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"{os.path.expanduser('~/Videos')}/camera_recording_{timestamp}.mp4"

    # Using ffmpeg for camera recording with microphone (using same audio device as your aliases)
    subprocess.Popen(
        [
            "ffmpeg",
            "-f",
            "v4l2",
            "-i",
            "/dev/video0",
            "-f",
            "pulse",
            "-i",
            "alsa_input.pci-0000_00_1f.3.analog-stereo",
            "-af",
            "aresample=async=1:min_hard_comp=0.100000:first_pts=0",
            "-c:v",
            "libx264",
            "-c:a",
            "aac",
            output_file,
        ]
    )


def start_audio_only_recording():
    """Start recording audio only (microphone)"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"{os.path.expanduser('~/Videos')}/audio_recording_{timestamp}.mp3"

    # Using ffmpeg for audio-only recording (using same audio device as your aliases)
    subprocess.Popen(
        [
            "ffmpeg",
            "-f",
            "pulse",
            "-i",
            "alsa_input.pci-0000_00_1f.3.analog-stereo",
            "-c:a",
            "mp3",
            output_file,
        ]
    )


def stop_recording():
    """Stop any active recording"""
    subprocess.run(["pkill", "wf-recorder"])
    subprocess.run(["pkill", "ffmpeg"])


def confirm() -> bool:
    stop_icon = "󰓛"  # Stop block
    continue_icon = "󰐊"  # Play/continue button
    options = [stop_icon, continue_icon]
    menu: str = "\n".join([f"{item}" for item in options])
    result = subprocess.run(
        [
            "rofi",
            "-theme",
            f"{config_dir}/power.rasi",
            "-theme-str",
            "listview {columns: 2; lines: 1;}",
            "-dmenu",
            "-p",
            "Recording Active",
            "-mesg",
            "Stop or continue recording?",
        ],
        input=menu,
        capture_output=True,
        text=True,
    ).stdout.strip()
    return result == stop_icon


def screen_recorder():
    # If recording is active, go straight to confirmation
    if is_recording():
        if confirm():
            stop_recording()
        return

    # Otherwise show the main menu
    selected = main_menu()

    if selected == system_record_icon:
        start_system_recording()
    elif selected == silent_record_icon:
        start_silent_recording()
    elif selected == mic_record_icon:
        start_microphone_recording()
    elif selected == camera_mic_record_icon:
        start_camera_microphone_recording()
    elif selected == audio_only_record_icon:
        start_audio_only_recording()


if __name__ == "__main__":
    screen_recorder()
