# -*- coding: utf-8 -*-
"""
@author: ZJ
@email: 1576094876@qq.com
@File : TestFind.py
@desc: 
@Created on: 2021/3/30 14:10
"""

from airtest.core.api import *
import unittest
from Base.BaseSettings import PictureDIR
from Base.PublicFunc import SetUpClass, get_parameter



class TestFind(SetUpClass):
    #
    # @get_parameter(__file__,"dayrecommend",casedesc="测试每日推荐",author="zs",title="报告")
    # def test_dayrecommend(self,):
    #     self.poco(text="每日推荐").click()
    #     actual_day = self.poco("com.netease.cloudmusic:id/dayRecommendDateInfo").get_text()
    #
    #     # 获取到当前系统的真实日期
    #     real_day = time.strftime("%d", time.localtime(time.time()))
    #     print(actual_day, real_day)
    #     assert_equal(actual_day, real_day, )
    #
    #     # assert_exists(Template(r"tpl1617070361566.png", record_pos=(-0.324, -0.456), resolution=(1080, 2340)), "请填写测试点")
    #     res = self.poco("com.netease.cloudmusic:id/playAllTextView").exists()
    #     assert_equal(res, True)
    #     actual_songname = \
    #     self.poco("android.widget.LinearLayout").offspring("com.netease.cloudmusic:id/pagerListview").child(
    #         "com.netease.cloudmusic:id/musicListItemContainer")[0].offspring("com.netease.cloudmusic:id/songName").attr(
    #         "text")
    #     print(actual_songname)
    #
    #     self.poco("android.widget.LinearLayout").offspring("com.netease.cloudmusic:id/pagerListview").child(
    #         "com.netease.cloudmusic:id/musicListItemContainer")[0].offspring(
    #         "com.netease.cloudmusic:id/songName").click()
    #
    #     expect_song_name = self.poco("com.netease.cloudmusic:id/custom_title").attr("text")
    #     assert_equal(actual_songname, expect_song_name)
    #     assert_exists(Template(PictureDIR+"tpl1617070761207.png", record_pos=(0.0, 0.956), resolution=(1080, 2340)), )

    @get_parameter(__file__, "FM",casedesc="测试私人FM",title="privte_FM",author="张三")
    def test_FM(self):
        self.poco(text="私人FM").click()
        assert_exists(Template(PictureDIR + "tpl1617070761207.png", record_pos=(0.0, 0.956), resolution=(1080, 2340)), )


    @get_parameter(__file__, "songlist", casedesc="测试歌单",author="李四")
    def test_songlist(self):
        self.poco(text="歌单").click()
        res = self.poco(text="推荐").exists() and self.poco(text="官方").exists() and self.poco(text="视频歌单").exists()
        assert_equal(res,True,"判断是否进入歌单页面")

    @get_parameter(__file__, "ranklist", casedesc="测试排行榜")
    def test_ranklist(self):
        self.poco(text="排行榜").click()
        assert_exists(Template(PictureDIR +"tpl1617155622747.png", record_pos=(-0.312, -0.693), resolution=(1080, 2340)), "请填写测试点")
    #
    # @get_parameter(__file__, "search",casedesc="测试搜素", author="ls")
    # def test_search(self):
    #     self.poco("com.netease.cloudmusic:id/searchBar").click()
    #     text("沉默是金")
    #     time.sleep(2)
    #     expect = "张国荣 - Ultimate "
    #     assert_equal(self.poco(text=expect).exists(),True)
    #     self.poco(text=expect).click()
    #     # 判断能否正常播放
    #     assert_exists(Template(PictureDIR + "tpl1617070761207.png", record_pos=(0.0, 0.956), resolution=(1080, 2340)), )
    #     # 判断是否收藏  没有收藏 就进行点击
    #     if exists(Template(PictureDIR +"tpl1617159233147.png", record_pos=(-0.356, 0.708), resolution=(1080, 2340))):
    #         self.poco("com.netease.cloudmusic:id/likeBtn").click()
    #
    #     keyevent("BACK")
    #     keyevent("BACK")
    #     keyevent("BACK")
    #
    #     self.poco(text="我的").click()
    #     self.poco("com.netease.cloudmusic:id/name").click()
    #     assert_equal(self.poco(text=expect).exists(),True)
    #     keyevent("BACK")
    #     self.poco(text="发现").click()

if __name__ == '__main__':

    unittest.main()