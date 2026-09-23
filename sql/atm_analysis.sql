-- =====================================================
-- ATM CASH UTILIZATION & DOWNTIME ANALYSIS
-- Database Setup
-- =====================================================

CREATE DATABASE IF NOT EXISTS atm_analysis_db;

USE atm_analysis_db;

CREATE TABLE IF NOT EXISTS atm_data (
    ATM_ID VARCHAR(20),
    Date DATE,
    Day_of_Week VARCHAR(20),
    Time_of_Day VARCHAR(30),

    Total_Withdrawals INT,
    Total_Deposits INT,

    Location_Type VARCHAR(50),

    Holiday_Flag TINYINT,
    Special_Event_Flag TINYINT,

    Previous_Day_Cash_Level INT,

    Weather_Condition VARCHAR(50),

    Nearby_Competitor_ATMs INT,

    Cash_Demand_Next_Day INT,

    Year INT,
    Month INT,
    Month_Name VARCHAR(20),
    Quarter INT,

    Net_Cash_Flow INT,
    Cash_Utilization_Rate DECIMAL(10,2),

    Cash_Risk VARCHAR(20)
);

-- 1. Total number of records
SELECT COUNT(*) AS Total_Records
FROM atm_data;

-- 2. Total number of ATMs
SELECT COUNT(DISTINCT ATM_ID) AS Total_ATMs
FROM atm_data;

-- 3. Date range
SELECT
    MIN(Date) AS Start_Date,
    MAX(Date) AS End_Date
FROM atm_data;

-- 4. Total withdrawals
SELECT
    SUM(Total_Withdrawals) AS Total_Withdrawals
FROM atm_data;

-- 5. Total deposits
SELECT
    SUM(Total_Deposits) AS Total_Deposits
FROM atm_data;

-- 6. Withdrawals vs deposits
SELECT
    SUM(Total_Withdrawals) AS Total_Withdrawals,
    SUM(Total_Deposits) AS Total_Deposits
FROM atm_data;

-- 7. Average withdrawals, deposits and cash demand
SELECT
    ROUND(AVG(Total_Withdrawals), 2) AS Avg_Withdrawals,
    ROUND(AVG(Total_Deposits), 2) AS Avg_Deposits,
    ROUND(AVG(Previous_Day_Cash_Level), 2) AS Avg_Cash_Level,
    ROUND(AVG(Cash_Demand_Next_Day), 2) AS Avg_Next_Day_Demand
FROM atm_data;

-- 8. ATM performance by total withdrawals
SELECT
    ATM_ID,
    SUM(Total_Withdrawals) AS Total_Withdrawals,
    SUM(Total_Deposits) AS Total_Deposits,
    ROUND(AVG(Previous_Day_Cash_Level), 2) AS Avg_Cash_Level,
    ROUND(AVG(Cash_Demand_Next_Day), 2) AS Avg_Cash_Demand,
    ROUND(AVG(Cash_Utilization_Rate), 2) AS Avg_Utilization
FROM atm_data
GROUP BY ATM_ID
ORDER BY Total_Withdrawals DESC;

-- 9. Top 10 ATMs by withdrawals
SELECT
    ATM_ID,
    SUM(Total_Withdrawals) AS Total_Withdrawals
FROM atm_data
GROUP BY ATM_ID
ORDER BY Total_Withdrawals DESC
LIMIT 10;

-- 10. Bottom 10 ATMs by withdrawals
SELECT
    ATM_ID,
    SUM(Total_Withdrawals) AS Total_Withdrawals
FROM atm_data
GROUP BY ATM_ID
ORDER BY Total_Withdrawals ASC
LIMIT 10;

-- 11. Cash utilization by location
SELECT
    Location_Type,
    COUNT(DISTINCT ATM_ID) AS ATM_Count,
    SUM(Total_Withdrawals) AS Total_Withdrawals,
    SUM(Total_Deposits) AS Total_Deposits,
    ROUND(AVG(Cash_Demand_Next_Day), 2) AS Avg_Cash_Demand,
    ROUND(AVG(Cash_Utilization_Rate), 2) AS Avg_Utilization
FROM atm_data
GROUP BY Location_Type
ORDER BY Total_Withdrawals DESC;

