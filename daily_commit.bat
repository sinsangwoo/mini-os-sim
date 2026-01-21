@echo off

echo === 1. Syncing TIL ===
python sync_til.py

echo === 2. Committing OS Project ===
git add .
git commit -m "Update OS project and logs"
git push

echo === 3. Committing TIL ===
cd TIL
git add .
git commit -m "Sync TIL from OS Project"
git push
cd ..

echo === ALL DONE! ===
pause