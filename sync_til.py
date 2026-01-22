from datetime import datetime
from pathlib import Path
import re

# 경로 설정
DEV_LOG = Path("DEV_log.md")
TIL_ROOT = Path("TIL")

# 오늘 날짜 (2026-01-22)
today = datetime.now().strftime("%Y-%m-%d")
year, month, _ = today.split('-')

# 저장할 폴더 만들기
til_dir = TIL_ROOT / year / month
til_dir.mkdir(parents=True, exist_ok=True)
til_file = til_dir / f"{today}.md"

# 1. dev_log.md 내용 읽기
text = DEV_LOG.read_text(encoding="utf-8")

# 2. '## 📅'를 기준으로 문서 나누기 (가장 똑똑한 방법)
# 이 방법은 숫자가 몇 일차인지 상관없이 마지막 덩어리만 쏙 빼옵니다.
sections = re.split(r'\n(?=## 📅)', text)
last_section = sections[-1].strip() # 맨 마지막 섹션 가져오기

# 3. 저장할 내용 구성
content = f"""# {today}

- [Project] Python mini OS simulator

{last_section}
"""

# 4. 파일 쓰기
til_file.write_text(content, encoding="utf-8")
print(f"✅ TIL 업데이트 완료: {til_file}")
