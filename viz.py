import json, os, glob, numpy as np, pandas as pd, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Polygon as MPoly
from matplotlib.lines import Line2D
from matplotlib.ticker import FixedLocator, FixedFormatter, NullFormatter, NullLocator
from shapely.geometry import shape, box

for f in glob.glob('fonts/*.otf') + ['/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc']:
    if os.path.exists(f): fm.fontManager.addfont(f)
_n = {f.name for f in fm.fontManager.ttflist}
FONT = next((n for n in ('Noto Sans CJK SC', 'Noto Sans CJK JP') if n in _n), 'DejaVu Sans')
plt.rcParams.update({'font.family': FONT, 'font.size': 10, 'axes.edgecolor': '#BBBBBB', 'axes.linewidth': .6,
                     'xtick.color': '#666666', 'ytick.color': '#666666', 'axes.labelcolor': '#444444', 'text.color': '#1F1F1F',
                     'savefig.dpi': 200})
INK, MID, LIGHT, LAND, PAPER = '#1F1F1F', '#8A8A8A', '#C9C6BF', '#ECE9E3', '#FFFFFF'
RED, RED_SOFT, BLUE, BLUE_SOFT = '#B33A2B', '#E3B5AE', '#2F4B7C', '#B9C4D6'
DENG = (1978, 1997)
os.makedirs('out/assets', exist_ok=True)

a = pd.read_parquet('out/data/annual.parquet').set_index('year')
peers = pd.read_parquet('out/data/peers.parquet')
zones = pd.read_parquet('out/data/reform_zones.parquet')
ev = pd.read_parquet('out/data/events.parquet')

def title(fig, t, s, y=.95):
    fig.text(.05, y, t, fontsize=15, weight='bold')
    fig.text(.05, y - .045, s, fontsize=9, color='#555555')
def deng_band(ax, label=True, ytext=None):
    ax.axvspan(DENG[0] - .5, DENG[1] + .5, color=LAND, lw=0, zorder=0)
    if label: ax.text(DENG[0] + .3, ytext if ytext is not None else ax.get_ylim()[1], 'Deng era', fontsize=7.5, color=MID, va='top')

# ------------------------------------------------------------------ 1. map of the reform zones
EXT = (97, 136, 17.5, 45)
clip = box(EXT[0] - 2, EXT[2] - 2, EXT[1] + 2, EXT[3] + 2)
cs = json.load(open('raw/ne_50m_admin_0_countries.geojson'))['features']
fig, ax = plt.subplots(figsize=(10, 8))
for f in cs:
    g = shape(f['geometry'])
    if not g.intersects(clip): continue
    g = g.intersection(clip)
    china = f['properties']['ADM0_A3'] in ('CHN', 'HKG', 'MAC')
    for p in getattr(g, 'geoms', [g]):
        if p.geom_type == 'Polygon':
            ax.add_patch(MPoly(np.array(p.exterior.coords), closed=True, fc=LAND if china else '#F5F3EF', ec=LIGHT if china else '#E2DFD9', lw=.5 if china else .4))
STY = {'Special Economic Zone': dict(s=120, marker='s', c=RED), 'Open coastal city': dict(s=46, marker='o', c=BLUE), 'New area': dict(s=80, marker='D', c=INK)}
for st, kw in STY.items():
    z = zones[zones.status == st]
    ax.scatter(z.longitude, z.latitude, edgecolors=PAPER, lw=.8, zorder=4, label=f'{st} ({len(z)})', **kw)
LAB = {'Shenzhen': (8, -14, 'left', RED, 'Shenzhen 1980'), 'Zhuhai': (-10, -4, 'right', RED, 'Zhuhai 1980'), 'Shantou': (8, -3, 'left', RED, 'Shantou 1980'),
       'Xiamen': (8, -3, 'left', RED, 'Xiamen 1980'), 'Hainan': (8, -3, 'left', RED, 'Hainan 1988'), 'Pudong': (9, -10, 'left', INK, 'Pudong 1990'),
       'Shanghai': (9, 2, 'left', BLUE, 'Shanghai'), 'Dalian': (7, 2, 'left', BLUE, 'Dalian'), 'Tianjin': (-7, 2, 'right', BLUE, 'Tianjin'),
       'Qingdao': (7, -3, 'left', BLUE, 'Qingdao'), 'Guangzhou': (-8, 5, 'right', BLUE, 'Guangzhou'), 'Beihai': (-8, 2, 'right', BLUE, 'Beihai'),
       'Wenzhou': (8, -3, 'left', BLUE, 'Wenzhou'), 'Fuzhou': (8, -3, 'left', BLUE, 'Fuzhou'), 'Qinhuangdao': (6, 4, 'left', BLUE, 'Qinhuangdao'),
       'Yantai': (8, -1, 'left', BLUE, 'Yantai'), 'Lianyungang': (8, -3, 'left', BLUE, 'Lianyungang'), 'Nantong': (-8, 0, 'right', BLUE, 'Nantong'),
       'Ningbo': (8, -3, 'left', BLUE, 'Ningbo'), 'Zhanjiang': (8, -6, 'left', BLUE, 'Zhanjiang')}
