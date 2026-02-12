#!/bin/bash

echo "=== 1. Syncing TIL ==="
py sync_til.py

echo "=== 2. Committing OS Project ==="
# 메시지 입력받기
echo "Enter OS commit message:"
read commit_msg

# 입력받은 변수($commit_msg)를 사용하기
git add .
git commit -m "$commit_msg"
git push

echo "=== 3. Committing TIL ==="
cd TIL
git add .
git commit -m "Daily TIL Update"
git push
cd ..

echo "=== ALL DONE! ==="
# 창이 바로 닫히지 않게 잠시 대기
read -p "Press enter to continue..."