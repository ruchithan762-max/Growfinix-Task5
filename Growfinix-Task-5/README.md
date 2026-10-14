# Growfinix Task 5: Healthcare Patient Admission Trends

## Project Overview
This project analyzes hospital admission records using Python to understand monthly admission patterns, calculate the average length of stay across hospital departments, and identify unusual hospital stays using statistical outlier detection.

## Objectives
- Analyze monthly hospital admission trends.
- Calculate the average and median length of stay by department.
- Identify outliers using the Interquartile Range (IQR) method.
- Clean and preprocess hospital admission data.
- Generate visualizations to communicate findings.

## Technologies Used
- Python
- Pandas
- Matplotlib
- Seaborn
- Visual Studio Code

## Dataset
The dataset contains admission IDs, admission dates, discharge dates, and hospital departments.

**Note:** If using the sample dataset created for practice, it contains illustrative records and is not real hospital data. Replace it with an appropriate public dataset before presenting findings as real-world results.

## Methodology
1. Load the CSV dataset using Pandas.
2. Convert admission and discharge dates into date formats.
3. Remove invalid records and duplicate admission IDs.
4. Calculate each patient's length of stay.
5. Group admissions by month.
6. Calculate department-wise average and median stays.
7. Detect length-of-stay outliers using the IQR method.
8. Generate charts and export analysis results.

## How to Run
Install the required libraries:

```bash
python -m pip install pandas matplotlib seaborn
```

Run the analysis:

```bash
python task5_analysis.py
```

## Expected Outputs
- Monthly admission summary
- Department-wise length-of-stay summary
- Outlier records
- Cleaned admission data
- Admission trend line chart
- Department average stay bar chart
- Length-of-stay box plot

## Learning Outcomes
This project demonstrates data cleaning, exploratory data analysis, date-based grouping, statistical outlier detection, data visualization, and exporting analytical results using Python.

## Acknowledgement
Completed as part of the Growfinix Data Analytics internship task series.
