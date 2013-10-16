#By Thomas O'Malley of the Illinois State Geological Survey.  ___ Incorporates both the Recursive_Glob and File_System_Restructure projects (found at https://github.com/Thom-OMalley)
#Relocates mxd, mdb, and gdb files which are not referenced in the service configuration files.

import glob, arcpy, os, shutil
import xml.dom.minidom as DOM

USstates = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

mxdList = []

cfgFolder = "C:\\Program Files (x86)\\ArcGIS\\Server10.0\\server\\user\\cfg\\aasggeothermal\\"
cfgList = glob.glob(cfgFolder + '*.cfg')
for cfg in cfgList:
    doc = DOM.parse(cfg)
    pathElmt = doc.getElementsByTagName("FilePath")
    for node in pathElmt:
        mxdPath = node.firstChild.data
        mxdPath = mxdPath.replace('\\\\GEOTHERMAL\\','C:\\')
    mxdList.append(mxdPath)

dataSauces = set([])
dataList = []

for eachMXD in mxdList:
    try:
        mxd = arcpy.mapping.MapDocument(str(eachMXD))

        layers = arcpy.mapping.ListLayers(mxd)
        for layer in layers:
            dataSauce = layer.dataSource
            dataSauceShrt = dataSauce.rsplit('\\',1)[0]
            dataSauceShort = dataSauceShrt.replace('\\\\GEOTHERMAL\\','C:\\')
            dataSauces.add(str(dataSauceShort))
    except:
        print "Invalid file name: "+ str(eachMXD)

#At this point we have a list of MXDs and sources that we need to keep in place

#Now let's use a Recursive_Glob to create a list of all file paths in our service directory

path = 'C:\\datafiles\\aasggeothermal\\' #your starting directory here
allList = []
findThis = ['pass']#in order to start the while loop
search_params = '.gdb' #file extension etc.
while len(findThis) > 0: #While a downward search still produces results
    findThis = glob.glob(path)
    for item in findThis:
        if item.endswith(search_params) or item.endswith('.mdb')or item.endswith('.mxd') == True:
            allList.append(item)
    path = path + '\\*'

#Now that we have our super list, we need to remove the our necessary files from this list.

for sauce in dataSauces:
    if sauce.endswith('INAqueousChemistry1_10.gdb'): print "hey i found " + sauce
    '''try:
        allList.remove(sauce)
    except:
        print "Was not in list: " + sauce'''
    for e in allList:
        tempLow = e.lower()
        if tempLow == sauce.lower():
                try:
                    allList.remove(e)
                except:
                    print "Was not in list: " + sauce

for mxd in mxdList:
    try:
        allList.remove(mxd)
    except:
        print "Was not in list: " + mxd

#Now allList is populated with only the mdb, gdb, and mxd files we can move

#Time to shuttle them off to a new file tree using the File_System_Restructure

for each in allList:
    i = 0
    filename = each.rsplit('\\',1)
    filename = filename[1]
    state = USstates.get(filename[0:2])
    if each.endswith('.gdb'):
        try:
            path = 'C:\\datafiles\\OldData\\'+state+'\\archived_gdb'
        except: path = 'C:\\datafiles\\OldData\\Unsorted'
    elif each.endswith('.mdb'):
        try:
            path = 'C:\\datafiles\\OldData\\'+state+'\\archived_mdb'
        except: path = 'C:\\datafiles\\OldData\\Unsorted'
    elif each.endswith('.mxd'):
        try:
            path = 'C:\\datafiles\\OldData\\'+state+'\\archived_mxd'
        except: path = 'C:\\datafiles\\OldData\\Unsorted'
    else:
        path = 'C:\\datafiles\\OldData\\Unsorted'
    if not os.path.exists(path):
        os.makedirs(path)

    fullPath = path+'\\'+filename
    while os.path.exists(fullPath): #while file of same name exists, add 1 to end of file name
        i+=1
        print "Renaming + " + str(i)
        path = fullPath
        a, b = path.rsplit('.',1)
        if i > 1:
            path = a[:-1]+ str(i) +'.'+ b #if number already added, remove number and replace with new (gets buggy after 9)
        else:
            path = a + str(i) +'.'+ b
        fullPath = path
    
    try:
        shutil.move(each,path)
    except: print "Could not move " + str(each) +'.  A file of the same name already exists.'
