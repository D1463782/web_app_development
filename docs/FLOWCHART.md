# 流程圖設計 — 食譜收藏系統

## 1. 使用者流程圖（User Flow）

以下流程圖描述使用者從進入網站到完成各項操作的完整路徑：

```mermaid
flowchart LR
    A([使用者開啟網頁]) --> B[首頁 - 食譜列表]

    B --> C{要執行什麼操作？}

    %% 新增食譜
    C -->|新增食譜| D[點擊「新增食譜」按鈕]
    D --> E[填寫食譜表單]
    E --> F["輸入食譜名稱與描述"]
    F --> G["輸入材料（名稱、份量）"]
    G --> H["輸入步驟（順序、說明）"]
    H --> I{確認送出？}
    I -->|送出| J[儲存食譜到資料庫]
    J --> B
    I -->|取消| B

    %% 檢視食譜
    C -->|檢視食譜| K[點擊食譜名稱]
    K --> L[食譜詳細頁]
    L --> M["查看材料清單"]
    L --> N["查看步驟清單"]
    L --> O{下一步？}
    O -->|返回列表| B
    O -->|編輯| P[進入編輯模式]
    O -->|刪除| S[顯示刪除確認]

    %% 編輯食譜
    P --> Q[修改食譜內容]
    Q --> R{確認更新？}
    R -->|更新| J2[更新資料庫]
    J2 --> L
    R -->|取消| L

    %% 刪除食譜
    S --> T{確認刪除？}
    T -->|確認| U[從資料庫刪除]
    U --> B
    T -->|取消| L
```

### 流程說明

- **起點**：使用者開啟網頁，進入首頁看到所有食譜列表
- **四條主要路徑**：
  1. **新增** → 填寫表單 → 儲存 → 回到列表
  2. **檢視** → 點擊食譜 → 查看材料與步驟
  3. **編輯** → 從詳細頁進入 → 修改內容 → 更新 → 回到詳細頁
  4. **刪除** → 從詳細頁進入 → 確認刪除 → 回到列表
- **安全機制**：刪除前會顯示確認頁面，避免誤刪

---

## 2. 系統序列圖（Sequence Diagram）

### 2.1 新增食譜

描述使用者新增一筆食譜時，從瀏覽器到資料庫的完整資料流：

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Route as Flask Route
    participant Model as Recipe Model
    participant DB as SQLite

    User->>Browser: 點擊「新增食譜」
    Browser->>Route: GET /recipes/new
    Route-->>Browser: 回傳空白表單頁面

    User->>Browser: 填寫名稱、材料、步驟並送出
    Browser->>Route: POST /recipes
    Route->>Route: 驗證表單資料

    alt 驗證通過
        Route->>Model: create_recipe(name, description)
        Model->>DB: INSERT INTO recipes (name, description)
        DB-->>Model: 回傳新食譜 ID
        Model-->>Route: recipe_id

        Route->>Model: add_ingredients(recipe_id, ingredients)
        Model->>DB: INSERT INTO ingredients (recipe_id, name, quantity)
        DB-->>Model: 成功

        Route->>Model: add_steps(recipe_id, steps)
        Model->>DB: INSERT INTO steps (recipe_id, step_number, description)
        DB-->>Model: 成功

        Route-->>Browser: 302 重導向到 /recipes/{id}
        Browser->>Route: GET /recipes/{id}
        Route->>Model: get_recipe(id)
        Model->>DB: SELECT 食譜 + 材料 + 步驟
        DB-->>Model: 完整資料
        Model-->>Route: recipe 物件
        Route-->>Browser: 食譜詳細頁 HTML
    else 驗證失敗
        Route-->>Browser: 回傳表單頁（附錯誤訊息）
    end
```

### 2.2 瀏覽食譜列表

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Route as Flask Route
    participant Model as Recipe Model
    participant DB as SQLite

    User->>Browser: 開啟首頁
    Browser->>Route: GET /
    Route->>Model: get_all_recipes()
    Model->>DB: SELECT * FROM recipes ORDER BY created_at DESC
    DB-->>Model: 食譜列表資料
    Model-->>Route: recipes 列表
    Route-->>Browser: 首頁 HTML（含食譜列表）
    Browser-->>User: 顯示所有食譜
```

### 2.3 編輯食譜

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Route as Flask Route
    participant Model as Recipe Model
    participant DB as SQLite

    User->>Browser: 點擊「編輯」按鈕
    Browser->>Route: GET /recipes/{id}/edit
    Route->>Model: get_recipe(id)
    Model->>DB: SELECT 食譜 + 材料 + 步驟
    DB-->>Model: 現有資料
    Model-->>Route: recipe 物件
    Route-->>Browser: 預填資料的編輯表單

    User->>Browser: 修改內容並送出
    Browser->>Route: POST /recipes/{id}/edit
    Route->>Model: update_recipe(id, new_data)
    Model->>DB: UPDATE recipes SET ...
    Model->>DB: DELETE + INSERT ingredients
    Model->>DB: DELETE + INSERT steps
    DB-->>Model: 成功
    Model-->>Route: 完成
    Route-->>Browser: 302 重導向到 /recipes/{id}
```

### 2.4 刪除食譜

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Route as Flask Route
    participant Model as Recipe Model
    participant DB as SQLite

    User->>Browser: 點擊「刪除」按鈕
    Browser->>Route: GET /recipes/{id}/delete
    Route->>Model: get_recipe(id)
    Model->>DB: SELECT recipe WHERE id=?
    DB-->>Model: 食譜資料
    Model-->>Route: recipe 物件
    Route-->>Browser: 刪除確認頁

    User->>Browser: 確認刪除
    Browser->>Route: POST /recipes/{id}/delete
    Route->>Model: delete_recipe(id)
    Model->>DB: DELETE FROM steps WHERE recipe_id=?
    Model->>DB: DELETE FROM ingredients WHERE recipe_id=?
    Model->>DB: DELETE FROM recipes WHERE id=?
    DB-->>Model: 成功
    Model-->>Route: 完成
    Route-->>Browser: 302 重導向到 /
```

---

## 3. 功能清單對照表

| 功能 | URL 路徑 | HTTP 方法 | 說明 |
|:---|:---|:---|:---|
| 瀏覽食譜列表 | `/` | GET | 首頁，顯示所有食譜（依建立時間倒序） |
| 新增食譜表單 | `/recipes/new` | GET | 顯示空白的食譜新增表單 |
| 新增食譜送出 | `/recipes` | POST | 接收表單資料，建立新食譜、材料與步驟 |
| 檢視食譜詳情 | `/recipes/<id>` | GET | 顯示單一食譜的完整資訊（材料 + 步驟） |
| 編輯食譜表單 | `/recipes/<id>/edit` | GET | 顯示預填資料的編輯表單 |
| 編輯食譜送出 | `/recipes/<id>/edit` | POST | 接收修改後的資料，更新食譜 |
| 刪除確認頁 | `/recipes/<id>/delete` | GET | 顯示刪除確認頁面 |
| 刪除食譜送出 | `/recipes/<id>/delete` | POST | 確認刪除，移除食譜及其材料與步驟 |