for p, (dx, dy, ha, col, t) in LAB.items():
    r = zones[zones.place == p].iloc[0]
    ax.annotate(t, (r.longitude, r.latitude), xytext=(dx, dy), textcoords='offset points', ha=ha, fontsize=8, color=col, zorder=5)
ax.scatter([116.40], [39.90], s=30, marker='*', c=INK, zorder=5); ax.annotate('Beijing', (116.40, 39.90), xytext=(-8, 4), textcoords='offset points', ha='right', fontsize=8.5)
ax.annotate('Hong Kong', (114.17, 22.32), xytext=(24, -30), textcoords='offset points', fontsize=7.5, color=MID, arrowprops=dict(arrowstyle='-', color=LIGHT, lw=.6))
ax.text(104, 33, 'C H I N A', fontsize=16, color='#D4D0C8', ha='center', weight='bold')
ax.set_xlim(EXT[0], EXT[1]); ax.set_ylim(EXT[2], EXT[3]); ax.set_aspect(1 / np.cos(np.radians(31)))
ax.set_xticks([]); ax.set_yticks([])
for s_ in ax.spines.values(): s_.set_visible(False)
ax.legend(loc='lower left', frameon=False, fontsize=8.5, markerscale=.9)
title(fig, 'Opening the coast, 1980 to 1990', 'Where China first let in foreign capital: the Special Economic Zones, the open coastal cities and Pudong.', y=.955)
fig.text(.05, .03, 'Zones and dates: curated for this dataset from standard histories of the reform. Borders: Natural Earth.', fontsize=7, color=MID)
plt.subplots_adjust(left=.02, right=.98, top=.88, bottom=.05)
fig.savefig('out/assets/map_reform_zones.png', facecolor=PAPER); plt.close(fig)

# ------------------------------------------------------------------ 2. growth and inflation, 1961 to 2000
fig, ax = plt.subplots(figsize=(12, 5))
ax.set_ylim(-32, 32); deng_band(ax, ytext=31)
yrs = a.index[a.index >= 1961]
cols = [INK if DENG[0] <= y <= DENG[1] else LIGHT for y in yrs]
ax.bar(yrs, a.loc[yrs, 'gdp_growth_pct'], color=cols, width=.75, zorder=2, label='Real GDP growth (dark: Deng era)')
ax.plot(a.index, a.inflation_pct, color=RED, lw=1.8, zorder=3, label='Inflation (GDP deflator, CPI from 1987)')
ax.axhline(0, color=MID, lw=.6, zorder=1)
SHORT = {'1980-08': 'SEZs', '1984-05': '14 cities', '1988-08': 'Price scare', '1989-06': 'June 1989', '1992-01': 'Southern Tour', '1994-01': 'One exchange rate'}
for i, (d, t) in enumerate(SHORT.items()):
    y = int(d[:4]) + (int(d[5:]) - .5) / 12
    lo = -26.5 if i % 2 == 0 else -21.5
    ax.plot([y, y], [lo + .5, -18], color=BLUE, lw=.8, alpha=.7)
    ax.text(y, lo, t, fontsize=7.2, color=BLUE, ha='center', va='top')
ax.text(1961.6, -12, 'Famine years', fontsize=7.5, color=MID)
ax.set_ylabel('Percent'); ax.set_xlim(1960, 2001)
ax.spines[['top', 'right']].set_visible(False)
ax.legend(loc='lower left', bbox_to_anchor=(0, 1.0), ncol=2, frameon=False, fontsize=8.2)
title(fig, 'Growth and prices, 1961 to 2000', 'Average growth doubles in the Deng years, about 10% a year against 5%; inflation flares twice, in 1988 and 1994.', y=.965)
plt.subplots_adjust(left=.07, right=.985, top=.8, bottom=.12)
fig.savefig('out/assets/timeline_growth.png', facecolor=PAPER); plt.close(fig)

# ------------------------------------------------------------------ 3. money and opening, small multiples
P = [('broad_money_pct_gdp', 'Broad money, % of GDP', BLUE, None), ('yuan_per_usd_official', 'Yuan per US dollar, official', RED, None),
     ('trade_pct_gdp', 'Trade, % of GDP', BLUE, None), ('fdi_inflows_usd_bn', 'Foreign direct investment, billion US$', RED, None)]
fig, axs = plt.subplots(2, 2, figsize=(12, 7))
for ax, (c, t, col, _) in zip(axs.flat, P):
    s = a.loc[1970:2000, c].dropna()
    ax.set_xlim(1969.5, 2000.5); lo, hi = 0, s.max() * 1.12; ax.set_ylim(lo, hi)
    deng_band(ax, label=False)
    ax.plot(s.index, s.values, color=col, lw=2, zorder=3)
    ax.scatter([1978, 1997], [s.get(1978, np.nan), s.get(1997, np.nan)], s=22, c=col, zorder=4)
    for y in (1978, 1997):
        if y in s.index: ax.annotate(f'{s[y]:.3g}', (y, s[y]), xytext=(0, 7), textcoords='offset points', ha='center', fontsize=8, color=col)
    ax.set_title(t, fontsize=10, loc='left', color=INK)
    ax.spines[['top', 'right']].set_visible(False); ax.tick_params(labelsize=8)
