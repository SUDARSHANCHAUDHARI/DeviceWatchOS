"""USB collector."""

from __future__ import annotations

from pathlib import Path


def collect_usb() -> list[dict]:
    """Return basic USB device metadata from sysfs when available."""
    root = Path("/sys/bus/usb/devices")
    devices: list[dict] = []
    if not root.exists():
        return devices
    for device in sorted(root.iterdir()):
        vendor_file = device / "idVendor"
        product_file = device / "idProduct"
        if vendor_file.exists() and product_file.exists():
            devices.append(
                {
                    "device": device.name,
                    "vendor": vendor_file.read_text(encoding="utf-8", errors="replace").strip(),
                    "product": product_file.read_text(encoding="utf-8", errors="replace").strip(),
                }
            )
    return devices
