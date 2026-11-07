"""Splits a channel-packed texture into one greyscale PNG per channel, keeping its bit depth (8 or 16).

The channel names come from the file name: its last tokens, one per non-constant channel in R, G, B, A
order. T_big_rock_01_MT_R_AO.png (alpha solid) -> T_big_rock_01_MT.png, _R.png, _AO.png.

Needs numpy and opencv-python-headless: Pillow reads a 16-bit colour PNG as 8-bit and loses the low byte.

Usage: drop files on it, or Explorer -> Send To. `--selftest` checks the naming rule and the 16-bit path.
"""
import sys
import tempfile
from pathlib import Path

import cv2
import numpy as np

LETTERS = "RGBA"


def channel_names(stem, count):
    """Base name and one suffix per channel; falls back to R/G/B/A when the name has too few tokens."""
    tokens = stem.split("_")

    # At least one token has to stay behind as the base name.
    if len(tokens) > count:
        return "_".join(tokens[:-count]), tokens[-count:], True

    return stem, list(LETTERS[:count]), False


def read(path):
    # imread cannot open a non-ASCII path on Windows; decoding from bytes can.
    image = cv2.imdecode(np.fromfile(path, np.uint8), cv2.IMREAD_UNCHANGED)

    if image is None:
        raise ValueError(f"cannot read {path.name}")

    if image.ndim == 2:
        return [image]

    # OpenCV keeps colour as BGR(A); put it back in R, G, B, A order.
    order = [2, 1, 0, 3][: image.shape[2]] if image.shape[2] >= 3 else range(image.shape[2])
    return [np.ascontiguousarray(image[..., i]) for i in order]


def write(path, channel):
    ok, encoded = cv2.imencode(".png", channel)

    if not ok:
        raise ValueError(f"cannot write {path.name}")

    encoded.tofile(path)


def unpack(path):
    # A channel that is one flat value carries nothing (an unused alpha), so it gets no name and no file.
    channels = [c for c in read(path) if c.min() != c.max()]
    base, suffixes, parsed = channel_names(path.stem, len(channels))

    if not parsed:
        print(f"! {path.name}: name has too few tokens for {len(channels)} channels, using {suffixes}")

    for channel, suffix in zip(channels, suffixes):
        out = path.with_name(f"{base}_{suffix}.png")
        write(out, channel)
        print(f"  {out.name} ({channel.dtype.itemsize * 8}-bit)")


def demo():
    assert channel_names("T_big_rock_01_MT_R_AO", 3) == ("T_big_rock_01", ["MT", "R", "AO"], True)
    assert channel_names("T_big_rock_01_MT_R_AO", 4) == ("T_big_rock", ["01", "MT", "R", "AO"], True)
    assert channel_names("ORM", 3) == ("ORM", ["R", "G", "B"], False)

    # 16-bit RGBA with a solid alpha: three 16-bit files, values intact, channels in R, G, B order.
    with tempfile.TemporaryDirectory() as folder:
        ramp = np.arange(256 * 256, dtype=np.uint16).reshape(256, 256)
        rgba = np.dstack([ramp, ramp // 2, ramp // 3, np.full_like(ramp, 65535)])
        source = Path(folder) / "T_test_A_B_C.png"
        write(source, rgba[..., [2, 1, 0, 3]].copy())
        unpack(source)

        for suffix, expected in (("A", ramp), ("B", ramp // 2), ("C", ramp // 3)):
            assert np.array_equal(read(source.with_name(f"T_test_{suffix}.png"))[0], expected), suffix

    print("selftest ok")


def main():
    if sys.argv[1:] == ["--selftest"]:
        demo()
        return

    failed = False

    for arg in sys.argv[1:]:
        print(arg)

        try:
            unpack(Path(arg))
        except Exception as error:
            print(f"! {error}")
            failed = True

    # The console window closes on its own; keep it open only when there is something to read.
    if failed:
        input("Enter to close")


if __name__ == "__main__":
    main()
