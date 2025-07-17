import pandas as pd
import numpy as np
from datetime import datetime
import sys
import os
import traceback

REQUIRED_FILES = {
    'team': ['id', 'name'],
    'budgets': ['task', 'budget'],
    'logged': ['id', 'task', 'logged'],
    'holidays': ['day', 'holiday'],
    'leaves': ['id', 'leaves']
}
HOURS_PER_DAY = 8

class ValidationError(Exception):
    pass

def validate_columns(df, required, filename):
    actual = df.columns.str.strip().tolist()
    missing = [col for col in required if col not in actual]
    if missing:
        raise ValidationError(f"Missing columns {missing} in {filename}. Found columns: {actual}")

def load_csv(filename, required_columns):
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File not found: {filename}")
    df = pd.read_csv(filename)
    df.columns = df.columns.str.strip()
    validate_columns(df, required_columns, filename)
    return df

def parse_dates(start_str, end_str):
    try:
        start = datetime.strptime(start_str, "%Y%m%d")
        end = datetime.strptime(end_str, "%Y%m%d")
    except ValueError:
        raise ValidationError("Dates must be in YYYYMMDD format.")
    if start > end:
        raise ValidationError("Start date must be before or equal to end date.")
    if start.month != end.month or start.year != end.year:
        raise ValidationError("Start and end dates must be within the same calendar month.")
    return start, end, (end - start).days + 1

def calculate_workdays(team_df, leaves_df, num_holidays, total_days):
    df = team_df.merge(leaves_df, on='id', how='left').fillna(0)
    df['leaves'] = df['leaves'].astype(int)
    df['holidays'] = num_holidays
    df['total_days'] = total_days
    df['work_days'] = df['total_days'] - df['holidays'] - df['leaves']
    return df

def summarize_logged(logged_df, task_list):
    logged_summary = logged_df.groupby('id')['logged'].sum().reset_index(name='logged_days')
    pivot = logged_df.pivot_table(index='id', columns='task', values='logged', aggfunc='sum').fillna(0).reset_index()
    for task in task_list:
        if task not in pivot.columns:
            pivot[task] = 0
    return logged_summary, pivot

def calculate_budgets(budgets_df, report_df):
    task_list = budgets_df['task'].tolist()
    total_work_days = report_df['work_days'].sum()
    task_budgets = {}
    remaining = {}
    for _, row in budgets_df.iterrows():
        task = row['task']
        task_budgets[task] = total_work_days * row['budget']
        used = report_df.get(task, pd.Series([0]*len(report_df))).sum()
        remaining[task] = max(0, task_budgets[task] - used)
    return task_budgets, remaining

def distribute_balance_days(report_df, remaining_budgets, task_list):
    np.random.seed(42)
    for task in task_list:
        report_df[f'log_{task}'] = 0.0

    for idx, row in report_df.iterrows():
        leftover = row['balance_days']
        if leftover <= 0:
            continue
        weights = np.array([remaining_budgets[task] for task in task_list])
        if weights.sum() == 0:
            continue
        norm_weights = weights / weights.sum()
        for i, task in enumerate(task_list):
            portion = round(leftover * norm_weights[i], 2)
            assignable = min(portion, remaining_budgets[task])
            report_df.at[idx, f'log_{task}'] += assignable
            remaining_budgets[task] -= assignable

        logged_total = report_df.loc[idx, [f'log_{t}' for t in task_list]].sum()
        report_df.at[idx, 'total_logged'] = logged_total
        report_df.at[idx, 'leftover_balance_days'] = leftover - logged_total
    return report_df

def export_report(df, task_list, output_file='time_allocations.csv'):
    final_cols = (
        ['id', 'name', 'leaves', 'holidays', 'total_days', 'work_days', 'logged_days']
        + task_list + ['total_original_logged', 'balance_days']
        + [f'log_{t}' for t in task_list]
        + ['total_logged', 'leftover_balance_days']
    )
    df.to_csv(output_file, index=False)
    print(f"Allocation exported to {output_file}")

def show_help():
    print("""
------------------------------------------------------------
Time Allocation Script

Usage:
    python time_allocation.py <start_date YYYYMMDD> <end_date YYYYMMDD>

Example:
    python time_allocation.py 20250701 20250731

Constraints:
    - Start and end date must be in the same month and year.
    - Requires 5 CSVs: team.csv, budgets.csv, logged.csv, holidays.csv, leaves.csv

Output:
    time_allocations.csv

------------------------------------------------------------
""")
    sys.exit(0)

def main():
    try:
        if '--help' in sys.argv or '-h' in sys.argv:
            show_help()

        if len(sys.argv) != 3:
            raise ValidationError("Missing arguments. Use --help for usage instructions.")

        start_str, end_str = sys.argv[1:3]
        start_dt, end_dt, total_days = parse_dates(start_str, end_str)
        start_num, end_num = int(start_str), int(end_str)

        # Load and validate data
        dfs = {name: load_csv(f"{name}.csv", cols) for name, cols in REQUIRED_FILES.items()}
        for df in dfs.values():
            df.columns = df.columns.str.strip()

        holidays_df = dfs['holidays']
        holidays_in_range = holidays_df[
            (holidays_df['day'] >= start_num) & (holidays_df['day'] <= end_num)
        ].shape[0]

        task_list = dfs['budgets']['task'].tolist()
        report_df = calculate_workdays(dfs['team'], dfs['leaves'], holidays_in_range, total_days)

        # Logged data
        logged_summary, task_pivot = summarize_logged(dfs['logged'], task_list)
        report_df = report_df.merge(logged_summary, on='id', how='left').fillna(0)
        report_df = report_df.merge(task_pivot, on='id', how='left').fillna(0)

        report_df['total_original_logged'] = report_df[task_list].sum(axis=1)
        report_df['balance_days'] = report_df['work_days'] - report_df['logged_days']

        # Budgets
        _, remaining_budgets = calculate_budgets(dfs['budgets'], report_df)

        # Finalize
        report_df = distribute_balance_days(report_df, remaining_budgets, task_list)
        report_df = report_df.sort_values(by='id').reset_index(drop=True)
        export_report(report_df, task_list)

    except ValidationError as ve:
        print(ve)
        sys.exit(1)
    except FileNotFoundError as fe:
        print(fe)
        sys.exit(1)
    except Exception as e:
        print("An unexpected error occurred.")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
