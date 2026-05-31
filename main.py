"""
Trade Reconciliation & Break Detection Tool
============================================
Author:  Vidisha 
Date:    27-04-3036
Purpose: Automated reconciliation of trade ledgers,
         break detection, SQL storage, and Excel reporting.
"""

import subprocess
import sys
import time

def run_step(script_name, description):
    print(f"\n{'='*50}")
    print(f"  {description}")
    print(f"{'='*50}")
    
    start = time.time()
    result = subprocess.run(
        [sys.executable, script_name],
        capture_output=False
    )
    elapsed = round(time.time() - start, 2)
    
    if result.returncode == 0:
        print(f"  Completed in {elapsed}s")
    else:
        print(f"  Failed — check errors above")
        sys.exit(1)

if __name__ == "__main__":
    print("\n" + "🔷 "*20)
    print("  TRADE RECONCILIATION & BREAK DETECTION TOOL")
    print("🔷 "*20)

    total_start = time.time()

    run_step("generate_data.py",  "STEP 1/4 — Generating trade data")
    run_step("reconcile.py",      "STEP 2/4 — Running reconciliation engine")
    run_step("database.py",       "STEP 3/4 — Loading SQL database")
    run_step("excel_report.py",   "STEP 4/4 — Generating Excel report")

    total_time = round(time.time() - total_start, 2)

    print(f"\n{'🎉 '*20}")
    print(f"  ALL STEPS COMPLETE IN {total_time} SECONDS")
    print(f"  Report saved to: output/reconciliation_report.xlsx")
    print(f"{'🎉 '*20}\n")