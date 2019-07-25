from pyecharts import Map, Geo

# maptype='china' 只显示全国直辖市和省级
# 数据只能是省名和直辖市的名称
map = Map("尿素",'尿素市价分布图', width=1200, height=800)
province_distribution = {
'山东':   1970,
'江苏':   1980,
'安徽':   1980,
'河南':   1920,
'湖南':   2000,
'湖北':   1970,
'河北':   1910,
'山西':   1800,
'黑龙江': 1950,
'吉林':   2050,
'辽宁':   1820,
'新疆':   1800,
'宁夏':   1720,
'青海':   1800,
'甘肃':   1940,
'陕西':   1850,
'内蒙古': 1700,
'云南':   2100,
'贵州':   2050,
'四川':   1960,
'广东':   2080,
'广西':   1980,
'福建':   2000
 }
list1 = [v for k,v in province_distribution.items()]
provice=list(province_distribution.keys())
values=list(province_distribution.values())
map.add("", provice, values, visual_range=[min(list1), max(list1)],  maptype='world', is_visualmap=True,is_label_show=True,
    visual_text_color='#000')
map.show_config()
map.render(path="nsMap.html")