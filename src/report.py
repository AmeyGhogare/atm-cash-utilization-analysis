from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    Image,
    KeepTogether
)


# ============================================================
# 1. PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_PATH = BASE_DIR / "data" / "processed" / "atm_cleaned.csv"

REPORT_DIR = BASE_DIR / "outputs" / "reports"
CHART_DIR = REPORT_DIR / "charts"

REPORT_DIR.mkdir(parents=True, exist_ok=True)
CHART_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# 2. LOAD DATA
# ============================================================

def load_data():

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found:\n{DATA_PATH}"
        )

    df = pd.read_csv(DATA_PATH)

    # Convert Date column
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(
            df["Date"],
            errors="coerce"
        )

    return df


# ============================================================
# 3. CALCULATE KPIs
# ============================================================

def calculate_kpis(df):

    total_records = len(df)

    total_atms = (
        df["ATM_ID"].nunique()
        if "ATM_ID" in df.columns
        else 0
    )

    total_withdrawals = (
        df["Total_Withdrawals"].sum()
        if "Total_Withdrawals" in df.columns
        else 0
    )

    total_deposits = (
        df["Total_Deposits"].sum()
        if "Total_Deposits" in df.columns
        else 0
    )

    average_withdrawal = (
        df["Total_Withdrawals"].mean()
        if "Total_Withdrawals" in df.columns
        else 0
    )

    average_demand = (
        df["Cash_Demand_Next_Day"].mean()
        if "Cash_Demand_Next_Day" in df.columns
        else 0
    )

    average_utilization = (
        df["Cash_Utilization_Rate"].mean()
        if "Cash_Utilization_Rate" in df.columns
        else 0
    )

    # Handle utilization stored either as 0-1 or 0-100
    if average_utilization <= 1:
        utilization_percentage = average_utilization * 100
    else:
        utilization_percentage = average_utilization

    if total_deposits != 0:
        withdrawal_deposit_ratio = (
            total_withdrawals / total_deposits
        )
    else:
        withdrawal_deposit_ratio = 0

    high_risk_count = 0

    if "Cash_Risk" in df.columns:
        high_risk_count = (
            df["Cash_Risk"]
            .astype(str)
            .str.lower()
            .eq("high risk")
            .sum()
        )

    high_risk_percentage = (
        high_risk_count / total_records * 100
        if total_records > 0
        else 0
    )

    return {
        "total_records": total_records,
        "total_atms": total_atms,
        "total_withdrawals": total_withdrawals,
        "total_deposits": total_deposits,
        "average_withdrawal": average_withdrawal,
        "average_demand": average_demand,
        "average_utilization": utilization_percentage,
        "withdrawal_deposit_ratio": withdrawal_deposit_ratio,
        "high_risk_count": high_risk_count,
        "high_risk_percentage": high_risk_percentage
    }


# ============================================================
# 4. FORMAT FUNCTIONS
# ============================================================

def format_number(value):

    if pd.isna(value):
        return "N/A"

    return f"{value:,.0f}"


def format_decimal(value):

    if pd.isna(value):
        return "N/A"

    return f"{value:,.2f}"


def format_percentage(value):

    if pd.isna(value):
        return "N/A"

    return f"{value:.2f}%"


# ============================================================
# 5. SAVE CHART
# ============================================================

def save_chart(fig, filename):

    path = CHART_DIR / filename

    fig.tight_layout()

    fig.savefig(
        path,
        dpi=200,
        bbox_inches="tight"
    )

    plt.close(fig)

    return path


# ============================================================
# 6. CREATE CHARTS
# ============================================================

