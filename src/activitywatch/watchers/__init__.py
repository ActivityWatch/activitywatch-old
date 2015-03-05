import platform

if platform.system() == "Linux":
    from .linux import X11Watcher
elif platform.system() == "Darwin":
    from .osx import OSXWatcher

from .afk import AFKWatcher
