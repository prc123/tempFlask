from app.lib.bilibili_api import utils 
import re
from app.utils.token import token



class userinfo(object):
    def __init__(self,**kwargs):
        self.cookies=""
        self.token=""
    def setCookies(self,cookies):
        ret={"code":-1,"message":"格式错误"}
        coookies,v=self.verifyCookies(cookies)
        ret=v.check()
        if ret['code']==0:
                self.cookies=cookies
                self.token=token.create_token(self.cookies)   
        return ret ,self.token
    def verifyCookies(self,cookies):
        sessdata=re.search(r"SESSDATA=(.*?);", cookies)
        csrf=re.search(r"bili_jct=(.*?);", cookies)      
        v=None
        if(sessdata and csrf):
            v=utils.Verify(sessdata.group(1),csrf.group(1))
        return cookies,v
    def verifyToken(self,inToken):
        self.token=inToken 
        tmp= token.verify_token(self.token)
        if tmp=="":
            return False
        self.cookies=tmp
        return True 
