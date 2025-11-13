#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
巡检自动化Android应用
基于Kivy框架开发的Android应用，集成原始巡检脚本功能
"""

import os
import json
import random
from datetime import datetime, timedelta
import re
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import StringProperty, ListProperty
import threading

class LoginScreen(Screen):
    """登录界面"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'login'
        self.build_ui()
    
    def build_ui(self):
        """构建登录界面UI"""
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        
        # 标题
        title = Label(
            text='SYSTEM',
            font_size='24sp',
            size_hint_y=None,
            height=60,
            color=(0.2, 0.6, 0.8, 1)
        )
        layout.add_widget(title)
        
        # 用户名输入
        username_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=80)
        username_layout.add_widget(Label(text='用户名 (Username):', size_hint_y=None, height=30))
        self.username_input = TextInput(
            multiline=False,
            size_hint_y=None,
            height=50,
            font_size='16sp'
        )
        username_layout.add_widget(self.username_input)
        layout.add_widget(username_layout)
        
        # 用户代码输入
        usercode_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=80)
        usercode_layout.add_widget(Label(text='用户代码 (Usercode):', size_hint_y=None, height=30))
        self.usercode_input = TextInput(
            multiline=False,
            size_hint_y=None,
            height=50,
            font_size='16sp'
        )
        usercode_layout.add_widget(self.usercode_input)
        layout.add_widget(usercode_layout)
        
        # 默认密码输入
        password_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=80)
        password_layout.add_widget(Label(text='默认密码:', size_hint_y=None, height=30))
        self.password_input = TextInput(
            multiline=False,
            password=True,
            size_hint_y=None,
            height=50,
            font_size='16sp'
        )
        password_layout.add_widget(self.password_input)
        layout.add_widget(password_layout)
        
        # 登录按钮
        login_button = Button(
            text='登录',
            size_hint_y=None,
            height=60,
            font_size='18sp',
            background_color=(0.2, 0.6, 0.8, 1),
            color=(1, 1, 1, 1)
        )
        login_button.bind(on_press=self.login)
        layout.add_widget(login_button)
        
        # 状态标签
        self.status_label = Label(
            text='',
            size_hint_y=None,
            height=40,
            color=(1, 0, 0, 1)
        )
        layout.add_widget(self.status_label)
        
        self.add_widget(layout)
    
    def login(self, instance):
        """处理登录逻辑"""
        username = self.username_input.text.strip()
        usercode = self.usercode_input.text.strip()
        password = self.password_input.text.strip()
        
        # 验证输入
        if not username:
            self.status_label.text = '用户名不能为空'
            return
        
        if not usercode:
            self.status_label.text = '用户代码不能为空'
            return
        
        if password != '12138':
            self.status_label.text = '默认密码错误'
            return
        
        # 登录成功，保存用户信息并切换到主界面
        app = App.get_running_app()
        app.user_info = {
            'username': username,
            'usercode': usercode
        }
        
        self.manager.current = 'main'

