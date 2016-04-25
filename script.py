from string import Template
import os
import shutil
from distutils.dir_util import copy_tree

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

button_skeleton = '<li><a href="{0}" class="btn btn-default btn-lg"><i class="{1}"></i> <span class="network-name">{2}</span></a></li>'
link_skeleton = '<li><a href="{0}">{1}</a></li>'
link_separator = '<li class="footer-menu-divider">&sdot;</li>'

input_folder = r'C:\Users\luke\Documents\GitHub\super-simple-homepage\materials'
template_folder = r'C:\Users\luke\Documents\GitHub\super-simple-homepage\Custom Theme'
output_folder = 'generated_website'

# read in template
with open('Custom Theme/template.html','r') as template_file:
	template_string = template_file.read()

# read in mission statement
with open(input_folder + '/mission.txt','r') as mission_text_file:
	mission_text = mission_text_file.read()
	
# read in user-submitted info
with open(input_folder + '/info.txt','r') as info_file:
	info_lines = info_file.readlines()

def as_kwarg_str (k, v):
	return k + '=' + '\'' + v + '\''
	

""" Argument 0 is the link location, 1 is the glyphicon, and 2 is the link text"""
def button_html(info):
	trimmed = info.strip().split(': {')[1][:-1]
	split = trimmed.split('","')
	location = split[0][1:]
	text = split[1]
	glyphicon = split[2][:-1]
	button = button_skeleton.format(location, glyphicon, text)
	return button
	
""" Argument 0 is link location, 1 is link text """
def link_html(info):
	trimmed = info.strip().split(': {')[1][:-1]
	split = trimmed.split('","')
	location = split[0][1:]
	text = split[1][:-1]
	link = link_skeleton.format(location, text)
	return link

def parse_info(text):
	kwarg_strs = []
	button_lines = []
	link_lines = []
	for line in info_lines:
		# extract strings from line
		raw = line.split(': "')
		k = raw[0]
		if 'button' in k:
			button_lines.append(line)
		elif 'link' in k:
			link_lines.append(line)
		else:
			v = raw[1][:raw[1].rfind('"')]
			# add info to kwarg_strs
			kwarg_strs.append(as_kwarg_str(k, v))
	# generate button and link html
	buttons = '\n'.join(sorted([button_html(info) for info in button_lines]))
	links = ('\n' + link_separator + '\n').join(sorted([link_html(info) for info in link_lines]))
	kwargs_as_string = ', '.join(kwarg_strs)
	d = eval('dict(%s)'%kwargs_as_string)
	d['button_html'] = buttons
	d['link_html'] = links
	return d
	
	
# generate template substitution dictionary
d = parse_info(info_lines)
d['mission_text'] = mission_text

template = Template(template_string)
result = template.safe_substitute(d)

# create output folder
try:
	shutil.rmtree(output_folder, ignore_errors = True)
except:
	pass
os.mkdir(output_folder)
copy_tree(template_folder, output_folder)

with open (output_folder + '/index.html','w') as output:
	output.write(result)

# move photos to output folder
shutil.copy2(input_folder + '/intro-bg.jpg', output_folder + '/img')
shutil.copy2(input_folder + '/profile-photo.jpg', output_folder + '/img')

# remove template.html from output folder
os.remove(output_folder + '/template.html')