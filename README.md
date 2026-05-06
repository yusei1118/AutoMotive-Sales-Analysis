# Automotive Sales Analysis Dashboard


## Overview

This project analyzes automotive sales performance across the USA and Canada from the 1980s to the 2010s using a cleaned vehicle sales dataset and an interactive Tableau dashboard.

The dashboard focuses on sales trends, pricing performance, order volume, profitability, vehicle characteristics, regional differences, and market value comparisons using MMR (Manheim Market Report) as the estimated market value.

The goal of this project is to understand how vehicle sales, prices, and profitability changed over time, and to identify which makes, colors, states, and vehicle characteristics performed better or worse compared to market expectations.

## Key Finding

One of the most impactful findings from this project was the relationship between economic conditions and used vehicle demand.

Although the automotive market declined sharply during the 2008–2009 financial crisis, used vehicle sales rebounded dramatically between 2010 and 2012.

Interestingly, while sales volume increased significantly after the recession, vehicles were sold closer to or below MMR more frequently. This suggests that the market shifted from a high-margin environment into a more competitive, high-volume market.

This finding highlights how economic uncertainty can significantly change consumer purchasing behavior, pushing buyers toward more affordable used vehicles rather than reducing demand entirely.

----------
## 👀 View the Interactive Tableau Dashboard

  ### 👉👉👉 [CLICK HERE TO EXPLORE THE DASHBOARD](https://public.tableau.com/app/profile/yusei.hosoya/viz/AutoMotiveSalesAnalysis/Summary#1) 👈👈👈
----------
# Tools Used

- Python
- Pandas
- SQL
- Tableau Public
- Excel
- CSV Data Cleaning
- Data Visualization
- Parameter-Driven Dashboard Design

---

# Dataset

The dataset contains vehicle transaction records including:

- Vehicle year
- Make
- Model
- Body type
- Transmission
- State / Country
- Condition
- Odometer
- Exterior color
- Interior color
- Seller
- MMR
- Selling price
- Sale date

MMR was used as a benchmark to compare actual selling price against estimated market value.

---

# Data Cleaning Process

The original dataset contained several major data quality issues that had to be fixed before analysis (The dataset contained approximately 560,000 rows).

## 1. Misaligned Columns

Some rows had values shifted into the wrong columns.  
For example, VIN values appeared inside the state column, causing multiple fields to become misaligned.

To detect this issue, I validated VIN length because VINs should normally contain exactly 17 characters.

Rows with invalid VIN length were isolated and shifted back into the correct positions using Python.

This was one of the most important cleaning steps because column shifts would completely distort location, make, and pricing analysis.

---

## 2. Text Standardization

Several categorical fields such as:

- Make
- Body type
- Seller
- Color

contained:

- Capitalization inconsistencies
- Misspellings
- Similar values that should be grouped together
- Blank values

Examples included categories such as:

- “Audi Truck”
- “Audi tk”

which should represent the same category.

Without cleaning, Tableau would treat them as separate values and split the analysis incorrectly.

---

## 3. Encoding / Corrupted Text Issues

The color column contained a large number of corrupted characters such as:

‚Äî

This corrupted value appeared 24,888 times, which was too significant to ignore.

These values were treated as invalid or unknown values and cleaned before performing color analysis.

---

## 4. Outlier Detection and Price Corrections

The dataset contained unrealistic selling prices, including:

- $1 selling prices
- Vehicles priced 10x higher than MMR
- Vehicles priced 10x lower than MMR

To handle this, I created a ratio:

Ratio After = Selling Price / MMR

I then applied automated correction logic using Python.

### Corrections Included

- Removing obviously invalid $1 sales
- Correcting values that appeared off by a factor of 10
- Flagging suspicious outliers
- Comparing corrected price vs original price

A total of 14,416 records were flagged as outliers.

Some of these records may represent real market drops, but many appeared to be unrealistic data errors. Because of this, flagged values were handled carefully to avoid misleading conclusions.

---

## 5. File Size Optimization

The cleaned CSV exceeded 100MB, which created issues when importing into SQL / BigQuery.

To solve this problem, I:

- Rounded ratio values to three decimal places
- Removed unnecessary columns such as:
  - VIN
  - trim
  - temporary correction columns
- Reduced unnecessary precision

This significantly reduced file size while keeping the important analytical information.

---

## 6. Country Mapping for Tableau

The dataset included both US states and Canadian provinces.

To correctly build Tableau maps, I created a country field using Python:

- US states → United States
- Canadian provinces such as ON, QC, AB, NS → Canada

