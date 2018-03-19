# -*- coding: utf-8 -*-

import re
import time
import torndb
import scrapy
import hashlib
from qichacha.items import QichachaItem
from scrapy.exceptions import CloseSpider
URL_PRE = "http://www.qichacha.com"
md5_handle = hashlib.md5()

class DmozSpider(scrapy.spiders.Spider):
    name = "qichacha"
    allowed_domains = ["www.qichacha.com"]
    customer_company_name_path = "/Users/liebaomac/PycharmProjects/qichacha/customer_company_name"
    client = torndb.Connection("192.168.203.16:3306", "beeper2_bi", user="ynapp", password="ynapppass")

    def start_requests(self):
        # main run
        customer_company_name_list = self.read_customer_company_name()
        for customer_company_name in customer_company_name_list:
            item = QichachaItem()
            item["yn_company_name"] = customer_company_name
            md5_handle.update(customer_company_name)
            item['yn_company_name_hash_code'] = md5_handle.hexdigest()
            # 如果没有存在mysql库里
            if not self.query_company_exits(item['yn_company_name_hash_code']):
                url = "http://www.qichacha.com/search?key=%s" % (customer_company_name)
                yield scrapy.Request(url, dont_filter=True, meta={'item': item})
            else:
                print "%s already in mysql" %(customer_company_name)

    def parse(self, response):
        # select one company
        item = response.meta['item']
        sel = response.xpath('//a[re:test(@href, "firm_.*.html")]')[0]
        company_name = ''.join(sel.xpath('.//text()').extract())
        m = re.match(r'(/firm_)(.*)(.html)', sel.xpath('./@href').extract()[0])
        if m is not None:
            company_unique = m.group(2)
            item['company_unique'] = company_unique
            item['qcc_company_name'] = company_name
            detail_url = "%s/company_getinfos?unique=%s&companyname=%s&tab=%s"
            item['detail_base_url'] = detail_url % (URL_PRE, item['company_unique'], item['qcc_company_name'], "base")
            item['detail_run_url'] = detail_url % (URL_PRE, item['company_unique'], item['qcc_company_name'], "run")
            yield scrapy.Request(item['detail_base_url'], dont_filter=True, meta={'item': item},
                                 headers=response.request.headers,
                                 callback=self.parse_company_base_detail)

    def parse_company_base_detail(self, response):
        """
        获取企业基础信息
        """
        item = response.meta['item']
        item["company_addr"] = self.get_xpath_info(response, '//*[@id="Cominfo"]/table[2]/tr[10]/td[2]/text()') # 公司地址
        item["headquarters_city_name"] = self.get_xpath_info(response, '//*[@id="Cominfo"]/table[2]/tr[7]/td[2]/text()') # 总部所在城市
        item["establishment_time"] = self.get_xpath_info(response, '//*[@id="Cominfo"]/table[2]/tr[2]/td[4]/text()') # 成立时间
        try:
            # 成立年限 需要用时间函数
            item["working_time"] = (time.time() - time.mktime(time.strptime(item["establishment_time"], "%Y-%m-%d"))) / 31536000
        except:
            item["working_time"] = 0  # 成立年限
        item["registered_money"] = self.get_xpath_info(response, '//*[@id="Cominfo"]/table[2]/tr[1]/td[2]/text()') # 注册资本
        item["industry_name"] = self.get_xpath_info(response, '//*[@id="Cominfo"]/table[2]/tr[5]/td[4]/text()') # 所属行业
        item["company_nature"] = self.get_xpath_info(response, '//*[@id="Cominfo"]/table[2]/tr[5]/td[2]/text()')  # 公司性质
        item["staff_num"] = self.get_xpath_info(response, '//*[@id="Cominfo"]/table[2]/tr[9]/td[2]/text()')  # 员工数
        item["scope_operation"] = self.get_xpath_info(response, '//*[@id="Cominfo"]/table[2]/tr[11]/td[2]/text()')  # 经营范围
        item["work_city_list"] = " + ".join(self.get_xpath_info(branch_name, './td[2]/a/span/text()') for branch_name in
                                            response.xpath('//*[@id="Subcom"]/table/tr')) # 业务城市列表(分支机构)
        yield scrapy.Request(item['detail_run_url'], dont_filter=True, meta={'item': item},
                             headers=response.request.headers,
                             callback=self.parse_company_run_detail)

    def parse_company_run_detail(self, response):
        """
        获取企业经营信息
        """
        item = response.meta['item']
        listing_situation = self.get_xpath_info(response, '//*[@id="financingList"]/table/tr[2]/td[4]/text()')  # 上市or融资情况
        if listing_situation == u"IPO":
            item["listing_situation"] = u"上市"
        else:
            item["listing_situation"] = u"未上市"
            item["financing_situation"] = listing_situation # 融资情况
        # item["financing_all_money"] = " + ".join(
        #     self.get_xpath_info(financing_turn, './td[5]/text()') for financing_turn in
        #     response.xpath('//*[@id="financingList"]/table/tr')[1:]) # 融资总额
        item["financing_last_time_money"] = self.get_xpath_info(response, '//*[@id="financingList"]/table/tr[1]/td[5]/text()') # 最近一次融资总额
        item["recruitment_num"] = self.get_xpath_info(response, '//*[@id="joblist"]/div[1]/span[2]/text()')  # 招聘岗位数
        # 公司估值 企名片
        item["company_valuation"] = ""
        # 营收规模
        # item["revenue_scale"] = ""

        item["competence_level"] = self.get_xpath_info(response, '//*[@id="V3_cwzl"]/table/tr[1]/td[2]/text()')  # 公司实力等级
        item["net_profit_rate"] = self.get_xpath_info(response, '//*[@id="V3_cwzl"]/table/tr[2]/td[2]/text()') # 销售净利润率
        item["tax_zone"] = self.get_xpath_info(response, '//*[@id="V3_cwzl"]/table/tr[1]/td[4]/text()') # 纳税区间
        item["profit_rate"] = self.get_xpath_info(response, '//*[@id="V3_cwzl"]/table/tr[2]/td[4]/text()') # 销售毛利率
        item["tax_credit_level"] = self.get_xpath_info(response, '//*[@id="taxCreditList"]/table/tr[3]/td[4]/text()') # 纳税信用等级 A
        return item

    def read_customer_company_name(self):
        with open(self.customer_company_name_path, 'r') as fp:
            customer_company_name_list = [line.strip() for line in fp]
        return customer_company_name_list

    def check_need_verify(self, response):
        """
        登录或验证码验证
        :param response:
        """
        # inspect_response(response, self)
        request_url = response.request.url
        self.logger.info("check_need_verify: " + request_url)
        m = re.search(r"user_login", request_url)
        if m:
            raise CloseSpider('need user_login')
            # sys.exit('need user_login')
            # os.abort()

        # <script>window.location.href='http://www.qichacha.com/index_verify?type=companysearch&back=/search?key=%E7%89%A9%E6%B5%81&ajaxflag=1&p=1&';</script>
        m = re.search(r"window.location.href.*index_verify\?", response.body)
        if m:
            raise CloseSpider('need index_verify')

    @staticmethod
    def get_xpath_info(response, xpath_str):
        """
        去除空格和\t
        """
        return response.xpath('normalize-space(%s)' % (xpath_str)).extract_first()

    def query_company_exits(self, yn_company_name_hash_code):
        return len(self.client.query(
            "select 1 from customer_company_extended_info_from_qichacha where yn_company_name_hash_code='%s'" % (
                yn_company_name_hash_code)))
