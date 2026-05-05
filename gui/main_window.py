from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.textinput import TextInput as KivyTextInput
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.spinner import Spinner
from core.project_init import ProjectInitializer
from core.requirement_analysis import RequirementAnalyzer
from core.resource_acquisition import ResourceAcquirer
from core.development import DevelopmentManager
from core.testing import TestManager
from core.acceptance import AcceptanceManager
from utils.api_config import APIConfig, APIProvider

class MainWindow(BoxLayout):
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        
        self.api_config = APIConfig()
        
        self.tab_panel = TabbedPanel(do_default_tab=False)
        self.add_widget(self.tab_panel)
        
        self._create_init_tab()
        self._create_analyze_tab()
        self._create_acquire_tab()
        self._create_develop_tab()
        self._create_test_tab()
        self._create_accept_tab()
        self._create_settings_tab()
    
    def _create_settings_tab(self):
        tab = TabbedPanelItem(text='API设置')
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        provider_layout = BoxLayout(orientation='horizontal', spacing=10)
        provider_layout.add_widget(Label(text='API提供商:', size_hint_x=0.3))
        self.provider_spinner = Spinner(
            text=self.api_config.get_provider(),
            values=['lmstudio', 'ollama', 'openai', 'anthropic', 'custom'],
            size_hint_x=0.7
        )
        self.provider_spinner.bind(text=self._on_provider_changed)
        provider_layout.add_widget(self.provider_spinner)
        layout.add_widget(provider_layout)
        
        base_url_layout = BoxLayout(orientation='horizontal', spacing=10)
        base_url_layout.add_widget(Label(text='API地址:', size_hint_x=0.3))
        self.base_url_input = TextInput(multiline=False, size_hint_x=0.7)
        base_url_layout.add_widget(self.base_url_input)
        layout.add_widget(base_url_layout)
        
        model_layout = BoxLayout(orientation='horizontal', spacing=10)
        model_layout.add_widget(Label(text='模型名称:', size_hint_x=0.3))
        self.model_input = TextInput(multiline=False, size_hint_x=0.7)
        model_layout.add_widget(self.model_input)
        layout.add_widget(model_layout)
        
        api_key_layout = BoxLayout(orientation='horizontal', spacing=10)
        api_key_layout.add_widget(Label(text='API密钥:', size_hint_x=0.3))
        self.api_key_input = TextInput(multiline=False, password=True, size_hint_x=0.7)
        api_key_layout.add_widget(self.api_key_input)
        layout.add_widget(api_key_layout)
        
        save_button = Button(text='保存设置', size_hint_y=0.1)
        save_button.bind(on_press=self._save_settings)
        layout.add_widget(save_button)
        
        test_button = Button(text='测试连接', size_hint_y=0.1)
        test_button.bind(on_press=self._test_connection)
        layout.add_widget(test_button)
        
        scroll = ScrollView()
        self.settings_result = TextInput(readonly=True, size_hint_y=None)
        self.settings_result.bind(text=lambda _, __: setattr(self.settings_result, 'height', max(self.settings_result.minimum_height, 100)))
        scroll.add_widget(self.settings_result)
        layout.add_widget(scroll)
        
        self._load_settings()
        
        tab.add_widget(layout)
        self.tab_panel.add_widget(tab)
    
    def _create_init_tab(self):
        tab = TabbedPanelItem(text='项目初始化')
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        workspace_layout = BoxLayout(orientation='horizontal', spacing=10)
        workspace_layout.add_widget(Label(text='工作空间目录:', size_hint_x=0.2))
        self.workspace_line = TextInput(multiline=False, size_hint_x=0.6)
        workspace_layout.add_widget(self.workspace_line)
        workspace_button = Button(text='浏览', size_hint_x=0.2)
        workspace_button.bind(on_press=self._browse_workspace)
        workspace_layout.add_widget(workspace_button)
        layout.add_widget(workspace_layout)
        
        project_layout = BoxLayout(orientation='horizontal', spacing=10)
        project_layout.add_widget(Label(text='项目名称:', size_hint_x=0.2))
        self.project_line = TextInput(multiline=False, size_hint_x=0.8)
        project_layout.add_widget(self.project_line)
        layout.add_widget(project_layout)
        
        init_button = Button(text='初始化项目', size_hint_y=0.1)
        init_button.bind(on_press=self._init_project)
        layout.add_widget(init_button)
        
        scroll = ScrollView()
        self.init_result = TextInput(readonly=True, size_hint_y=None)
        self.init_result.bind(text=lambda _, __: setattr(self.init_result, 'height', max(self.init_result.minimum_height, 200)))
        scroll.add_widget(self.init_result)
        layout.add_widget(scroll)
        
        tab.add_widget(layout)
        self.tab_panel.add_widget(tab)
    
    def _create_analyze_tab(self):
        tab = TabbedPanelItem(text='需求分析')
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        layout.add_widget(Label(text='需求文本:'))
        
        scroll1 = ScrollView()
        self.req_text = TextInput(multiline=True, size_hint_y=None)
        self.req_text.bind(text=lambda _, __: setattr(self.req_text, 'height', max(self.req_text.minimum_height, 200)))
        scroll1.add_widget(self.req_text)
        layout.add_widget(scroll1)
        
        analyze_button = Button(text='分析需求', size_hint_y=0.1)
        analyze_button.bind(on_press=self._analyze_requirements)
        layout.add_widget(analyze_button)
        
        scroll2 = ScrollView()
        self.analyze_result = TextInput(readonly=True, size_hint_y=None)
        self.analyze_result.bind(text=lambda _, __: setattr(self.analyze_result, 'height', max(self.analyze_result.minimum_height, 200)))
        scroll2.add_widget(self.analyze_result)
        layout.add_widget(scroll2)
        
        tab.add_widget(layout)
        self.tab_panel.add_widget(tab)
    
    def _create_acquire_tab(self):
        tab = TabbedPanelItem(text='资源获取')
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        layout.add_widget(Label(text='需求文本:'))
        
        scroll1 = ScrollView()
        self.acquire_req_text = TextInput(multiline=True, size_hint_y=None)
        self.acquire_req_text.bind(text=lambda _, __: setattr(self.acquire_req_text, 'height', max(self.acquire_req_text.minimum_height, 150)))
        scroll1.add_widget(self.acquire_req_text)
        layout.add_widget(scroll1)
        
        output_layout = BoxLayout(orientation='horizontal', spacing=10)
        output_layout.add_widget(Label(text='输出目录:', size_hint_x=0.2))
        self.output_line = TextInput(multiline=False, size_hint_x=0.6)
        output_layout.add_widget(self.output_line)
        output_button = Button(text='浏览', size_hint_x=0.2)
        output_button.bind(on_press=self._browse_output)
        output_layout.add_widget(output_button)
        layout.add_widget(output_layout)
        
        acquire_button = Button(text='获取资源', size_hint_y=0.1)
        acquire_button.bind(on_press=self._acquire_resources)
        layout.add_widget(acquire_button)
        
        scroll2 = ScrollView()
        self.acquire_result = TextInput(readonly=True, size_hint_y=None)
        self.acquire_result.bind(text=lambda _, __: setattr(self.acquire_result, 'height', max(self.acquire_result.minimum_height, 200)))
        scroll2.add_widget(self.acquire_result)
        layout.add_widget(scroll2)
        
        tab.add_widget(layout)
        self.tab_panel.add_widget(tab)
    
    def _create_develop_tab(self):
        tab = TabbedPanelItem(text='开发实施')
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        project_layout = BoxLayout(orientation='horizontal', spacing=10)
        project_layout.add_widget(Label(text='项目目录:', size_hint_x=0.2))
        self.develop_project_line = TextInput(multiline=False, size_hint_x=0.6)
        project_layout.add_widget(self.develop_project_line)
        project_button = Button(text='浏览', size_hint_x=0.2)
        project_button.bind(on_press=self._browse_project)
        project_layout.add_widget(project_button)
        layout.add_widget(project_layout)
        
        layout.add_widget(Label(text='需求文本:'))
        
        scroll1 = ScrollView()
        self.develop_req_text = TextInput(multiline=True, size_hint_y=None)
        self.develop_req_text.bind(text=lambda _, __: setattr(self.develop_req_text, 'height', max(self.develop_req_text.minimum_height, 150)))
        scroll1.add_widget(self.develop_req_text)
        layout.add_widget(scroll1)
        
        develop_button = Button(text='开发实施', size_hint_y=0.1)
        develop_button.bind(on_press=self._develop)
        layout.add_widget(develop_button)
        
        scroll2 = ScrollView()
        self.develop_result = TextInput(readonly=True, size_hint_y=None)
        self.develop_result.bind(text=lambda _, __: setattr(self.develop_result, 'height', max(self.develop_result.minimum_height, 200)))
        scroll2.add_widget(self.develop_result)
        layout.add_widget(scroll2)
        
        tab.add_widget(layout)
        self.tab_panel.add_widget(tab)
    
    def _create_test_tab(self):
        tab = TabbedPanelItem(text='测试验证')
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        project_layout = BoxLayout(orientation='horizontal', spacing=10)
        project_layout.add_widget(Label(text='项目目录:', size_hint_x=0.2))
        self.test_project_line = TextInput(multiline=False, size_hint_x=0.6)
        project_layout.add_widget(self.test_project_line)
        project_button = Button(text='浏览', size_hint_x=0.2)
        project_button.bind(on_press=self._browse_test_project)
        project_layout.add_widget(project_button)
        layout.add_widget(project_layout)
        
        test_button = Button(text='运行测试', size_hint_y=0.1)
        test_button.bind(on_press=self._run_tests)
        layout.add_widget(test_button)
        
        scroll = ScrollView()
        self.test_result = TextInput(readonly=True, size_hint_y=None)
        self.test_result.bind(text=lambda _, __: setattr(self.test_result, 'height', max(self.test_result.minimum_height, 200)))
        scroll.add_widget(self.test_result)
        layout.add_widget(scroll)
        
        tab.add_widget(layout)
        self.tab_panel.add_widget(tab)
    
    def _create_accept_tab(self):
        tab = TabbedPanelItem(text='验收')
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        project_layout = BoxLayout(orientation='horizontal', spacing=10)
        project_layout.add_widget(Label(text='项目目录:', size_hint_x=0.2))
        self.accept_project_line = TextInput(multiline=False, size_hint_x=0.6)
        project_layout.add_widget(self.accept_project_line)
        project_button = Button(text='浏览', size_hint_x=0.2)
        project_button.bind(on_press=self._browse_accept_project)
        project_layout.add_widget(project_button)
        layout.add_widget(project_layout)
        
        layout.add_widget(Label(text='需求文本:'))
        
        scroll1 = ScrollView()
        self.accept_req_text = TextInput(multiline=True, size_hint_y=None)
        self.accept_req_text.bind(text=lambda _, __: setattr(self.accept_req_text, 'height', max(self.accept_req_text.minimum_height, 150)))
        scroll1.add_widget(self.accept_req_text)
        layout.add_widget(scroll1)
        
        accept_button = Button(text='生成验收报告', size_hint_y=0.1)
        accept_button.bind(on_press=self._generate_acceptance)
        layout.add_widget(accept_button)
        
        scroll2 = ScrollView()
        self.accept_result = TextInput(readonly=True, size_hint_y=None)
        self.accept_result.bind(text=lambda _, __: setattr(self.accept_result, 'height', max(self.accept_result.minimum_height, 200)))
        scroll2.add_widget(self.accept_result)
        layout.add_widget(scroll2)
        
        tab.add_widget(layout)
        self.tab_panel.add_widget(tab)
    
    def _load_settings(self):
        provider = self.api_config.get_provider()
        provider_config = self.api_config.config.get(provider, {})
        
        self.base_url_input.text = provider_config.get('base_url', '')
        self.model_input.text = provider_config.get('model', '')
        self.api_key_input.text = provider_config.get('api_key', '')
    
    def _on_provider_changed(self, spinner, text):
        self.api_config.set_provider(text)
        self._load_settings()
    
    def _save_settings(self, instance):
        provider = self.provider_spinner.text
        
        base_url = self.base_url_input.text
        model = self.model_input.text
        api_key = self.api_key_input.text
        
        self.api_config.set_api_config(provider, base_url=base_url, model=model, api_key=api_key)
        self.api_config.set_provider(provider)
        
        self.settings_result.text = "设置已保存"
    
    def _test_connection(self, instance):
        from utils.ai_client import AIClient
        
        try:
            client = AIClient()
            result = client.chat([
                {"role": "user", "content": "你好，请回复'连接成功'"}
            ], max_tokens=50)
            
            if result.get("success"):
                self.settings_result.text = f"连接测试成功！\n响应: {result['content']}"
            else:
                self.settings_result.text = f"连接测试失败: {result.get('error')}"
        except Exception as e:
            self.settings_result.text = f"连接测试失败: {str(e)}"
    
    def _show_file_chooser(self, callback):
        content = BoxLayout(orientation='vertical', spacing=10)
        filechooser = FileChooserListView()
        content.add_widget(filechooser)
        
        button_layout = BoxLayout(orientation='horizontal', spacing=10)
        cancel_button = Button(text='取消')
        select_button = Button(text='选择')
        button_layout.add_widget(cancel_button)
        button_layout.add_widget(select_button)
        content.add_widget(button_layout)
        
        popup = Popup(title='选择目录', content=content, size_hint=(0.9, 0.9))
        
        cancel_button.bind(on_press=popup.dismiss)
        select_button.bind(on_press=lambda x: [callback(filechooser.selection), popup.dismiss()])
        
        popup.open()
    
    def _browse_workspace(self, instance):
        self._show_file_chooser(lambda x: setattr(self.workspace_line, 'text', x[0]) if x else None)
    
    def _browse_output(self, instance):
        self._show_file_chooser(lambda x: setattr(self.output_line, 'text', x[0]) if x else None)
    
    def _browse_project(self, instance):
        self._show_file_chooser(lambda x: setattr(self.develop_project_line, 'text', x[0]) if x else None)
    
    def _browse_test_project(self, instance):
        self._show_file_chooser(lambda x: setattr(self.test_project_line, 'text', x[0]) if x else None)
    
    def _browse_accept_project(self, instance):
        self._show_file_chooser(lambda x: setattr(self.accept_project_line, 'text', x[0]) if x else None)
    
    def _show_warning(self, message):
        popup = Popup(title='警告', content=Label(text=message), size_hint=(0.6, 0.4))
        popup.open()
    
    def _init_project(self, instance):
        workspace = self.workspace_line.text
        project_name = self.project_line.text
        
        if not workspace or not project_name:
            self._show_warning('请输入工作空间目录和项目名称')
            return
        
        try:
            initializer = ProjectInitializer(workspace, project_name)
            success = initializer.initialize()
            
            if success:
                self.init_result.text = f"项目初始化成功: {workspace}/{project_name}"
            else:
                self.init_result.text = "项目初始化失败"
        except Exception as e:
            self.init_result.text = f"初始化项目时出错: {e}"
    
    def _analyze_requirements(self, instance):
        requirements = self.req_text.text
        
        if not requirements:
            self._show_warning('请输入需求文本')
            return
        
        try:
            analyzer = RequirementAnalyzer()
            analysis_result = analyzer.analyze_requirements(requirements)
            
            if analysis_result.get('success'):
                self.analyze_result.text = f"需求分析完成\n\n{analysis_result.get('raw_analysis')}"
            else:
                self.analyze_result.text = f"需求分析失败: {analysis_result.get('error')}"
        except Exception as e:
            self.analyze_result.text = f"分析需求时出错: {e}"
    
    def _acquire_resources(self, instance):
        requirements = self.acquire_req_text.text
        output_dir = self.output_line.text
        
        if not requirements:
            self._show_warning('请输入需求文本')
            return
        
        if not output_dir:
            output_dir = 'resources'
        
        try:
            acquirer = ResourceAcquirer()
            result = acquirer.acquire_resources(requirements, output_dir)
            
            if result.get('success'):
                network_resources = result.get('network_resources', [])
                created_resources = result.get('created_resources', [])
                user_provided_resources = result.get('user_provided_resources', [])
                
                output = f"资源获取完成\n"
                output += f"网络获取的资源: {len(network_resources)}\n"
                output += f"创作的资源: {len(created_resources)}\n"
                output += f"用户提供的资源: {len(user_provided_resources)}\n\n"
                
                if network_resources:
                    output += "网络获取的资源:\n" + '\n'.join(f"- {r}" for r in network_resources) + "\n\n"
                if created_resources:
                    output += "创作的资源:\n" + '\n'.join(f"- {r}" for r in created_resources) + "\n\n"
                if user_provided_resources:
                    output += "用户提供的资源:\n" + '\n'.join(f"- {r}" for r in user_provided_resources) + "\n"
                
                self.acquire_result.text = output
            else:
                self.acquire_result.text = f"资源获取失败: {result.get('error')}"
        except Exception as e:
            self.acquire_result.text = f"获取资源时出错: {e}"
    
    def _develop(self, instance):
        project_dir = self.develop_project_line.text
        requirements = self.develop_req_text.text
        
        if not project_dir:
            self._show_warning('请选择项目目录')
            return
        
        if not requirements:
            self._show_warning('请输入需求文本')
            return
        
        try:
            analyzer = RequirementAnalyzer()
            analysis_result = analyzer.analyze_requirements(requirements)
            
            if not analysis_result.get('success'):
                self.develop_result.text = f"需求分析失败: {analysis_result.get('error')}"
                return
            
            manager = DevelopmentManager(project_dir)
            result = manager.develop(analysis_result)
            
            if result.get('success'):
                modules = result.get('modules', [])
                output = f"开发实施完成\n"
                output += f"实现的模块数: {len(modules)}\n\n"
                output += "实现的模块:\n" + '\n'.join(f"- {m['name']}: {m['description']}" for m in modules)
                self.develop_result.text = output
            else:
                self.develop_result.text = f"开发实施失败: {result.get('error')}"
        except Exception as e:
            self.develop_result.text = f"开发实施时出错: {e}"
    
    def _run_tests(self, instance):
        project_dir = self.test_project_line.text
        
        if not project_dir:
            self._show_warning('请选择项目目录')
            return
        
        try:
            test_manager = TestManager(project_dir)
            result = test_manager.run_tests()
            
            if result.get('success'):
                unit_success = result.get('unit_tests', {}).get('success', False)
                boundary_success = result.get('boundary_tests', {}).get('success', False)
                integration_success = result.get('integration_tests', {}).get('success', False)
                
                output = f"测试执行完成\n"
                output += f"单元测试: {'通过' if unit_success else '失败'}\n"
                output += f"边界条件测试: {'通过' if boundary_success else '失败'}\n"
                output += f"系统集成测试: {'通过' if integration_success else '失败'}\n\n"
                output += "测试报告已生成: docs/test_report.md"
                self.test_result.text = output
            else:
                self.test_result.text = f"测试执行失败: {result.get('error')}"
        except Exception as e:
            self.test_result.text = f"运行测试时出错: {e}"
    
    def _generate_acceptance(self, instance):
        project_dir = self.accept_project_line.text
        requirements = self.accept_req_text.text
        
        if not project_dir:
            self._show_warning('请选择项目目录')
            return
        
        if not requirements:
            self._show_warning('请输入需求文本')
            return
        
        try:
            analyzer = RequirementAnalyzer()
            analysis_result = analyzer.analyze_requirements(requirements)
            
            if not analysis_result.get('success'):
                self.accept_result.text = f"需求分析失败: {analysis_result.get('error')}"
                return
            
            test_manager = TestManager(project_dir)
            test_result = test_manager.run_tests()
            
            if not test_result.get('success'):
                self.accept_result.text = f"测试执行失败: {test_result.get('error')}"
                return
            
            acceptance_manager = AcceptanceManager(project_dir)
            result = acceptance_manager.generate_acceptance_report(analysis_result, test_result)
            
            if result.get('success'):
                output = f"验收报告生成完成: {result.get('report_path')}\n"
                output += f"验收状态: {result.get('acceptance_status')}\n\n"
                output += "验收报告已生成: docs/acceptance_report.md"
                self.accept_result.text = output
            else:
                self.accept_result.text = f"生成验收报告失败: {result.get('error')}"
        except Exception as e:
            self.accept_result.text = f"生成验收报告时出错: {e}"

class GocodeApp(App):
    def build(self):
        Window.size = (1000, 700)
        self.title = 'gocode - 代码编程工具'
        return MainWindow()

def run():
    GocodeApp().run()
