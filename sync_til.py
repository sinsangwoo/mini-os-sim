import os
import re
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DEV_LOG = BASE_DIR / "DEV_log.md"
TIL_ROOT = BASE_DIR / "TIL"

# 오늘 날짜 및 저장 경로 설정
today = datetime.now().strftime("%Y-%m-%d")
year, month, _ = today.split('-')
til_dir = TIL_ROOT / year / month
til_dir.mkdir(parents=True, exist_ok=True)
til_file = til_dir / f"{today}.md"

# 1. 파일 읽기
text = DEV_LOG.read_text(encoding="utf-8")

# 2. 파싱 (성공 사례 포맷에 맞춘 가장 확실한 분리)
# '## 📅' 또는 '📅'를 기준으로 자르고 마지막 덩어리 선택
sections = re.split(r'\n(?=## 📅|📅)', text)
last_section = sections[-1].strip()

# 3. 저장 내용 구성
content = f"# {today}\n\n- [Project] Python mini OS simulator\n\n{last_section}"

# 4. 파일 쓰기
til_file.write_text(content, encoding="utf-8")

print(f"✅ TIL 업데이트 완료: {til_file.absolute()}")
