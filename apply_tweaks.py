from collections import defaultdict
from bs4 import BeautifulSoup

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
# >> Class relabeling works in the node details screen, but class labels don't appear in the group selector. Just numbers.
#    We're going to need to modify line 280 of main.js

def two_list():
    return [[],[]]

community_prototypes = defaultdict(two_list)

k=2
with open(data_fpath, 'r') as f:
    data = json.load(f)

for node in data['nodes']:
    class_id = node['attributes']['Modularity Class']
    count = node['attributes']['count'] # I should rename this to 'active users' or something like that
    
    class_list = community_prototypes[class_id]
    #for i in range(k):
    rec = [node['label'], count]
    if any(item == [] for item in class_list):
        for i in range(k):
            if not class_list[i]:
                class_list[i] = rec
                break
    else:
        for i in range(k):
            if class_list[i][1] < count:
                class_list[i] = rec
                break

# Less descriptive than I'd've liked. I should probably use subscriber counts instead
# of active user counts. Anyway...

# Relabel classes
for node in data['nodes']:
    class_id = node['attributes']['Modularity Class']
    node['attributes']['Modularity Class'] = ' | '.join(zip(*community_prototypes[class_id])[0])

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