__all__ = (
    
)

def __version__() -> str:
    return "0.4.12"

def info():
    print(f"Version {__version__()} of EpikCord.py, written by EpikHost. This is an unstable build and will contain bugs. Please report any bugs to https://github.com/EpikHost/EpikCord.py/issues.")

if __name__ == "__main__":
    info()