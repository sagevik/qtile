import subprocess
import re
from libqtile.lazy import lazy


def get_mic_status():
    """Get current mic mute status using pactl"""
    try:
        result = subprocess.run(
            ["pactl", "get-source-mute", "@DEFAULT_SOURCE@"],
            capture_output=True,
            text=True,
            check=True,
        )
        is_muted = "yes" in result.stdout.lower()
        return is_muted
    except subprocess.CalledProcessError:
        return True  # Assume muted if we can't check


def send_mic_notification(is_muted):
    """Send notification with mic status"""
    if is_muted:
        icon = "🎤❌"
        message = "Microphone: Muted"
        urgency = "normal"
    else:
        icon = "🎤"
        message = "Microphone: Live"
        urgency = "critical"  # Red notification when mic is live

    notification_body = f"{icon} {message}"

    try:
        subprocess.run(
            [
                "dunstify",
                "-a",
                "mic-control",
                "-r",
                "2000",
                "-u",
                urgency,
                "-t",
                "3000",
                "Microphone",
                notification_body,
            ],
            check=True,
        )
    except subprocess.CalledProcessError:
        subprocess.run(["notify-send", "-t", "3000", "Microphone", notification_body])


@lazy.function
def toggle_mute_audio_input(qtile):
    """Toggle microphone mute status"""
    try:
        subprocess.run(
            ["pactl", "set-source-mute", "@DEFAULT_SOURCE@", "toggle"],
            check=True,
            capture_output=True,
        )

        is_muted = get_mic_status()
        send_mic_notification(is_muted)

    except subprocess.CalledProcessError:
        subprocess.run(
            [
                "dunstify",
                "-a",
                "mic-control",
                "-u",
                "critical",
                "-t",
                "3000",
                "Microphone Error",
                "Could not toggle mic",
            ]
        )


def get_default_sink():
    """Get the default PulseAudio/PipeWire sink name"""
    try:
        result = subprocess.run(
            ["pactl", "get-default-sink"], capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None


def get_volume() -> [int, bool]:
    """Get current volume level and mute status using pactl"""
    sink = get_default_sink()
    if not sink:
        return 0, False

    try:
        result = subprocess.run(
            ["pactl", "get-sink-volume", sink],
            capture_output=True,
            text=True,
            check=True,
        )
        mute_result = subprocess.run(
            ["pactl", "get-sink-mute", sink], capture_output=True, text=True, check=True
        )

        # Parse volume (first percentage)
        volume_match = re.search(r"/\s*(\d+)%", result.stdout)
        volume = int(volume_match.group(1)) if volume_match else 0

        # Parse mute
        is_muted = "yes" in mute_result.stdout

        return volume, is_muted
    except subprocess.CalledProcessError:
        return 0, False


def send_notification(volume, is_muted) -> None:
    """Send notification with volume level"""
    if is_muted:
        icon = "🔇"
        message = f"Volume: Muted ({volume}%)"
        urgency = "normal"
    else:
        icon = "🔈" if volume == 0 else "🔉" if volume < 50 else "🔊"
        message = f"Volume: {volume}%"
        urgency = "low"

    bar_length = 20
    filled = int((volume / 100) * bar_length)
    bar = "█" * filled + "░" * (bar_length - filled)

    notification_body = f"{icon} {message}\n{bar}"

    try:
        subprocess.Popen(
            [
                "dunstify",
                "-a",
                "volume-control",
                "-r",
                "1000",
                "-u",
                urgency,
                "-t",
                "2000",
                "Volume Control",
                notification_body,
            ]
        )
    except Exception as e:
        print(f"Notification failed: {notification_body} ({e})")


@lazy.function()
def raise_volume(_qtile) -> None:
    """Raise volume by 5% using pactl, up to a max of 130%"""
    sink = get_default_sink()
    if sink:
        try:
            volume, is_muted = get_volume()
            if volume >= 130:
                send_notification(volume, is_muted)
                return

            subprocess.Popen(["pactl", "set-sink-volume", sink, "+5%"])
            # Wait briefly for volume to update before reading again
            subprocess.Popen(["sleep", "0.1"])
            volume, is_muted = get_volume()
            send_notification(volume, is_muted)
        except Exception as e:
            print(f"Error raising volume: {e}")


@lazy.function()
def lower_volume(_qtile) -> None:
    """Lower volume by 5% using pactl"""
    sink = get_default_sink()
    if sink:
        try:
            subprocess.Popen(["pactl", "set-sink-volume", sink, "-5%"])
            # Wait briefly for volume to update before reading again
            subprocess.Popen(["sleep", "0.1"])
            volume, is_muted = get_volume()
            send_notification(volume, is_muted)
        except Exception as e:
            print(f"Error raising volume: {e}")
        except Exception as e:
            print(f"Error lowering volume: {e}")


@lazy.function()
def toggle_mute_audio_output(_qtile) -> None:
    """Toggle mute using pactl"""
    sink = get_default_sink()
    if sink:
        try:
            subprocess.Popen(["pactl", "set-sink-mute", sink, "toggle"])
            volume, is_muted = get_volume()
            send_notification(volume, is_muted)
        except Exception as e:
            print(f"Error toggling mute: {e}")
