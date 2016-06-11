import requests



def get_pageid_from_article_title(language="en", title=None):
    r =requests.get('https://'+language+'.wikipedia.org/w/api.php?action=query&titles='+title+'&format=json')
    data = r.json()
    return get_value_from_key(data,"pageid")

def get_title_from_pageid(language="en", pageid=None):
    r =requests.get('https://'+language+'.wikipedia.org/w/api.php?action=query&pageids='+str(pageid)+'&format=json')
    data = r.json()
    return get_value_from_key(data,"title")

def get_fullurl_from_pageid(language="en", pageid=None):
    r = requests.get('http://'+language+'.wikipedia.org/w/api.php?action=query&prop=info&pageids='+str(pageid)+'&inprop=url&format=json')
    data = r.json()
    return get_value_from_key(data,"fullurl")

def get_summary_from_pageid(language="en", pageid=None):
    r = requests.get('http://'+language+'.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&pageids='+str(pageid))
    data = r.json()
    return get_value_from_key(data,"extract")

def get_value_from_key(d,key):
  for k, v in d.iteritems():
    if isinstance(v, dict):
        return get_value_from_key(v,key)
    else:
      if k == key:
          return v

