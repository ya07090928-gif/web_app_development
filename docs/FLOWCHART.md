# 流程圖文件 (FLOWCHART)

根據我們定義的專案需求 (PRD) 與系統架構 (ARCHITECTURE)，本文件描繪了使用者在系統中的操作路線，以及在特定操作下系統背後的資料流動情形。

---

## 1. 使用者流程圖 (User Flow)

此流程圖展示出目標用戶（大學生）進入任務管理系統後，他們可以進行的各項操作路徑。由於我們採用了**回歸首頁設計**(PRG模式)，各項操作完成後，系統都會引導用戶回到「任務列表首頁」，讓體驗流暢且維持單一的進度檢視點。

```mermaid
flowchart TD
    A([使用者開啟網頁]) --> B[首頁 - 任務清單]
    
    B --> C{想執行什麼操作？}
    
    C -->|新增任務| D[在首頁上方的表單輸入任務內容與重要性]
    D --> E[點擊「新增」]
    E --> F([系統儲存回到首頁])
    F --> B
    
    C -->|標記完成| G[點選特定任務旁邊的「完成」按鈕]
    G --> H([系統更新狀態回到首頁])
    H --> B
    
    C -->|編輯任務| I[點擊特定任務的「編輯」]
    I --> J[跳轉至編輯頁面]
    J --> K[修改任務名稱或重要度，並點選「儲存」]
    K --> L([系統更新資料回到首頁])
    L --> B
    J -.取消.- B
    
    C -->|刪除任務| M[點擊特定任務的「刪除」]
    M --> N{系統跳出確認對話框}
    N -->|確認| O([系統刪除資料回到首頁])
    O --> B
    N -->|取消| B
```

---

## 2. 系統序列圖 (Sequence Diagram)

此序列圖以核心功能「**新增任務**」為例，展現從使用者在瀏覽器送出表單開始，經由 Flask 路由、資料庫寫入，直到重新渲染 (Post-Redirect-Get) 畫面的系統內部運作流程。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 使用者瀏覽器
    participant Route as Flask Router (路由)
    participant Model as Task Model (邏輯模型)
    participant DB as SQLite (資料庫)
    
    User->>Browser: 在表單填寫新任務並點擊送出
    Browser->>Route: 發送 POST /tasks/add (挾帶表單資料)
    
    Route->>Model: 呼叫新增任務函數，傳入資料
    Model->>DB: 執行 SQL: INSERT INTO tasks ...
    DB-->>Model: 寫入成功
    Model-->>Route: 任務新增完成，回傳成功訊號
    
    Route-->>Browser: 回傳 HTTP 302 Redirect (重導向至首頁 "/")
    
    Note over Browser,Route: (進入 PRG 模式的 GET 流程)
    Browser->>Route: 發送 GET / (請求首頁與最新內容)
    Route->>Model: 呼叫取得所有任務函數
    Model->>DB: 執行 SQL: SELECT * FROM tasks
    DB-->>Model: 回傳任務清單資料
    Model-->>Route: 準備好的任務 Python 物件清單
    Route->>Browser: 透過 Jinja2 渲染 index.html 並回傳
    Browser->>User: 顯示已包含新任務的最新頁面
```

---

## 3. 功能清單對照表

做為之後撰寫程式及設計資料庫 API 的依據，這是本系統將要實作的所有功能與其對應的 URL 設計規範。

| 功能描述 | HTTP 方法 | URL 路徑 (Route) | 動作 / 說明 |
| :--- | :--- | :--- | :--- |
| **檢視任務首頁** | `GET` | `/` | 讀取全部任務清單並渲染首頁 `index.html`。 |
| **新增任務操作** | `POST` | `/tasks/add` | 接收表單傳來的名稱與重要性，寫入後重導向 `/`。 |
| **標記/切換完成狀態** | `POST` | `/tasks/<int:task_id>/toggle` | 更新目標任務是否完成的狀態，完成後重導向 `/`。 |
| **載入編輯任務頁面** | `GET` | `/tasks/<int:task_id>/edit` | 尋找目標任務並渲染專屬的編輯表單頁面 `edit.html`。 |
| **送出編輯更新任務** | `POST` | `/tasks/<int:task_id>/edit` | 接收更新後的表單資料覆寫任務內容，完成後重導向 `/`。 |
| **刪除任務操作** | `POST` | `/tasks/<int:task_id>/delete` | 直接把目標任務從資料庫刪除，完成後重導向 `/`。 |

> **提示：** 修改（除了載入表單）、狀態切換、刪除等行為皆設計為 `POST` 方法，以防禦 CSRF 攻擊及預防瀏覽器因預載（Preload）而產生非預期的資料庫更動。
