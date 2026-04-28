"""
食譜收藏系統 — Recipe Model

使用原生 sqlite3 操作資料庫，提供食譜、材料、步驟的 CRUD 方法。
"""

import sqlite3
from datetime import datetime


def get_db(db_path):
    """
    取得資料庫連線。

    Args:
        db_path (str): SQLite 資料庫檔案路徑

    Returns:
        sqlite3.Connection: 資料庫連線物件
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # 讓查詢結果可以用欄位名稱存取
    conn.execute("PRAGMA foreign_keys = ON")  # 啟用外鍵約束
    return conn


# ============================================
# 食譜（Recipe）CRUD
# ============================================

def create_recipe(db_path, name, description=""):
    """
    新增一筆食譜。

    Args:
        db_path (str): 資料庫路徑
        name (str): 食譜名稱
        description (str): 食譜描述（選填）

    Returns:
        int: 新建食譜的 ID
    """
    conn = get_db(db_path)
    try:
        cursor = conn.execute(
            "INSERT INTO recipes (name, description) VALUES (?, ?)",
            (name, description)
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def get_all_recipes(db_path):
    """
    取得所有食譜列表（依建立時間倒序排列）。

    Args:
        db_path (str): 資料庫路徑

    Returns:
        list[sqlite3.Row]: 食譜列表
    """
    conn = get_db(db_path)
    try:
        recipes = conn.execute(
            "SELECT * FROM recipes ORDER BY created_at DESC"
        ).fetchall()
        return recipes
    finally:
        conn.close()


def get_recipe_by_id(db_path, recipe_id):
    """
    根據 ID 取得單一食譜。

    Args:
        db_path (str): 資料庫路徑
        recipe_id (int): 食譜 ID

    Returns:
        sqlite3.Row or None: 食譜資料，找不到時回傳 None
    """
    conn = get_db(db_path)
    try:
        recipe = conn.execute(
            "SELECT * FROM recipes WHERE id = ?",
            (recipe_id,)
        ).fetchone()
        return recipe
    finally:
        conn.close()


def update_recipe(db_path, recipe_id, name, description=""):
    """
    更新食譜的基本資訊。

    Args:
        db_path (str): 資料庫路徑
        recipe_id (int): 食譜 ID
        name (str): 新的食譜名稱
        description (str): 新的食譜描述
    """
    now = datetime.now().isoformat(timespec='seconds')
    conn = get_db(db_path)
    try:
        conn.execute(
            "UPDATE recipes SET name = ?, description = ?, updated_at = ? WHERE id = ?",
            (name, description, now, recipe_id)
        )
        conn.commit()
    finally:
        conn.close()


def delete_recipe(db_path, recipe_id):
    """
    刪除食譜（CASCADE 會自動刪除相關的材料與步驟）。

    Args:
        db_path (str): 資料庫路徑
        recipe_id (int): 食譜 ID
    """
    conn = get_db(db_path)
    try:
        conn.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
        conn.commit()
    finally:
        conn.close()


# ============================================
# 材料（Ingredient）CRUD
# ============================================

def add_ingredients(db_path, recipe_id, ingredients):
    """
    為食譜新增多筆材料。

    Args:
        db_path (str): 資料庫路徑
        recipe_id (int): 食譜 ID
        ingredients (list[dict]): 材料列表，每項需包含 'name'，可選 'quantity'
            範例：[{'name': '雞蛋', 'quantity': '3顆'}, {'name': '鹽', 'quantity': '適量'}]
    """
    conn = get_db(db_path)
    try:
        for item in ingredients:
            conn.execute(
                "INSERT INTO ingredients (recipe_id, name, quantity) VALUES (?, ?, ?)",
                (recipe_id, item['name'], item.get('quantity', ''))
            )
        conn.commit()
    finally:
        conn.close()


def get_ingredients_by_recipe(db_path, recipe_id):
    """
    取得某食譜的所有材料。

    Args:
        db_path (str): 資料庫路徑
        recipe_id (int): 食譜 ID

    Returns:
        list[sqlite3.Row]: 材料列表
    """
    conn = get_db(db_path)
    try:
        ingredients = conn.execute(
            "SELECT * FROM ingredients WHERE recipe_id = ?",
            (recipe_id,)
        ).fetchall()
        return ingredients
    finally:
        conn.close()


def delete_ingredients_by_recipe(db_path, recipe_id):
    """
    刪除某食譜的所有材料（用於編輯時先清除再重新新增）。

    Args:
        db_path (str): 資料庫路徑
        recipe_id (int): 食譜 ID
    """
    conn = get_db(db_path)
    try:
        conn.execute(
            "DELETE FROM ingredients WHERE recipe_id = ?",
            (recipe_id,)
        )
        conn.commit()
    finally:
        conn.close()


# ============================================
# 步驟（Step）CRUD
# ============================================

def add_steps(db_path, recipe_id, steps):
    """
    為食譜新增多筆步驟。

    Args:
        db_path (str): 資料庫路徑
        recipe_id (int): 食譜 ID
        steps (list[dict]): 步驟列表，每項需包含 'step_number' 和 'description'
            範例：[{'step_number': 1, 'description': '打蛋'}, {'step_number': 2, 'description': '熱鍋'}]
    """
    conn = get_db(db_path)
    try:
        for step in steps:
            conn.execute(
                "INSERT INTO steps (recipe_id, step_number, description) VALUES (?, ?, ?)",
                (recipe_id, step['step_number'], step['description'])
            )
        conn.commit()
    finally:
        conn.close()


def get_steps_by_recipe(db_path, recipe_id):
    """
    取得某食譜的所有步驟（依步驟編號排序）。

    Args:
        db_path (str): 資料庫路徑
        recipe_id (int): 食譜 ID

    Returns:
        list[sqlite3.Row]: 步驟列表（已按 step_number 排序）
    """
    conn = get_db(db_path)
    try:
        steps = conn.execute(
            "SELECT * FROM steps WHERE recipe_id = ? ORDER BY step_number ASC",
            (recipe_id,)
        ).fetchall()
        return steps
    finally:
        conn.close()


def delete_steps_by_recipe(db_path, recipe_id):
    """
    刪除某食譜的所有步驟（用於編輯時先清除再重新新增）。

    Args:
        db_path (str): 資料庫路徑
        recipe_id (int): 食譜 ID
    """
    conn = get_db(db_path)
    try:
        conn.execute(
            "DELETE FROM steps WHERE recipe_id = ?",
            (recipe_id,)
        )
        conn.commit()
    finally:
        conn.close()