def create_charts(df):

    sns.set_theme(style="whitegrid")

    charts = {}

    # --------------------------------------------------------
    # Chart 1: Monthly Withdrawals
    # --------------------------------------------------------

    if "Date" in df.columns:

        temp = df.dropna(subset=["Date"]).copy()

        temp["Month_Year"] = (
            temp["Date"]
            .dt.to_period("M")
            .astype(str)
        )

        monthly = (
            temp.groupby("Month_Year")["Total_Withdrawals"]
            .sum()
            .reset_index()
        )

        fig, ax = plt.subplots(figsize=(10, 5))

        ax.plot(
            monthly["Month_Year"],
            monthly["Total_Withdrawals"],
            marker="o"
        )

        ax.set_title(
            "Monthly ATM Withdrawal Trend",
            fontsize=14,
            fontweight="bold"
        )

        ax.set_xlabel("Month")
        ax.set_ylabel("Total Withdrawals")

        ax.tick_params(
            axis="x",
            rotation=45
        )

        charts["monthly"] = save_chart(
            fig,
            "monthly_withdrawals.png"
        )


    # --------------------------------------------------------
    # Chart 2: Withdrawals by Location
    # --------------------------------------------------------

    if "Location_Type" in df.columns:

        location = (
            df.groupby("Location_Type")["Total_Withdrawals"]
            .sum()
            .sort_values(ascending=False)
        )

        fig, ax = plt.subplots(figsize=(8, 5))

        location.plot(
            kind="bar",
            ax=ax
        )

        ax.set_title(
            "ATM Withdrawals by Location",
            fontsize=14,
            fontweight="bold"
        )

        ax.set_xlabel("Location Type")
        ax.set_ylabel("Total Withdrawals")

        ax.tick_params(
            axis="x",
            rotation=30
        )

        charts["location"] = save_chart(
            fig,
            "withdrawals_by_location.png"
        )


    # --------------------------------------------------------
    # Chart 3: Withdrawals by Time of Day
    # --------------------------------------------------------

    if "Time_of_Day" in df.columns:

        time_analysis = (
            df.groupby("Time_of_Day")["Total_Withdrawals"]
            .sum()
            .sort_values(ascending=False)
        )

        fig, ax = plt.subplots(figsize=(8, 5))

        time_analysis.plot(
            kind="bar",
            ax=ax
        )

        ax.set_title(
            "ATM Withdrawals by Time of Day",
            fontsize=14,
            fontweight="bold"
        )

        ax.set_xlabel("Time of Day")
        ax.set_ylabel("Total Withdrawals")

        ax.tick_params(
            axis="x",
            rotation=30
        )

        charts["time"] = save_chart(
            fig,
            "withdrawals_by_time.png"
        )


    # --------------------------------------------------------
    # Chart 4: Cash Risk Distribution
    # --------------------------------------------------------

    if "Cash_Risk" in df.columns:

        risk = df["Cash_Risk"].value_counts()

        fig, ax = plt.subplots(figsize=(7, 5))

        risk.plot(
            kind="bar",
            ax=ax
        )

        ax.set_title(
            "Cash Risk Distribution",
            fontsize=14,
            fontweight="bold"
        )

        ax.set_xlabel("Cash Risk")
        ax.set_ylabel("Number of Records")

        ax.tick_params(
            axis="x",
            rotation=0
        )

        charts["risk"] = save_chart(
            fig,
            "cash_risk_distribution.png"
        )


    # --------------------------------------------------------
    # Chart 5: Withdrawals vs Deposits
    # --------------------------------------------------------

    if (
        "Total_Withdrawals" in df.columns
        and "Total_Deposits" in df.columns
    ):

        fig, ax = plt.subplots(figsize=(8, 5))

        ax.scatter(
            df["Total_Deposits"],
            df["Total_Withdrawals"],
            alpha=0.4
        )

        ax.set_title(
            "Withdrawals vs Deposits",
            fontsize=14,
            fontweight="bold"
        )

        ax.set_xlabel("Total Deposits")
        ax.set_ylabel("Total Withdrawals")

        charts["withdrawal_deposit"] = save_chart(
            fig,
            "withdrawals_vs_deposits.png"
        )


    # --------------------------------------------------------
    # Chart 6: Utilization by Location
    # --------------------------------------------------------

    if (
        "Location_Type" in df.columns
        and "Cash_Utilization_Rate" in df.columns
    ):

        utilization = (
            df.groupby("Location_Type")
            ["Cash_Utilization_Rate"]
            .mean()
            .sort_values(ascending=False)
        )

        # Convert if required
        if utilization.max() <= 1:
            utilization = utilization * 100

        fig, ax = plt.subplots(figsize=(8, 5))

        utilization.plot(
            kind="bar",
            ax=ax
        )

        ax.set_title(
            "Average Cash Utilization by Location",
            fontsize=14,
            fontweight="bold"
        )

        ax.set_xlabel("Location Type")
        ax.set_ylabel("Average Utilization (%)")

        ax.tick_params(
            axis="x",
            rotation=30
        )

        charts["utilization"] = save_chart(
            fig,
            "utilization_by_location.png"
        )


    return charts


