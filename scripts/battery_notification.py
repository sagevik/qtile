import os
from pathlib import Path
from libqtile.lazy import lazy


@lazy.function()
def notify_all_batteries(_qtile):
    base_path = Path("/sys/class/power_supply/")
    battery_dirs = [d for d in base_path.iterdir() if d.name.startswith("BAT") and d.is_dir()]

    messages = []
    total_now = 0
    total_full = 0

    for bat in battery_dirs:
        try:
            energy_now = int((bat / "energy_now").read_text().strip())
            energy_full = int((bat / "energy_full").read_text().strip())
            status = (bat / "status").read_text().strip()
        except (FileNotFoundError, ValueError):
            continue  # Skip battery if files are missing or unreadable

        percent = (energy_now / energy_full) * 100 if energy_full > 0 else 0
        total_now += energy_now
        total_full += energy_full

        messages.append(
            f"{bat.name}: {energy_now // 1000} / {energy_full // 1000} mWh ({percent:.0f}%), {status}"
        )

    if total_full > 0:
        total_percent = (total_now / total_full) * 100
        messages.insert(
            0, f"Total: {total_now // 1000} / {total_full // 1000} mWh ({total_percent:.0f}%)"
        )
    else:
        messages.insert(0, "No battery data available")

    full_message = "\n".join(messages)
    os.system(f'notify-send "Battery Info" "{full_message}"')
