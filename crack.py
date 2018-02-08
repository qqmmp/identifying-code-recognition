#-*- coding:utf-8 -*-
from PIL import Image
import math
import os
import time
import hashlib

#图片相似性比较函数
class VectorCompare(object):
	#计算图片矢量大小
	def magnitude(self,concordance):
		total = 0
		for word,count in concordance.items():
			total += count **2
		return math.sqrt(total)
	#计算相似度
	def relation(self,concordance1,concordance2):
		relevance = 0
		topvalue = 0
		for word,count in concordance1.items():
			if word in concordance2:
				topvalue += count * concordance2[word]
		return topvalue/(self.magnitude(concordance1)*self.magnitude(concordance2))


#得到图片每一个像素的值并构建一个行向量存储
def buildvector(im):
	d1 = {}
	count = 0
	for i in im.getdata():
		d1[count] = i
		count += 1
	return d1


iconset = ['0','1','2','3','4','5','6','7','8','9','0','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

imageset = []

#将素材里面的1-z的GIF变成一串长的行向量存入imageset里面
for letter in iconset:
	for img in os.listdir('./iconset/%s/'%(letter)):
		temp = []
		if img != "Thumbs.db" and img != ".DS_Store":
			temp.append(buildvector(Image.open("./iconset/%s/%s"%(letter,img))))
		imageset.append({letter:temp})

#打开目标gif
im = Image.open('./examples/0q3tje.gif')

#转换为8位像素模式
im.convert('P')
'''
#列出颜色直方图
his = im.histogram()
values={}

for i in range(256):
	values[i]=his[i]
	
#列出出现最多的十种颜色
for j,k in sorted(values.items(),key=lambda x:x[1],reverse = True)[:10]:
	print （j，k）
'''
#新建一个Image纯白色对象
im2 = Image.new('P', im.size, 255)


#for将图片的别的颜色去掉只留红色和灰色代表数字
for y in range(im.size[1]):
	for x in range(im.size[0]):
		pix = im.getpixel((x,y))

		#只需要红色220和灰色227
		if pix == 220 or pix == 227:
			#将目标的红色和灰色点用黑色画在im2上
			im2.putpixel((x,y),0)

#将图上每个字符分割开
inletter = False
foundletter = False
start = 0
end = 0
letters = []
for x in range(im2.size[0]):
	for y in range(im2.size[1]):
		pix = im2.getpixel((x,y))
		#不是白色代表是字符
		if pix != 255:
			inletter = True
	#找到第一个字符记录start
	if foundletter == False and inletter == True:
		foundletter = True
		start = x
	#找到start后面第一个不是字符的项，记录end
	if foundletter == True and inletter == False:
		foundletter = False
		end = x
		letters.append((start,end))

	inletter = False


#新建一个类实例
v = VectorCompare()

#letters是分割好的（start，end）元组
for letter in letters:
	#m = hashlib.md5()
	#根据im2的分割将每个字单独拿出来
	im3 = im2.crop((letter[0],0,letter[1],im2.size[1]))
		#m.update("%s%s"%(time.time(),count))
		#im3.save("./%s.gif"%(m.hexdigest()))
		#count += 1
	guess = []
	for image in imageset:
		for x,y in image.items():
			if len(y) != 0:
				guess.append((v.relation(y[0],buildvector(im3)),x))
	guess.sort(reverse=True)	
	print ("",guess[0])
