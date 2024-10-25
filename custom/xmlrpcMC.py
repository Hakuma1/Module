url = "http://127.0.0.1:8016"
db = 'TestMC'
username = 'admin'
password = 'admin'

import xmlrpc.client

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
version = common.version()
print(version)

uid = common.authenticate(db, username, password, {})
print("UID ----", uid)

""" Récupération de toutes les demandes """
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
# ids = models.execute_kw(db, uid, password, 'kzm.instance.request', 'search', [[]])
# partners_records = models.execute_kw(db, uid, password, 'kzm.instance.request', 'read', [ids],
# {'fields': ['name', 'treat_date', 'cpu']})
partners_records = models.execute_kw(db, uid, password, 'kzm.instance.request', 'search_read', [[]],
                                     {'fields': ['name', 'state', 'cpu']})
for x in partners_records:
    print(x)

""" Creation de données """

# id_instance = models.execute_kw(db, uid, password, 'kzm.instance.request', 'create',
#                                [{'state': "Draft", 'cpu': 4, 'ram': 8}])
# print(id_instance)

""" Option de récupération des commandes par statut  """
partners_records = models.execute_kw(db, uid, password, 'kzm.instance.request', 'search_read',
                                     [[['state', '=', 'Draft']]],
                                     {'fields': ['name', 'state', 'cpu']})
print("Only Draft")
for x in partners_records:
    print(x)
