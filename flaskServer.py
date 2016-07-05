# -*- coding: utf-8 -*-

#/ usually written in app.py
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
import MeCab as mecab
import json
from sqlalchemy.orm import relationship
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/applicot'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
#./ usually written in app.py

# / modified model

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120),unique=True)
    created_at = db.Column(db.DateTime, nullable=False, default = datetime.now())
    family = db.relationship('Family', backref=db.backref('projects', lazy='immediate', ))
    node = db.relationship('Node', backref=db.backref('projects'), lazy='immediate',)

    def __init__(self,**kwargs):
        self.name = kwargs['name']

    def __repr__(self):
        return '<Project %r %r %r>' % (self.id, self.name, self.created_at)

class Family(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique =True)
    nodes = db.Column(db.String(255),)

    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.nodes = kwargs['nodes']
        self.project_id = kwargs['project_id']

    def __repr__(self):
        return '<Family id={id} name={name} nodes={nodes} protject_id={project_id} >'.format(id=self.id, name=self.name, nodes=self.nodes, project_id=self.project_id)
    
class Node(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    parent_name = db.Column(db.String(80), nullable=False)
    color = db.Column(db.String(80), nullable=True)

    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.parent_name = kwargs['parent_name']
        self.project_id = kwargs['project_id']
        self.color = kwargs['color']

    def __repr__(self):
        return '<Node id={id} name={name} parent_name={parent_name} project_id={project_id}>'.format(id=self.id, name=self.name, parent_name=self.parent_name, project_id=self.project_id)


# /. modified

"""
# / original
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    created_at = db.Column(db.DateTime,nullable=False, default=datetime.now())

    def __init__(self,**kwargs):
        self.name = kwargs['name']

    def __repr__(self):
        return u'<Project id={id} name={name} created_at={created_at}>'.format(id = self.id, name=self.name, created_at=self.created_at)

class Family(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    nodes = db.Column(db.String(80), unique = True)
    project_id = db.Column(db.Integer, nullable = False)

    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.nodes = kwargs['nodes']
        self.project_id = kwargs['project_id']

    def __repr__(self, project_id):
        return u'<Family id = {id}, family_name = {name}, nodes={nodes}, project_id={project_id}>'.format(id= self.id, name=self.name, nodes=self.nodes, project_id=self.project_id)

class Node(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable = False)
    parent_name = db.Column(db.String(80), nullable=False)
    project_id = db.Column(db.Integer, nullable=False)

    def __init__(self, **kwargs):
        self.project_id = kwargs['project_id']
        self.name = kwargs['name']
        self.parent_name = kwargs['parent_name']

    def __repr__(self):
        return u'<Node name={name} parent_id={parent_name} project_id={project_id}>'.format(name=self.name, parent_name=self.parent_name, project_id=self.project_id)

# ./original sqlalchemy 
"""

# ここからindex : method とかを定義していく。

@app.route('/api')
def index():
    proj_obj = Project.query.all()
    proj_list = []
    for i in proj_obj:
        cont = {'id': i.id, 'name': i.name, 'created_at': i.created_at}
        proj_list.append(cont)

    return jsonify(Project=proj_list)

@app.route('/api/create', methods=['POST'])
def create_project():
    data = json.loads(request.json[u'data'])
    theme = data[u'theme']
    new_proj = Project(name=data[u'name'])

    db.session.add(new_proj)
    result = {}
    try:
        db.session.commit()
        db.session.flush(new_proj)
        origin_node = Node(name=theme, parent_name=u"", project_id=new_proj.id, color="skyblue")
        db.session.add(origin_node)
        db.session.commit()
        result.update({'result':'success', 'project_id':new_proj.id})
    except:
        result.update({'result':'fail', 'msg':u'もう一度やり直してください。'})
    return jsonify(Result=result)

@app.route('/api/delete/<project_id>')
def delete_project(project_id):
    proj = Project.query.filter(Project.id == project_id).first()
    db.session.delete(proj)
    result = {}
    try:
        db.session.commit()
        db.session.flush(proj)
        result.update({'result': 'success'})
    except:
        result.update({'result': 'fail'})
    finally:
        return jsonyfi(Result = result)
    
    return "Projectの削除をした"

#brain_storming部分の画面
@app.route('/api/project/<project_id>')
def brain_storming(project_id):
    node_obj = Node.query.filter(Node.project_id == project_id).all()
    node_list = []
    for i in node_obj:
        cont = {'id': i.id, 'name': i.name, 'parent_name': i.parent_name, 'color': i.color}
        node_list.append(cont)

    return jsonify(Nodes=node_list)


@app.route('/api/node/create', methods=['POST'])
def create_node():
    data = json.loads(request.json['data'])
    node = Node(project_id=data['project_id'], name=data['name'], parent_name=data['parent_name'], color=data['color'])
    db.session.add(node)
    try:
        db.session.commit()
        return jsonify({'result': 'success'})
    except:
        return jsonify({'result': 'fail'})

@app.route('/api/project/<project_id>/family/create', methods=['POST'])
def family_create(project_id):
    data = json.loads(request.json['data'])
    fam_obj = Family(name=data['name'], nodes=data['nodes'], project_id=project_id)
    db.session.add(fam_obj)
    result = {}
    try:
        db.session.commit()
        db.session.flush(fam_obj)
        result.update({'result':'success', 'family_id': fam_obj.id})
    except:
        result.update({'result': 'fail', 'msg':'失敗しました。'})
    finally:
        return jsonify(Result=result)

@app.route('/api/project/<project_id>/families')
def familyList(project_id):
    fam = Family.query.filter(Family.project_id == project_id).all()
    fam_list = []
    for i in fam:
        cont = {'id':i.id, 'nodes':i.nodes, 'name': i.name}
        fam_list.append(cont)
    return jsonify(Families=fam_list)

@app.route('/api/morphologic', methods=['POST'])
def extractKeyword():
    result = {}
    if not request.json['text'] == '':
        text = request.json[u'text']
        tagger = mecab.Tagger("-Ochasen")
        node = tagger.parseToNode(text.encode('utf-8'))
        keywords = []
        while node:
            try:
                surface = node.surface.decode('utf-8')
                if len(surface) >1:
                    f = node.feature.split(',')
                    if f[0].decode('utf-8') == u'名詞':
                        keywords.append(surface)
                    elif f[0].decode('utf-8') == u'動詞':
                        keywords.append(f[-3].decode('utf-8'))
                else:
                    pass
            except UnicodeDecodeError:
                pass
            node = node.next
        return jsonify(keywords=keywords)

if __name__ == '__main__':
    app.run()
