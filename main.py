
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ----------------------------------------------------------------------
# Constants (arrays/lists used throughout the program)
# ----------------------------------------------------------------------
DEFAULT_FILE = "library_transactions.csv"

REQUIRED_COLUMNS = [
    "Transaction ID", "Date", "User ID", "Book Title",
    "Genre", "Borrowing Duration (Days)"
]

WEEKDAYS = [
    "Monday", "Tuesday", "Wednesday", "Thursday",
    "Friday", "Saturday", "Sunday"
]

LATE_LIMIT_DAYS = 14
FREQUENT_MIN_BORROWS = 8
CHART_FOLDER = "charts"

sns.set_theme(style="whitegrid")


class LibraryDashboard:

    def __init__(self):
        self.df = None

    # ==================================================================
    # 1. DATA INPUT AND VALIDATION
    # ==================================================================
    def load_data(self, file_path):

        if file_path == "":
            print("Error: No file name entered.")
            return False

        if not file_path.lower().endswith(".csv"):
            print("Error: Invalid file format. Please provide a .csv file.")
            return False

        if not os.path.exists(file_path):
            print("Error: File not found ->", file_path)
            return False

        try:
            df = pd.read_csv(file_path)

        except pd.errors.EmptyDataError:
            print("Error: The file is empty.")
            return False

        except Exception as error:
            print("Error: Could not read the file ->", error)
            return False

        if df.empty:
            print("Error: The file has no data rows.")
            return False

        # Column validation
        df.columns = df.columns.str.strip()

        missing_columns = []

        for column in REQUIRED_COLUMNS:
            if column not in df.columns:
                missing_columns.append(column)

        if len(missing_columns) > 0:
            print("Error: Missing required columns ->", missing_columns)
            return False

        # Data cleaning
        total_rows = len(df)

        df = df.drop_duplicates()
        duplicates_removed = total_rows - len(df)

        df = df.replace(r"^\s*$", np.nan, regex=True)

        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

        df["Borrowing Duration (Days)"] = pd.to_numeric(
            df["Borrowing Duration (Days)"], errors="coerce"
        )

        before = len(df)

        df = df.dropna(subset=REQUIRED_COLUMNS)

        invalid_removed = before - len(df)

        before = len(df)

        df = df[df["Borrowing Duration (Days)"] > 0]

        invalid_removed += before - len(df)

        if df.empty:
            print("Error: No valid rows left after cleaning.")
            return False

        # Text cleaning
        for column in ["Transaction ID", "User ID", "Book Title", "Genre"]:
            df[column] = df[column].astype(str).str.strip()

        df["Genre"] = df["Genre"].str.title()

        df["Borrowing Duration (Days)"] = (
            df["Borrowing Duration (Days)"].astype(int)
        )

        # Computed columns
        df["Month"] = df["Date"].dt.strftime("%Y-%m")

        df["Weekday"] = df["Date"].dt.day_name()

        df["Late Return"] = (
            df["Borrowing Duration (Days)"] > LATE_LIMIT_DAYS
        )

        borrow_counts = df["User ID"].value_counts()

        frequent_users = borrow_counts[
            borrow_counts >= FREQUENT_MIN_BORROWS
        ].index

        df["Frequent Borrower"] = df["User ID"].isin(frequent_users)

        self.df = df.reset_index(drop=True)

        print("\nData loaded successfully!")

        print("  Total rows in file        :", total_rows)
        print("  Duplicate rows removed    :", duplicates_removed)
        print("  Missing/invalid removed   :", invalid_removed)
        print("  Valid rows used           :", len(self.df))

        return True

    def _data_ready(self):
        """Helper: check that data has been loaded."""

        if self.df is None or self.df.empty:
            print("Warning: Please load the dataset first.")
            return False

        return True

    # ==================================================================
    # 2. LIBRARY MANAGEMENT SYSTEM
    # ==================================================================
    def calculate_statistics(self, data=None):

        if data is None:
            data = self.df

        if data is None or data.empty:
            print("Warning: No data available to analyse.")
            return {}

        durations = np.array(data["Borrowing Duration (Days)"])

        book_counts = data["Book Title"].value_counts()
        day_counts = data["Weekday"].value_counts()
        user_counts = data["User ID"].value_counts()

        stats = {
            "total_transactions": len(data),

            "most_borrowed_book": book_counts.idxmax(),
            "most_borrowed_count": int(book_counts.max()),

            "busiest_day": day_counts.idxmax(),
            "busiest_day_count": int(day_counts.max()),

            "most_active_user": user_counts.idxmax(),
            "most_active_user_count": int(user_counts.max()),

            "avg_duration": float(np.mean(durations)),
            "median_duration": float(np.median(durations)),
            "std_duration": float(np.std(durations)),

            "min_duration": int(np.min(durations)),
            "max_duration": int(np.max(durations)),

            "late_returns": int(data["Late Return"].sum()),

            "frequent_borrowers": int(
                data.loc[
                    data["Frequent Borrower"], "User ID"
                ].nunique()
            ),
        }

        return stats

    def filter_transactions(self, condition):

        if not self._data_ready():
            return pd.DataFrame()

        data = self.df.copy()

        if "genre" in condition:
            data = data[
                data["Genre"].str.lower() == condition["genre"].lower()
            ]

        if "start_date" in condition:
            data = data[data["Date"] >= condition["start_date"]]

        if "end_date" in condition:
            data = data[data["Date"] <= condition["end_date"]]

        if "min_days" in condition:
            data = data[
                data["Borrowing Duration (Days)"] >= condition["min_days"]
            ]

        if "max_days" in condition:
            data = data[
                data["Borrowing Duration (Days)"] <= condition["max_days"]
            ]

        return data

    def generate_report(self, data=None):

        stats = self.calculate_statistics(data)

        if not stats:
            return

        line = "=" * 58

        print("\n" + line)
        print("E-LIBRARY DATA INSIGHTS REPORT")
        print(line)

        print("Total transactions       :", stats["total_transactions"])

        print(
            "Most borrowed book       :",
            stats["most_borrowed_book"],
            "(" + str(stats["most_borrowed_count"]) + " times)"
        )

        print(
            "Busiest day              :",
            stats["busiest_day"],
            "(" + str(stats["busiest_day_count"]) + " borrowings)"
        )

        print(
            "Most active user         :",
            stats["most_active_user"],
            "(" + str(stats["most_active_user_count"]) + " borrowings)"
        )

        print("-" * 58)

        print("Borrowing duration (calculated with NumPy)")

        print("  Average                : %.2f days" % stats["avg_duration"])
        print("  Median                 : %.2f days" % stats["median_duration"])
        print("  Standard deviation     : %.2f" % stats["std_duration"])

        print(
            "  Minimum / Maximum      : %d / %d days"
            % (stats["min_duration"], stats["max_duration"])
        )

        print("-" * 58)

        print(
            "Late returns (>%d days)  : %d"
            % (LATE_LIMIT_DAYS, stats["late_returns"])
        )

        print("Frequent borrowers       :", stats["frequent_borrowers"])

        print(line)

    # ==================================================================
    # 3. DATA ANALYSIS AND COMPUTATIONS
    # ==================================================================
    def group_analysis(self, data=None):

        if data is None:
            data = self.df

        if data is None or data.empty:
            print("Warning: No data available to analyse.")
            return

        genre_summary = data.groupby("Genre").agg(
            Total_Borrowings=("Transaction ID", "count"),
            Avg_Duration=("Borrowing Duration (Days)", "mean")
        ).round(2).sort_values(
            "Total_Borrowings", ascending=False
        )

        print("\n--- Summary by Genre ---")
        print(genre_summary)

        print("\n--- Total Borrowings per Book (Top 5) ---")

        print(
            data.groupby("Book Title")
            .size()
            .sort_values(ascending=False)
            .head(5)
        )

        print("\n--- Average Borrowing Duration per User (Top 5 longest) ---")

        print(
            data.groupby("User ID")["Borrowing Duration (Days)"]
            .mean()
            .round(2)
            .sort_values(ascending=False)
            .head(5)
        )

    # ==================================================================
    # 4. DATA VISUALIZATION
    # ==================================================================
    def _save_and_show(self, file_name):

        plt.tight_layout()

        plt.savefig(file_name, dpi=120)

        plt.show()

    def plot_top_books(self, data):

        top5 = data["Book Title"].value_counts().head(5)

        plt.figure(figsize=(10, 6))

        sns.barplot(
            x=top5.values,
            y=top5.index,
            color="steelblue",
            label="Borrowings"
        )

        for i, value in enumerate(top5.values):
            plt.text(value + 0.2, i, str(value), va="center")

        plt.title(
            "Top 5 Most Borrowed Books",
            fontsize=14,
            fontweight="bold"
        )

        plt.xlabel("Number of Borrowings")
        plt.ylabel("Book Title")

        plt.legend()

        self._save_and_show("bar_top5_books.png")

    def plot_monthly_trend(self, data):

        monthly = data.groupby("Month").size()

        plt.figure(figsize=(10, 6))

        sns.lineplot(
            x=monthly.index,
            y=monthly.values,
            marker="o",
            color="teal",
            label="Borrowings"
        )

        plt.title(
            "Borrowing Trends Over Months",
            fontsize=14,
            fontweight="bold"
        )

        plt.xlabel("Month")
        plt.ylabel("Number of Borrowings")

        plt.xticks(rotation=45)

        plt.legend()

        self._save_and_show("line_monthly_trend.png")

    def plot_genre_distribution(self, data):

        genre_counts = data["Genre"].value_counts()

        plt.figure(figsize=(8, 8))

        plt.pie(
            genre_counts.values,
            labels=genre_counts.index,
            autopct="%1.1f%%",
            startangle=140,
            colors=sns.color_palette("pastel")
        )

        plt.title(
            "Distribution of Books Borrowed by Genre",
            fontsize=14,
            fontweight="bold"
        )

        plt.legend(
            genre_counts.index,
            title="Genre",
            loc="center left",
            bbox_to_anchor=(1, 0.5)
        )

        self._save_and_show("pie_genre_distribution.png")

    def plot_activity_heatmap(self, data):

        table = pd.crosstab(
            data["Weekday"],
            data["Month"]
        ).reindex(WEEKDAYS).fillna(0).astype(int)

        plt.figure(figsize=(12, 6))

        sns.heatmap(
            table,
            annot=True,
            fmt="d",
            cmap="YlGnBu",
            cbar_kws={"label": "Number of Borrowings"}
        )

        plt.title(
            "Borrowing Activity by Day and Month",
            fontsize=14,
            fontweight="bold"
        )

        plt.xlabel("Month")
        plt.ylabel("Day of the Week")

        self._save_and_show("heatmap_activity.png")

    def show_all_charts(self, data=None):

        if data is None:
            data = self.df

        if data is None or data.empty:
            print("Warning: No data available to visualise.")
            return

        print("Generating charts... (close each chart window to see the next one)")

        self.plot_top_books(data)
        self.plot_monthly_trend(data)
        self.plot_genre_distribution(data)
        self.plot_activity_heatmap(data)

        print("Charts saved in the '" + CHART_FOLDER + "' folder.")


