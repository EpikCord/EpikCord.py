import os
import logging

logger = logging.getLogger(__name__)


def test_imports():
    """
    This test is meant to check that library imports are correct and do not
    lead to any errors such as circular imports.
    """
    for path, sub_dirs, files in os.walk("EpikCord"):
        if "__init__.py" not in files:
            continue

        module_name = path.replace("/", ".")

        try:
            module = __import__(module_name)
        except ImportError as e:
            logger.error(f"Error importing {module_name}: {e}")
            raise e

        assert len(dir(module)) > 0
