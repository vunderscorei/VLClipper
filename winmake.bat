@ECHO ON

pip install -r requirements.txt
python defaults_generator.py
rmdir dist
pyinstaller --noconfirm pyinstaller.spec
ECHO Finished
PAUSE