import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask (__name__)

app.config["MONGO_DBNAME"] = "RecipeBook"
app.config["MONGO_URI"] = 'mongodb+srv://root:r00tUser@recipecluster-t7ztj.mongodb.net/RecipeBook?retryWrites=true'

mongo = PyMongo(app)

# Landing page + view recipe list
@app.route('/')
@app.route('/recipes')
def get_recipes():
    return render_template("recipes.html", result=mongo.db.recipe.find().limit(5))

@app.route('/recipes_next')    
def get_next():
    return render_template("recipes.html", result=mongo.db.recipe.find().skip(5).limit(5))

# add recipes + insert function    
@app.route('/addrecipe')
def add_recipe():
    return render_template("addrecipe.html")
    
@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipe=mongo.db.recipe
    recipe.insert_one(request.form.to_dict())
    return redirect(url_for('get_recipes'))

# edit function
@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    the_recipe = mongo.db.recipe.find_one({"_id" : ObjectId(recipe_id)})
    all_categories = mongo.db.categories.find()
    return render_template('editrecipe.html', recipe=the_recipe, categories=all_categories)

# Update function
@app.route('/update_recipe/<recipe_id>', methods=["POST"])
def update_recipe(recipe_id):
    recipe=mongo.db.recipe
    recipe.update({"_id" : ObjectId(recipe_id)},
    {
        'recipe_name' : request.form.get('recipe_name'),
        'user' : request.form.get('user'),
        'cuisine' : request.form.get('cuisine'),
        'category' : request.form.get('category'),
        'ingredients' : request.form.get('ingredients'),
        'timing' : request.form.get('timing'),
        'method' : request.form.get('method'),
    })
    return redirect(url_for('get_recipes'))

# Delete function  
@app.route('/delete_recipe<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipe.remove({"_id" : ObjectId(recipe_id)})
    return redirect(url_for('get_recipes'))
    
# View single reipe. Includes view counter update. 
@app.route('/view_recipe<recipe_id>')
def view_recipe(recipe_id):
    the_recipe = mongo.db.recipe.find_one({"_id" : ObjectId(recipe_id)})
    all_categories = mongo.db.categories.find()
    return render_template('view_recipe.html', recipe=the_recipe, categories=all_categories)
   

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)


                            
