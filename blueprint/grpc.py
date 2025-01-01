from .generated import users_pb2, users_pb2_grpc
from DBConnection import work_with_db, make_update
from psycopg2.extensions import AsIs
from .functions import get_users, make_response
from . import provider



class UsersSer(users_pb2_grpc.UsersServicer):
    def __init__(self):
        users_pb2_grpc.UsersServicer.__init__(self)
        self.flag_for_update_cache = False
        #если True, то произошло обновление в базе данных и необходимо обратиться к бд, чтобы поместить данные в кэш

    def GetUsers(self, request, context):
        if request.message == 'Получить список пользователей':
            result = get_users(flag_for_update_cache=self.flag_for_update_cache)
            self.flag_for_update_cache = False

            return users_pb2.GetUsersResponse(message = result)
        pass
        #можно обойтись и без if, но по логике grpc показалось нужным добавить

    def AddUser(self, request, context):
        if request.message == 'Добавить нового пользователя':
            sql = provider.get('add_user.sql',
                               name = request.user.name,
                               surname = request.user.surname,
                               email = request.user.email,
                               login = request.user.login,
                               hash_password = request.user.hash_password)
            make_update(sql)
            self.flag_for_update_cache = True

            return users_pb2.AddUserResponse(message = 'Новый пользователь \n' + \
                                             'name: ' + request.user.name + '\n' + \
                                             'surname: ' + request.user.surname + '\n' + \
                                             'email: ' + request.user.email + '\n' + \
                                             'login: ' + request.user.login + '\n' + \
                                             'hash_password: ' + request.user.hash_password)
        pass

    def DeleteUser(self, request, context):
        if request.message == 'Удалить пользователя':
            sql = provider.get('find_user_with_id.sql', id = request.id)
            user = work_with_db(sql)[0]

            sql = provider.get('delete_user.sql', id = request.id)
            make_update(sql)
            self.flag_for_update_cache = True

            return users_pb2.DeleteUserResponse(message = make_response('Удален пользователь',
                                                                        user))
        pass

    def UpdateUser(self, request, context):
        if request.message == 'Обновить пользователя':
            sql = provider.get('update_user.sql', parameter = AsIs(request.parameter),
                               value = request.value,
                               id = request.id)
            make_update(sql)
            self.flag_for_update_cache = True

            sql = provider.get('find_user_with_id.sql', id=request.id)
            user = work_with_db(sql)[0]


            return users_pb2.UpdateUserResponse(message = make_response('Обновлен пользователь',
                                                                        user))
        pass