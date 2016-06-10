# -*- coding: utf-8 -*-

#/ usually written in app.py 
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
import MeCab as mecab
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/applicot'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
#./ usually written in app.py


# / should be in models.py
class Project(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(120), unique=True)

	def __init__(self,name):
		self.name = name

	def __repr__(self):
		return '<Project id={id} name={name}>'.format(id = self.id, name=self.name)


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


# ここからindex : method とかを定義していく。

@app.route('/api')
def index():
	proj_obj = Project.query.all()
	proj_list = []
	for i in proj_obj:
		cont = {'id': i.id, 'name': i.name}
		proj_list.append(cont)

	return jsonify(Project=proj_list)

@app.route('/api/create', methods=['POST'])
def create_project():
    data = json.loads(request.json['data'])
    project_name = data['name']
    theme = data['theme']
    new_proj = Project(data['name'])

    db.session.add(new_proj)
    result = {}
    try:
        db.session.commit()
        db.session.flush(new_proj)
        print(new_proj.id)
        result.update({'result':'success', 'project_id':new_proj.id})
    except:
        result.update({'result':'fail', 'msg':u'同じ名前のプロジェクト名があります。'})
    return jsonify(Result=result)

@app.route('/api/delete')
def delete_project(project_id):
	return "Projectの削除をする"


#brain_storming部分の画面
@app.route('/api/project/<project_id>')
def brain_storming(project_id):
	return "Brain Storming"


@app.route('/api/project/update')
def update_node(project_id):
	return "update node"

@app.route('/api/morphologic', methods=['POST'])
def extractKeyword():
    text = request.json[u'text']
    tagger = mecab.Tagger("-Ochasen")
    node = tagger.parseToNode(text.encode('utf-8'))
    keywords = []
    while node:
        if node.feature.split(",")[0].decode('utf-8') == u'名詞':
            keywords.append(node.surface)
        elif node.feature.split(",")[0].decode('utf-8') == u'動詞':
            keywords.append(node.feature.split(",")[6])
        node = node.next
    return jsonify(keywords=keywords)


if __name__ == '__main__':
    app.run()
