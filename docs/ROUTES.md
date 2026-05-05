# 路由設計 — 食譜收藏系統

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
|:---|:---|:---|:---|:---|
| 食譜列表（首頁） | GET | `/` | `index.html` | 顯示所有食譜列表 |
| 新增食譜頁面 | GET | `/recipes/new` | `recipe_form.html` | 顯示空白新增表單 |
| 建立食譜 | POST | `/recipes` | — | 接收表單，存入 DB，重導向到詳細頁 |
| 食譜詳情 | GET | `/recipes/<id>` | `recipe_detail.html` | 顯示單筆食譜（含材料與步驟） |
| 編輯食譜頁面 | GET | `/recipes/<id>/edit` | `recipe_form.html` | 顯示預填資料的編輯表單 |
| 更新食譜 | POST | `/recipes/<id>/edit` | — | 接收修改資料，更新 DB，重導向到詳細頁 |
| 刪除確認頁面 | GET | `/recipes/<id>/delete` | `confirm_delete.html` | 顯示刪除確認頁 |
| 刪除食譜 | POST | `/recipes/<id>/delete` | — | 刪除食譜，重導向到首頁 |

---

## 2. 每個路由的詳細說明

### 2.1 食譜列表（首頁）

```
GET /
```

| 項目 | 說明 |
|:---|:---|
| **輸入** | 無 |
| **處理邏輯** | 呼叫 `get_all_recipes()` 取得所有食譜 |
| **輸出** | 渲染 `index.html`，傳入 `recipes` 變數 |
| **錯誤處理** | 無特殊處理，空列表正常顯示 |

---

### 2.2 新增食譜頁面

```
GET /recipes/new
```

| 項目 | 說明 |
|:---|:---|
| **輸入** | 無 |
| **處理邏輯** | 無 |
| **輸出** | 渲染 `recipe_form.html`，表單為空白狀態 |
| **錯誤處理** | 無 |

---

### 2.3 建立食譜

```
POST /recipes
```

| 項目 | 說明 |
|:---|:---|
| **輸入** | 表單欄位：`name`（必填）、`description`（選填）、`ingredient_name[]`、`ingredient_quantity[]`、`step_description[]` |
| **處理邏輯** | 1. 驗證 `name` 不為空 → 2. 呼叫 `create_recipe()` → 3. 呼叫 `add_ingredients()` → 4. 呼叫 `add_steps()` |
| **輸出** | 成功：重導向到 `/recipes/<new_id>` |
| **錯誤處理** | `name` 為空 → 重新渲染表單，附上錯誤訊息 |

---

### 2.4 食譜詳情

```
GET /recipes/<id>
```

| 項目 | 說明 |
|:---|:---|
| **輸入** | URL 參數：`id`（整數） |
| **處理邏輯** | 呼叫 `get_recipe_by_id()`、`get_ingredients_by_recipe()`、`get_steps_by_recipe()` |
| **輸出** | 渲染 `recipe_detail.html`，傳入 `recipe`、`ingredients`、`steps` |
| **錯誤處理** | 食譜不存在 → 回傳 404 頁面 |

---

### 2.5 編輯食譜頁面

```
GET /recipes/<id>/edit
```

| 項目 | 說明 |
|:---|:---|
| **輸入** | URL 參數：`id`（整數） |
| **處理邏輯** | 呼叫 `get_recipe_by_id()`、`get_ingredients_by_recipe()`、`get_steps_by_recipe()` |
| **輸出** | 渲染 `recipe_form.html`，表單預填現有資料 |
| **錯誤處理** | 食譜不存在 → 回傳 404 頁面 |

---

### 2.6 更新食譜

```
POST /recipes/<id>/edit
```

| 項目 | 說明 |
|:---|:---|
| **輸入** | URL 參數：`id`（整數）、表單欄位同新增 |
| **處理邏輯** | 1. 驗證 `name` 不為空 → 2. 呼叫 `update_recipe()` → 3. `delete_ingredients_by_recipe()` + `add_ingredients()` → 4. `delete_steps_by_recipe()` + `add_steps()` |
| **輸出** | 成功：重導向到 `/recipes/<id>` |
| **錯誤處理** | 食譜不存在 → 404；`name` 為空 → 重新渲染表單附錯誤訊息 |

---

### 2.7 刪除確認頁面

```
GET /recipes/<id>/delete
```

| 項目 | 說明 |
|:---|:---|
| **輸入** | URL 參數：`id`（整數） |
| **處理邏輯** | 呼叫 `get_recipe_by_id()` 取得食譜名稱供確認 |
| **輸出** | 渲染 `confirm_delete.html`，顯示食譜名稱與確認按鈕 |
| **錯誤處理** | 食譜不存在 → 回傳 404 頁面 |

---

### 2.8 刪除食譜

```
POST /recipes/<id>/delete
```

| 項目 | 說明 |
|:---|:---|
| **輸入** | URL 參數：`id`（整數） |
| **處理邏輯** | 呼叫 `delete_recipe()`（CASCADE 自動刪除材料與步驟） |
| **輸出** | 重導向到 `/` |
| **錯誤處理** | 食譜不存在 → 回傳 404 頁面 |

---

## 3. Jinja2 模板清單

| 模板檔案 | 繼承自 | 用途 |
|:---|:---|:---|
| `base.html` | — | 基礎模板：HTML 結構、`<head>`、導覽列、`<footer>`、CSS/JS 引入 |
| `index.html` | `base.html` | 首頁：食譜列表，含新增按鈕 |
| `recipe_detail.html` | `base.html` | 食譜詳細頁：名稱、描述、材料清單、步驟清單、編輯/刪除按鈕 |
| `recipe_form.html` | `base.html` | 新增/編輯共用表單：食譜名稱、描述、動態材料欄位、動態步驟欄位 |
| `confirm_delete.html` | `base.html` | 刪除確認頁：顯示食譜名稱、確認/取消按鈕 |

### 模板繼承結構

```
base.html
├── index.html
├── recipe_detail.html
├── recipe_form.html
└── confirm_delete.html
```

### 模板中的區塊（Block）設計

```html
<!-- base.html 定義的區塊 -->
{% block title %}食譜收藏夾{% endblock %}
{% block content %}{% endblock %}
```
