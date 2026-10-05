import requests
from django.conf import settings
from urllib.parse import urlencode

class ApiError(Exception):
    def __init__(self,message,status=None,payload=None):
        super().__init__(message); self.status=status; self.payload=payload or {}

class SiraApi:
    def __init__(self,request): self.request=request; self.base=settings.SIRA_API_URL.rstrip('/')
    def _headers(self):
        h={'Accept':'application/json'}; token=self.request.session.get('token')
        if token: h['Authorization']=f'Bearer {token}'
        return h
    def call(self,method,path,data=None,params=None):
        try:r=requests.request(method,self.base+path,json=data,params=params,headers=self._headers(),timeout=25)
        except requests.RequestException as e: raise ApiError('No fue posible comunicarse con SIRA API. Verifique Spring Boot.') from e
        try: payload=r.json() if r.content else {}
        except ValueError: payload={}
        if not r.ok:
            msg=payload.get('detail') or payload.get('mensaje') or payload.get('error') or f'Error de API ({r.status_code})'
            raise ApiError(msg,r.status_code,payload)
        return payload
    def get(self,p,params=None):return self.call('GET',p,params=params)
    def post(self,p,d=None):return self.call('POST',p,d or {})
    def put(self,p,d=None):return self.call('PUT',p,d or {})
    def delete(self,p):return self.call('DELETE',p)
