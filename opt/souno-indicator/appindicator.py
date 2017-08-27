#!/usr/bin/env python3
# coding:utf-8


import os
import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,GLib,GObject
gi.require_version('AppIndicator3', '0.1')
from gi.repository import AppIndicator3
import weatherinfo
import time
gi.require_version('Notify', '0.7')
from gi.repository import Notify


class AppIndicatorWeather:
    def __init__(self, indicator_id):
        self.ind = AppIndicator3.Indicator.new("天气", os.path.split(os.path.realpath(__file__))[0]+'/weather.svg',AppIndicator3.IndicatorCategory.SYSTEM_SERVICES)
        self.ind.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.frist_refresh()
        try:
            fp = open(os.environ['HOME']+"/.config/Souno/indicator/autoupdate.cfg", "r")
        except FileNotFoundError:
            isExists = os.path.exists(os.environ['HOME'] + "/.config/Souno/indicator")
            if not isExists:
                os.makedirs(os.environ['HOME'] + "/.config/Souno/indicator")
            fp = open(os.environ['HOME'] + "/.config/Souno/indicator/autoupdate.cfg", "w+")
            fp.write('0')
        ind_cfg = fp.read(1)
        if ind_cfg == '1':
            self.check_item.set_active(True)
        else:
            self.check_item.set_active(False)
        fp.close()


    def frist_refresh(self):
        # 调用天气模块获取天气信息
        wea_info = weatherinfo.get_wea()
        wea_info = eval(wea_info)

        # 创建菜单项
        self.menu = Gtk.Menu()
        self.name_item = Gtk.MenuItem("Souno天气指示器")
        self.name_item.show()
        self.menu.append(self.name_item)
        self.sep_item = Gtk.SeparatorMenuItem()
        self.sep_item.show()
        self.menu.append(self.sep_item)
        self.check_item = Gtk.CheckMenuItem("自动更新")
        self.check_item.connect("activate", self.autoupdate)
        self.check_item.show()
        self.menu.append(self.check_item)
        self.sep_item = Gtk.SeparatorMenuItem()
        self.sep_item.show()
        self.menu.append(self.sep_item)
        self.wea_item = Gtk.MenuItem("天气：" + wea_info['weatherinfo']['weather'])
        self.wea_item.show()
        self.menu.append(self.wea_item)
        self.temp_item = Gtk.MenuItem("温度：" + wea_info['weatherinfo']['ntemp'])
        self.temp_item.show()
        self.menu.append(self.temp_item)
        self.jian_item = Gtk.MenuItem("区间：" + wea_info['weatherinfo']['temp1'] + '~' + wea_info['weatherinfo']['temp2'])
        self.jian_item.show()
        self.menu.append(self.jian_item)
        self.fengl_item = Gtk.MenuItem("风力：" + wea_info['weatherinfo']['fengli'])
        self.fengl_item.show()
        self.menu.append(self.fengl_item)
        self.fengx_item = Gtk.MenuItem("风向：" + wea_info['weatherinfo']['fengxiang'])
        self.fengx_item.show()
        self.menu.append(self.fengx_item)
        self.place_item = Gtk.MenuItem("地点：" + wea_info['weatherinfo']['city'])
        self.place_item.show()
        self.menu.append(self.place_item)
        self.time_item = Gtk.MenuItem("更新：" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        self.time_item.show()
        self.menu.append(self.time_item)
        self.sep_item = Gtk.SeparatorMenuItem()
        self.sep_item.show()
        self.menu.append(self.sep_item)
        self.aur_item = Gtk.MenuItem("关于")
        self.aur_item.connect("activate", self.onabout)
        self.aur_item.show()
        self.menu.append(self.aur_item)

        self.image = Gtk.ImageMenuItem("退出")
        self.image.connect("activate", self.quit)
        self.image.show()
        self.menu.append(self.image)
        self.menu.show()
        self.ind.set_menu(self.menu)
        # 显示状态信息标签
        #self.ind.set_label(str(wea_info['weatherinfo']['ntemp']), "")


    def autoupdate(self, widget):
        fp = open(os.environ['HOME'] + "/.config/Souno/indicator/autoupdate.cfg", "w")
        if self.check_item.get_active():
            fp.write('1')
            self.get_refresh()
        else:
            fp.write('0')
            GObject.source_remove(self.timer_id)
        fp.close()





    def get_refresh(self):
        wea_info = weatherinfo.get_wea()
        wea_info = eval(wea_info)
        self.wea_item.get_child().set_text("天气：" + wea_info['weatherinfo']['weather'])
        self.temp_item.get_child().set_text("温度：" + wea_info['weatherinfo']['ntemp'])
        self.jian_item.get_child().set_text("区间：" + wea_info['weatherinfo']['temp1'] + '~' + wea_info['weatherinfo']['temp2'])
        self.fengl_item.get_child().set_text("风力：" + wea_info['weatherinfo']['fengli'])
        self.fengx_item.get_child().set_text("风向：" + wea_info['weatherinfo']['fengxiang'])
        self.place_item.get_child().set_text("地点：" + wea_info['weatherinfo']['city'])
        self.time_item.get_child().set_text("更新：" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        self.notice()
        self.timer_id = GObject.timeout_add(300000, self.get_refresh)



    def quit(self, widget):
        sys.exit()


    def notice(self):
        Notify.init('天气')
        n = Notify.Notification.new('Souno天气指示器', '最新天气信息已更新！', 'indicator-weather')
        n.show()
        Notify.uninit()



    def onabout(self,widget):
        widget.set_sensitive(False)
        ad=Gtk.AboutDialog()
        ad.set_logo_icon_name('indicator-weather')
        ad.set_name("关于")
        ad.set_program_name("Souno天气指示器")
        ad.set_version("0.1")
        ad.set_copyright('Copyrignt (c) 2017 Souno.cc')
        ad.set_comments('Souno.cc')
        ad.set_license(''+
        '本程序是在GNU通用公共许可证的条款下发布的自由软件你可以重新分配/修改。\n\n'+
        '本程序的发布是为了给大家提供一个有用的功能，并且希望它越来越好用，\n但作者本人不提供任何担保；甚至没有任何适当性的默示保证或规定适用于某一特定目的。\n具体情形请参照GNU通用公共授权里面的更多的细节。\n\n'+
        '你也应该同样遵循GNU通用公共许可证\n'+
        '当你使用这个程序。需要了解更多授权信息，请看 <http://www.gnu.org/licenses/>.')
        ad.set_website('https://Souno.cc')
        ad.set_website_label('访问Souno.cc主页')
        ad.set_authors(['Shenya|Yexing <88459122@qq.com>'])
        ad.set_documenters(['fred_hu <huu_007@qq.com>'])
        ad.run()
        ad.destroy()
        widget.set_sensitive(True)

if __name__ == "__main__":
    indicator = AppIndicatorWeather(1)
    Gtk.main()