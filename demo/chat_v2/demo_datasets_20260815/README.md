# DeepAnalyze Demo Datasets

This directory contains 4 public benchmark datasets: 2 single-file datasets and 2 multi-file datasets. The WebUI "Load Sample" dialog reads `catalog.json` to load the selected dataset and pre-fill curated analysis questions.

| Type | Dataset | Scale | Use Cases |
| --- | --- | ---: | --- |
| Single File | Palmer Penguins | 344 rows, 8 columns | Missing value checks, cohort comparison, scatter visualization |
| Single File | Global Life Expectancy | 21,565 rows, 4 columns | Time series trends, cross-country benchmarking, anomaly detection |
| Multi File | UCI Bike Sharing | Daily: 731 rows; Hourly: 17,379 rows | Cross-table reconciliation, temporal and hourly usage patterns |
| Multi File | FiveThirtyEight College Majors | 4 CSVs, ~76–174 rows each | Relational joins, employment & salary distributions |

## Suggested Exploration Flow

1. Quick Start: `single_file/palmer_penguins`
2. Time Series Analysis: `single_file/life_expectancy`
3. Cross-Table Consistency: `multi_file/bike_sharing`
4. Multi-Table Relational Analysis: `multi_file/college_majors`

## Sources & Provenance

- **Palmer Penguins**: <https://allisonhorst.github.io/palmerpenguins/>, CC0 license. Original data by Palmer Station LTER and Kristen Gorman.
- **Global Life Expectancy**: <https://ourworldindata.org/grapher/life-expectancy>, compiled by Our World in Data from Riley, Zijdeman, HMD, and UN WPP. See `source_metadata.json` for details.
- **UCI Bike Sharing**: <https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset>, CC BY 4.0, Reference: Fanaee-T, H. (2013), DOI 10.24432/C5W894.
- **FiveThirtyEight College Majors**: <https://github.com/fivethirtyeight/data/tree/master/college-majors>, 2010–2012 ACS PUMS data, CC BY 4.0.
