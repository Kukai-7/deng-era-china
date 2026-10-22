"""Build the Deng-era China dataset from raw/bundle.json (World Bank) plus curated reform zones and events."""
import json, os, numpy as np, pandas as pd

RAW, OUT = 'raw', 'out/data'
os.makedirs(OUT, exist_ok=True)
B = json.load(open(f'{RAW}/bundle.json'))

NAMES = {
    'NY.GDP.MKTP.KD.ZG': 'gdp_growth_pct', 'NY.GDP.PCAP.KD': 'gdp_per_capita_usd2015', 'NY.GDP.DEFL.KD.ZG': 'gdp_deflator_inflation_pct',
    'FP.CPI.TOTL.ZG': 'cpi_inflation_pct', 'FM.LBL.BMNY.GD.ZS': 'broad_money_pct_gdp', 'FM.LBL.BMNY.ZG': 'broad_money_growth_pct',
    'PA.NUS.FCRF': 'yuan_per_usd_official', 'NE.TRD.GNFS.ZS': 'trade_pct_gdp', 'NE.EXP.GNFS.ZS': 'exports_pct_gdp',
    'BX.KLT.DINV.WD.GD.ZS': 'fdi_inflows_pct_gdp', 'BX.KLT.DINV.CD.WD': 'fdi_inflows_usd', 'NV.AGR.TOTL.ZS': 'agriculture_pct_gdp',
    'NV.IND.TOTL.ZS': 'industry_pct_gdp', 'SP.URB.TOTL.IN.ZS': 'urban_pct_population', 'SI.POV.DDAY': 'poverty_headcount_pct',
    'SI.POV.GINI': 'gini_index', 'SP.DYN.LE00.IN': 'life_expectancy_years', 'NE.GDI.TOTL.ZS': 'investment_pct_gdp',
    'FI.RES.TOTL.CD': 'reserves_usd', 'SP.POP.TOTL': 'population', 'NY.GDP.MKTP.CD': 'gdp_current_usd',
}
rows = []
for code, col in NAMES.items():
    for iso, year, v in B[f'wb_CHN_{code}']:
        rows.append((iso, year, col, v))
long = pd.DataFrame(rows, columns=['country', 'year', 'indicator', 'value'])

# ------------------------------------------------------------------ peers: China, India, Japan, United States, 1960 onwards
peers = long.pivot_table(index=['country', 'year'], columns='indicator', values='value').reset_index()
peers = peers[['country', 'year'] + [c for c in NAMES.values() if c in peers.columns]].sort_values(['country', 'year'])
peers.to_parquet(f'{OUT}/peers.parquet', index=False)

# ------------------------------------------------------------------ China annual, 1960 to 2000, with eras
ch = peers[peers.country == 'CHN'].drop(columns='country')
ch = ch[(ch.year >= 1960) & (ch.year <= 2000)].copy()
def era(y):
    if y < 1978: return 'before reform (1960 to 1977)'
    if y <= 1984: return 'rural reform (1978 to 1984)'
    if y <= 1991: return 'dual track (1985 to 1991)'
    if y <= 1997: return 'market push (1992 to 1997)'
    return 'after Deng (1998 to 2000)'
ch.insert(1, 'era', ch.year.map(era))
# one inflation series: CPI from 1987, GDP deflator before
ch['inflation_pct'] = ch.cpi_inflation_pct.fillna(ch.gdp_deflator_inflation_pct)
ch['inflation_source'] = np.where(ch.cpi_inflation_pct.notna(), 'CPI', 'GDP deflator')
base = ch.loc[ch.year == 1978, 'gdp_per_capita_usd2015'].iloc[0]
ch['gdp_per_capita_index_1978'] = (ch.gdp_per_capita_usd2015 / base).round(3)
ch['fdi_inflows_usd_bn'] = (ch.fdi_inflows_usd / 1e9).round(3)
ch['reserves_usd_bn'] = (ch.reserves_usd / 1e9).round(3)
ch.to_parquet(f'{OUT}/annual.parquet', index=False)

