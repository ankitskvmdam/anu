"""cli download bar utility."""

import click


def get_nearest_unit(size: int) -> (str, int):
    """Return the unit.
    
    Args:
        size: size in bytes.

    Return:
        The nearest unit and size.
    """
    B = 1
    KB = B << 10
    MB = KB << 10
    GB = MB << 10
    TB = GB << 10

    if size // TB > 0:
        return "TB", round(size / TB, 2)

    if size // GB > 0:
        return "GB", round(size / GB, 2)

    if size // MB > 0:
        return "MB", round(size / MB, 2)

    if size // KB > 0:
        return "KB", round(size / KB, 2)

    return "B", size


def print_progress(total: int, current_progress: int, speed: int) -> None:
    """Print progress bar.

    Args:
        total: total size of file in bytes.
        current_progress: downloaded size of the file.
        speed: downloaded bytes in one second
    """

    bar_size = 60
    progress = current_progress * bar_size // total
    completed = str(int(current_progress * 100 // total)) + "%"

    total_unit, total_size = get_nearest_unit(total)
    current_unit, current_size = get_nearest_unit(current_progress)
    speed_unit, speed_size = get_nearest_unit(speed)

    print(" " * 100, end="\r")
    print(
        f"[{chr(9608) * int(progress)} {completed}{'-' * int(bar_size-progress)}] {current_size}{current_unit}/{total_size}{total_unit} [{speed_size}{speed_unit}/s]",
        end="\r",
        flush=True,
    )
