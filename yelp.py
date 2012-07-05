import oauth2 as oauth
import simplejson


class yelpResponse(object):
	def __init__(self, response={}, content={}, isDetails=False):
		self.response = response
		self.content = content
		self.isDetails = isDetails
	
	def getHeaders(self):
		return self.response
		
	def getContent(self):
		return self.content

class yelpRequest(object):
	
	def __init__(self):
		self.searchbylocation = 'http://api.yelp.com/v2/search?term={0}&location={1}'
		self.searchbygeo = 'http://api.yelp.com/v2/search?term={0}&ll={1},{2}'
		self.businessurl = 'http://api.yelp.com/v2/business/{0}'
		self.client = yelpRequest.getClient()

	@staticmethod
	def getClient():
		consumer = oauth.Consumer(key="9PL5pl33rIJHtStp0oxG2A", secret="GTUuBHMN8xGqcsaebmLmmK7giZ8")
		token = oauth.Token('rNFvqLfLfJIJqoz-WgrkfG7yCCa7YVhs','P_-g5kqou13dgG1f1crOysIFgmo')
		client = oauth.Client(consumer, token)
		return client   
	
	def searchByGeo(self, term='', geo=[], details=False):
		return self._searchapi(self.searchbygeo.format(term, geo[0], geo[1]), details)
				
	def searchByLocation(self, term='', location='', details=False):
		return self._searchapi(self.searchbylocation.format(term, location), details)
		
	def _searchapi(self, searchurl, details=False):
		response, contentstr = self.client.request(searchurl, "GET")
		success = (response.status == 200)	
		content = simplejson.loads(contentstr)
		total = content['total']
		if(success == False or total == 0):
			return yelpResponse(response, {})
			
		if (details == False):
			return yelpResponse(response, content['businesses'][0])
		else:
			return yelpResponse(response, self.getBusinessDetails(content['businesses'][0]['id']))
			
	def getBusinessDetails(self, yelpbusinessid):
		response, contentstr =  self.client.request(self.businessurl.format(yelpbusinessid), "GET")
		return yelpResponse(response, simplejson.loads(contentstr), True)
		
