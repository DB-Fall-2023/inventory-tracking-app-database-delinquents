from dao.UsersDao import UsersDao
from flask import jsonify

class UsersHandler:
    def build_users_dict(self, row):
        result = {}
        result['uid'] = row[0]
        result['uname'] = row[1]
        result['ulastname'] = row[2]
        result['uemail'] = row[3]
        result['upassword'] = row[4]
        result['uphone'] = row[5]
        result['ucountry'] = row[6]
        result['ucity'] = row[7]
        result['wid'] = row[8]
        return result

    def build_top_transactions_users_dict(self, row):
        result = {}
        result['uid'] = row[0]
        result['uname'] = row[1]
        result['ulastname'] = row[2]
        result['uemail'] = row[3]
        result['upassword'] = row[4]
        result['uphone'] = row[5]
        result['ucountry'] = row[6]
        result['ucity'] = row[7]
        result['wid'] = row[8]
        result['total_transactions'] = row[9]
        return result
    def get_all_users(self):
        dao = UsersDao()
        users_list = dao.get_all_users()
        result = []
        for row in users_list:
            result.append(self.build_users_dict(row))
        return jsonify(result)

    def get_top3_transactioners(self):
        dao = UsersDao()
        users_list = dao.get_top3_transactioners()
        result = []
        for row in users_list:
            result.append(self.build_top_transactions_users_dict(row))
        return jsonify(result)




