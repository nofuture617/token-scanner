"""Build script for creating .exe file."""
import os
import sys
import subprocess
from pathlib import Path
from loguru import logger


def setup_build_environment():
    """Setup build environment."""
    logger.info("Setting up build environment...")
    
    # Create assets directory if not exists
    assets_dir = Path("assets")
    assets_dir.mkdir(exist_ok=True)
    
    # Create placeholder icon if not exists
    icon_path = assets_dir / "icon.ico"
    if not icon_path.exists():
        logger.warning("Icon not found. Creating placeholder...")
        # Create a simple placeholder (in real scenario, you'd have a real icon)
        icon_path.touch()
    
    logger.info("Build environment ready")


def build_exe():
    """Build executable using PyInstaller."""
    logger.info("Building executable...")
    
    try:
        # Install PyInstaller if not installed
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        logger.info("PyInstaller installed")
        
        # Build executable
        subprocess.check_call([
            sys.executable,
            "-m",
            "PyInstaller",
            "--onefile",
            "--windowed",
            "--name",
            "TokenScanner",
            "--icon",
            "assets/icon.ico",
            "--add-data",
            "assets:assets",
            "--add-data",
            ".env.example:.",
            "--hidden-import=PySide6",
            "--hidden-import=axiomtradeapi",
            "--hidden-import=sqlalchemy",
            "--hidden-import=pydantic",
            "--hidden-import=loguru",
            "--hidden-import=plyer",
            "--hidden-import=playwright",
            "--hidden-import=aiohttp",
            "gui_app.py",
        ])
        
        logger.info("✅ Executable built successfully!")
        logger.info("📁 Location: dist/TokenScanner.exe")
        
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Build failed: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        return False


def create_installer():
    """Create NSIS installer (optional)."""
    logger.info("Creating installer...")
    
    try:
        subprocess.check_call([
            sys.executable,
            "-m",
            "pip",
            "install",
            "pyinstaller-hooks-contrib",
        ])
        logger.info("Installer tools installed")
        return True
    except Exception as e:
        logger.warning(f"Could not create installer: {e}")
        return False


def main():
    """Main build function."""
    from utils import setup_logger
    setup_logger(debug=True)
    
    logger.info("🔨 Token Scanner Build System")
    logger.info("="*50)
    
    # Setup
    setup_build_environment()
    
    # Build
    if build_exe():
        logger.info("="*50)
        logger.info("\n✨ Build complete!")
        logger.info("📦 Your executable is ready at: dist/TokenScanner.exe")
        logger.info("\n📋 Next steps:")
        logger.info("  1. Copy .env.example to .env")
        logger.info("  2. Add your Axiom Trade tokens")
        logger.info("  3. Run TokenScanner.exe")
        logger.info("\n💡 Tip: You can distribute the .exe to other users!")
        return 0
    else:
        logger.error("Build failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
