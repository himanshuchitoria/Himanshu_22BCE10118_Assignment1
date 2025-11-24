import subprocess
import tempfile
import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SeleniumExecutor:
    """
    Runs generated Selenium Python scripts safely in a subprocess.
    Executes headless Chrome for automated, non-blocking test execution.
    Captures stdout, stderr, and returns execution status.
    """

    def __init__(self, python_executable: str = "python3"):
        self.python_executable = python_executable

    def run_script(self, script_code: str, timeout: int = 60) -> Dict[str, Any]:
        """
        Executes the given Selenium script code as a temporary Python file.
        Returns a dict with keys:
         - 'success': bool indicating test pass/fail (assumes exit code 0 is pass)
         - 'stdout': captured stdout string
         - 'stderr': captured stderr string
         - 'error': error message in case of failure to execute
        """

        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as tmp_file:
            tmp_file.write(script_code)
            tmp_script_path = tmp_file.name

        cmd = [self.python_executable, tmp_script_path]
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            success = (result.returncode == 0)
            return {
                "success": success,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "error": None,
            }
        except subprocess.TimeoutExpired as e:
            logger.error(f"Execution timed out: {e}")
            return {
                "success": False,
                "stdout": "",
                "stderr": "",
                "error": "Execution timed out",
            }
        except Exception as e:
            logger.error(f"Execution error: {e}")
            return {
                "success": False,
                "stdout": "",
                "stderr": "",
                "error": str(e),
            }
        finally:
            try:
                os.remove(tmp_script_path)
            except Exception as e:
                logger.warning(f"Failed to delete temp script file: {e}")