title(fig, 'Money and opening', 'Shaded: the Deng era, 1978 to 1997. The economy monetises, the yuan is devalued step by step, trade and foreign capital arrive.', y=.965)
plt.subplots_adjust(left=.06, right=.98, top=.83, bottom=.06, hspace=.38, wspace=.15)
fig.savefig('out/assets/money_and_opening.png', facecolor=PAPER); plt.close(fig)

# ------------------------------------------------------------------ 4. GDP per head against peers, index 1978 = 1
fig, ax = plt.subplots(figsize=(12, 5))
ax.set_yscale('log'); ax.set_ylim(.25, 60); deng_band(ax, ytext=55)
STY2 = {'CHN': (RED, 2.4, 'China'), 'IND': (BLUE, 1.6, 'India'), 'JPN': (MID, 1.3, 'Japan'), 'USA': (INK, 1.3, 'United States')}
for c, (col, lw, lab) in STY2.items():
    s = peers[peers.country == c].set_index('year').gdp_per_capita_usd2015.dropna()
    s = s / s[1978]
    ax.plot(s.index, s.values, color=col, lw=lw, label=lab)
    ax.annotate(f'{lab} ×{s.iloc[-1]:.1f}', (s.index[-1], s.iloc[-1]), xytext=(5, -9 if c == 'JPN' else (4 if c == 'USA' else 0)), textcoords='offset points', fontsize=8.5, color=col, va='center')
ch97 = peers[(peers.country == 'CHN')].set_index('year').gdp_per_capita_usd2015
ax.scatter([1997], [ch97[1997] / ch97[1978]], c=RED, s=26, zorder=4)
ax.annotate(f'×{ch97[1997] / ch97[1978]:.1f} by 1997', (1997, ch97[1997] / ch97[1978]), xytext=(-10, 10), textcoords='offset points', ha='right', fontsize=8.5, color=RED)
ax.yaxis.set_major_locator(FixedLocator([.25, .5, 1, 2, 5, 10, 20, 50])); ax.yaxis.set_major_formatter(FixedFormatter(['¼', '½', '1', '2', '5', '10', '20', '50']))
ax.yaxis.set_minor_locator(NullLocator())
ax.axhline(1, color=MID, lw=.6)
ax.set_xlim(1960, 2032); ax.set_ylabel('GDP per head, 1978 = 1 (log scale)')
ax.spines[['top', 'right']].set_visible(False)
title(fig, 'GDP per head since 1960, 1978 = 1', 'Real GDP per head in constant dollars. China multiplies its 1978 level almost five times by 1997, India by 1.6. Right: multiple by 2025.', y=.965)
plt.subplots_adjust(left=.07, right=.985, top=.82, bottom=.08)
fig.savefig('out/assets/peers.png', facecolor=PAPER); plt.close(fig)

# ------------------------------------------------------------------ 5. scatter-plot matrix: made by correlations.py, with r, confidence intervals and p-values

# ------------------------------------------------------------------ 6. how life changed
P = [('agriculture_pct_gdp', 'Agriculture, % of GDP', BLUE), ('urban_pct_population', 'Urban population, %', BLUE),
     ('poverty_headcount_pct', 'Below the international poverty line, %', RED), ('life_expectancy_years', 'Life expectancy at birth, years', INK)]
fig, axs = plt.subplots(1, 4, figsize=(13, 3.8))
for ax, (c, t, col) in zip(axs, P):
    s = a.loc[1960:2000, c].dropna()
    ax.set_xlim(1959, 2001); ax.set_ylim(0 if c != 'life_expectancy_years' else 30, max(100 if 'poverty' in c else 0, s.max() * 1.15))
    deng_band(ax, label=False)
    ax.plot(s.index, s.values, color=col, lw=2, marker='o' if len(s) < 15 else None, ms=4)
    for y0 in (1978, 1997):
        y = min(s.index, key=lambda v: abs(v - y0))
        ax.scatter([y], [s[y]], s=16, c=col, zorder=4)
        ax.annotate(f'{s[y]:.0f} ({y})', (y, s[y]), xytext=(0, 8), textcoords='offset points', fontsize=7.5, color=col, ha='center')
    ax.set_title(t, fontsize=9.2, loc='left')
    ax.spines[['top', 'right']].set_visible(False); ax.tick_params(labelsize=7.5)
title(fig, 'How daily life changed', 'Shaded: the Deng era. Poverty: World Bank international line, surveys from 1981 only.', y=.95)
plt.subplots_adjust(left=.04, right=.99, top=.74, bottom=.09, wspace=.22)
fig.savefig('out/assets/society.png', facecolor=PAPER); plt.close(fig)
print('ok')
