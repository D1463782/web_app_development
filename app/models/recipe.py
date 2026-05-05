import sqlite3
import os
from flask import current_app

def get_db_connection():
    """
    建立並回傳與 SQLite 資料庫的連線。
    預設使用 app 設定的 DATABASE 路徑，若無 app context 則退回到 instance/database.db
    """
    try:
        db_path = current_app.config['DATABASE']
    except (RuntimeError, KeyError):
        # 當不在 app context 內，或是沒有 DATABASE 設定時的退回機制
        db_path = os.path.join('instance', 'database.db')
        
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    # 啟用外鍵支援，讓 ON DELETE CASCADE 生效
    conn.execute('PRAGMA foreign_keys = ON;')
    return conn

# ==========================================
# Recipe (食譜) 相關操作
# ==========================================

def get_all_recipes():
    """取得所有食譜，按建立時間反序排列"""
    try:
        conn = get_db_connection()
        recipes = conn.execute('SELECT * FROM recipes ORDER BY created_at DESC').fetchall()
        conn.close()
        return recipes
    except sqlite3.Error as e:
        print(f"Database error in get_all_recipes: {e}")
        return []

def get_recipe_by_id(recipe_id):
    """根據 ID 取得單筆食譜"""
    try:
        conn = get_db_connection()
        recipe = conn.execute('SELECT * FROM recipes WHERE id = ?', (recipe_id,)).fetchone()
        conn.close()
        return recipe
    except sqlite3.Error as e:
        print(f"Database error in get_recipe_by_id: {e}")
        return None

def create_recipe(name, description):
    """
    新增一筆食譜
    :param name: 食譜名稱
    :param description: 食譜描述
    :return: 新增的食譜 ID，若失敗則回傳 None
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO recipes (name, description) VALUES (?, ?)',
            (name, description)
        )
        recipe_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return recipe_id
    except sqlite3.Error as e:
        print(f"Database error in create_recipe: {e}")
        return None

def update_recipe(recipe_id, name, description):
    """
    更新食譜基本資料
    :param recipe_id: 食譜 ID
    :param name: 食譜名稱
    :param description: 食譜描述
    """
    try:
        conn = get_db_connection()
        conn.execute(
            'UPDATE recipes SET name = ?, description = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
            (name, description, recipe_id)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Database error in update_recipe: {e}")
        return False

def delete_recipe(recipe_id):
    """
    刪除食譜（SQLite CASCADE 會自動刪除相關的材料與步驟）
    :param recipe_id: 食譜 ID
    """
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM recipes WHERE id = ?', (recipe_id,))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Database error in delete_recipe: {e}")
        return False

# ==========================================
# Ingredients (材料) 相關操作
# ==========================================

def get_ingredients_by_recipe(recipe_id):
    """取得特定食譜的所有材料"""
    try:
        conn = get_db_connection()
        ingredients = conn.execute('SELECT * FROM ingredients WHERE recipe_id = ?', (recipe_id,)).fetchall()
        conn.close()
        return ingredients
    except sqlite3.Error as e:
        print(f"Database error in get_ingredients_by_recipe: {e}")
        return []

def add_ingredients(recipe_id, ingredients_data):
    """
    新增材料清單到特定食譜
    :param recipe_id: 食譜 ID
    :param ingredients_data: 材料清單，格式為 [{'name': '...', 'quantity': '...'}, ...]
    """
    try:
        conn = get_db_connection()
        for item in ingredients_data:
            if item.get('name') and item['name'].strip():  # 確保材料名稱存在
                conn.execute(
                    'INSERT INTO ingredients (recipe_id, name, quantity) VALUES (?, ?, ?)',
                    (recipe_id, item['name'].strip(), item.get('quantity', '').strip())
                )
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Database error in add_ingredients: {e}")
        return False

def delete_ingredients_by_recipe(recipe_id):
    """刪除特定食譜的所有材料（更新時使用）"""
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM ingredients WHERE recipe_id = ?', (recipe_id,))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Database error in delete_ingredients_by_recipe: {e}")
        return False

# ==========================================
# Steps (步驟) 相關操作
# ==========================================

def get_steps_by_recipe(recipe_id):
    """取得特定食譜的所有步驟，依順序排列"""
    try:
        conn = get_db_connection()
        steps = conn.execute('SELECT * FROM steps WHERE recipe_id = ? ORDER BY step_number ASC', (recipe_id,)).fetchall()
        conn.close()
        return steps
    except sqlite3.Error as e:
        print(f"Database error in get_steps_by_recipe: {e}")
        return []

def add_steps(recipe_id, steps_data):
    """
    新增步驟清單到特定食譜
    :param recipe_id: 食譜 ID
    :param steps_data: 步驟字串清單，格式為 ['切菜', '下鍋炒', ...]
    """
    try:
        conn = get_db_connection()
        for i, desc in enumerate(steps_data):
            if desc and desc.strip():  # 確保步驟不為空
                conn.execute(
                    'INSERT INTO steps (recipe_id, step_number, description) VALUES (?, ?, ?)',
                    (recipe_id, i + 1, desc.strip())
                )
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Database error in add_steps: {e}")
        return False

def delete_steps_by_recipe(recipe_id):
    """刪除特定食譜的所有步驟（更新時使用）"""
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM steps WHERE recipe_id = ?', (recipe_id,))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Database error in delete_steps_by_recipe: {e}")
        return False
