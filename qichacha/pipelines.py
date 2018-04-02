# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import torndb

column_list = ['company_unique','company_status','detail_base_url','detail_run_url','qcc_company_name','company_addr',
               'headquarters_city_name','establishment_time','working_time','registered_money','industry_name','company_nature',
               'work_city_num','staff_num','recruitment_num','listing_situation','financing_situation','financing_last_time_money',
               'company_valuation','scope_operation','competence_level','net_profit_rate','tax_zone','profit_rate','tax_credit_level']
insert_sql = "insert into customer_company_extended_info_from_qichacha_2(%s) values (%s)" %(",".join(column_list), ",".join(["%s"] * len(column_list)))

class MysqlPipeline(object):
    def __init__(self):
        # self.mysql_host = "192.168.203.16"
        # self.mysql_port = "3306"
        # self.mysql_user = "ynapp"
        # self.mysql_password = "ynapppass"
        self.mysql_host = "localhost"
        self.mysql_port = "3306"
        self.mysql_user = "root"
        self.mysql_password = "root"
        self.mysql_database = "beeper2_bi"
        self.client = torndb.Connection("%s:%s" % (self.mysql_host, self.mysql_port), self.mysql_database,
                                        user=self.mysql_user, password=self.mysql_password)

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        print "insert_sql: ", insert_sql
        print "INSERT VALUES: ", [item[column] for column in column_list]
        self.client.insertmany(insert_sql, [[item[column] for column in column_list]])
        return item
