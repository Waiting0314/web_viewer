# Web Viewer

**簡介** ✅

`Web Viewer` 是一個以 Django 開發的簡易媒體管理/檢視應用，包含兩個主要 app：`albums`（相簿）與 `videos`（影片）。專案已支援透過 Docker Compose 快速在本機啟動 PostgreSQL 與 Django 伺服器。

---

## 主要功能 🔧

以下為更詳細的功能說明：

- Albums（相簿）
  - 支援透過 **Zip 檔上傳**（會自動解壓並依檔名排序建立 Photo 物件）或 **選擇多個檔案上傳（資料夾上傳）**。
  - 相簿有標題、描述、封面圖片、與多個標籤（Tag），標籤以逗號分隔輸入。
  - 在後台管理介面（Django admin）可編輯相簿與內含的照片（Photo inline）並查看圖片數量。

- 相片管理（Photos）
  - 支援常見影像格式（.jpg / .jpeg / .png / .gif / .webp / .bmp），上傳時會過濾不支援的檔案。
  - 每張 Photo 有順序（order）欄位，Zip / 多檔上傳時會根據檔名或壓縮檔內順序自動排序。

- 檢索與篩選
  - 支援關鍵字搜尋（標題/描述）以及**標籤過濾**（Tag Cloud / 篩選連結）。
  - 支援依 `created_at` 或 `title` 之排序選擇。

- 相簿檢視（Viewer）
  - 提供 **Scroll（滾動）** 與 **Flip（翻頁）** 兩種檢視模式，Flip 模式內建分頁導航與跳頁滑桿。

- Videos（影片）
  - 可以上傳影片檔並建立 Video 物件（包含 title/description/file/cover 等欄位）。
  - 上傳後會 **背景生成縮圖（thumbnail）**，目前使用本地執行緒觸發 `ffmpeg`（若未安裝 ffmpeg，程式會顯示警告且不會生成縮圖）。
  - 支援影片清單、影片播放頁（detail）以及刪除功能。
  - 上傳表單會在偵測到 AJAX（XMLHttpRequest）時回傳 JSON（成功或錯誤訊息，並包含 redirect_url），方便在前端做非同步上傳體驗。

- 使用者體驗與前端
  - 前端模板提供 Tag Cloud、搜尋列、相簿卡片（含標籤）、以及影片/相簿上傳頁面。
  - Viewer 有基本的 JS 控制（分頁、跳至特定頁面、保留 query params 的檢視模式等）。

- 開發/部署注意事項
  - 媒體檔與靜態檔案預設存放在專案內的 `media/` 與 `static/`（開發方便），生產環境建議改用外部儲存或 CDN。
  - 影片縮圖需要 `ffmpeg`，若要在生產環境做穩定的背景任務，建議改用 Celery / RQ 與外部 worker。

---

---

## 專案結構 🗂️

- `docker-compose.yml` - Docker Compose 設定（web 與 db）
- `Dockerfile` - 建構 web container 的映像檔
- `requirements.txt` - Python 套件清單
- `src/` - Django 專案根目錄
  - `manage.py` - Django 管理指令
  - `config/` - Django 應用設定（`settings.py`, `urls.py`, `wsgi.py`, `asgi.py`）
  - `albums/` - 相簿 app（models, views, forms, urls, templates）
  - `videos/` - 影片 app（models, views, forms, urls, templates）
  - `templates/` - 全域模板（如 `base.html`）
  - `static/` - CSS/JS 等靜態資源
  - `media/` - 上傳的媒體檔案（在開發時直接儲存在此資料夾）

---

## 快速啟動（推薦：Docker） 🚀

先確保已安裝 Docker 與 Docker Compose。

在專案根目錄執行：

```powershell
docker-compose up --build
```

- 服務會根據 `docker-compose.yml` 建構並啟動
- web service 的預設啟動指令會執行遷移（`makemigrations`、`migrate`）並啟動開發伺服器

若要在背景執行：

```powershell
docker-compose up --build -d
```

常用指令：

```powershell
# 進入 web container 的 shell
docker-compose exec web sh
# 在容器內建立 superuser
docker-compose exec web python manage.py createsuperuser
# 執行 Django 測試
docker-compose exec web python manage.py test
```

---

## 本地開發（不使用 Docker） ⚙️

1. 建立並啟動虛擬環境（PowerShell 範例）

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. 設定環境變數（可參考 `docker-compose.yml`）
3. 執行遷移並啟動伺服器

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

---

## 環境變數（範例） 💡

請參考 `docker-compose.yml` 中 `environment`：

- `DEBUG` = 1 或 0
- `SECRET_KEY` = Django 的 secret key
- `DJANGO_ALLOWED_HOSTS` = 允許的 host
- `SQL_ENGINE` = `django.db.backends.postgresql`
- `SQL_DATABASE`, `SQL_USER`, `SQL_PASSWORD`, `SQL_HOST`, `SQL_PORT`

---

## 資料庫 & 遷移 📦

專案預設使用 PostgreSQL（Docker Compose 已為 `db` service 提供設定）。

如需手動執行：

```powershell
python manage.py makemigrations
python manage.py migrate
```

---

## 靜態檔與媒體檔案

- 開發時靜態檔案由 `static/` 提供；媒體檔案上傳到 `media/`
- 部署時請確認已正確配置 web server（如 nginx）或使用 WhiteNoise 處理靜態檔

---

## 測試 🧪

執行 Django 內建測試套件：

```powershell
python manage.py test
```

（或在 Docker 中執行 `docker-compose exec web python manage.py test`）

---

## 常見問題（Troubleshooting） ⚠️

- Postgres 連線錯誤：檢查 `SQL_HOST`、`SQL_PORT`、使用者與密碼是否一致
- 靜態檔未載入：確認 `DEBUG` 設為 `True`（開發）或在生產環境收集並提供靜態檔案
- 檔案權限問題：確保 `media/` 與 `static/` 有適當的寫入權限

---

## 想要的擴充（建議） ✨

- 新增 README 中的 API 使用範例或前端介面截圖
- 撰寫單元測試與 CI 設定（GitHub Actions）
- 加入部署流程範例（使用 gunicorn + nginx）

---

## 聯絡 / 貢獻 🙏

歡迎發送 PR 或 issues。在提交 PR 前，請建立議題描述變更內容與目的。

---

> 註：此 README 為初版，若你想加入更細部的 API 文件、架構圖或部署說明，我可以繼續協助展開內容。
