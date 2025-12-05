try:
    import textual
    import unicodedataplus as unicodedata 
except ImportError:
    raise ImportError("failed to import required libraries make sure you have run `python -m pip install pyfont[viewer]`")

from .run import run

if __name__ == "__main__":
    run()
