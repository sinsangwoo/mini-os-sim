from datetime import datetime
from pathlib import Path
import re

# 경로 설정 
DEV_LOG = Path("DEV_log.md")
TIL_ROOT = Path("TIL")

today = datetime.now().strftime("%Y-%m-%d")
year = today[:4]
month = today[5:7]

til_dir = TIL_ROOT / year / month
til_dir.mkdir(parents=True, exist_ok=True)

til_file = til_dir / f"{today}.md"

# dev_log.md에서 오늘 섹션만 추출
text = DEV_LOG.read_text(encoding="utf-8")

pattern = rf"## 📅 .*?{today[-2:]}일 차:(.*?)(?=## 📅|\Z)"
match = re.search(pattern, text, re.S)

if not match:
    print("❌ 오늘 로그 섹션을 찾지 못함")
    exit()

section = match.group(0).strip()

content = f"""# {today}

- [Project] Python mini OS simulator

{section}
"""

til_file.write_text(content, encoding="utf-8")
print(f"✅ TIL 업데이트 완료: {til_file}")
