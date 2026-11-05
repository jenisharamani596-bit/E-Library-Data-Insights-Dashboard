# 📚 E-Library Data Insights Dashboard

**Developed By:** Jenisha Ramani

## 📌 Project Description

The E-Library Data Insights Dashboard is a Python-based data analysis project that analyzes library transaction records using NumPy, Pandas, Matplotlib, and Seaborn.

It provides useful insights about book borrowing patterns, popular books, active users, borrowing duration, late returns, and genre-wise analysis.

## ✨ Features

- CSV Data Loading
- Data Cleaning and Preprocessing
- Duplicate and Missing Value Removal
- Summary Report Generation
- Group Analysis by Genre, Book, and User
- Transaction Filtering
- Filtered Data Report
- Statistical Analysis using NumPy
- Data Visualization using Matplotlib and Seaborn

## 🛠️ Technologies Used

- Python
- NumPy
- Pandas
- Matplotlib
- Seaborn

## 📁 Project Structure

```text
final_practical/
│
├── main.py
├── library_transactions.csv
├── bar_top5_books.png
├── line_monthly_trend.png
├── pie_genre_distribution.png
├── heatmap_activity.png
└── README.md
```

## 🚀 How to Run

**1. Install required libraries**

```bash
pip install numpy pandas matplotlib seaborn
```

**2. Run the Python file**

```bash
python library_dashboard.py
```

**3. Enter the CSV file name**

```text
library_transactions.csv
```

**4. Select an option from the menu.**

---

# 📸 Complete Sample Output

```text
==================================================
 E-LIBRARY DATA INSIGHTS DASHBOARD
==================================================
Enter CSV file name (press Enter for library_transactions.csv): library_transactions.csv

Data loaded successfully!
  Total rows in file        : 302
  Duplicate rows removed    : 2
  Missing/invalid removed   : 3
  Valid rows used           : 297

-------------------- MENU --------------------
1. Show summary report
2. Show group analysis (genre / book / user)
3. Filter transactions
4. Show report of filtered data
5. Show all visualizations
6. Exit
Enter your choice: 1

==========================================================
E-LIBRARY DATA INSIGHTS REPORT
==========================================================
Total transactions       : 297
Most borrowed book       : The Great Gatsby (30 times)
Busiest day              : Wednesday (53 borrowings)
Most active user         : U030 (13 borrowings)
----------------------------------------------------------
Borrowing duration (calculated with NumPy)
  Average                : 11.57 days
  Median                 : 11.00 days
  Standard deviation     : 5.97
  Minimum / Maximum      : 1 / 28 days
----------------------------------------------------------
Late returns (>14 days)  : 95
Frequent borrowers       : 20
==========================================================

-------------------- MENU --------------------
1. Show summary report
2. Show group analysis (genre / book / user)
3. Filter transactions
4. Show report of filtered data
5. Show all visualizations
6. Exit
Enter your choice: 2

--- Summary by Genre ---
            Total_Borrowings  Avg_Duration
Genre                                     
Fiction                   70         11.73
Biography                 60         12.60
Self-Help                 48         10.38
History                   46         11.09
Science                   37         10.95
Technology                36         12.42

--- Total Borrowings per Book (Top 5) ---
Book Title
The Great Gatsby        30
Long Walk to Freedom    22
Think and Grow Rich     21
1984                    20
Wings of Fire           17
dtype: int64

--- Average Borrowing Duration per User (Top 5 longest) ---
User ID
U036    16.30
U037    15.83
U012    14.80
U038    14.67
U019    14.38
Name: Borrowing Duration (Days), dtype: float64

-------------------- MENU --------------------
1. Show summary report
2. Show group analysis (genre / book / user)
3. Filter transactions
4. Show report of filtered data
5. Show all visualizations
6. Exit
Enter your choice: 3

Enter filter values (press Enter to skip any filter)
Available genres: Biography, Fiction, History, Science, Self-Help, Technology
Genre: Biography
Start date (YYYY-MM-DD): 2024-03-01
End date (YYYY-MM-DD): 2024-09-30
Minimum borrowing days: 5
Maximum borrowing days: 

39 records found.
Transaction ID       Date User ID                             Book Title     Genre  Borrowing Duration (Days)   Month   Weekday  Late Return  Frequent Borrower
         T0214 2024-03-03    U039 The Story of My Experiments with Truth Biography                          9 2024-03    Sunday        False              False
         T0203 2024-03-06    U015                   Long Walk to Freedom Biography                         13 2024-03 Wednesday        False              False
         T0024 2024-03-10    U001                             Steve Jobs Biography                         12 2024-03    Sunday        False               True
         T0278 2024-03-25    U022                   Long Walk to Freedom Biography                         15 2024-03    Monday         True              False
         T0267 2024-03-30    U038                          Wings of Fire Biography                         19 2024-03  Saturday         True              False
         T0168 2024-04-09    U004 The Story of My Experiments with Truth Biography                         14 2024-04   Tuesday        False               True
         T0294 2024-04-16    U015                   Long Walk to Freedom Biography                         10 2024-04   Tuesday        False              False
         T0223 2024-04-17    U014                          Wings of Fire Biography                         15 2024-04 Wednesday         True               True
         T0106 2024-04-17    U040                          Wings of Fire Biography                         12 2024-04 Wednesday        False               True
         T0088 2024-04-20    U035                          Wings of Fire Biography                         13 2024-04  Saturday        False              False

-------------------- MENU --------------------
1. Show summary report
2. Show group analysis (genre / book / user)
3. Filter transactions
4. Show report of filtered data
5. Show all visualizations
6. Exit
Enter your choice: 4

==========================================================
E-LIBRARY DATA INSIGHTS REPORT
==========================================================
Total transactions       : 39
Most borrowed book       : Long Walk to Freedom (16 times)
Busiest day              : Wednesday (10 borrowings)
Most active user         : U038 (3 borrowings)
----------------------------------------------------------
Borrowing duration (calculated with NumPy)
  Average                : 13.28 days
  Median                 : 13.00 days
  Standard deviation     : 3.90
  Minimum / Maximum      : 7 / 23 days
----------------------------------------------------------
Late returns (>14 days)  : 16
Frequent borrowers       : 13
==========================================================

-------------------- MENU --------------------
1. Show summary report
2. Show group analysis (genre / book / user)
3. Filter transactions
4. Show report of filtered data
5. Show all visualizations
6. Exit
Enter your choice: 5
Generating charts... (close each chart window to see the next one)
Charts saved in the 'charts' folder.

-------------------- MENU --------------------
1. Show summary report
2. Show group analysis (genre / book / user)
3. Filter transactions
4. Show report of filtered data
5. Show all visualizations
6. Exit
Enter your choice: 6
Thank you for using the E-Library Dashboard. Goodbye!
PS D:\python\final_practical>
```

---

## 📊 Visualizations

The project generates four charts:

1. **Bar Chart:** Top 5 Most Borrowed Books
2. **Line Chart:** Borrowing Trends Over Months
3. **Pie Chart:** Distribution of Books Borrowed by Genre
4. **Heatmap:** Borrowing Activity by Day and Month

