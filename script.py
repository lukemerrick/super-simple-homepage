from string import Template

""" -----------------Template key-------------------------
	title: page title to be displayed on the tab in which page is open
	name: name to be shown front-and-center in large text
	subtitle: subtitle to be shown right under the name section in smaller text
	mission_title: header to the mission/mission-statement section of the page
	mission_text: (paragraph) text of the mission/mission-statement section of the page
	full_name: name to be used for copyright
	copyright_year: year to be used in the copyright section
	button_html: html code for the button links to be shown front-and-center
		syntax = multiple instanes of "<li><a href="${LINK_TEXT_HERE}">&{LINK_NAME_HERE}</a></li><li class="footer-menu-divider">&sdot;</li>"
	link_html: html code for the links to be shown at the bottom of the page
		syntax = multiple instanes of "<li><a href="${LINK_TEXT_HERE}">&{LINK_NAME_HERE}</a></li><li class="footer-menu-divider">&sdot;</li>"
	-----------------------------------------------------
"""

# read in template
with open('Custom Theme/template.html','r') as template_file:
	template_string = template_file.read()

# read in mission statement
with open('mission.txt','r') as mission_text_file:
	mission_text = mission_text_file.read()
	
# read in user-submitted info
with open('info.txt','r') as info_file:
	info_lines = info_file.readlines()

def as_kwarg_str (k, v):
	return k + '=' + '\'' + v + '\''

def parse_info(text):
	kwarg_strs = []
	for line in info_lines:
		# extract strings from line
		raw = line.split(': "')
		k = raw[0]
		v = raw[1][:raw[1].rfind('"')]
		# add info to kwarg_strs
		kwarg_strs.append(as_kwarg_str(k, v))
	kwargs_as_string = ', '.join(kwarg_strs)
	d = eval('dict(%s)'%kwargs_as_string)
	return d
	
	
# generate template substitution dictionary
d = dict(
	name = 'JOHN Doe'
	,subtitle = 'Homepage'
	,mission_title = 'Mission Statement'
	,mission_text = mission_text
	,full_name = 'Jane Doe'
)
d = parse_info(info_lines)

template = Template(template_string)
result = template.safe_substitute(d)
with open ('result.html','w') as output:
	output.write(result)
print('done?')