# ============================================================
# 7. FIND BUSINESS INSIGHTS
# ============================================================

def generate_insights(df, kpis):

    insights = []

    # --------------------------------------------------------
    # Location insights
    # --------------------------------------------------------

    if "Location_Type" in df.columns:

        location_withdrawals = (
            df.groupby("Location_Type")
            ["Total_Withdrawals"]
            .sum()
            .sort_values(ascending=False)
        )

        if len(location_withdrawals) > 0:

            top_location = location_withdrawals.index[0]

            top_value = location_withdrawals.iloc[0]

            insights.append(
                f"The {top_location} location category "
                f"records the highest aggregate withdrawals "
                f"with approximately {format_number(top_value)} "
                f"withdrawal transactions."
            )


    # --------------------------------------------------------
    # Demand insights
    # --------------------------------------------------------

    if "Location_Type" in df.columns:

        demand = (
            df.groupby("Location_Type")
            ["Cash_Demand_Next_Day"]
            .mean()
            .sort_values(ascending=False)
        )

        if len(demand) > 0:

            top_demand_location = demand.index[0]

            top_demand = demand.iloc[0]

            insights.append(
                f"The highest average next-day cash demand "
                f"is observed in the {top_demand_location} "
                f"location category, at approximately "
                f"{format_decimal(top_demand)}."
            )


    # --------------------------------------------------------
    # Utilization insights
    # --------------------------------------------------------

    if "Location_Type" in df.columns:

        utilization = (
            df.groupby("Location_Type")
            ["Cash_Utilization_Rate"]
            .mean()
        )

        if len(utilization) > 0:

            if utilization.max() <= 1:
                utilization = utilization * 100

            top_util_location = utilization.idxmax()

            top_util_value = utilization.max()

            insights.append(
                f"The highest average cash utilization "
                f"is observed in the {top_util_location} "
                f"location category at "
                f"{format_percentage(top_util_value)}."
            )


    # --------------------------------------------------------
    # Time-of-day insight
    # --------------------------------------------------------

    if "Time_of_Day" in df.columns:

        time_analysis = (
            df.groupby("Time_of_Day")
            ["Total_Withdrawals"]
            .sum()
            .sort_values(ascending=False)
        )

        if len(time_analysis) > 0:

            peak_time = time_analysis.index[0]

            insights.append(
                f"{peak_time} records the highest aggregate "
                f"withdrawal activity among the available "
                f"time-of-day categories."
            )


    # --------------------------------------------------------
    # Day-of-week insight
    # --------------------------------------------------------

    if "Day_of_Week" in df.columns:

        day_analysis = (
            df.groupby("Day_of_Week")
            ["Total_Withdrawals"]
            .sum()
            .sort_values(ascending=False)
        )

        if len(day_analysis) > 0:

            peak_day = day_analysis.index[0]

            insights.append(
                f"{peak_day} records the highest aggregate "
                f"withdrawal activity among the available "
                f"days of the week."
            )


    # --------------------------------------------------------
    # Risk insight
    # --------------------------------------------------------

    insights.append(
        f"The dataset contains {format_number(kpis['high_risk_count'])} "
        f"records classified as High Risk, representing "
        f"approximately {format_percentage(kpis['high_risk_percentage'])} "
        f"of all records."
    )


    # --------------------------------------------------------
    # Overall utilization
    # --------------------------------------------------------

    insights.append(
        f"Average cash utilization across the dataset is "
        f"{format_percentage(kpis['average_utilization'])}."
    )


    return insights