class MainScreen(Screen):
    """主操作界面"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'main'
        self.log_text = ""
        self.build_ui()
    
    def build_ui(self):
        """构建主界面UI"""
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 顶部信息栏
        info_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        self.user_label = Label(text='', size_hint_x=0.7)
        logout_button = Button(text='退出登录', size_hint_x=0.3)
        logout_button.bind(on_press=self.logout)
        info_layout.add_widget(self.user_label)
        info_layout.add_widget(logout_button)
        layout.add_widget(info_layout)
        
        # 数据目录选择
        dir_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=80)
        dir_layout.add_widget(Label(text='数据目录路径:', size_hint_y=None, height=30))
        self.dir_input = TextInput(
            text='/storage/emulated/0/widgetone/apps/NormalPIM/data',
            multiline=False,
            size_hint_y=None,
            height=50,
            font_size='14sp'
        )
        dir_layout.add_widget(self.dir_input)
        layout.add_widget(dir_layout)
        
        # 操作按钮
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=60, spacing=10)
        
        self.start_button = Button(
            text='开始巡检',
            font_size='16sp',
            background_color=(0.2, 0.8, 0.2, 1),
            color=(1, 1, 1, 1)
        )
        self.start_button.bind(on_press=self.start_inspection)
        
        self.stop_button = Button(
            text='停止',
            font_size='16sp',
            background_color=(0.8, 0.2, 0.2, 1),
            color=(1, 1, 1, 1),
            disabled=True
        )
        self.stop_button.bind(on_press=self.stop_inspection)
        
        button_layout.add_widget(self.start_button)
        button_layout.add_widget(self.stop_button)
        layout.add_widget(button_layout)
        
        # 日志显示区域
        log_layout = BoxLayout(orientation='vertical', size_hint_y=0.7)
        log_layout.add_widget(Label(text='执行日志:', size_hint_y=None, height=30))
        
        # 滚动视图
        scroll_view = ScrollView()
        self.log_label = Label(
            text='',
            size_hint_y=None,
            height=400,
            text_size=(Window.width - 40, None),
            valign='top',
            halign='left',
            color=(0.1, 0.1, 0.1, 1)
        )
        scroll_view.add_widget(self.log_label)
        log_layout.add_widget(scroll_view)
        layout.add_widget(log_layout)
        
        self.add_widget(layout)
    
    def on_pre_enter(self):
        """进入界面前的准备工作"""
        app = App.get_running_app()
        if hasattr(app, 'user_info'):
            self.user_label.text = f"用户: {app.user_info['username']}"
    
    def logout(self, instance):
        """退出登录"""
        app = App.get_running_app()
        app.user_info = {}
        self.manager.current = 'login'
        
        # 清空输入框
        login_screen = self.manager.get_screen('login')
        login_screen.username_input.text = ''
        login_screen.usercode_input.text = ''
        login_screen.password_input.text = ''
        login_screen.status_label.text = ''
    
    def start_inspection(self, instance):
        """开始巡检"""
        data_dir = self.dir_input.text.strip()
        
        if not os.path.exists(data_dir):
            self.update_log(f"错误: 数据目录不存在: {data_dir}")
            return
        
        # 禁用开始按钮，启用停止按钮
        self.start_button.disabled = True
        self.stop_button.disabled = False
        
        # 清空日志
        self.log_text = ""
        self.update_log("=== 开始执行自动化 ===")
        
        # 在新线程中运行巡检任务
        self.inspection_thread = threading.Thread(target=self.run_inspection, args=(data_dir,))
        self.inspection_thread.daemon = True
        self.inspection_thread.start()
    
    def stop_inspection(self, instance):
        """停止巡检"""
        self.update_log("=== 任务已停止 ===")
        self.start_button.disabled = False
        self.stop_button.disabled = True
    
    def run_inspection(self, data_dir):
        """运行巡检自动化"""
        try:
            app = App.get_running_app()
            automation = InspectionAutomation(data_dir, app.user_info, self)
            success = automation.run_inspection()
            
            Clock.schedule_once(lambda dt: self.on_inspection_complete(success), 0)
        except Exception as e:
            Clock.schedule_once(lambda dt: self.update_log(f"执行出错: {str(e)}"), 0)
            Clock.schedule_once(lambda dt: self.on_inspection_complete(False), 0)
    
    def on_inspection_complete(self, success):
        """巡检完成后的处理"""
        self.start_button.disabled = False
        self.stop_button.disabled = True
        
        if success:
            self.update_log("\n===自动化完成 ===")
        else:
            self.update_log("\n=== 自动化失败 ===")
    
    def update_log(self, message):
        """更新日志显示"""
        self.log_text += message + "\n"
        self.log_label.text = self.log_text
        # 自动滚动到底部
        self.log_label.height = len(self.log_text.split('\n')) * 20

class InspectionAutomationApp(App):
    """主应用类"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_info = {}
        self.title = 'SYSTEM'
    
    def build(self):
        """构建应用界面"""
        # 设置窗口大小（移动设备上会自动调整）
        Window.size = (400, 600)
        
        # 创建屏幕管理器
        sm = ScreenManager()
        
        # 添加登录界面
        login_screen = LoginScreen()
        sm.add_widget(login_screen)
        
        # 添加主界面
        main_screen = MainScreen()
        sm.add_widget(main_screen)
        
        return sm