# ------------------------------------------------------------------ reform zones (curated)
Z = [
    ('Shenzhen', '深圳', 22.543, 114.058, 'Special Economic Zone', 1980, 'Guangdong', 'Next to Hong Kong; the flagship zone'),
    ('Zhuhai', '珠海', 22.271, 113.577, 'Special Economic Zone', 1980, 'Guangdong', 'Next to Macau'),
    ('Shantou', '汕头', 23.354, 116.682, 'Special Economic Zone', 1980, 'Guangdong', 'Home region of many overseas Chinese'),
    ('Xiamen', '厦门', 24.480, 118.089, 'Special Economic Zone', 1980, 'Fujian', 'Facing Taiwan'),
    ('Hainan', '海南', 20.044, 110.199, 'Special Economic Zone', 1988, 'Hainan', 'Whole island made a province and a zone'),
    ('Dalian', '大连', 38.914, 121.615, 'Open coastal city', 1984, 'Liaoning', ''),
    ('Qinhuangdao', '秦皇岛', 39.935, 119.600, 'Open coastal city', 1984, 'Hebei', ''),
    ('Tianjin', '天津', 39.125, 117.190, 'Open coastal city', 1984, 'Tianjin', ''),
    ('Yantai', '烟台', 37.464, 121.448, 'Open coastal city', 1984, 'Shandong', ''),
    ('Qingdao', '青岛', 36.067, 120.383, 'Open coastal city', 1984, 'Shandong', ''),
    ('Lianyungang', '连云港', 34.597, 119.222, 'Open coastal city', 1984, 'Jiangsu', ''),
    ('Nantong', '南通', 31.981, 120.894, 'Open coastal city', 1984, 'Jiangsu', ''),
    ('Shanghai', '上海', 31.231, 121.474, 'Open coastal city', 1984, 'Shanghai', ''),
    ('Ningbo', '宁波', 29.868, 121.544, 'Open coastal city', 1984, 'Zhejiang', ''),
    ('Wenzhou', '温州', 28.000, 120.672, 'Open coastal city', 1984, 'Zhejiang', 'Known for private firms'),
    ('Fuzhou', '福州', 26.074, 119.296, 'Open coastal city', 1984, 'Fujian', ''),
    ('Guangzhou', '广州', 23.129, 113.264, 'Open coastal city', 1984, 'Guangdong', ''),
    ('Zhanjiang', '湛江', 21.271, 110.359, 'Open coastal city', 1984, 'Guangdong', ''),
    ('Beihai', '北海', 21.481, 109.120, 'Open coastal city', 1984, 'Guangxi', ''),
    ('Pudong', '浦东', 31.221, 121.544, 'New area', 1990, 'Shanghai', 'Opened to foreign investment in 1990'),
]
zones = pd.DataFrame(Z, columns=['place', 'place_zh', 'latitude', 'longitude', 'status', 'year', 'province', 'note'])
zones.to_parquet(f'{OUT}/reform_zones.parquet', index=False)

# ------------------------------------------------------------------ events (curated)
E = [
    ('1978-12', 'politics', 'Third Plenum of the 11th Central Committee', 'The party turns from class struggle to economic construction; usually taken as the start of reform and opening.'),
    ('1979-01', 'agriculture', 'Higher state prices for grain', 'Procurement prices raised by about a fifth, with a premium above quota.'),
    ('1980-08', 'opening', 'First Special Economic Zones', 'Shenzhen, Zhuhai, Shantou and Xiamen get their own rules for foreign investment and trade.'),
    ('1982-01', 'agriculture', 'Household contracts endorsed', 'The household responsibility system spreads; by 1984 nearly all farm households work their own plots.'),
    ('1984-05', 'opening', 'Fourteen coastal cities opened', 'From Dalian to Beihai, cities get powers to attract foreign capital.'),
    ('1984-10', 'reform', 'Reform moves to the cities', 'Decision on reform of the economic structure: enterprises, prices and planning.'),
    ('1985-01', 'money', 'Dual-track prices', 'Plan prices for quota output, market prices above it.'),
    ('1988-08', 'money', 'Price reform scare', 'Announcement of price liberalisation triggers bank runs and panic buying; inflation reaches about 19%.'),
    ('1989-06', 'politics', 'Crackdown in Beijing', 'Protests end with the army clearing Tiananmen Square on 3 and 4 June; reform slows and foreign lending pauses.'),
    ('1990-12', 'money', 'Shanghai Stock Exchange opens', 'Shenzhen follows in 1991.'),
    ('1992-01', 'politics', 'Southern Tour', 'Deng visits Wuchang, Shenzhen, Zhuhai and Shanghai and calls for faster reform; the 14th Congress adopts the socialist market economy.'),
    ('1993-07', 'money', 'Austerity programme', 'Credit tightened against overheating and inflation.'),
    ('1994-01', 'money', 'Single exchange rate', 'Official and swap market rates unified at about 8.7 yuan per dollar; tax-sharing reform between centre and provinces.'),
    ('1997-02', 'politics', 'Death of Deng Xiaoping', 'Hong Kong returns to China in July.'),
]
ev = pd.DataFrame(E, columns=['date', 'category', 'event', 'description'])
ev.to_parquet(f'{OUT}/events.parquet', index=False)

def mean(a, b, c): return float(ch[(ch.year >= a) & (ch.year <= b)][c].mean())
stats = dict(growth_1978_1997=round(mean(1978, 1997, 'gdp_growth_pct'), 2), growth_1961_1977=round(mean(1961, 1977, 'gdp_growth_pct'), 2),
             gdppc_multiple_1978_1997=round(float(ch.loc[ch.year == 1997, 'gdp_per_capita_index_1978'].iloc[0]), 2))
json.dump(stats, open('out/stats.json', 'w'), indent=1)
print(stats, len(peers), len(ch))