# ============================================================
# 8. REPORT STYLES
# ============================================================

def create_styles():

    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="ReportTitle",
            parent=styles["Title"],
            fontSize=24,
            leading=30,
            alignment=TA_CENTER,
            spaceAfter=20
        )
    )

    styles.add(
        ParagraphStyle(
            name="Subtitle",
            parent=styles["Normal"],
            fontSize=12,
            leading=18,
            alignment=TA_CENTER,
            spaceAfter=20
        )
    )

    styles.add(
        ParagraphStyle(
            name="SectionHeading",
            parent=styles["Heading2"],
            fontSize=16,
            leading=20,
            spaceBefore=12,
            spaceAfter=10
        )
    )

    styles.add(
        ParagraphStyle(
            name="BodyTextCustom",
            parent=styles["BodyText"],
            fontSize=10,
            leading=15,
            alignment=TA_LEFT,
            spaceAfter=8
        )
    )

    styles.add(
        ParagraphStyle(
            name="SmallText",
            parent=styles["BodyText"],
            fontSize=8,
            leading=11
        )
    )

    return styles


# ============================================================
# 9. PAGE NUMBER
# ============================================================

def add_page_number(canvas, document):

    canvas.saveState()

    canvas.setFont(
        "Helvetica",
        8
    )

    canvas.drawCentredString(
        A4[0] / 2,
        10 * mm,
        f"Page {document.page}"
    )

    canvas.restoreState()


# ============================================================
# 10. KPI TABLE
# ============================================================

def create_kpi_table(kpis):

    data = [
        [
            "Metric",
            "Value"
        ],
        [
            "Total Records",
            format_number(kpis["total_records"])
        ],
        [
            "Distinct ATMs",
            format_number(kpis["total_atms"])
        ],
        [
            "Total Withdrawals",
            format_number(kpis["total_withdrawals"])
        ],
        [
            "Total Deposits",
            format_number(kpis["total_deposits"])
        ],
        [
            "Average Withdrawal",
            format_decimal(kpis["average_withdrawal"])
        ],
        [
            "Average Next-Day Demand",
            format_decimal(kpis["average_demand"])
        ],
        [
            "Average Utilization",
            format_percentage(kpis["average_utilization"])
        ],
        [
            "Withdrawal / Deposit Ratio",
            format_decimal(kpis["withdrawal_deposit_ratio"])
        ],
        [
            "High-Risk Records",
            format_number(kpis["high_risk_count"])
        ]
    ]

    table = Table(
        data,
        colWidths=[
            85 * mm,
            70 * mm
        ]
    )

    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#1F4E78")
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold"
                ),
                (
                    "FONTNAME",
                    (0, 1),
                    (-1, -1),
                    "Helvetica"
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),
                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "ALIGN",
                    (1, 1),
                    (1, -1),
                    "RIGHT"
                )
            ]
        )
    )

    return table


# ============================================================
# 11. ADD CHART
# ============================================================

def add_chart(story, chart_path, width=170 * mm):

    if chart_path and Path(chart_path).exists():

        img = Image(
            str(chart_path),
            width=width,
            height=85 * mm
        )

        story.append(img)
        story.append(Spacer(1, 8))


# ============================================================
# 12. PROJECT REPORT
# ============================================================

