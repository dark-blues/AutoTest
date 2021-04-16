# -*- coding: utf-8 -*-
"""
@author: ZJ
@email: 1576094876@qq.com
@File : Page.py
@desc: 
@Created on: 2021/4/2 10:08
"""
#
from Base.PublicFunc import GetPoco

class FindPage():
    songlist_ele = ("text","歌单") # 歌单元素
    # 歌单页面内的元素
    recommend_ele = ("text","推荐") # 推荐元素
    official_ele = ("text","官方") # 官方元素
    video_ele = ("text","视频歌单") # 视频歌单元素

    ranklist_ele = ("text","排行榜")  # 排行榜元素

    search_ele = ("name","com.netease.cloudmusic:id/searchBar") # 搜索框元素

    dayrecommend_ele = (1,"每日推荐") # 每日推荐元素
    # 每日推荐页面内的元素
    actual_day_ele= (2,"com.netease.cloudmusic:id/dayRecommendDateInfo") # 当前天元素
    play_all_ele = (2,"com.netease.cloudmusic:id/playAllTextView") # 播放全部按钮元素

    @staticmethod
    def first_song_ele():#推荐页面第一首歌的元素
        return GetPoco.poco("android.widget.LinearLayout").offspring("com.netease.cloudmusic:id/pagerListview").child(
            "com.netease.cloudmusic:id/musicListItemContainer")[0].offspring("com.netease.cloudmusic:id/songName")

    song_title_ele = (2,"com.netease.cloudmusic:id/custom_title") # 歌曲详情页面标题元素
