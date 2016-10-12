import urllib
import urllib2
import json
import os
import time
import sys
print sys.getdefaultencoding()
reload(sys)
sys.setdefaultencoding('utf-8')
def main():
	keyUserName = "{username}"
	keyNodeCode = "{nodecode}"
	keyNodeTime = "{nodetime}"

	keyUserNameListFileName = "c:/insImage/usernames"


	#https://www.instagram.com/{username}/?__a=1
	originInfoUrl = "https://www.instagram.com/" + keyUserName + "/?__a=1"
	#https://www.instagram.com/p/{nodecode}/?__a=1
	nodeUrl = "https://www.instagram.com/p/" + keyNodeCode + "/?__a=1"

	originFilePath = "c:/insImage/" + keyUserName
	nodeFilePath = originFilePath + "/" + keyNodeTime
	imageFileName = nodeFilePath + "/" + keyNodeTime + ".jpg"


	usernameListFile = open(keyUserNameListFileName,"r",1024)
	usernameList = usernameListFile.readlines()
	for i in range(len(usernameList)):
	    usernameList[i] = usernameList[i].replace("\n","")

	print usernameList

	for j in range(len(usernameList)):
	    page = urllib.urlopen(originInfoUrl.replace(keyUserName,usernameList[j]))
	    jsonData = json.loads(page.read())
	    print len(jsonData["user"]["media"]["nodes"])

	    for i in range(len(jsonData["user"]["media"]["nodes"])):
		node = urllib.urlopen(nodeUrl.replace('{nodecode}',jsonData["user"]["media"]["nodes"][i]["code"]))
		nodeJsonData = json.loads(node.read())
		nodeCaption = nodeJsonData["media"]["caption"]
		nodeImageSrc = nodeJsonData["media"]["display_src"]
		nodeImageTime = time.strftime("%Y_%m_%d_%H_%M_%S",time.localtime(nodeJsonData["media"]["date"]))
		nodeImageDirectoryName = nodeFilePath.replace(keyUserName,usernameList[j]).replace(keyNodeTime,nodeImageTime)
		nodeImageFileName = imageFileName.replace(keyUserName,usernameList[j]).replace(keyNodeTime,nodeImageTime)
		nodeIsVideo = nodeJsonData["media"]["is_video"]
		
		
		if not nodeIsVideo and not os.path.exists(nodeImageDirectoryName):
		    os.makedirs(nodeImageDirectoryName)
		    docfile=open(nodeImageDirectoryName+'/doc.txt','w')
		    docfile.write(nodeCaption)
                    docfile.close()
		    urllib.urlretrieve(nodeImageSrc,nodeImageFileName)

if __name__ == "__main__":  
    main()  

