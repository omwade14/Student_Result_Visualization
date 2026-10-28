import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "student_results.csv")
CHART_DIR = os.path.join(BASE_DIR, "charts")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

os.makedirs(CHART_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

subjects = ["English", "Maths", "Science", "Python", "DBMS"]

def calculate_grade(percentage):
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 50:
        return "D"
    elif percentage >= 35:
        return "E"
    return "F"

def main():
    if not os.path.exists(DATA_FILE):
        raise FileNotFoundError(f"CSV file not found: {DATA_FILE}")

    df = pd.read_csv(DATA_FILE)
    missing_columns = [col for col in ["Roll_No", "Name"] + subjects if col not in df.columns]
    if missing_columns:
        raise ValueError("Missing CSV columns: " + ", ".join(missing_columns))

    df[subjects] = df[subjects].apply(pd.to_numeric, errors="coerce")
    if df[subjects].isna().any().any():
        raise ValueError("Marks must be numeric and cannot be blank.")

    df["Total"] = df[subjects].sum(axis=1)
    df["Percentage"] = df[subjects].mean(axis=1).round(2)
    df["Result"] = np.where((df[subjects] >= 35).all(axis=1), "Pass", "Fail")
    df["Grade"] = df["Percentage"].apply(calculate_grade)

    print("\n===== STUDENT RESULT VISUALIZATION SYSTEM =====")
    print(df.to_string(index=False))
    print("\n===== SUBJECT-WISE AVERAGE MARKS =====")
    subject_average = df[subjects].mean().round(2)
    print(subject_average.to_string())
    print("\n===== RESULT SUMMARY =====")
    print("Total Students:", len(df))
    print("Passed Students:", int((df["Result"] == "Pass").sum()))
    print("Failed Students:", int((df["Result"] == "Fail").sum()))
    print("Class Average:", round(df["Percentage"].mean(), 2), "%")
    print("Highest Percentage:", df["Percentage"].max(), "%")
    print("Lowest Percentage:", df["Percentage"].min(), "%")

    plt.figure(figsize=(10, 5))
    plt.bar(df["Name"], df["Percentage"])
    plt.title("Student-wise Percentage")
    plt.xlabel("Student Name")
    plt.ylabel("Percentage (%)")
    plt.ylim(0, 100)
    plt.tight_layout()
    plt.savefig(os.path.join(CHART_DIR, "student_performance.png"), dpi=150)
    plt.close()

    plt.figure(figsize=(8, 5))
    plt.bar(subjects, subject_average)
    plt.title("Subject-wise Average Marks")
    plt.xlabel("Subject")
    plt.ylabel("Average Marks")
    plt.ylim(0, 100)
    plt.tight_layout()
    plt.savefig(os.path.join(CHART_DIR, "subject_average.png"), dpi=150)
    plt.close()

    grade_counts = df["Grade"].value_counts().sort_index()
    plt.figure(figsize=(7, 7))
    plt.pie(grade_counts, labels=grade_counts.index, autopct="%1.1f%%", startangle=90)
    plt.title("Grade Distribution")
    plt.tight_layout()
    plt.savefig(os.path.join(CHART_DIR, "grade_distribution.png"), dpi=150)
    plt.close()

    output_file = os.path.join(OUTPUT_DIR, "student_result_analysis.csv")
    df.to_csv(output_file, index=False)
    print("\nAnalysis completed successfully!")
    print("Charts saved in:", CHART_DIR)
    print("Analyzed results saved in:", output_file)

if __name__ == "__main__":
    main()
