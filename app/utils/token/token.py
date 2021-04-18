from flask import request,jsonify,current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature
def create_token(user_data):

    #第二个参数是有效期(秒) 
    s = Serializer(current_app.config["SECRET_KEY"],expires_in=36000)
    #接收用户id转换与编码
    token = s.dumps(user_data).decode("ascii")
    return token

def verify_token(token):
    s=Serializer(current_app.config["SECRET_KEY"])
    data=""
    try:
        data=s.loads(token)
    except SignatureExpired :
        # token正确但是过期了
        print("token 过期")
    except BadSignature:
        print("token error")

    return data