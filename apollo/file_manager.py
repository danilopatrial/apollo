# file_manager.py
# File manager

from __future__ import annotations

'''
# this border is controlled by the size of the terminal
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│ NAME              TYPE        SIZE        other...
└─────────────────────────────────────────────────────────────────────────────────────────────┘
│ 📁 myfolder       dir         20 MB       ...
└─────────────────────────────────────────────────────────────────────────────────────────────┘

name
size
type
ext
modified
created
permissions
owner
group
is_exe
extension
lines
mime
sha256
git_stat

'''

import os
import pathlib
import datetime
import stat
import mimetypes
import hashlib
import subprocess

try:
    import pwd
except ImportError:
    pwd = None
try:
    import grp
except ImportError:
    grp = None

from typing import Any, Iterator


width, height = os.get_terminal_size()


class Path():

    def __init__(self, file: pathlib.Path, shortsha: bool = True) -> None:

        self._file: pathlib.Path = file
        self._stat_info = file.stat()

        self.name: str = file.name
        self.size: int = self._stat_info.st_size
        self.type: str = 'directory' if file.is_dir() else 'symlink' if file.is_symlink() else 'file'
        self.modified: str = str(datetime.datetime.fromtimestamp(self._stat_info.st_mtime).strftime('%Y-%m-%d %H:%M'))
        self.created: str = str(datetime.datetime.fromtimestamp(self._stat_info.st_birthtime).strftime('%Y-%m-%d %H:%M'))
        self.permissions: str = stat.filemode(self._stat_info.st_mode)
        self.owner: str = self.get_owner()
        self.group: str = self.get_group()
        self.is_exe: str = 'exe' if os.access(file, os.X_OK) else 'non-exe'
        self.ext: str = file.suffix
        self.lines: int = self.count_lines() if file.is_file() and self.ext in ['.py', '.txt', '.md'] else None
        self.mime: str = mimetypes.guess_type(file)[0]
        self.sha256: str = self.get_sha256(shortsha)
        self.git_stats: str = self.get_git_stats()


    def get_owner(self) -> str:
        if pwd: return pwd.getpwuid(self.self._stat_info.st_uid).pw_name
        import getpass
        return getpass.getuser()

    def get_group(self) -> str:
        if grp: return grp.getgrgid(self.self._stat_info.st_gid).gr_name
        return 'N/A'

    def get_sha256(self, shortsha: bool) -> str | None:
        try:
            sha256 = hashlib.sha256()
            with self._file.open('rb') as file:
                for block in iter(lambda: file.read(4096), b''):
                    sha256.update(block)

            if shortsha:
                return sha256.hexdigest()[:8]

            return sha256.hexdigest()
        except Exception:
            return None

    def get_git_stats(self) -> str | None:
        try:
            result = subprocess.run(
                ['git', 'status', '--porcelain', str(self._file)],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
                cwd=self._file.parent
            )

            if result.stdout.strip() == '':
                return '✓ clean'

            return result.stdout.strip()

        except Exception:
            return None


    def count_lines(self) -> int | None:
        try:
            with self.file.open('r', encoding='utf-8', errors='ignore') as f:
                return sum(1 for _ in f)
        except:
            return None


    def iter_properties(self, *args: Any) -> Iterator[str]:
        if len(args) == 0:
            for var, val in vars(self).items():
                if var.startswith('_'): continue
                yield val
        else:
            for var, val in vars(self).items():
                if var.startswith('_'): continue
                if val in args: yield val


def ls(dir: str, n: int) -> None:
    standard_args: list = [
        'sha256', 'ext', 'name', 'size', 'git_stats', 'is_exe', 'created',
        'modified', 'owner', 'group', 'permissions', 'mime']

    dirpath: pathlib.Path = pathlib.Path(dir)
    files: list = [f for f in dirpath.iterdir()]
    files.sort(key=lambda f: f.is_dir(), reverse=True)

    for file in files:
        file: Path = Path(file)
        print([getattr(file, i) for i in standard_args])