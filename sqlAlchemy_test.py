from flaskServer import db, Project, Family, Node
"""
p1 = Project(name='applicot')
p2 = Project(name='chatStorming')
p3 = Project(name='SecretaryBot')

db.session.add(p1)
db.session.add(p2)
db.session.add(p3)

db.session.commit()
db.session.close()

f1 = Family(name='Nonoyama', nodes='["test", "dayo"]', project_id=1)
f2 = Family(name='Tsutsumi', nodes='["chanto", "dekiteru"]', project_id=1)
f3 = Family(name='Uchida', nodes='["kana","?"]', project_id=2)
f4 = Family(name='Suzuki', nodes='["kakukoto", "nakunattyata"]', project_id=3)

db.session.add(f1)
db.session.add(f2)
db.session.add(f3)

db.session.commit()
db.session.close()

n1 = Node(name='hiro', parent_name='', project_id=1)
n2 = Node(name='takamichi', parent_name='hiro', project_id=1)
n3 = Node(name='risako', parent_name='hiro', project_id=1)
n4 = Node(name='Kan', parent_name='risako', project_id=1)

n5 = Node(name='chat', parent_name='', project_id=2)
n6 = Node(name='stream', parent_name='chat', project_id=2)
n7 = Node(name='ing', parent_name='chat', project_id=2)
n8 = Node(name='kanseisaseyou', parent_name='chat', project_id=2)

n9 = Node(name='secretary', parent_name='bot', project_id=3)
n10 = Node(name='bot', parent_name='', project_id=3)
n11 = Node(name='nakanaka', parent_name='secretary', project_id=3)
n12 = Node(name='susumanaine', parent_name='nakanaka', project_id=3)

db.session.add(n1)
db.session.add(n2)
db.session.add(n3)
db.session.add(n4)
db.session.add(n5)
db.session.add(n6)
db.session.add(n7)
db.session.add(n8)
db.session.add(n9)
db.session.add(n10)
db.session.add(n11)
db.session.add(n12)


db.session.commit()
db.session.close()

print '=============   check if call works ok =========== '
project_id = 1

p1 = Project.query.filter(Project.id==project_id).first()
p2 = Project.query.filter(Project.id==2).first()
print '____________________________ Project _______________________'
print 'p1 =', p1
print 'id = ', p1.id
print 'name = ', p1.name
print 'created_at = ', p1.created_at
print 'family = ', p1.family
print 'node = ', p1.node

f1 = Family.query.filter(Family.project_id==project_id).first()
print '_____________________ Family ___________________'
print 'f1', f1
print 'id = ' , f1.id
print 'name = ', f1.name
print 'nodes = ', f1.nodes
print 'project_id = ', f1.projects.id
print 'projects_name = ', f1.projects.name

n1 = Node.query.filter(Node.project_id==project_id).first()
print 'id = ', n1.id
print 'name = ', n1.name
print 'parent_name = ', n1.parent_name
print 'project_id = ', n1.project_id
print 'projects_name (ForeginKey) =  ', n1.projects.name
"""
print '============ check if related delete works ok ================='
project_id=3
p1 = Project.query.filter(Project.id==project_id).first()
print p1

db.session.delete(p1)
db.session.commit()
db.session.close()

print  Family.query.filter(Family.project_id==project_id).all()

