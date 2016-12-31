from collections import defaultdict
from bs4 import BeautifulSoup
from operator import itemgetter

try:
    import ujson as json
except:
    import json


css_path =  r'C:\Users\davidmarx\Documents\Projects\Toy Projects\RedditGraphEvolution\reddit_map_active_subs\network\css\style.css'  
html_path = r'C:\Users\davidmarx\Documents\Projects\Toy Projects\RedditGraphEvolution\reddit_map_active_subs\network\index.html'  
config_fpath = r'C:\Users\davidmarx\Documents\Projects\Toy Projects\RedditGraphEvolution\reddit_map_active_subs\network\config.json'
data_fpath   = r'C:\Users\davidmarx\Documents\Projects\Toy Projects\RedditGraphEvolution\reddit_map_active_subs\network\data.json'

#######################
# fix the config file #
#######################

with open(config_fpath, 'r') as f:
    config = json.load(f)
    
# Replace newline characters with HTML breaks
for k,v in config['text'].iteritems():
    config['text'][k] = v.replace('\n', '<br>')
    
# Adjust sigma settings
config['sigma']['graphProperties']['minNodeSize'] = 0.07
config['sigma']['graphProperties']['maxNodeSize'] = 4
config['sigma']['graphProperties']['minEdgeSize'] = 0.1
config['sigma']['graphProperties']['maxEdgeSize'] = 0.3
config['sigma']['mouseProperties']['maxRatio'] = 80
config['sigma']['drawingProperties']['labelThreshold'] = 6

# Rename group selector from "Modularity Class" to something cleaner
pass

#Relabel modularity classes according to their k most active subreddits

k=2
with open(data_fpath, 'r') as f:
    data = json.load(f)

communities = defaultdict(list)
for node in data['nodes']:
    rec = (node['label'], int(node['attributes']['count']))
    communities[node['attributes']['Modularity Class']].append(rec)
    
for c_id in communities:
    comm = communities[c_id]
    communities[c_id] = sorted(comm, key=itemgetter(1), reverse=True)[:k]


# Relabel classes
for node in data['nodes']:
    class_id = node['attributes']['Modularity Class']
    node['attributes']['Modularity Class'] = ' | '.join(zip(*communities[class_id])[0])

with open(data_fpath, 'wb') as outfile:
    json.dump(data, outfile)
    
with open(config_fpath, 'wb') as outfile:
    json.dump(config, outfile)
    
##############

## Dump the legend and OII branding
with open(html_path, 'r') as f:
    soup = BeautifulSoup(f.read())

element = soup.find('div', {'id':'legend'})
element.extract()
    
element = soup.find('div', {'id':'developercontainer'})
element.extract()

    
## Improve title
#soup.title.replace_with('<title>Map of Reddit - David Marx</title>')
new_title = soup.new_tag('title')
new_title.string = 'Map of Reddit - David Marx'
soup.title.replace_with(new_title)

    
with open(html_path, 'wb') as f:
    f.write(soup.__repr__()) # there's probably a better method I can use for this
    
    
## Modifications to CSS

# It's sorta lazy, but if we just add a new rule to the bottom of the CSS document,
# it'll override the previous rule. Way simpler than modifying the document in-place.

with open(css_path, 'r') as f:
    css = f.read()
    
css += """

#maintitle {
/*

height: 72px;
*/
margin-bottom:20px;
height:0px;
}

#maintitle h1 {
/*display: none;*/
display:block;
}
"""

with open(css_path, 'wb') as f:
    f.write(css)