# ----------------------------------------------------------------------
# USER INTERACTION HELPERS
# ----------------------------------------------------------------------
def read_date(message):

    text = input(message).strip()

    if text == "":
        return None

    try:
        return pd.to_datetime(text, format="%Y-%m-%d")

    except ValueError:
        print("Warning: Invalid date format, this filter will be skipped.")
        return None


def read_number(message):

    text = input(message).strip()

    if text == "":
        return None

    if text.isdigit():
        return int(text)

    print("Warning: Please enter a valid number, this filter will be skipped.")

    return None


def ask_filter_condition(dashboard):

    print("\nEnter filter values (press Enter to skip any filter)")

    print(
        "Available genres:",
        ", ".join(sorted(dashboard.df["Genre"].unique()))
    )

    condition = {}

    genre = input("Genre: ").strip()

    if genre != "":
        condition["genre"] = genre

    start_date = read_date("Start date (YYYY-MM-DD): ")

    if start_date is not None:
        condition["start_date"] = start_date

    end_date = read_date("End date (YYYY-MM-DD): ")

    if end_date is not None:
        condition["end_date"] = end_date

    min_days = read_number("Minimum borrowing days: ")

    if min_days is not None:
        condition["min_days"] = min_days

    max_days = read_number("Maximum borrowing days: ")

    if max_days is not None:
        condition["max_days"] = max_days

    return condition


