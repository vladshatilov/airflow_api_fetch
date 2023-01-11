import resource
from datetime import datetime, timedelta

DAGS_FOLDER = 'src'

MEM_LIMIT_SOFT = 10 * 1024 * 1024 * 1024
MEM_LIMIT_HARD = 12 * 1024 * 1024 * 1024
resource.setrlimit(resource.RLIMIT_AS, (MEM_LIMIT_SOFT, MEM_LIMIT_HARD))

TASK_TIMEOUT = timedelta(minutes=10)
DEFAULT_START_DATE = datetime(2023, 1, 1)

SYSTEM_PRIORITY_WEIGHT = 999

PROJECT_DEBUG = 'debug'
PROJECT_SYSTEM = 'system'
