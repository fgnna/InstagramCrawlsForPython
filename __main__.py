import json
import sys
import urllib

reload(sys)
sys.setdefaultencoding('utf-8')

keyUserName = "{username}"
keyNodeCode = "{nodecode}"
keyNodeTime = "{nodetime}"
# https://www.instagram.com/{username}/?__a=1
originInfoUrl = "https://www.instagram.com/" + keyUserName + "/?__a=1"
# https://www.instagram.com/p/{nodecode}/?__a=1
nodeUrl = "https://www.instagram.com/p/" + keyNodeCode + "/?__a=1"

originFilePath = "c:/insImage/" + keyUserName
nodeFilePath = originFilePath + "/" + keyNodeTime
imageFileName = nodeFilePath + "/" + keyNodeTime + ".jpg"

username_list = []
IMAGE_DOWNLOAD_FILE_SRC = "./insImage"
TEAM_ARRAY_FILE = "./usernames.txt"


def _init_config():
    username_list_file = open(TEAM_ARRAY_FILE, "r", 1024)
    temp_list = username_list_file.readlines()
    for i in range(len(temp_list)):
        username_list.append(temp_list[i].replace("\n", ""))
    print username_list


def _download_and_upload():
    print len(username_list)
    for i in range(len(username_list)):
        print "查询:" + username_list[i]
        page = urllib.urlopen(originInfoUrl.replace(keyUserName, username_list[i]))
        jsonData = json.loads(page.read())


def main():
    _init_config()
    _download_and_upload()

if __name__ == "__main__":
    main()