def load_with_retry(dashboard, attempts=3):

    for attempt in range(attempts):

        file_path = input(
            "Enter CSV file name (press Enter for "
            + DEFAULT_FILE + "): "
        ).strip()

        if file_path == "":
            file_path = DEFAULT_FILE

        if dashboard.load_data(file_path):
            return True

        print("Attempt", attempt + 1, "of", attempts, "failed.\n")

    return False


# ----------------------------------------------------------------------
# MAIN PROGRAM
# ----------------------------------------------------------------------
def main():

    dashboard = LibraryDashboard()

    filtered_data = None

    print("==================================================")
    print(" E-LIBRARY DATA INSIGHTS DASHBOARD")
    print("==================================================")

    if not load_with_retry(dashboard):
        print("Could not load the dataset. Exiting program.")
        return

    while True:

        print("\n-------------------- MENU --------------------")

        print("1. Show summary report")
        print("2. Show group analysis (genre / book / user)")
        print("3. Filter transactions")
        print("4. Show report of filtered data")
        print("5. Show all visualizations")
        print("6. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":

            dashboard.generate_report()

        elif choice == "2":

            dashboard.group_analysis()

        elif choice == "3":

            condition = ask_filter_condition(dashboard)

            filtered_data = dashboard.filter_transactions(condition)

            print("\n" + str(len(filtered_data)), "records found.")

            if not filtered_data.empty:
                print(filtered_data.head(10).to_string(index=False))

        elif choice == "4":

            if filtered_data is None:
                print("Warning: Please filter the data first (option 3).")

            else:
                dashboard.generate_report(filtered_data)

        elif choice == "5":

            dashboard.show_all_charts()

        elif choice == "6":

            print(
                "Thank you for using the E-Library Dashboard. Goodbye!"
            )

            break

        else:

            print("Invalid choice. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()
