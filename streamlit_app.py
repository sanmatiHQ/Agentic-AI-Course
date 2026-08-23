"""Streamlit Community Cloud entry point (delegates to Home.py)."""

from pathlib import Path
import runpy

runpy.run_path(str(Path(__file__).resolve().parent / "Home.py"), run_name="__main__")
