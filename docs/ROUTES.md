# 路由設計文件 (ROUTES)

根據 PRD 的需求與 FLOWCHART 定義好的流程，以下為本任務管理系統的 Flask 路由與 API 規劃。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| 檢視任務首頁 | GET | `/` | `index.html` | 讀取並顯示全部任務清單，包含新增任務表單 |
| 新增任務操作 | POST | `/tasks/add` | — | 接收並寫入新任務，完成後重導向首頁 `/` |
| 切換完成狀態 | POST | `/tasks/<int:task_id>/toggle` | — | 切換任務的已完成/未完成狀態，重導向首頁 `/` |
| 載入編輯頁面 | GET | `/tasks/<int:task_id>/edit` | `edit.html` | 讀取單筆任務資料，顯示該任務專屬編輯表單 |
| 更新任務操作 | POST | `/tasks/<int:task_id>/edit` | — | 接收編輯表單修正的內容，重導向首頁 `/` |
| 刪除任務 | POST | `/tasks/<int:task_id>/delete` | — | 從資料庫刪除該任務，完成後重導向首頁 `/` |

## 2. 每個路由的詳細說明

### `GET /` (檢視任務首頁)
- **輸入**: 無
- **處理邏輯**: 呼叫 `Task.get_all()` 取得所有任務（排序依據 `created_at` DESC）。
- **輸出**: 渲染 `index.html`，並傳遞 `tasks` 變數供 Jinja2 生成畫面。
- **錯誤處理**: —

### `POST /tasks/add` (新增任務操作)
- **輸入**: 表單傳遞欄位 `title` (字串)、`priority` (字串：高、中、低)。
- **處理邏輯**: 驗證 `title` 是否空白。若無空白則呼叫 `Task.create(title, priority)` 寫入 SQLite。
- **輸出**: 回傳 HTTP 302 重導向 (Redirect) 至首頁 `/`。
- **錯誤處理**: 若 `title` 為空，可使用 flash 回報錯誤訊息並重導至 `/` 讓使用者重填。

### `POST /tasks/<int:task_id>/toggle` (切換完成狀態)
- **輸入**: URL 引數 `task_id`。
- **處理邏輯**: 呼叫 `Task.toggle_status(task_id)` 切換資料庫中的 `is_completed` 狀態。
- **輸出**: HTTP 302 重導向至首頁 `/`。
- **錯誤處理**: 假若找不到該 `task_id`，回傳 404 Not Found。

### `GET /tasks/<int:task_id>/edit` (載入編輯頁面)
- **輸入**: URL 引數 `task_id`。
- **處理邏輯**: 呼叫 `Task.get_by_id(task_id)` 取得欲編輯的任務原始資料。
- **輸出**: 渲染 `edit.html`，並將取得的 `task` 物件傳回版型中做為表單預設值。
- **錯誤處理**: 如果找不到此任務，退回首頁或顯示 404。

### `POST /tasks/<int:task_id>/edit` (更新任務操作)
- **輸入**: URL 引數 `task_id`；表單欄位傳入 `title`、`priority` 與完成狀態選取值。
- **處理邏輯**: 驗證 `title` 若非空值，呼叫 `Task.update(task_id, title, priority, is_completed)` 覆寫資料庫。
- **輸出**: HTTP 302 重導向至首頁 `/`。
- **錯誤處理**: 若 `title` 為空，提示錯誤訊息並導回原原本該編輯頁面 `/tasks/<task_id>/edit`。

### `POST /tasks/<int:task_id>/delete` (刪除任務)
- **輸入**: URL 引數 `task_id`。
- **處理邏輯**: 呼叫 `Task.delete(task_id)` 從 DB 清除指定任務。
- **輸出**: HTTP 302 重導向至首頁 `/`。
- **錯誤處理**: 找不到任務跳轉 404 或直接回歸首頁不處理。

---

## 3. Jinja2 模板清單

所有的視圖模板都會繼承一個共同的基礎模板，確保整站的外觀風格。

| 模板檔名 | 說明 |
| :--- | :--- |
| `base.html` | **網站共同外框**。包含 HTML head 資源設定、主要架構與共用的 CSS/JS 引入。 |
| `index.html` | 繼承自 `base.html`。首頁內容，用於顯示「**新增表單**」與渲染全部 `tasks` 清單列表。 |
| `edit.html` | 繼承自 `base.html`。獨立的編輯畫面，呈現單筆任務包含標題與緊急狀態等參數的修改表單。 |

---

## 4. 路由骨架程式碼

路由的骨架定義在 `app/routes/task_routes.py`，請參閱實際檔案。
