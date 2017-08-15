from flask import Blueprint, render_template, request, flash, redirect, json, url_for
from src.common.database import Database
from src.models.stores.store import Store
import src.models.stores.constants as StoreConstants
import src.models.users.decorators as user_decorators

store_blueprint = Blueprint('stores', __name__)

@store_blueprint.route('/')
def index():
    stores = Store.all()
    return render_template('/stores/store_index.html', stores=stores)

@store_blueprint.route('/store/<string:store_id>')
def store_page(store_id):
    return render_template('/stores/store.html', store=Store.get_by_id(store_id))

@store_blueprint.route('/new', methods=['GET', 'POST'])
@user_decorators.is_admin
def create_store():
    if request.method == 'POST':
        name = request.form['name']
        url_prefix = request.form['url_prefix']
        tag_name = request.form['tag_name']
        query = json.loads(request.form['query'])

        store = Store(name, url_prefix, tag_name, query)
        store.save_to_mongo()
        flash("Store {} successfully added.".format(name))
        return redirect(url_for('.index'))

    return render_template('/stores/create_store.html')

@store_blueprint.route('/edit/<string:store_id>', methods=['GET', 'POST'])
@user_decorators.is_admin
def edit_store(store_id):
    if request.method == 'POST':
        store = Store.get_by_id(store_id)
        store.name = request.form['name']
        store.url_prefix = request.form['url_prefix']
        store.tag_name = request.form['tag_name']
        store.query =  json.loads(request.form['query'])

        store.save_to_mongo()

        flash("Store {} successfully updated.".format(store_id))
        return redirect(url_for('.index'))

    return render_template('/stores/edit_store.html', store=Store.get_by_id(store_id))

@store_blueprint.route('/delete/<string:store_id>')
@user_decorators.is_admin
def delete_store(store_id):
    Store.get_by_id(store_id).remove()
    flash("Store with ID: {} successfully deleted.".format(store_id))
    return redirect(url_for('.index'))