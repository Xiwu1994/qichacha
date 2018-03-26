import torndb
import random
import requests
import urllib

mysql_port = "3327"
mysql_user = "bi"
mysql_host = "beeper2_bi.write.3327.mysql.prod.yn.cn"
mysql_passwd = "beeper_bi_Production"
mysql_database = "beeper2_bi"



mysql_port = "3306"
mysql_user = "ynapp"
mysql_host = "192.168.203.16"
mysql_passwd = "ynapppass"


# redis_host="192.168.0.29"
# redis_port=6422
#
# r = redis.Redis(redis_host, redis_port)

def process():
    conn = torndb.Connection("%s:%s" % (mysql_host, mysql_port), mysql_database, user=mysql_user, password=mysql_passwd)
    driver_id = 2000004
    driver_list = []
    for i in xrange(1500):
        driver_list.append([driver_id])
        driver_id += 1

    sql = "update bigdata_realtime_trans_driver_live_position set speed=666 where driver_id=%s"
    conn.insertmany(sql, driver_list)



def get_proxy_ip():
    order = "9185a90f4d399f88c0cb3dbb6de084a1"
    apiUrl = "http://dynamic.goubanjia.com/dynamic/get/" + order + ".html"

    res = urllib.urlopen(apiUrl).read().strip("\n")
    ips = res.split("\n")
    return random.choice(ips)

def process():
    proxy_flag = True
    url = "http://www.qichacha.com/search?key=%E5%8C%97%E4%BA%AC%E9%87%91%E6%B5%B7%E6%89%AC%E5%B8%86%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8"
    headers = {
        "Host": "www.qichacha.com",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
        "Cookie": "UM_distinctid=15fec0cb23e22-011c396f402b69-173f6d55-13c680-15fec0cb23f995; _uab_collina=151149377611443635838717; zg_did=%7B%22did%22%3A%20%2215fec0cb2271f1-05151bf9c91987-173f6d55-13c680-15fec0cb2298bb%22%7D; PHPSESSID=pnh69c5ddf61e6gbf10ba6efm1; _umdata=6AF5B463492A874DC4153C4CC15B118E116721C6C576D3AA29A8E60A198A4D7C0277982C901A511ACD43AD3E795C914C3E590067E2B27CC5BD26DA836427384C; hasShow=1; acw_tc=AQAAAA7WpFkOTQIA6pVtO1xgIm5qfhlc; CNZZDATA1254842228=778431658-1511493319-%7C1521983598; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1521776057,1521956853,1521969718,1521987067; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1521987817; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201521987066516%2C%22updated%22%3A%201521987824038%2C%22info%22%3A%201521426085018%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22cuid%22%3A%20%2231d2666d27a6739e060c60c767f8e6a7%22%7D"
    }
    if proxy_flag:
        proxyip = get_proxy_ip()
        print "proxyip: ", proxyip
        respones = requests.get(url, headers=headers, proxies={'http':'http://' + proxyip})
    else:
        respones = requests.get(url, headers=headers)
    print respones


# process()
