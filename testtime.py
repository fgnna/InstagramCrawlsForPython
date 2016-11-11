import urllib2

data = urllib2.urlopen("https://scontent.cdninstagram.com/t51.2885-15/e35/14607129_209985206092979_2689480040827060224_n.jpg?ig_cache_key=MTM3ODQxMjU4MTg5MTY2MjI2MA%3D%3D.2").read()
img_file = open('./temp/temp.jpg', 'w')
img_file.write(data)
img_file.close()