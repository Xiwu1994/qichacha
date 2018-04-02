# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class DmozItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()
    pass

class QichachaItem(scrapy.Item):
    # define the fields for your item here like:

    company_unique = scrapy.Field()
    detail_base_url = scrapy.Field()
    detail_run_url = scrapy.Field()

    yn_company_name = scrapy.Field() # 云鸟公司名称
    yn_company_name_hash_code = scrapy.Field()  # 云鸟公司名称hash code
    qcc_company_name = scrapy.Field() # 企查查公司名称
    company_addr = scrapy.Field()  # 公司地址
    headquarters_city_name = scrapy.Field()  # 总部所在城市
    establishment_time = scrapy.Field()  # 成立时间
    working_time = scrapy.Field()  # 成立年限
    registered_money = scrapy.Field()  # 注册资本
    industry_name = scrapy.Field()  # 所属行业
    company_nature = scrapy.Field()  # 公司性质
    work_city_num = scrapy.Field()  # 业务城市列表
    staff_num = scrapy.Field()  # 员工数
    recruitment_num = scrapy.Field()  # 招聘岗位数

    listing_situation = scrapy.Field()  # 上市情况
    financing_situation = scrapy.Field()  # 融资情况
    financing_last_time_money = scrapy.Field()  # 融资总额
    company_valuation = scrapy.Field()  # 公司估值
    # revenue_scale = scrapy.Field()  # 营收规模
    scope_operation = scrapy.Field()  # 经营范围

    competence_level = scrapy.Field()  # 公司实力等级
    net_profit_rate = scrapy.Field() # 销售净利润率
    tax_zone = scrapy.Field() # 纳税区间
    profit_rate = scrapy.Field() # 销售毛利率
    tax_credit_level = scrapy.Field() # 纳税信用等级
    pass