class InspectionAutomation:
    """巡检自动化核心类（适配Android应用）"""
    
    def __init__(self, data_dir, user_info, ui_callback):
        self.data_dir = data_dir
        self.user_info = user_info
        self.ui_callback = ui_callback
        self.checker_list = None
        self.task_data = None
        self._stop_flag = False
    
    def log(self, message):
        """日志输出"""
        if self.ui_callback:
            from kivy.clock import Clock
            Clock.schedule_once(lambda dt: self.ui_callback.update_log(message), 0)
    
    def load_checker_list(self):
        """加载CHECKERLIST文件"""
        checker_path = os.path.join(self.data_dir, "CHECKERLIST.txt")
        try:
            with open(checker_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                self.checker_list = json.loads(content)
                self.log(f"✓ 成功加载CHECKERLIST，共{len(self.checker_list)}个检查员")
                return True
        except Exception as e:
            self.log(f"✗ 加载CHECKERLIST失败: {e}")
            return False
    
    def load_task_data(self):
        """加载TASK文件"""
        task_path = os.path.join(self.data_dir, "TASK.txt")
        try:
            with open(task_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                self.task_data = json.loads(content)
                self.log(f"✓ 成功加载TASK文件，共{len(self.task_data)}个任务")
                return True
        except Exception as e:
            self.log(f"✗ 加载TASK文件失败: {e}")
            return False
    
    def find_user_id(self):
        """在CHECKERLIST中查找对应的userid"""
        if not self.checker_list:
            return False
        
        for checker in self.checker_list:
            if (checker.get('username') == self.user_info['username'] and 
                checker.get('usercode') == self.user_info['usercode']):
                self.user_info['userid'] = checker.get('userid')
                self.log(f"✓ 找到匹配的用户ID: {self.user_info['userid']}")
                return True
        
        self.log(f"✗ 在CHECKERLIST中未找到用户 {self.user_info['username']} ({self.user_info['usercode']})")
        return False
    
    def generate_random_time_offset(self, min_minutes, max_minutes):
        """生成随机时间偏移（分钟）"""
        return random.randint(min_minutes, max_minutes)
    
    def parse_datetime(self, datetime_str):
        """解析日期时间字符串"""
        try:
            return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
        except:
            return None
    
    def format_datetime(self, dt):
        """格式化日期时间为字符串"""
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    
    def process_task_item_file(self, task_code):
        """处理单个TASKITEMLIST文件"""
        file_name = f"TASKITEMLIST{task_code}.txt"
        file_path = os.path.join(self.data_dir, file_name)
        
        if not os.path.exists(file_path):
            self.log(f"✗ TASKITEMLIST文件不存在: {file_name}")
            return None, None, None
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                task_items = json.loads(content)
        except Exception as e:
            self.log(f"✗ 读取TASKITEMLIST文件失败: {e}")
            return None, None, None
        
        # 按areacode分组
        area_groups = {}
        for item in task_items:
            areacode = item.get('areacode')
            if areacode not in area_groups:
                area_groups[areacode] = []
            area_groups[areacode].append(item)
        
        # 按areacode排序（数值小的在前）
        sorted_areas = sorted(area_groups.keys())
        
        return task_items, sorted_areas, area_groups
    
    def generate_time_sequence(self, start_time, area_count):
        """生成时间序列"""
        import random
        times = [start_time.replace(second=random.randint(0, 59))]
        current_time = times[0]
        
        for i in range(area_count - 1):
            interval = self.generate_random_time_offset(3, 5)
            current_time += timedelta(minutes=interval)
            times.append(current_time.replace(second=random.randint(0, 59)))
        
        return times
    
    def update_task_item_data(self, task_items, area_groups, sorted_areas, time_sequence):
        """更新TASKITEMLIST数据"""
        updated_items = []
        
        for i, areacode in enumerate(sorted_areas):
            check_time = time_sequence[i]
            
            for item in area_groups[areacode]:
                # 更新字段
                item['checkusrid'] = self.user_info['userid']
                item['checkusrname'] = self.user_info['username']
                item['checktime'] = self.format_datetime(check_time)
                item['checkresult'] = "ZC"
                item['fdesc'] = "正常"
                
                updated_items.append(item)
        
        return updated_items
    
    def update_task_data(self, task, start_time, end_time):
        """更新TASK数据"""
        updated_task = task.copy()
        updated_task['startdate'] = self.format_datetime(start_time)
        updated_task['donedate'] = self.format_datetime(end_time)
        return updated_task
    
    def save_updated_data(self, file_path, data):
        """保存更新后的数据"""
        try:
            new_content = json.dumps(data, ensure_ascii=False, indent=None, separators=(',', ':'))
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        except Exception as e:
            self.log(f"✗ 保存文件失败: {e}")
            return False
    
    def run_inspection(self):
        """执行巡检自动化"""
        # 加载数据
        if not self.load_checker_list() or not self.load_task_data():
            return False
        
        # 查找用户ID
        if not self.find_user_id():
            return False
        
        # 处理每个任务
        updated_tasks = []
        processed_count = 0
        
        for task in self.task_data:
            if self._stop_flag:
                break
            
            task_code = task.get('taskcode')
            plan_start = task.get('planstartdate')
            plan_end = task.get('planenddate')
            
            self.log(f"\n处理任务: {task.get('taskname')} ({task_code})")
            
            # 随机秒生成器
            def rand_sec(max_s=59):
                return timedelta(seconds=random.randint(0, max_s))
            
            if not task_code or not plan_start or not plan_end:
                self.log("✗ 任务数据不完整，跳过")
                continue
            
            # 解析计划时间
            plan_start_dt = self.parse_datetime(plan_start)
            plan_end_dt = self.parse_datetime(plan_end)
            
            if not plan_start_dt or not plan_end_dt:
                self.log("✗ 时间格式错误，跳过")
                continue
            
            # 处理TASKITEMLIST文件
            task_items, sorted_areas, area_groups = self.process_task_item_file(task_code)
            if not task_items:
                continue
            
            # 生成startdate（planstartdate后1-5分钟 + 0-59秒随机）
            start_time = plan_start_dt + timedelta(minutes=random.randint(1, 5)) + rand_sec()
            
            # 生成时间序列（每步 2-4 分钟 + 0-59 秒）
            time_sequence = []
            current = start_time
            for _ in range(len(sorted_areas)):
                current += timedelta(minutes=random.randint(2, 4)) + rand_sec()
                time_sequence.append(current)
            
            # 生成donedate（最晚checktime后1-2分钟 + 0-59秒）
            latest_check_time = time_sequence[-1]
            end_time = latest_check_time + timedelta(minutes=random.randint(1, 2)) + rand_sec()
            
            # 确保donedate在planenddate之前
            if end_time > plan_end_dt:
                end_time = plan_end_dt - rand_sec(30)  # 留 0-30 秒余量
            
            # 更新TASKITEMLIST数据
            updated_task_items = self.update_task_item_data(task_items, area_groups, sorted_areas, time_sequence)
            
            # 更新TASK数据
            updated_task = self.update_task_data(task, start_time, end_time)
            updated_tasks.append(updated_task)
            
            # 保存TASKITEMLIST文件
            task_item_file = f"TASKITEMLIST{task_code}.txt"
            task_item_path = os.path.join(self.data_dir, task_item_file)
            
            if self.save_updated_data(task_item_path, updated_task_items):
                self.log(f"✓ 成功更新 {task_item_file}")
                processed_count += 1
            else:
                self.log(f"✗ 更新 {task_item_file} 失败")
        
        # 保存TASK文件
        if updated_tasks and not self._stop_flag:
            task_path = os.path.join(self.data_dir, "TASK.txt")
            if self.save_updated_data(task_path, updated_tasks):
                self.log(f"\n✓ 成功更新 TASK.txt")
            else:
                self.log(f"\n✗ 更新 TASK.txt 失败")
        
        self.log(f"\n=== SYSTEM完成 ===")
        self.log(f"成功处理 {processed_count} 个任务")
        return not self._stop_flag

if __name__ == '__main__':
    InspectionAutomationApp().run()