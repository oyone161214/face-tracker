# face-tracker

## 🚀 クイックスタート(RaspberryPi)

### 1. リポジトリのクローン

```bash
git clone https://github.com/yamamoto/face-tracker
cd face-tracker
```


### 2. 仮想環境の作成・有効化

```bash
# Windows (Git Bash)
py -3.11 -m venv .venv
source .venv/Scripts/activate

# Windows (PowerShell)
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1

# macOS/Linux
python3.11 -m venv .venv
source .venv/bin/activate
```

### 3.環境構築(pigpiod)
```bash
sudo apt update
sudo apt upgrade
sudo apt install pigpio
which pigpiod　　（でpigpiodがあるか確認）
sudo systemctl stop pigpiod
sudo pigpiod
```

### 4.インストール方法（YOLO）
```bash
psudo apt update
sudo apt install python3-pip -y
pip install -U pip
pip install ultralytics[export]
sudo reboot

```