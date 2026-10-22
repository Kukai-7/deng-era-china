"""Download the raw series used by build.py into raw/bundle.json (World Bank API, no key needed)."""
import json, os, requests

PEERS = 'CHN;IND;JPN;USA'
INDICATORS = ['NY.GDP.MKTP.KD.ZG', 'NY.GDP.PCAP.KD', 'NY.GDP.DEFL.KD.ZG', 'FP.CPI.TOTL.ZG', 'FM.LBL.BMNY.GD.ZS', 'FM.LBL.BMNY.ZG',
              'PA.NUS.FCRF', 'NE.TRD.GNFS.ZS', 'NE.EXP.GNFS.ZS', 'BX.KLT.DINV.WD.GD.ZS', 'BX.KLT.DINV.CD.WD', 'NV.AGR.TOTL.ZS',
              'NV.IND.TOTL.ZS', 'SP.URB.TOTL.IN.ZS', 'SI.POV.DDAY', 'SI.POV.GINI', 'SP.DYN.LE00.IN', 'NE.GDI.TOTL.ZS',
              'FI.RES.TOTL.CD', 'SP.POP.TOTL', 'NY.GDP.MKTP.CD']


def wb(countries, ind):
    url = f'https://api.worldbank.org/v2/country/{countries}/indicator/{ind}?format=json&per_page=2000&date=1960:2026'
    rows = requests.get(url, timeout=60).json()[1] or []
    return [[r['countryiso3code'], int(r['date']), float(f"{float(r['value']):.6g}")] for r in rows if r['value'] is not None]


if __name__ == '__main__':
    os.makedirs('raw', exist_ok=True)
    out = {f'wb_CHN_{i}': wb(PEERS, i) for i in INDICATORS}
    json.dump(out, open('raw/bundle.json', 'w'))
    print({k: len(v) for k, v in out.items()})
