# China under Deng: Money, Growth and Opening, 1978 to 1997

[Dataset on Hugging Face](https://huggingface.co/datasets/Kukai-7/deng-era-china) · code in this repository

**What changed in China's economy between the Third Plenum of 1978 and Deng Xiaoping's death in 1997?** This dataset gathers the money, growth, trade and living-standard series of the period, set against the two decades before and against India, Japan and the United States, with a map of the zones where the country first opened to foreign capital and a dated list of the main reforms.

*L'économie chinoise des années Deng : monnaie, croissance et ouverture.*

![Opening the coast, 1980 to 1990](https://huggingface.co/datasets/Kukai-7/deng-era-china/resolve/main/assets/map_reform_zones.png)

*Reading the map: red squares are the five Special Economic Zones with their opening year, blue dots the fourteen coastal cities opened in 1984, the black diamond Pudong (1990). Opening started in the south, next to Hong Kong, then moved up the coast.*

## At a glance

| | |
|---|---|
| Period | China 1960 to 2000 (annual); peers 1960 to 2025 |
| Series | 21 World Bank indicators: growth, inflation, money, exchange rate, trade, FDI, structure, poverty, life expectancy |
| Peers | China, India, Japan, United States |
| Map | 20 reform zones with status, year and coordinates |
| Events | 14 dated reforms and turning points, 1978 to 1997 |
| Format | Parquet, four configurations: `annual`, `peers`, `reform_zones`, `events` |

## What it shows

![Growth and prices, 1961 to 2000](https://huggingface.co/datasets/Kukai-7/deng-era-china/resolve/main/assets/timeline_growth.png)

*Reading the chart: bars are real GDP growth (dark in the Deng era), the red line inflation. Growth is higher and steadier after 1978 than before; inflation flares twice, in 1988 and 1994, each followed by a slowdown.*

- **Growth doubles.** Real GDP grows by 10.1% a year on average from 1978 to 1997, against 5.0% from 1961 to 1977, a period that includes the end of the great famine and the Cultural Revolution. Real GDP per head is 4.7 times its 1978 level by 1997; India's is 1.6 times.
- **The economy turns to money.** Broad money goes from 24% of GDP in 1978 to 115% in 1997, as households save in banks and prices are freed.
- **Prices bite twice.** Consumer inflation reaches 19% in 1988, the year of the price reform scare, and 24% in 1994; growth then falls to 4% in 1989 and 1990, years that also include the June 1989 crackdown and the pause that followed.
- **The country opens step by step.** The official rate moves from 1.7 to 8.3 yuan per dollar, trade from 15% to 34% of GDP, and foreign direct investment from almost nothing to 45 billion dollars a year, most of it after the 1992 Southern Tour.
- **Daily life changes.** The urban share of the population goes from 18% to 32%, agriculture's share of output from 28% to 18%, life expectancy from 63 to 71 years. The share of people below the World Bank's international poverty line falls from 97% (1981) to 63% (1996): a large fall, from a very high level.

![Money and opening](https://huggingface.co/datasets/Kukai-7/deng-era-china/resolve/main/assets/money_and_opening.png)

*Reading the chart: four indicators of monetisation and opening, Deng era shaded. Broad money goes from 24% to 115% of GDP, the yuan from 1.68 to 8.29 per dollar, trade from 15% to 34% of GDP, foreign investment from almost nothing to 45 billion dollars a year.*

![GDP per head since 1960, 1978 = 1](https://huggingface.co/datasets/Kukai-7/deng-era-china/resolve/main/assets/peers.png)

*Reading the chart: real GDP per head with 1978 set to 1, on a log scale so equal slopes mean equal growth rates. China's line steepens in 1978 and keeps its slope; India accelerates later.*

![What moved together, 1979 to 1997](https://huggingface.co/datasets/Kukai-7/deng-era-china/resolve/main/assets/scatter_matrix.png)

*Reading the chart: see "Reading the correlations" below. Trade and foreign investment rise together; few other pairs are clear with nineteen years.*

![How daily life changed](https://huggingface.co/datasets/Kukai-7/deng-era-china/resolve/main/assets/society.png)

*Reading the chart: four markers of daily life, Deng era shaded. Agriculture's share of output falls, the urban share rises, extreme poverty drops from 97% in 1981 to 63% in 1996 by the international line, life expectancy keeps rising.*

## Reading the correlations

**How to read r.** Pearson's r measures how closely two variables move along a straight line: +1 is a perfect positive line, 0 no linear link, -1 a perfect negative line. r² is the share of the variance of one variable that a straight line on the other accounts for (r = 0.7 means about half). The labels used here: under 0.1 negligible, 0.1 to 0.3 weak, 0.3 to 0.5 moderate, 0.5 to 0.7 strong, 0.7 and above very strong.

**How sure is it?** The 95% confidence interval gives the range of r compatible with the data; when it excludes zero, p is below 0.05 and the link is distinguishable from chance. Strength and certainty are different things: a weak r can be certain with many observations, and a strong r can be uncertain with few. Spearman's ρ repeats the exercise on ranks, so a large gap between r and ρ points to outliers or a curved relationship.

**Yearly changes.** Two series that both trend upward will correlate even if they are unrelated. The last column correlates the year-on-year changes instead, which removes shared trends: a link that survives in changes is more convincing than one that exists only in levels.

In the scatter-plot matrix (`scatter_matrix.png`), the panels below the diagonal show the points with a least-squares line, the diagonal shows each distribution, and the panels above the diagonal give r, its 95% confidence interval, p and n for the pair in that row and column. A figure is in colour only when p < 0.05.

**What stands out**

- **Trade and foreign investment move together (+0.92, 95% CI +0.79 to +0.97)**, and still at +0.53 in yearly changes: opening to trade and to capital were the same process.
- **Inflation goes with opening (+0.61 with trade, +0.55 with FDI)**, mostly because the inflation peaks of 1988 and 1994 fall in years of fast opening; in yearly changes the link with trade holds (+0.50) and the one with FDI fades.
- **Growth is not clearly linked to money, inflation or trade in a single year.** All its correlations are positive (+0.27 to +0.38) but the intervals include zero: nineteen years are too few to tell.

**All pairs**, sorted by the size of r. The same figures are in the `correlations` configuration.

| Pair | r | 95% CI | p | n | Spearman ρ | r of yearly changes | Reading |
|---|---|---|---|---|---|---|---|
| Trade (% of GDP) × FDI (% of GDP) | **+0.92** | +0.79 to +0.97 | < 0.001 | 19 | +0.93 | +0.53 (p = 0.02) | very strong, positive; distinguishable from zero |
| Inflation (%) × Trade (% of GDP) | **+0.61** | +0.21 to +0.83 | 0.006 | 19 | +0.55 | +0.50 (p = 0.04) | strong, positive; distinguishable from zero |
| Inflation (%) × FDI (% of GDP) | **+0.55** | +0.13 to +0.81 | 0.01 | 19 | +0.57 | +0.41 (p = 0.09) | strong, positive; distinguishable from zero |
| GDP growth (%) × FDI (% of GDP) | **+0.38** | -0.09 to +0.71 | 0.11 | 19 | +0.42 | +0.20 (p = 0.43) | moderate, positive; not distinguishable from zero |
| GDP growth (%) × Money growth (%) | **+0.36** | -0.11 to +0.70 | 0.13 | 19 | +0.46 | +0.22 (p = 0.39) | moderate, positive; not distinguishable from zero |
| GDP growth (%) × Inflation (%) | **+0.27** | -0.21 to +0.64 | 0.27 | 19 | +0.46 | +0.19 (p = 0.45) | weak, positive; not distinguishable from zero |
| GDP growth (%) × Trade (% of GDP) | **+0.27** | -0.21 to +0.64 | 0.27 | 19 | +0.29 | +0.32 (p = 0.20) | weak, positive; not distinguishable from zero |
| Money growth (%) × FDI (% of GDP) | **+0.25** | -0.23 to +0.63 | 0.30 | 19 | +0.18 | +0.49 (p = 0.04) | weak, positive; not distinguishable from zero |
| Inflation (%) × Money growth (%) | **+0.16** | -0.32 to +0.57 | 0.51 | 19 | +0.36 | -0.03 (p = 0.90) | weak, positive; not distinguishable from zero |
| Money growth (%) × Trade (% of GDP) | **+0.04** | -0.42 to +0.48 | 0.88 | 19 | +0.05 | -0.02 (p = 0.94) | negligible; not distinguishable from zero |

**What it does not say**

- Nineteen years make every interval wide; a moderate r can be noise.
- Official statistics of the period are debated, inflation in particular.
- No correlation here measures the effect of a reform.

## Load it

```python
from datasets import load_dataset

china = load_dataset("Kukai-7/deng-era-china", "annual", split="train").to_pandas()

# Growth, inflation and money growth by stage of the reform
china.groupby("era")[["gdp_growth_pct", "inflation_pct", "broad_money_growth_pct"]].mean()
```

## Configurations

### `annual` (default), 41 rows, China 1960 to 2000

| column | description |
|---|---|
| `year`, `era` | Year and stage: before reform (1960 to 1977), rural reform (1978 to 1984), dual track (1985 to 1991), market push (1992 to 1997), after Deng (1998 to 2000) |
| `gdp_growth_pct`, `gdp_per_capita_usd2015`, `gdp_per_capita_index_1978`, `gdp_current_usd` | Output |
| `gdp_deflator_inflation_pct`, `cpi_inflation_pct`, `inflation_pct`, `inflation_source` | Prices; `inflation_pct` uses the CPI from 1987 and the GDP deflator before |
| `broad_money_pct_gdp`, `broad_money_growth_pct` | Money (M2) |
| `yuan_per_usd_official`, `reserves_usd`, `reserves_usd_bn` | Exchange rate and reserves |
| `trade_pct_gdp`, `exports_pct_gdp`, `fdi_inflows_usd`, `fdi_inflows_usd_bn`, `fdi_inflows_pct_gdp`, `investment_pct_gdp` | Opening and investment |
| `agriculture_pct_gdp`, `industry_pct_gdp`, `urban_pct_population`, `population` | Structure |
| `poverty_headcount_pct`, `gini_index`, `life_expectancy_years` | Living standards |

### `peers`, 264 rows

The same indicators for China, India, Japan and the United States, 1960 to 2025, one row per country and year.

### `reform_zones`, 20 rows

`place`, `place_zh`, `latitude`, `longitude`, `status` (Special Economic Zone, open coastal city, new area), `year`, `province`, `note`.

### `events`, 14 rows

`date` (year and month), `category` (politics, agriculture, opening, reform, money), `event`, `description`.

### `correlations`, 10 rows

One row per pair of variables in the scatter-plot matrix: `x`, `y` and their labels, `n`, `pearson_r`, `r_squared`, `ci95_low`, `ci95_high` (Fisher z interval), `p_value` (two-sided t test), `spearman_rho`, `strength`, `direction`, and for annual series `n_changes`, `pearson_r_changes` and `p_value_changes`, the same correlation on year-on-year differences. Made by `correlations.py`.

## How it was built

1. **Series.** [World Bank Open Data](https://data.worldbank.org/) through its public API (`collect.py`), downloaded in October 2026.
2. **Zones and events.** Curated for this dataset from standard histories of the reform; coordinates are those of the city centre.
3. **Charts.** Python and Matplotlib; borders from Natural Earth. The full pipeline is in [`code/`](./). The correlation figures come from `correlations.py`, which reads only the published Parquet files.

## Limitations

- **Official statistics.** The series rest on China's national accounts. Several economists (Angus Maddison, Harry Wu) estimate that official figures overstate growth in this period, by one to three points a year depending on the method.
- **A flattering baseline.** The 1961 to 1977 average includes the end of the great famine and the Cultural Revolution, so part of the gap with the Deng years is recovery and catching up, not reform alone. Demography and the move of labour out of farming also helped.
- **Two inflation series.** The CPI starts in 1987; before that the GDP deflator stands in, and it moves differently.
- **An official exchange rate.** Before 1994 much trade went through swap markets at a weaker rate than the official one shown here.
- **Foreign investment.** Part of the inflow is Chinese money routed through Hong Kong and counted as foreign.
- **Poverty.** The World Bank's international line ($3.00 a day at 2021 prices) and its survey years (1981, 1984, 1987, 1990, 1993, 1996, 1999); changing the line changes the level a lot, less the trend.
- **What is not measured.** The data cover output and prices, not political freedom, the environment or the regional and urban to rural gaps, which widened in the period.
- **Correlation only.** With nineteen years, the scatter-plot matrix describes the period; it does not identify the effect of any single reform.

## Credits and licences

- Data: World Bank, World Development Indicators, CC BY 4.0.
- Borders: Natural Earth (public domain).
- This compilation, curated tables and charts: CC BY 4.0.

## Related

- [France 1980 to 2026](https://huggingface.co/datasets/Kukai-7/france-economy-1980-2026), the same approach applied to France.
- [Silver Road: Potosí to Ming China](https://huggingface.co/datasets/Kukai-7/silver-road-potosi-ming), money and China four centuries earlier.
- [GitHub: Kukai-7](https://github.com/Kukai-7)