def generate_project_report(
    df,
    kpis,
    charts,
    insights,
    styles
):

    output_path = REPORT_DIR / "ATM_Project_Report.pdf"

    document = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm
    )

    story = []

    # --------------------------------------------------------
    # Title
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "ATM Cash Utilization & Downtime Analysis",
            styles["ReportTitle"]
        )
    )

    story.append(
        Paragraph(
            "Data Analytics Project Report",
            styles["Subtitle"]
        )
    )

    story.append(
        Paragraph(
            "Python • Pandas • SQL • MySQL • Power BI",
            styles["Subtitle"]
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "<b>Project Objective</b>",
            styles["SectionHeading"]
        )
    )

    story.append(
        Paragraph(
            "This project analyzes ATM transaction activity, "
            "cash demand, utilization, location patterns, "
            "time-based behavior and potential cash availability "
            "risk using a structured analytical dataset.",
            styles["BodyTextCustom"]
        )
    )

    story.append(PageBreak())

    # --------------------------------------------------------
    # Dataset Overview
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "1. Dataset Overview",
            styles["SectionHeading"]
        )
    )

    date_min = df["Date"].min() if "Date" in df.columns else None
    date_max = df["Date"].max() if "Date" in df.columns else None

    date_text = "Not available"

    if pd.notna(date_min) and pd.notna(date_max):

        date_text = (
            f"{date_min.strftime('%Y-%m-%d')} "
            f"to "
            f"{date_max.strftime('%Y-%m-%d')}"
        )

    overview_data = [
        ["Attribute", "Value"],
        ["Records", format_number(kpis["total_records"])],
        ["Distinct ATMs", format_number(kpis["total_atms"])],
        ["Date Range", date_text],
        ["Total Withdrawals", format_number(kpis["total_withdrawals"])],
        ["Total Deposits", format_number(kpis["total_deposits"])]
    ]

    table = Table(
        overview_data,
        colWidths=[
            70 * mm,
            85 * mm
        ]
    )

    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#1F4E78")
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),
                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    7
                )
            ]
        )
    )

    story.append(table)

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            "2. Key Performance Indicators",
            styles["SectionHeading"]
        )
    )

    story.append(create_kpi_table(kpis))

    story.append(PageBreak())

    # --------------------------------------------------------
    # Monthly Trend
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "3. Monthly Withdrawal Trend",
            styles["SectionHeading"]
        )
    )

    story.append(
        Paragraph(
            "The monthly trend illustrates how aggregate ATM "
            "withdrawal activity changes over the analyzed period.",
            styles["BodyTextCustom"]
        )
    )

    add_chart(
        story,
        charts.get("monthly")
    )

    story.append(PageBreak())

    # --------------------------------------------------------
    # Location Analysis
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "4. Location Analysis",
            styles["SectionHeading"]
        )
    )

    story.append(
        Paragraph(
            "Withdrawal activity is compared across the available "
            "ATM location categories to identify differences in "
            "transaction volume.",
            styles["BodyTextCustom"]
        )
    )

    add_chart(
        story,
        charts.get("location")
    )

    add_chart(
        story,
        charts.get("utilization")
    )

    story.append(PageBreak())

    # --------------------------------------------------------
    # Time Analysis
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "5. Time-Based Analysis",
            styles["SectionHeading"]
        )
    )

    story.append(
        Paragraph(
            "Time-of-day and day-of-week patterns provide an "
            "understanding of when ATM withdrawal activity is "
            "relatively higher or lower.",
            styles["BodyTextCustom"]
        )
    )

    add_chart(
        story,
        charts.get("time")
    )

    story.append(PageBreak())

    # --------------------------------------------------------
    # Risk Analysis
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "6. Cash Availability Risk Analysis",
            styles["SectionHeading"]
        )
    )

    story.append(
        Paragraph(
            "The Cash_Risk indicator is used to identify records "
            "where the combination of previous-day cash level and "
            "next-day cash demand indicates potential cash "
            "availability pressure.",
            styles["BodyTextCustom"]
        )
    )

    add_chart(
        story,
        charts.get("risk")
    )

    story.append(
        Paragraph(
            "<b>Important limitation:</b> The dataset does not "
            "contain a direct ATM downtime or outage field. "
            "Therefore, Cash_Risk should be interpreted as a "
            "potential cash-availability risk indicator rather "
            "than confirmed ATM downtime.",
            styles["BodyTextCustom"]
        )
    )

    story.append(PageBreak())

    # --------------------------------------------------------
    # Business Insights
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "7. Business Insights",
            styles["SectionHeading"]
        )
    )

    for i, insight in enumerate(insights, start=1):

        story.append(
            Paragraph(
                f"<b>{i}.</b> {insight}",
                styles["BodyTextCustom"]
            )
        )

    story.append(PageBreak())

    # --------------------------------------------------------
    # Withdrawals vs Deposits
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "8. Withdrawal and Deposit Relationship",
            styles["SectionHeading"]
        )
    )

    story.append(
        Paragraph(
            "The following visualization compares withdrawal and "
            "deposit activity across the dataset.",
            styles["BodyTextCustom"]
        )
    )

    add_chart(
        story,
        charts.get("withdrawal_deposit")
    )

    story.append(PageBreak())

    # --------------------------------------------------------
    # Conclusion
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "9. Conclusion",
            styles["SectionHeading"]
        )
    )

    story.append(
        Paragraph(
            "The analysis provides a structured view of ATM cash "
            "utilization, transaction behavior, cash demand and "
            "potential cash availability risk. The results can "
            "support data-driven monitoring of ATM activity and "
            "cash planning.",
            styles["BodyTextCustom"]
        )
    )

    story.append(
        Paragraph(
            "The final Power BI dashboard can be used as the "
            "interactive visualization layer for presenting these "
            "findings to business users.",
            styles["BodyTextCustom"]
        )
    )

    document.build(
        story,
        onFirstPage=add_page_number,
        onLaterPages=add_page_number
    )

    return output_path


