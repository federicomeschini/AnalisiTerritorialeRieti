"""Download the ISTAT 2021 study-commuting matrix once esploradati.istat.it is reachable.

Usage:  python analysis/scripts/fetch_istat_study_matrix.py [--list]
  --list  only list the commuting dataflows the SDMX service exposes.

The file is saved to analysis/sources/istat_pendolarismo/istat_studio_2021_<dataflow>.csv, where
build_commuting_evidence.py picks it up automatically. If the SDMX service is unavailable but the web
data browser works, export the study matrix manually from
https://esploradati.istat.it/databrowser/#/it/censpop/categories/IT1,Z1200CPA,1.0/MATRICE_PEND
and save it in the same folder with 'studio' and '2021' in the file name.
"""
from pathlib import Path
import re
import sys
import urllib.request
import urllib.error

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'analysis/sources/istat_pendolarismo'
BASES = ['https://esploradati.istat.it/SDMXWS/rest', 'https://sdmx.istat.it/SDMXWS/rest']
UA = {'User-Agent': 'Mozilla/5.0'}

def get(url, accept='application/xml', timeout=120):
    req = urllib.request.Request(url, headers={**UA, 'Accept': accept})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()

def dataflows():
    for base in BASES:
        try:
            xml = get(f'{base}/dataflow/IT1', timeout=60).decode('utf8', 'replace')
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            print(f'{base}: unreachable ({e})')
            continue
        flows = []
        for m in re.finditer(r'<(?:\w+:)?Dataflow\b[^>]*\bid="([^"]+)"[^>]*\bversion="([^"]+)".*?</(?:\w+:)?Dataflow>', xml, re.S):
            names = re.findall(r'<(?:\w+:)?Name xml:lang="(\w+)">([^<]+)<', m.group(0))
            name = dict(names).get('it') or (names[0][1] if names else '')
            if re.search(r'pend|matrice', m.group(1) + name, re.I):
                flows.append((m.group(1), m.group(2), name))
        return base, flows
    sys.exit('ISTAT SDMX service still unreachable; try again later or use the manual export described above.')

base, flows = dataflows()
for f in flows:
    print('  %-40s v%-6s %s' % f)
if '--list' in sys.argv:
    sys.exit()
study = [f for f in flows if re.search(r'stud', f[0] + f[2], re.I)] or [f for f in flows if re.search(r'pend', f[0] + f[2], re.I)]
if not study:
    sys.exit('No commuting dataflow found; rerun with --list and pick one manually.')
SRC.mkdir(parents=True, exist_ok=True)
for fid, ver, name in study:
    url = f'{base}/data/IT1,{fid},{ver}/ALL/'
    print(f'downloading {fid} ({name}) ...')
    try:
        data = get(url, accept='application/vnd.sdmx.data+csv;version=1.0.0', timeout=1800)
    except urllib.error.HTTPError as e:
        print(f'  failed: HTTP {e.code}; try the manual export')
        continue
    out = SRC / f'istat_studio_2021_{fid}.csv'
    out.write_bytes(data)
    head = data[:600].decode('utf8', 'replace').splitlines()
    print(f'  saved {out.relative_to(ROOT)} ({len(data)/1e6:.1f} MB)')
    print('  header:', head[0] if head else '(empty)')
    print('  If build_commuting_evidence.py cannot identify origin/destination/count columns, set STUDY_2021_COLUMNS there.')
