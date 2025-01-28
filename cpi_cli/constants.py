import os
from pathlib import Path

CPI_CONFIG_PATH = Path.home() / ".cpi_config"
API_BASE_PATHS = {
    "dev": "https://your-dev-instance.cpi.sap",
    "test": "https://your-test-instance.cpi.sap",
    "prod": "https://your-prod-instance.cpi.sap"
}