# ============================================================
# 13. BUSINESS INSIGHTS REPORT
# ============================================================

def generate_business_insights(
    kpis,
    insights,
    styles
):

    output_path = REPORT_DIR / "Business_Insights.pdf"

    document = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm
    )

    story = []

    story.append(
        Paragraph(
            "ATM Business Insights",
            styles["ReportTitle"]
        )
    )

    story.append(
        Paragraph(
            "Key findings from ATM cash utilization analysis",
            styles["Subtitle"]
        )
    )

    story.append(
        Paragraph(
            "Key Metrics",
            styles["SectionHeading"]
        )
    )

    story.append(
        create_kpi_table(kpis)
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "Key Findings",
            styles["SectionHeading"]
        )
    )

    for i, insight in enumerate(insights, start=1):

        story.append(
            Paragraph(
                f"<b>{i}.</b> {insight}",
                styles["BodyTextCustom"]
            )
        )

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            "<b>Analytical Limitation:</b> "
            "Actual ATM downtime cannot be directly measured "
            "because the dataset does not provide a downtime or "
            "outage field.",
            styles["BodyTextCustom"]
        )
    )

    document.build(
        story,
        onFirstPage=add_page_number,
        onLaterPages=add_page_number
    )

    return output_path


# ============================================================
# 14. EXECUTIVE SUMMARY
# ============================================================

