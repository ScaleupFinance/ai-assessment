import csv
import os

from langchain_core.tools import tool
from typing_extensions import TypedDict


class Metric(TypedDict):
    date: str
    metric: str
    value: float
    category: str
    notes: str


@tool
async def financial_statements_tool(month: str) -> list[Metric]:
    """
    Retrieves financial statements data for a specific month.

    Args:
        month: The month to retrieve data for in ISO format (e.g., "2025-03", "2025-04", etc.)

    Returns:
        A list of Metric objects containing financial data for the specified month.

    Raises:
        ValueError: If the requested month is not in the available range (2025-03 to 2025-06)
    """
    # Validate month input
    valid_months = ["2025-03", "2025-04", "2025-05", "2025-06"]
    if month not in valid_months:
        raise ValueError(
            "Data not available for the requested month. Available months: 2025-03 to 2025-06"
        )

    # Map month to filename
    month_to_file = {
        "2025-03": "march-2025.csv",
        "2025-04": "april-2025.csv",
        "2025-05": "may-2025.csv",
        "2025-06": "june-2025.csv",
    }

    # Get the directory path relative to the project root
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(current_dir, "..", "..", "..")
    file_path = os.path.join(
        project_root, "sample_data", "financial_statements", month_to_file[month]
    )

    # Read CSV file and convert to Metric format
    metrics = []
    try:
        with open(file_path) as file:
            reader = csv.DictReader(file)
            for row in reader:
                metric = Metric(
                    date=row["Date"],
                    metric=row["Metric"],
                    value=float(row["Value"]),
                    category=row["Category"],
                    notes=row["Notes"],
                )
                metrics.append(metric)
    except FileNotFoundError as e:
        raise ValueError(f"Data file not found for {month}") from e

    return metrics
