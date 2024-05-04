def jwt_response_handler(token,user=None,request=None):
    # 自定义jwt认证成功返回数据
    return{
        'token':token,
        'userId':user.id,
        'username': user.username,
    }