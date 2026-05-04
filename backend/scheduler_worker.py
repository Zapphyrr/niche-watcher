"""
Scheduler worker - Exécution unique
Appelé par Railway Cron toutes les 10 minutes
Exécute le scheduler une fois et s'arrête
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from scheduler import run_weekly_digest

if __name__ == "__main__":
    run_weekly_digest()
