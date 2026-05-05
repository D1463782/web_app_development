from flask import Blueprint, render_template, request, redirect, url_for

# 建立 Blueprint，命名為 recipe
recipe_bp = Blueprint('recipe', __name__)

@recipe_bp.route('/')
def index():
    """
    食譜列表（首頁）
    
    處理邏輯：
    - 呼叫 get_all_recipes() 取得所有食譜
    - 渲染 index.html，傳入 recipes 變數
    """
    pass

@recipe_bp.route('/recipes/new', methods=['GET'])
def new_recipe():
    """
    新增食譜頁面
    
    處理邏輯：
    - 渲染 recipe_form.html，表單為空白狀態
    """
    pass

@recipe_bp.route('/recipes', methods=['POST'])
def create_recipe():
    """
    建立食譜
    
    處理邏輯：
    - 驗證 name 不為空
    - 呼叫 create_recipe() 寫入食譜表
    - 呼叫 add_ingredients() 寫入材料表
    - 呼叫 add_steps() 寫入步驟表
    - 成功後重導向到 /recipes/<new_id>
    """
    pass

@recipe_bp.route('/recipes/<int:id>', methods=['GET'])
def recipe_detail(id):
    """
    食譜詳情
    
    處理邏輯：
    - 呼叫 get_recipe_by_id() 取得基本資料
    - 呼叫 get_ingredients_by_recipe() 取得材料
    - 呼叫 get_steps_by_recipe() 取得步驟
    - 渲染 recipe_detail.html
    """
    pass

@recipe_bp.route('/recipes/<int:id>/edit', methods=['GET'])
def edit_recipe(id):
    """
    編輯食譜頁面
    
    處理邏輯：
    - 呼叫 get_recipe_by_id() 取得基本資料
    - 呼叫 get_ingredients_by_recipe() 取得材料
    - 呼叫 get_steps_by_recipe() 取得步驟
    - 渲染 recipe_form.html，表單預填現有資料
    """
    pass

@recipe_bp.route('/recipes/<int:id>/edit', methods=['POST'])
def update_recipe_action(id):
    """
    更新食譜
    
    處理邏輯：
    - 驗證 name 不為空
    - 呼叫 update_recipe() 更新基本資料
    - 刪除舊材料並新增新材料 (add_ingredients)
    - 刪除舊步驟並新增新步驟 (add_steps)
    - 成功後重導向到 /recipes/<id>
    """
    pass

@recipe_bp.route('/recipes/<int:id>/delete', methods=['GET'])
def confirm_delete_recipe(id):
    """
    刪除確認頁面
    
    處理邏輯：
    - 呼叫 get_recipe_by_id() 取得食譜名稱供確認
    - 渲染 confirm_delete.html
    """
    pass

@recipe_bp.route('/recipes/<int:id>/delete', methods=['POST'])
def delete_recipe_action(id):
    """
    刪除食譜
    
    處理邏輯：
    - 呼叫 delete_recipe() (SQLite CASCADE 會自動刪除關聯的材料與步驟)
    - 成功後重導向到首頁 (/)
    """
    pass
