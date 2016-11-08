#coding:utf-8
import httplib
import json
import os
import sys
import urllib
import upyun

from config import api_check, api_upyun_secret, api_submit_host, api_submit_host_number, api_submit_url

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
up_object = upyun.UpYun('bopimage', None, None, api_upyun_secret, timeout=200, endpoint=upyun.ED_AUTO)


def _init_config():
    print "初始化下载列表"
    username_list_file = open(TEAM_ARRAY_FILE, "r", 1024)
    temp_list = username_list_file.readlines()
    username_list_file.close()
    count = len(temp_list)
    if (count % 3) is not 0:
        print "配置列表不正确，结束"
        return

    for i in range(count):
        if (i % 3) is 0 and i + 2 < count:
            username_list.append({"username": temp_list[i].strip(),
                                  "teamname": temp_list[i+1].strip(),
                                  "teamid": temp_list[i+2].strip()})
    print username_list
    if not os.path.exists("./temp"):
        os.makedirs("./temp")
    print "初始化结束"


def _download_and_upload():
    for i in range(len(username_list)):
        print "开始执行任务:" + username_list[i]["username"]
        print "    获取ins信息:" + username_list[i]["username"]
        page = urllib.urlopen(originInfoUrl.replace(keyUserName, username_list[i]["username"]))
        print "    获取ins信息成功-开始下载"
        json_data = json.loads(page.read())
        _download(json_data, username_list[i])
        print "任务结束:" + username_list[i]["username"]


def _download(json_data, user_info):
    for i in range(len(json_data["user"]["media"]["nodes"])):
        print "      开始加载第"+str(i+1)+"条"
        nodeJsonData = json_data["user"]["media"]["nodes"][i]
        if nodeJsonData["is_video"]:
            print "        视频，跳过"
            continue
        if not check(nodeJsonData["id"]):
            print "        出现重复信息"
            break

        if downlaod_upload_img(nodeJsonData["display_src"], nodeJsonData["id"]):
            try:
                post_api(user_info, nodeJsonData["caption"], nodeJsonData["id"])
            except KeyError:
                post_api(user_info, " ", nodeJsonData["id"])


def downlaod_upload_img(img_src, _id):
    print "        下载图片"
    urllib.urlretrieve(img_src, "./temp/temp.jpg")

    print "        上传图片"
    kwargs = {'allow-file-type': 'jpg,jpeg,png'}
    with open('./temp/temp.jpg', 'rb') as f:
        res = up_object.put('/SponiaSWData/Instagram/'+_id+'.jpg', f, checksum=True, form=True, **kwargs)
        if res["code"] is 200:
            return True
    print "        上传图片　失败"
    return False

'''
related_team Array 类似[{clubname:"阿森纳",teamid:"660"}]
mute Boolean 默认传false
pic String http://release.zqkong.com/SponiaSWData/Instagram/图片名
text Stirng 格式参见如右（不包括引号）： "晓池：今天天气特别好"
source String 可不传，默认为空字符串
title String 不可重复的。。。。
'''


def post_api(user_info, caption, _id):
    print "        提交接口数据"
    if caption is None:
        caption = " "
    httpClient = None
    try:
        params = {'related_team': [{'clubname': user_info["teamname"], 'teamid':user_info["teamid"]}],
                                   'mute': False, 'text': user_info["username"]+': '+caption, 'pic': 'http://release.zqkong.com/SponiaSWData/Instagram/'+_id+'.jpg',
                                   'title': _id}
        print json.JSONEncoder().encode(params)
        headers = {"Content-type": "application/json"}
        httpClient = httplib.HTTPConnection(api_submit_host, api_submit_host_number, timeout=30)
        httpClient.request('POST', api_submit_url, json.JSONEncoder().encode(params), headers)
        response = httpClient.getresponse()
        print response
        json_data = json.loads(response)
        if json_data["code"] is 0:
            print "        提交接口数据 成功"
            return True
    except Exception, e:
        print e
    finally:
        if httpClient:
            httpClient.close()
    print "        提交接口数据 失败"
    return False


def check(title):
    print "        检查数据是否重复"
    response = json.loads(urllib.urlopen(api_check+title).read())
    if response["code"] is not 0:
        return False
    return True


def main():
    _init_config()
    try:
        _download_and_upload()
    except IOError:
        print "网络异常"

if __name__ == "__main__":
    main()
