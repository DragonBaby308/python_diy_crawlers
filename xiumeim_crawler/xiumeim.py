import urllib.request
import urllib.error
from lxml import html

def get_html(url):
  '输入URL，获取HTML'
  # 浏览器伪装
  headers = ("User-Agent", "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36")
  opener = urllib.request.build_opener()
  opener.addheaders = [headers]
  # 将opener安装为全局
  urllib.request.install_opener(opener)

  # 获取HTML
  try:
    data = urllib.request.urlopen(url).read().decode("utf-8")
  except urllib.error.URLError as e:
    if hasattr(e,"code"):
      print(e.code)
    if hasattr(e,"reason"):
      print(e.reason)
  finally:
    return data

# 拿到4 x 6个子URL
data = get_html("http://www.xiumeim.com")
sub_urls = html.etree.HTML(data).xpath('//span[@class="name"]/a[@class="photosUrl"]/@href')
# 处理每个子URL
for h in range(len(sub_urls) ):
  # print(sub_urls[h])
  sub_data = get_html(sub_urls[h])
  # print(sub_data)
  # print("--------------------------------------")
  # 爬第一页图片
  pic_urls = html.etree.HTML(sub_data).xpath('//img[@class="photosImg"]/@src')
  # 下载24个URL第一页的每一张图片
  for i in range(len(pic_urls) ):
    response = urllib.request.urlopen(pic_urls[i])
    img = response.read()
    # with语句可以保证文件操作的安全性
    with open('D://python/little_sister_too_poor_to_afford_clothes/' + str(h+1) + '-' + str(i+1) + '.jpg', 'wb') as f:
      f.write(img)