This allowed Tableau to correctly recognize both countries inside a single dashboard.

---

# Tableau Dashboard Design

The dashboard was designed around dynamic parameter-driven analysis.

The dashboard includes:

- Summary Page
- Make Analysis
- Color Analysis
- State Analysis

Navigation buttons allow users to move between pages interactively.

Every page includes a year selector parameter so users can dynamically compare market behavior across different years.

---

# Parameters and Dynamic Features

## Selected Year Parameter

A parameter was created to dynamically update all charts and KPI cards.

Example:

```tableau
IF YEAR([Year]) = [Years Selection]
THEN [Sellingprice]
END

This allows every chart to respond dynamically to the selected year.

---

## Top N Parameter

A Top N parameter allows users to choose how many categories are displayed in ranking charts.

This makes the dashboard more interactive and customizable.

---

# Key Calculations

## Selected Year Sales

```tableau
SUM(
IF YEAR([Year]) = [Years Selection]
THEN [Sellingprice]
END
)
```

---

## Previous Year Sales

```tableau
SUM(
IF YEAR([Year]) = [Years Selection] - 1
THEN [Sellingprice]
END
)
```

---

## YoY Sales %

```tableau
(
SUM(IF YEAR([Year]) = [Years Selection] THEN [Sellingprice] END)
-
SUM(IF YEAR([Year]) = [Years Selection] - 1 THEN [Sellingprice] END)
)
/
SUM(IF YEAR([Year]) = [Years Selection] - 1 THEN [Sellingprice] END)
```

---

## YoY Orders %

```tableau
(
COUNT(IF YEAR([Year]) = [Years Selection] THEN [Sellingprice] END)
-
COUNT(IF YEAR([Year]) = [Years Selection] - 1 THEN [Sellingprice] END)
)
/
COUNT(IF YEAR([Year]) = [Years Selection] - 1 THEN [Sellingprice] END)
```

---

## Average Selling Price

```tableau
SUM([Sellingprice]) / COUNT([Sellingprice])
```

---

## Sales vs MMR

```tableau
SUM([Sellingprice]) - SUM([MMR])
```

This calculation shows whether vehicles sold above or below estimated market value.

# Dashboard Structure

## Summary Page

The Summary page provides a high-level overview of the selected year.

It includes:

- Total sales
- Total orders
- Previous year sales
- Previous year orders
- YoY sales growth
- YoY order growth
- Sales trend line
- Top makes
- Top states
- Most profitable make/color combinations

This page is designed to quickly answer:

> How did the automotive market perform in the selected year compared to the previous year?

---

# Make Analysis

The Make page analyzes performance by vehicle brand.

## Key Questions

- Which makes generated the highest revenue?
- Which makes sold the most vehicles?
- Which makes performed above or below MMR?
- How does odometer affect selling price by make?
- Which brands rely on high volume versus high average price?

---

## Key Insights

Ford consistently appeared as one of the strongest brands in both sales and order volume.

Chevrolet was also highly competitive, especially in earlier years, but its dominance became less consistent after the late 2000s.

Luxury brands such as BMW and Mercedes-Benz often ranked highly not because of order volume, but because of higher average selling prices. This suggests that their revenue strength came more from unit value than from sales volume.

Japanese brands appeared stronger in earlier years, especially around the 1990s and early 2000s. However, after the market expanded, Ford and Chevrolet became more dominant in total revenue and volume.

The Sales vs MMR analysis showed that many brands performed better against market value before 2009.

After 2009, several luxury brands such as Porsche, Mercedes-Benz, Audi, and Rolls-Royce showed weaker performance relative to MMR, suggesting that the market became less favorable for selling above expected value.

The odometer vs selling price scatter plot showed that luxury vehicles tend to lose value sharply after mileage increases, especially after around 100,000 miles.

In contrast, several Japanese brands appeared to retain value more consistently even with higher mileage.

One particularly interesting insight was that the relationship between mileage and selling price became much stronger after 2010.

In earlier years, odometer did not always show a clear relationship with value, but after 2010, pricing became much more sensitive to mileage differences.

This suggests that buyers became increasingly focused on mileage when evaluating used vehicle value.

---

# Color Analysis

The Color page analyzes exterior and interior color performance.

## Key Questions

- Which exterior colors have the highest average selling price?
- Which interior colors sell for higher prices?
- Which colors perform above or below MMR?
- Did consumer color preferences change over time?

---

## Key Insights

Before around 2010, off-white vehicles frequently sold above MMR and performed strongly compared to other colors.

After 2010, there was no single exterior color that consistently dominated profitability, but yellow repeatedly appeared near the top in average selling price.

White, black, and off-white became more stable and valuable colors in later years.

These colors also maintained strong sales volume, suggesting that neutral colors became more desirable in the modern market.

In earlier decades, rarer colors such as:

- Pink
- Red
- Yellow
- Orange

sometimes had extremely high average selling prices.

This may suggest that rare colors were associated with specialty or premium vehicles during earlier periods.

Interior colors showed a more stable pattern.

White, off-white, and red-based interiors consistently appeared among higher-value categories across multiple years.

Overall, the analysis suggests that the market shifted from valuing rarity toward valuing widely preferred neutral colors.

---

# State Analysis

The State page analyzes regional performance across the USA and Canada.

## Key Questions

- Which states generated the highest sales?
- Which states had the highest order volume?
- Which states sold vehicles above or below MMR?
- How did regional profitability change over time?

---

## Key Insights

The dashboard shows that sales and order volume were generally stronger in coastal or highly populated regions.

California and Florida consistently appeared as the two strongest markets.

Pennsylvania and Texas also frequently ranked near the top.

California was especially interesting because it combined:

- High sales volume
- High order volume
- Positive Sales vs MMR performance

This suggests that California was not only selling many vehicles, but was also consistently selling above estimated market value.

Other high-volume states often remained much closer to MMR, meaning they had strong volume but weaker pricing advantage.

Before 2009, many states appeared capable of selling vehicles above MMR.

However, after the market decline around 2009, more states shifted toward negative Sales vs MMR values.

This suggests that after the market cooled down, it became harder to sell vehicles significantly above expected market value.

New York consistently appeared on the negative side of Sales vs MMR, suggesting weaker profitability relative to other major markets.

# Market Trend Analysis

The overall automotive market gradually increased from around 2000 to 2008.

However, around 2009, the market experienced a major decline, with sales dropping by approximately 30%.

After that, the market rebounded strongly between 2010 and 2012.

Sales increased rapidly, and order volume also grew significantly.

The 2015 data appears incomplete, likely because the dataset only contains part of the year, so 2015 should be interpreted carefully.

After 2012, the market became much more stable with fewer dramatic year-over-year fluctuations.

This suggests the market entered a more mature and stabilized phase following the strong post-crisis recovery.

---

# 2009–2010 Market Context and Interpretation

One of the most important patterns in this dashboard is the sharp market decline around 2009, followed by a strong recovery from 2010 to 2012.

This trend likely reflects the impact of the 2008–2009 global financial crisis, which heavily affected the automotive industry.

During this period:

- Consumer confidence dropped
- Credit became harder to access
- Buyers delayed expensive purchases such as vehicles
- Automotive demand weakened significantly

As a result, vehicle sales and transaction activity declined sharply around 2009.

This decline also affected pricing performance relative to MMR.

Before 2009, many makes, states, and categories were more likely to sell above estimated market value.

However, after the downturn, more categories began selling closer to or below MMR.

This suggests that the market became more price-sensitive after the crisis.

Buyers likely gained stronger negotiating power, while sellers may have needed to accept lower margins to maintain sales volume.

From 2010 onward, the dashboard shows a strong rebound in both sales and order volume.

However, even though total sales recovered, the ability to consistently sell above MMR did not fully recover in the same way.

This reveals an important insight:

> Higher sales volume does not always mean stronger pricing power.

After 2010, the market appears to have shifted toward a higher-volume but more competitive environment.

Dealers were able to move more vehicles, but generating significant profit above estimated market value became more difficult.

This pattern is especially visible in both the State and Make analysis pages.

Luxury brands that previously sold strongly above MMR before 2009 became weaker afterward, while many states also shifted toward lower relative profitability.

Overall, the 2009–2010 period represents a major turning point in the dataset.

The automotive market shifted from a strong pre-crisis growth phase into a more competitive recovery phase where volume increased, but pricing advantage became harder to maintain.

---
# Economic Interpretation and Used Car Market Behavior

One particularly interesting insight from this analysis is the relationship between economic conditions and used vehicle demand.

The dashboard suggests that after the 2008–2009 financial crisis, the automotive market changed significantly.

While the overall economy weakened during the recession, the used car market appears to have recovered very strongly afterward, especially between 2010 and 2012.

One possible explanation is that consumers became more price-sensitive during and after the economic downturn.

Instead of purchasing expensive new vehicles, many buyers may have shifted toward used vehicles as a more affordable alternative.

This would help explain why:

- Total sales volume increased sharply after 2010
- Order volume grew significantly
- High-volume brands such as Ford and Chevrolet became more dominant
- Pricing competition intensified
- Vehicles were sold closer to or below MMR more frequently

In other words, the market may have shifted from a high-margin environment into a higher-volume but more competitive market.

The analysis suggests that economic uncertainty does not necessarily reduce vehicle demand entirely. Instead, it may change consumer behavior toward more affordable vehicle options.

This interpretation is especially consistent with the strong growth observed in used vehicle sales following the recovery period after the financial crisis.

# Odometer vs Selling Price Analysis

The odometer analysis revealed a strong relationship between mileage and vehicle value.

In general:

- Lower mileage vehicles sold for higher prices
- Higher mileage vehicles sold for lower prices
- Luxury vehicles lost value sharply after mileage increased
- Several Japanese brands retained value more consistently

Luxury vehicles often showed dramatic value drops after approximately 100,000 miles.

Meanwhile, brands such as Ford and Chevrolet showed much more scattered relationships between mileage and price, likely because these brands contain many different vehicle categories and conditions.

One of the most interesting findings was that the relationship between mileage and value became much stronger after 2010.

Earlier years did not always show clear pricing patterns relative to mileage, but later years demonstrated much more consistent buyer sensitivity toward odometer readings.

This suggests that consumer perception of used vehicle value evolved significantly over time.

# Business Insights

This dashboard helps answer several important business questions:

- Which brands generate the strongest revenue?
- Which brands rely on volume versus premium pricing?
- Which colors retain stronger resale value?
- Which regions outperform estimated market value?
- How does mileage influence resale value?
- How did the automotive market behave before and after the financial crisis?

The analysis shows that profitability is not only about selling more vehicles.

Some brands and categories generate stronger value through higher average selling prices, while others rely primarily on transaction volume.

For example:

- California combines both high volume and strong profitability
- Luxury brands rely more on premium pricing
- Ford dominates through scale and volume
- Neutral colors became more valuable in later years
- Post-2010 markets became more competitive despite increased sales

---

# Limitations

There are several limitations to this analysis:

- Some outliers were removed or flagged due to unrealistic pricing
- 2015 data appears incomplete
- MMR was treated as estimated market value, but may not perfectly represent actual expected value
- Some categories contained missing or inconsistent values before cleaning
- Rare categories may appear inflated due to smaller sample sizes
- Order count is based on transaction records rather than unique order IDs

---

# What I Learned

Through this project, I learned that data cleaning is often more difficult and important than visualization itself.

The biggest challenge was not building charts, but ensuring the data was reliable enough to trust.

I had to solve issues involving:

- Misaligned rows
- Corrupted text encoding
- Missing values
- Geographic mapping
- Outlier detection
- Category standardization
- File size limitations
- SQL import limitations

I also learned how to build dynamic Tableau dashboards using:

- Parameters
- KPI cards
- YoY calculations
- Navigation buttons
- Dynamic filtering
- Scatter plots
- Geographic analysis

Most importantly, this project taught me that strong analysis requires constantly questioning whether the data itself is trustworthy before drawing conclusions.

---


# Final Conclusion

This project demonstrates how vehicle sales performance evolved across decades, brands, colors, mileage, and regions.

One of the most impactful findings from this analysis was the relationship between economic conditions and used vehicle demand.

The analysis found that the automotive market grew steadily before 2009, dropped sharply during the 2008–2009 financial crisis, and recovered strongly between 2010 and 2012.

However, the recovery did not fully restore previous pricing strength.

After 2010, sales volume increased significantly, but many vehicles sold closer to or below MMR. This suggests that while demand for used vehicles increased rapidly after the recession, the market also became more competitive and price-sensitive.

This may indicate a shift in consumer behavior, where buyers moved toward more affordable used vehicles during the post-crisis recovery period rather than reducing vehicle purchases entirely.

Ford remained one of the strongest brands by volume and revenue, while luxury brands maintained strength primarily through higher average selling prices.

California and Florida emerged as key regional markets, with California standing out for both strong sales volume and consistent performance above MMR.

Color analysis showed a shift from rare colors commanding premium prices in earlier years toward neutral colors such as white, black, and off-white becoming dominant in later years.

The dashboard also revealed that consumer sensitivity toward vehicle mileage became significantly stronger after 2010, especially for luxury vehicles.

Overall, this project demonstrates how macroeconomic conditions, mileage, geography, vehicle type, brand perception, and changing consumer behavior interact to influence automotive pricing and profitability.
---

# Author

Yusei Hosoya  
Data Analyst  
SQL | Python | Tableau | Excel | Data Visualization
