"""Regenerate every paper diagram into images/papers/."""
import glob, os, runpy, sys

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
for script in sorted(glob.glob(os.path.join(here, "d[0-9]*_*.py"))):
    runpy.run_path(script, run_name="__main__")
