# -*- coding: utf-8 -*-

#/ usually written in app.py 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
import MeCab as mecab

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/applicot'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
#./ usually written in app.py


# / should be in models.py
class Project(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(120))
	category_name = db.Column(db.String(120))

	def __init__(self,name,category_name):
		self.name = name
		self.category_name = category_name

	def __repr__(self):
		return '<Project name={name} category_name={category_name}>'.format(name=self.name, category_name=self.category_name)


class Node(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), nullable = False)
	parent_id = db.Column(db.Integer, nullable=False)

	project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

	def __init__(self, name, parent_id, project_id):
		self.name = name
		self.parent_id = parent_id
		self.project_id = project_id

	def __repr__(self):
		return '<Node name={name} parent_id={parent_id} project_id={project_id}>'.format(name = self.name, parent_id = self.parent_id, project_id = self.project_id) 

# ./ should be in models.py

#""" データベースに入れるところ書いておく

proj = Project('3-proj', '3-cat')

#"""


# ここからindex : method とかを定義していく。

@app.route('/')
def index():
	proj_obj = Project.query.all()
	proj_list = []
	for i in proj_obj:
		cont = {'id': i.id, 'name': i.name, 'category_name': i.category_name}
		proj_list.append(cont)

	return jsonify(Project=proj_list)

@app.route('/create')
def create_project():

	return "新しいProjectの作成"

@app.route('/delete')
def delete_project(project_id):
	return "Projectの削除をする"


#brain_storming部分の画面
@app.route('/project/<project_id>')
def brain_storming(project_id):
	return "Brain Storming"


@app.route('/project/update')
def update_node(project_id):
	return "update node"

@app.route('/morphologic')
def extractKeyword(text):
	#textを形態素解析して、名詞・動詞のみのリストを返す
	tagger = mecab.Tagger("-Ochasen")
	node = tagger.parseToNode(text.encode('utf-8'))
	keywords = []
	while node:
		if node.feature.split(",")[0].decode('utf-8') == u'名詞':
			keywords.append(node.surface)
		elif node.feature.split(",")[0].decode('utf-8') == u'動詞':
			keywords.append(node.feature.split(",")[6])
		node = node.next
	return jsonify(keywords= keywords)


if __name__ == '__main__':
    app.run()
