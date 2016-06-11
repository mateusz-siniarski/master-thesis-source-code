import requests

class getParentFromLocationId:

    def __init__(self,id):
        #print 'http://www.marineregions.org/rest/getGazetteerRelationsByMRGID.json/'+str(id)+'/upper/partof/'
        r =requests.get('http://www.marineregions.org/rest/getGazetteerRelationsByMRGID.json/'+str(id)+'/upper/partof/')
        try:
            self.data = r.json()
        except:
            self.data = None

    def get_parent_id(self):
        return get_value_from_key_parent(self.data, "MRGID")

    def get_latitude(self):
        return get_value_from_key(self.data,"latitude")

    def get_longitude(self):
        return get_value_from_key(self.data, "longitude")

    def get_placeType(self):
        return get_value_from_key(self.data, "placeType")

    def get_name(self):
        return get_value_from_key_parent(self.data, "preferredGazetteerName")

def get_value_from_key_parent(d, key):

    for k, v in d[0].iteritems():
        if isinstance(v, dict):
            return get_value_from_key(v, key)
        else:
            if k == key:
                return v

class getDataFromLocationId:

    def __init__(self,id):
        r =requests.get('http://www.marineregions.org/rest/getGazetteerRecordByMRGID.json/'+str(id)+'/')
        self.data = r.json()

    def get_latitude(self):
        return get_value_from_key(self.data,"latitude")

    def get_longitude(self):
        return get_value_from_key(self.data, "longitude")

    def get_placeType(self):
        return get_value_from_key(self.data, "placeType")

    def get_name(self):
        return get_value_from_key(self.data, "preferredGazetteerName")



def get_value_from_key(d, key):
    if d is None:
        return None

    for k, v in d.iteritems():
        if isinstance(v, dict):
            return get_value_from_key(v, key)
        else:
            if k == key:
                return v



