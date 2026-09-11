from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
ASSETS = {
    'assets/images/apple.jpg': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=1600&q=85',
    'assets/images/tesla.jpg': 'https://images.unsplash.com/photo-1560958089-b8a1929cea89?auto=format&fit=crop&w=1200&q=85',
    'assets/images/gaming.jpg': 'https://images.unsplash.com/photo-1542751371-adc38448a05e?auto=format&fit=crop&w=1200&q=85',
    'assets/fonts/space-grotesk.ttf': 'https://raw.githubusercontent.com/google/fonts/main/ofl/spacegrotesk/SpaceGrotesk%5Bwght%5D.ttf',
    'assets/fonts/source-sans-3.ttf': 'https://raw.githubusercontent.com/google/fonts/main/ofl/sourcesans3/SourceSans3%5Bwght%5D.ttf',
    'assets/fonts/space-grotesk-LICENSE.txt': 'https://raw.githubusercontent.com/google/fonts/main/ofl/spacegrotesk/OFL.txt',
    'assets/fonts/source-sans-3-LICENSE.txt': 'https://raw.githubusercontent.com/google/fonts/main/ofl/sourcesans3/OFL.txt',
}

if __name__ == '__main__':
    for filename, url in ASSETS.items():
        path = ROOT / filename
        if path.exists() and path.stat().st_size > 100:
            print('Existing:', filename)
            continue
        data = urlopen(Request(url, headers={'User-Agent': 'Bitora educational website asset setup'}), timeout=45).read()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        print(filename, len(data), 'bytes')
