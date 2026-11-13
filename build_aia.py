#!/usr/bin/env python3
"""Pack src/ into dist/NewsDataReader.aia (an .aia is a zip archive)."""
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
APP = "NewsDataReader"
PKG = f"src/appinventor/ai_user/{APP}"

PROPERTIES = """main=appinventor.ai_user.{app}.Screen1
name={app}
assets=../assets
source=../src
build=../build
versioncode=1
versionname=1.0
useslocation=False
aname={app}
sizing=Responsive
showlistsasjson=True
tutorialurl=
subsetjson=
actionbar=False
theme=AppTheme.Light.DarkActionBar
color.primary=&HFF3F51B5
color.primary.dark=&HFF303F9F
color.accent=&HFFFF4081
defaultfilescope=App
""".format(app=APP)


def main() -> int:
    scm = SRC / "Screen1.scm"
    if not scm.exists():
        print("src/Screen1.scm not found", file=sys.stderr)
        return 1
    bky = SRC / "Screen1.bky"
    out_dir = ROOT / "dist"
    out_dir.mkdir(exist_ok=True)
    out = out_dir / f"{APP}.aia"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("youngandroidproject/project.properties", PROPERTIES)
        z.write(scm, f"{PKG}/Screen1.scm")
        if bky.exists():
            z.write(bky, f"{PKG}/Screen1.bky")
        else:
            print("note: no src/Screen1.bky, blocks must be added after import (see docs/blocks.md)")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
