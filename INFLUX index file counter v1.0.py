#Copyright (c) 2017 Genome Research Ltd.

#Index file counter
#v1.0 Jun 2017
#Python 3.5 (2016)
#Author : Christopher Hall, Wellcome Trust Sanger Institute, christopher.hall@sanger.ac.uk

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.


#Counts all the index files in it's folder and subfolders and displays the statisitics.  
#We orgainise our files using one subfolder per user and another subfolder per experiment.  This script uses this routine to count the number of experiments.  i.e. User1\01jan2017\file.fcs

import os
from collections import Counter

counter=0
expt=[]
folders=[]
rootDir = '.'
userlist=[]
exptcounter=0
for dirName, subdirList, fileList in os.walk(rootDir): #walks through the subdirectories
	for x in fileList:
		if x.endswith('.fcs'): #looks for my file type
			filename = os.path.join(dirName, x) #creates a filename and path to open
			f = open(filename,'r', encoding='Latin-1') #opens the file
			for whereisit in f.readlines(): #reads the lines (its much faster using this)
				if "INDEXSORTPOSITIONS" in whereisit: # looks for my dtring in the file
					print ("index file ",f.name)
					counter+=1 #counts the files with INDEXSORTPOSITIONS
					expt+=[filename.rpartition('\\')[0]] #creates a list of direcotries with INDEXSORTPOSITIONS files
					folders+=[filename.split('\\')[1]] #creates a list of first subdirectories (usernames) with INDEXSORTPOSITIONS files
					f.close()
					userlist+=[str([filename.split('\\')[1]])]

#This produses the overal stats					
numfold=set(expt)
usernum=set(folders)
writecount="number of individual index files",counter
writeexpt="number of index experiments",len(numfold)
writeuser="number of index users",len(usernum)
statstowrite=str(writecount)+'\n'+str(writeexpt)+'\n'+str(writeuser)+'\n'
with open("stats.csv", 'w')	as s:
	s.write(statstowrite.replace("(", "").replace(")", "").replace("'", ""))
s.close()

#this counter shows how many index files each user has produced
cnt = Counter()
for userfile in folders:
	cnt[userfile]+=1
with open("stats.csv", 'a') as s:
	s.write('\nThe number of files generated by each user:\n')
s.close()
with open("stats.csv", 'a') as s:
    for k,v in  cnt.most_common():
        s.write( "{},{}\n".format(k,v) )
s.close()
with open("stats.csv", 'a') as s:
	s.write('\nThe number of experiments (folders) by each user:\n')
s.close()

#this counter shows how many experiments each user has completed	
uniqueuser=list(set(userlist))
numfold1=str(numfold)
x=0
for e in numfold1:
	while x < len(set(userlist)):
		nameofuser=uniqueuser[x].strip("['']")
		towrite= nameofuser,numfold1.count(nameofuser)
		with open("stats.csv", "a") as s:
			s.write(str(towrite).replace("(", "").replace(")", "").replace("'", "")+'\n')
			x+=1
s.close()
