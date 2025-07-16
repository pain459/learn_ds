import pandas as pd
import numpy as np
from datetime import datetime
import sys
import os

def validate_csv_columns(df, required_columns, filename):
    actual_columns = df.columns.str.strip().tolist()
    missing = [col for col in required_columns if col not in actual_columns]
    if missing:
        raise Exception(f"Missing columns {missing} in {filename}. Found columns: {actual_columns}")

def main():
    if '--help' in sys.argv or '-h' in sys.argv:
        print("""
------------------------------------------------------------
Time Allocation Script

Usage:
    python time_allocation.py <start_date YYYYMMDD> <end_date YYYYMMDD>

Example:
    python time_allocation.py 20250701 20250731

This script requires 5 CSV files in the current folder:
    1. team.csv      - Columns: id, name
    2. budgets.csv   - Columns: task, budget
    3. logged.csv    - Columns: id, task, logged
    4. holidays.csv  - Columns: day, holiday
    5. leaves.csv    - Columns: id, leaves  (summarized)

It validates inputs, calculates allocations, and exports:
    time_allocations.csv

------------------------------------------------------------
        """)
        sys.exit(0)

    if len(sys.argv) != 3:
        print("ERROR: Missing arguments.")
        print("Run with --help for usage instructions.")
        sys.exit(1)
    # if len(sys.argv) != 3:
    #     print("Usage: python time_allocation.py <start_date YYYYMMDD> <end_date YYYYMMDD>")
    #     sys.exit(1)

    # from_date = int(sys.argv[1])
    # to_date = int(sys.argv[2])
    from_date_input = sys.argv[1]
    to_date_input = sys.argv[2]

    # ---------------------------
    # Load input files with validation
    # ---------------------------
    required_files = ['team.csv', 'budgets.csv', 'logged.csv', 'holidays.csv', 'leaves.csv']

    for file in required_files:
        if not os.path.exists(file):
            raise Exception(f"Required file {file} not found in current directory.")

    team_df = pd.read_csv('team.csv')
    budgets_df = pd.read_csv('budgets.csv')
    holidays_df = pd.read_csv('holidays.csv')
    leaves_df = pd.read_csv('leaves.csv')  # summarized: id,leaves
    logged_df = pd.read_csv('logged.csv')

    # Strip columns
    for df in [team_df, budgets_df, holidays_df, leaves_df, logged_df]:
        df.columns = df.columns.str.strip()

    # Validate structures
    validate_csv_columns(team_df, ['id', 'name'], 'team.csv')
    validate_csv_columns(budgets_df, ['task', 'budget'], 'budgets.csv')
    validate_csv_columns(holidays_df, ['day', 'holiday'], 'holidays.csv')
    validate_csv_columns(leaves_df, ['id', 'leaves'], 'leaves.csv')   # summarized version!
    validate_csv_columns(logged_df, ['id', 'task', 'logged'], 'logged.csv')

    # ---------------------------
    # Date range
    # ---------------------------
    # from_dt = datetime.strptime(str(from_date), "%Y%m%d")
    # to_dt = datetime.strptime(str(to_date), "%Y%m%d")
    # total_days = (to_dt - from_dt).days + 1
    try:
        from_dt = datetime.strptime(from_date_input, "%Y%m%d")
        to_dt = datetime.strptime(to_date_input, "%Y%m%d")
    except ValueError:
        print("ERROR: Dates must be in YYYYMMDD format and be valid calendar dates.")
        sys.exit(1)

    from_date = int(from_date_input)
    to_date = int(to_date_input)

    if from_dt > to_dt:
        print("ERROR: Start date must be before or equal to end date.")
        sys.exit(1)

    total_days = (to_dt - from_dt).days + 1

    # ---------------------------
    # Holidays
    # ---------------------------
    num_holidays = holidays_df[
        (holidays_df['day'] >= from_date) & (holidays_df['day'] <= to_date)
    ].shape[0]

    # ---------------------------
    # Build base report with summarized leaves
    # ---------------------------
    report_df = team_df.merge(leaves_df[['id', 'leaves']], on='id', how='left').fillna(0)
    report_df['leaves'] = report_df['leaves'].astype(int)
    report_df['holidays'] = num_holidays
    report_df['total_days'] = total_days
    report_df['work_days'] = report_df['total_days'] - report_df['holidays'] - report_df['leaves']

    # ---------------------------
    # Add original logged days
    # ---------------------------
    logged_days = logged_df.groupby('id')['logged'].sum().reset_index(name='logged_days')
    report_df = report_df.merge(logged_days, on='id', how='left').fillna(0)

    task_pivot = logged_df.pivot_table(index='id', columns='task', values='logged', aggfunc='sum').reset_index().fillna(0)
    report_df = report_df.merge(task_pivot, on='id', how='left')

    for task in ['task1', 'task2', 'task3', 'task4']:
        if task not in report_df.columns:
            report_df[task] = 0.0
    report_df[['task1', 'task2', 'task3', 'task4']] = report_df[['task1', 'task2', 'task3', 'task4']].fillna(0)

    report_df['total_original_logged'] = report_df[['task1', 'task2', 'task3', 'task4']].sum(axis=1)
    report_df['balance_days'] = report_df['work_days'] - report_df['logged_days']

    # ---------------------------
    # Budgets & task caps
    # ---------------------------
    team_size = report_df.shape[0]
    hours_per_day = 8

    total_team_work_days = report_df['work_days'].sum()
    total_team_work_hours = total_team_work_days * hours_per_day

    task_budgets_days = {}
    task_remaining_budget = {}

    for _, row in budgets_df.iterrows():
        task = row['task']
        budget = row['budget']
        task_budgets_days[task] = total_team_work_days * budget
        used = report_df[task].sum()
        task_remaining_budget[task] = max(0, task_budgets_days[task] - used)

    # ---------------------------
    # Pooled-proportional allocation
    # ---------------------------
    for task in ['task1', 'task2', 'task3', 'task4']:
        report_df[f'log_{task}'] = 0.0

    np.random.seed(42)

    for idx, row in report_df.iterrows():
        leftover = row['balance_days']
        if leftover <= 0:
            continue

        task_weights = np.array([task_remaining_budget[task] for task in ['task1', 'task2', 'task3', 'task4']])
        if task_weights.sum() == 0:
            continue

        normalized_weights = task_weights / task_weights.sum()

        for i, task in enumerate(['task1', 'task2', 'task3', 'task4']):
            portion = round(leftover * normalized_weights[i], 2)
            assignable = min(portion, task_remaining_budget[task])
            report_df.at[idx, f'log_{task}'] += assignable
            task_remaining_budget[task] -= assignable

        total_logged = report_df.loc[idx, ['log_task1', 'log_task2', 'log_task3', 'log_task4']].sum()
        report_df.at[idx, 'total_logged'] = total_logged
        report_df.at[idx, 'leftover_balance_days'] = row['balance_days'] - total_logged

    report_df = report_df.sort_values(by='id').reset_index(drop=True)

    final_cols = [
        'id', 'name', 'leaves', 'holidays', 'total_days', 'work_days',
        'logged_days', 'task1', 'task2', 'task3', 'task4', 'total_original_logged',
        'balance_days', 'log_task1', 'log_task2', 'log_task3', 'log_task4',
        'total_logged', 'leftover_balance_days'
    ]

    report_df = report_df[final_cols]

    # ---------------------------
    # Export result
    # ---------------------------
    output_file = 'time_allocations.csv'
    report_df.to_csv(output_file, index=False)
    print(f"\nAllocation exported to {output_file}")

if __name__ == '__main__':
    main()