def generate_executive_summary(
    kpis,
    insights,
    styles
):

    output_path = REPORT_DIR / "Executive_Summary.pdf"

    document = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm
    )

    story = []

    story.append(
        Paragraph(
            "Executive Summary",
            styles["ReportTitle"]
        )
    )

    story.append(
        Paragraph(
            "ATM Cash Utilization & Downtime Analysis",
            styles["Subtitle"]
        )
    )

    story.append(
        Paragraph(
            "Project Overview",
            styles["SectionHeading"]
        )
    )

    story.append(
        Paragraph(
            "This project evaluates ATM transaction volumes, "
            "cash demand, utilization patterns and potential "
            "cash availability risk using Python-based data "
            "analysis and SQL-based reporting.",
            styles["BodyTextCustom"]
        )
    )

    story.append(
        Paragraph(
            "Key Metrics",
            styles["SectionHeading"]
        )
    )

    summary_data = [
        ["Metric", "Value"],
        [
            "ATM Records",
            format_number(kpis["total_records"])
        ],
        [
            "Distinct ATMs",
            format_number(kpis["total_atms"])
        ],
        [
            "Total Withdrawals",
            format_number(kpis["total_withdrawals"])
        ],
        [
            "Total Deposits",
            format_number(kpis["total_deposits"])
        ],
        [
            "Average Utilization",
            format_percentage(kpis["average_utilization"])
        ],
        [
            "High-Risk Records",
            format_number(kpis["high_risk_count"])
        ]
    ]

    table = Table(
        summary_data,
        colWidths=[
            80 * mm,
            70 * mm
        ]
    )

    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#1F4E78")
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),
                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    7
                )
            ]
        )
    )

    story.append(table)

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "Major Findings",
            styles["SectionHeading"]
        )
    )

    # Keep executive summary concise
    for insight in insights[:5]:

        story.append(
            Paragraph(
                f"• {insight}",
                styles["BodyTextCustom"]
            )
        )

    story.append(Spacer(1, 10))

    story.append(
        Paragraph(
            "Conclusion",
            styles["SectionHeading"]
        )
    )

    story.append(
        Paragraph(
            "The analysis demonstrates how ATM transaction "
            "data can be transformed into actionable metrics "
            "for cash utilization monitoring, demand analysis "
            "and potential cash availability risk assessment.",
            styles["BodyTextCustom"]
        )
    )

    story.append(
        Paragraph(
            "<b>Note:</b> Cash_Risk represents an analytical "
            "risk indicator and should not be interpreted as "
            "confirmed ATM downtime.",
            styles["BodyTextCustom"]
        )
    )

    document.build(
        story,
        onFirstPage=add_page_number,
        onLaterPages=add_page_number
    )

    return output_path


# ============================================================
# 15. GENERATE ALL REPORTS
# ============================================================

def generate_all_reports():

    print("\n" + "=" * 60)
    print("ATM REPORT GENERATION")
    print("=" * 60)

    print("\nLoading dataset...")

    df = load_data()

    print(
        f"Dataset loaded successfully: "
        f"{len(df):,} records"
    )

    print("\nCalculating KPIs...")

    kpis = calculate_kpis(df)

    print("\nCreating charts...")

    charts = create_charts(df)

    print(
        f"{len(charts)} charts created successfully."
    )

    print("\nGenerating business insights...")

    insights = generate_insights(
        df,
        kpis
    )

    styles = create_styles()

    print("\nGenerating PDF reports...")

    project_report = generate_project_report(
        df,
        kpis,
        charts,
        insights,
        styles
    )

    business_report = generate_business_insights(
        kpis,
        insights,
        styles
    )

    executive_report = generate_executive_summary(
        kpis,
        insights,
        styles
    )

    print("\n" + "=" * 60)
    print("REPORT GENERATION COMPLETED")
    print("=" * 60)

    print(
        f"\nProject Report:\n{project_report}"
    )

    print(
        f"\nBusiness Insights:\n{business_report}"
    )

    print(
        f"\nExecutive Summary:\n{executive_report}"
    )

    print(
        f"\nCharts saved in:\n{CHART_DIR}"
    )


# ============================================================
# 16. MAIN
# ============================================================

if __name__ == "__main__":
    generate_all_reports()