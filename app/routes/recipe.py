from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.recipe import (
    get_all_recipes,
    get_recipe_by_id,
    create_recipe as db_create_recipe,
    update_recipe as db_update_recipe,
    delete_recipe as db_delete_recipe,
    get_ingredients_by_recipe,
    add_ingredients,
    delete_ingredients_by_recipe,
    get_steps_by_recipe,
    add_steps,
    delete_steps_by_recipe
)

# 建立 Blueprint，命名為 recipe
recipe_bp = Blueprint('recipe', __name__)

@recipe_bp.route('/')
def index():
    """食譜列表（首頁）"""
    recipes = get_all_recipes()
    return render_template('index.html', recipes=recipes)

@recipe_bp.route('/recipes/new', methods=['GET'])
def new_recipe():
    """新增食譜頁面"""
    return render_template('recipe_form.html')

@recipe_bp.route('/recipes', methods=['POST'])
def create_recipe():
    """建立食譜"""
    name = request.form.get('name')
    description = request.form.get('description', '')
    
    if not name or not name.strip():
        flash('食譜名稱為必填項目', 'error')
        return render_template('recipe_form.html', name=name, description=description)
        
    recipe_id = db_create_recipe(name.strip(), description.strip())
    
    if recipe_id:
        # 處理材料
        ingredient_names = request.form.getlist('ingredient_name[]')
        ingredient_quantities = request.form.getlist('ingredient_quantity[]')
        ingredients_data = [
            {'name': n, 'quantity': q} 
            for n, q in zip(ingredient_names, ingredient_quantities) if n.strip()
        ]
        if ingredients_data:
            add_ingredients(recipe_id, ingredients_data)
        
        # 處理步驟
        step_descriptions = request.form.getlist('step_description[]')
        if step_descriptions:
            add_steps(recipe_id, step_descriptions)
        
        flash('食譜建立成功！', 'success')
        return redirect(url_for('recipe.recipe_detail', id=recipe_id))
    else:
        flash('建立食譜時發生錯誤', 'error')
        return render_template('recipe_form.html', name=name, description=description)

@recipe_bp.route('/recipes/<int:id>', methods=['GET'])
def recipe_detail(id):
    """食譜詳情"""
    recipe = get_recipe_by_id(id)
    if not recipe:
        flash('找不到該食譜', 'error')
        return redirect(url_for('recipe.index'))
        
    ingredients = get_ingredients_by_recipe(id)
    steps = get_steps_by_recipe(id)
    return render_template('recipe_detail.html', recipe=recipe, ingredients=ingredients, steps=steps)

@recipe_bp.route('/recipes/<int:id>/edit', methods=['GET'])
def edit_recipe(id):
    """編輯食譜頁面"""
    recipe = get_recipe_by_id(id)
    if not recipe:
        flash('找不到該食譜', 'error')
        return redirect(url_for('recipe.index'))
        
    ingredients = get_ingredients_by_recipe(id)
    steps = get_steps_by_recipe(id)
    return render_template('recipe_form.html', recipe=recipe, ingredients=ingredients, steps=steps)

@recipe_bp.route('/recipes/<int:id>/edit', methods=['POST'])
def update_recipe_action(id):
    """更新食譜"""
    recipe = get_recipe_by_id(id)
    if not recipe:
        flash('找不到該食譜', 'error')
        return redirect(url_for('recipe.index'))

    name = request.form.get('name')
    description = request.form.get('description', '')
    
    if not name or not name.strip():
        flash('食譜名稱為必填項目', 'error')
        ingredients = get_ingredients_by_recipe(id)
        steps = get_steps_by_recipe(id)
        # 把使用者輸入的暫存下來，避免使用者重新填寫
        recipe_temp = {'id': id, 'name': name, 'description': description}
        return render_template('recipe_form.html', recipe=recipe_temp, ingredients=ingredients, steps=steps)
        
    success = db_update_recipe(id, name.strip(), description.strip())
    
    if success:
        # 更新材料：先刪除再新增
        delete_ingredients_by_recipe(id)
        ingredient_names = request.form.getlist('ingredient_name[]')
        ingredient_quantities = request.form.getlist('ingredient_quantity[]')
        ingredients_data = [
            {'name': n, 'quantity': q} 
            for n, q in zip(ingredient_names, ingredient_quantities) if n.strip()
        ]
        if ingredients_data:
            add_ingredients(id, ingredients_data)
        
        # 更新步驟：先刪除再新增
        delete_steps_by_recipe(id)
        step_descriptions = request.form.getlist('step_description[]')
        if step_descriptions:
            add_steps(id, step_descriptions)
        
        flash('食譜更新成功！', 'success')
        return redirect(url_for('recipe.recipe_detail', id=id))
    else:
        flash('更新食譜時發生錯誤', 'error')
        return redirect(url_for('recipe.edit_recipe', id=id))

@recipe_bp.route('/recipes/<int:id>/delete', methods=['GET'])
def confirm_delete_recipe(id):
    """刪除確認頁面"""
    recipe = get_recipe_by_id(id)
    if not recipe:
        flash('找不到該食譜', 'error')
        return redirect(url_for('recipe.index'))
        
    return render_template('confirm_delete.html', recipe=recipe)

@recipe_bp.route('/recipes/<int:id>/delete', methods=['POST'])
def delete_recipe_action(id):
    """刪除食譜"""
    success = db_delete_recipe(id)
    if success:
        flash('食譜已成功刪除', 'success')
    else:
        flash('刪除食譜時發生錯誤', 'error')
        
    return redirect(url_for('recipe.index'))
