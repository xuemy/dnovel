# Scrapy settings for novelspider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy-0.16.org/topics/settings.html
#

#BOT_NAME = 'novelspider'
#
#SPIDER_MODULES = ['novelspider.spiders']
#NEWSPIDER_MODULE = 'novelspider.spiders'
#ITEM_PIPELINES = [
#        'novelspider.pipelines.NovelspiderPipeline'
#        ]
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'novelspider (+http://www.yourdomain.com)'
#def setup_django_env(path):
#    import imp, os
#    from django.core.management import setup_environ
#
#    f, filename, desc = imp.find_module('settings', [path])
#    project = imp.load_module('settings', f, filename, desc)
#
#    setup_environ(project)
#setup_django_env('../../dnovel')

ITEM_PIPELINES=['zhizhu.pipelines.CollectionPipeline',]