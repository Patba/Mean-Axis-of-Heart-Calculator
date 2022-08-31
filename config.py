from pathlib import Path
def get_project_root() -> Path:
    return Path(__file__).parent

def make_dpi_aware() -> None:
    import ctypes
    import platform
    if int(platform.release()) >= 8:
        ctypes.windll.shcore.SetProcessDpiAwareness(True)