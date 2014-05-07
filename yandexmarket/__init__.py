import requests
import json


class YandexMarketContent(object):
  API_VERSION = 1

  class NotAuthorized(BaseException):
    pass

  def __init__(self, key=None):
    if not key:
      raise YandexMarketContent.NotAuthorized("You must provide authorization key to access Yandex.Market API!")
    self.key = key

  def _make_url(self, resource, format='json', version=API_VERSION):
    return 'https://api.content.market.yandex.ru/v%s/%s.%s' % (version, resource, format)

  def _make_request(self, resource, format='json', version=API_VERSION, params={}):
    url = self._make_url(resource, format, version) 
    query_params = params
    params['Authorization'] = self.key

    response = requests.get(url, params=params, headers={'Authorization':self.key, 'Accept':'*/*'})
    output = json.loads(response.content)
    print output
    if response.status_code == 401:
      server_response = []
      for error in output['errors']:
        server_response.append(error)
      raise YandexMarketContent.NotAuthorized("Your key `%s' wasn't authorized at Yandex.Market API. Server response: %s" % (self.key, server_response))

    return output

  def category(self):
    response = self._make_request('category')
    return response

if __name__=='__main__':
  api = YandexMarketContent(key='zGSsd7NxgsZw5C4Hj8721GucO739PO')
  print api.category()
