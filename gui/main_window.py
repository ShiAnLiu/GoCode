from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QPushButton, QLabel, QTextEdit, QLineEdit, QFileDialog, QMessageBox, QProgressBar
from PyQt5.QtCore import Qt
from core.project_init import ProjectInitializer
from core.requirement_analysis import RequirementAnalyzer
from core.resource_acquisition import ResourceAcquirer
from core.development import DevelopmentManager
from core.testing import TestManager
from core.acceptance import AcceptanceManager

class MainWindow(QMainWindow):
    """
    主窗口
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle('gocode - 代码编程工具')
        self.setGeometry(100, 100, 1000, 700)
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 创建标签页
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # 创建各个标签页
        self._create_init_tab()
        self._create_analyze_tab()
        self._create_acquire_tab()
        self._create_develop_tab()
        self._create_test_tab()
        self._create_accept_tab()
        
    def _create_init_tab(self):
        """
        创建项目初始化标签页
        """
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 工作空间目录
        workspace_layout = QHBoxLayout()
        workspace_label = QLabel('工作空间目录:')
        self.workspace_line = QLineEdit()
        workspace_button = QPushButton('浏览')
        workspace_button.clicked.connect(self._browse_workspace)
        workspace_layout.addWidget(workspace_label)
        workspace_layout.addWidget(self.workspace_line)
        workspace_layout.addWidget(workspace_button)
        layout.addLayout(workspace_layout)
        
        # 项目名称
        project_layout = QHBoxLayout()
        project_label = QLabel('项目名称:')
        self.project_line = QLineEdit()
        project_layout.addWidget(project_label)
        project_layout.addWidget(self.project_line)
        layout.addLayout(project_layout)
        
        # 初始化按钮
        init_button = QPushButton('初始化项目')
        init_button.clicked.connect(self._init_project)
        layout.addWidget(init_button)
        
        # 结果显示
        self.init_result = QTextEdit()
        self.init_result.setReadOnly(True)
        layout.addWidget(self.init_result)
        
        self.tabs.addTab(tab, '项目初始化')
    
    def _create_analyze_tab(self):
        """
        创建需求分析标签页
        """
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 需求文本
        req_label = QLabel('需求文本:')
        self.req_text = QTextEdit()
        layout.addWidget(req_label)
        layout.addWidget(self.req_text)
        
        # 分析按钮
        analyze_button = QPushButton('分析需求')
        analyze_button.clicked.connect(self._analyze_requirements)
        layout.addWidget(analyze_button)
        
        # 结果显示
        self.analyze_result = QTextEdit()
        self.analyze_result.setReadOnly(True)
        layout.addWidget(self.analyze_result)
        
        self.tabs.addTab(tab, '需求分析')
    
    def _create_acquire_tab(self):
        """
        创建资源获取标签页
        """
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 需求文本
        req_label = QLabel('需求文本:')
        self.acquire_req_text = QTextEdit()
        layout.addWidget(req_label)
        layout.addWidget(self.acquire_req_text)
        
        # 输出目录
        output_layout = QHBoxLayout()
        output_label = QLabel('输出目录:')
        self.output_line = QLineEdit()
        output_button = QPushButton('浏览')
        output_button.clicked.connect(self._browse_output)
        output_layout.addWidget(output_label)
        output_layout.addWidget(self.output_line)
        output_layout.addWidget(output_button)
        layout.addLayout(output_layout)
        
        # 获取资源按钮
        acquire_button = QPushButton('获取资源')
        acquire_button.clicked.connect(self._acquire_resources)
        layout.addWidget(acquire_button)
        
        # 结果显示
        self.acquire_result = QTextEdit()
        self.acquire_result.setReadOnly(True)
        layout.addWidget(self.acquire_result)
        
        self.tabs.addTab(tab, '资源获取')
    
    def _create_develop_tab(self):
        """
        创建开发实施标签页
        """
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 项目目录
        project_layout = QHBoxLayout()
        project_label = QLabel('项目目录:')
        self.develop_project_line = QLineEdit()
        project_button = QPushButton('浏览')
        project_button.clicked.connect(self._browse_project)
        project_layout.addWidget(project_label)
        project_layout.addWidget(self.develop_project_line)
        project_layout.addWidget(project_button)
        layout.addLayout(project_layout)
        
        # 需求文本
        req_label = QLabel('需求文本:')
        self.develop_req_text = QTextEdit()
        layout.addWidget(req_label)
        layout.addWidget(self.develop_req_text)
        
        # 开发按钮
        develop_button = QPushButton('开发实施')
        develop_button.clicked.connect(self._develop)
        layout.addWidget(develop_button)
        
        # 结果显示
        self.develop_result = QTextEdit()
        self.develop_result.setReadOnly(True)
        layout.addWidget(self.develop_result)
        
        self.tabs.addTab(tab, '开发实施')
    
    def _create_test_tab(self):
        """
        创建测试验证标签页
        """
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 项目目录
        project_layout = QHBoxLayout()
        project_label = QLabel('项目目录:')
        self.test_project_line = QLineEdit()
        project_button = QPushButton('浏览')
        project_button.clicked.connect(self._browse_test_project)
        project_layout.addWidget(project_label)
        project_layout.addWidget(self.test_project_line)
        project_layout.addWidget(project_button)
        layout.addLayout(project_layout)
        
        # 测试按钮
        test_button = QPushButton('运行测试')
        test_button.clicked.connect(self._run_tests)
        layout.addWidget(test_button)
        
        # 结果显示
        self.test_result = QTextEdit()
        self.test_result.setReadOnly(True)
        layout.addWidget(self.test_result)
        
        self.tabs.addTab(tab, '测试验证')
    
    def _create_accept_tab(self):
        """
        创建验收标签页
        """
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 项目目录
        project_layout = QHBoxLayout()
        project_label = QLabel('项目目录:')
        self.accept_project_line = QLineEdit()
        project_button = QPushButton('浏览')
        project_button.clicked.connect(self._browse_accept_project)
        project_layout.addWidget(project_label)
        project_layout.addWidget(self.accept_project_line)
        project_layout.addWidget(project_button)
        layout.addLayout(project_layout)
        
        # 需求文本
        req_label = QLabel('需求文本:')
        self.accept_req_text = QTextEdit()
        layout.addWidget(req_label)
        layout.addWidget(self.accept_req_text)
        
        # 验收按钮
        accept_button = QPushButton('生成验收报告')
        accept_button.clicked.connect(self._generate_acceptance)
        layout.addWidget(accept_button)
        
        # 结果显示
        self.accept_result = QTextEdit()
        self.accept_result.setReadOnly(True)
        layout.addWidget(self.accept_result)
        
        self.tabs.addTab(tab, '验收')
    
    def _browse_workspace(self):
        """
        浏览工作空间目录
        """
        directory = QFileDialog.getExistingDirectory(self, '选择工作空间目录')
        if directory:
            self.workspace_line.setText(directory)
    
    def _browse_output(self):
        """
        浏览输出目录
        """
        directory = QFileDialog.getExistingDirectory(self, '选择输出目录')
        if directory:
            self.output_line.setText(directory)
    
    def _browse_project(self):
        """
        浏览项目目录
        """
        directory = QFileDialog.getExistingDirectory(self, '选择项目目录')
        if directory:
            self.develop_project_line.setText(directory)
    
    def _browse_test_project(self):
        """
        浏览测试项目目录
        """
        directory = QFileDialog.getExistingDirectory(self, '选择项目目录')
        if directory:
            self.test_project_line.setText(directory)
    
    def _browse_accept_project(self):
        """
        浏览验收项目目录
        """
        directory = QFileDialog.getExistingDirectory(self, '选择项目目录')
        if directory:
            self.accept_project_line.setText(directory)
    
    def _init_project(self):
        """
        初始化项目
        """
        workspace = self.workspace_line.text()
        project_name = self.project_line.text()
        
        if not workspace or not project_name:
            QMessageBox.warning(self, '警告', '请输入工作空间目录和项目名称')
            return
        
        try:
            initializer = ProjectInitializer(workspace, project_name)
            success = initializer.initialize()
            
            if success:
                self.init_result.setText(f"项目初始化成功: {workspace}/{project_name}")
            else:
                self.init_result.setText("项目初始化失败")
        except Exception as e:
            self.init_result.setText(f"初始化项目时出错: {e}")
    
    def _analyze_requirements(self):
        """
        分析需求
        """
        requirements = self.req_text.toPlainText()
        
        if not requirements:
            QMessageBox.warning(self, '警告', '请输入需求文本')
            return
        
        try:
            analyzer = RequirementAnalyzer()
            analysis_result = analyzer.analyze_requirements(requirements)
            
            if analysis_result.get('success'):
                self.analyze_result.setText(f"需求分析完成\n\n{analysis_result.get('raw_analysis')}")
            else:
                self.analyze_result.setText(f"需求分析失败: {analysis_result.get('error')}")
        except Exception as e:
            self.analyze_result.setText(f"分析需求时出错: {e}")
    
    def _acquire_resources(self):
        """
        获取资源
        """
        requirements = self.acquire_req_text.toPlainText()
        output_dir = self.output_line.text()
        
        if not requirements:
            QMessageBox.warning(self, '警告', '请输入需求文本')
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
                
                self.acquire_result.setText(output)
            else:
                self.acquire_result.setText(f"资源获取失败: {result.get('error')}")
        except Exception as e:
            self.acquire_result.setText(f"获取资源时出错: {e}")
    
    def _develop(self):
        """
        开发实施
        """
        project_dir = self.develop_project_line.text()
        requirements = self.develop_req_text.toPlainText()
        
        if not project_dir:
            QMessageBox.warning(self, '警告', '请选择项目目录')
            return
        
        if not requirements:
            QMessageBox.warning(self, '警告', '请输入需求文本')
            return
        
        try:
            # 分析需求
            analyzer = RequirementAnalyzer()
            analysis_result = analyzer.analyze_requirements(requirements)
            
            if not analysis_result.get('success'):
                self.develop_result.setText(f"需求分析失败: {analysis_result.get('error')}")
                return
            
            # 开发实施
            manager = DevelopmentManager(project_dir)
            result = manager.develop(analysis_result)
            
            if result.get('success'):
                modules = result.get('modules', [])
                output = f"开发实施完成\n"
                output += f"实现的模块数: {len(modules)}\n\n"
                output += "实现的模块:\n" + '\n'.join(f"- {m['name']}: {m['description']}" for m in modules)
                self.develop_result.setText(output)
            else:
                self.develop_result.setText(f"开发实施失败: {result.get('error')}")
        except Exception as e:
            self.develop_result.setText(f"开发实施时出错: {e}")
    
    def _run_tests(self):
        """
        运行测试
        """
        project_dir = self.test_project_line.text()
        
        if not project_dir:
            QMessageBox.warning(self, '警告', '请选择项目目录')
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
                self.test_result.setText(output)
            else:
                self.test_result.setText(f"测试执行失败: {result.get('error')}")
        except Exception as e:
            self.test_result.setText(f"运行测试时出错: {e}")
    
    def _generate_acceptance(self):
        """
        生成验收报告
        """
        project_dir = self.accept_project_line.text()
        requirements = self.accept_req_text.toPlainText()
        
        if not project_dir:
            QMessageBox.warning(self, '警告', '请选择项目目录')
            return
        
        if not requirements:
            QMessageBox.warning(self, '警告', '请输入需求文本')
            return
        
        try:
            # 分析需求
            analyzer = RequirementAnalyzer()
            analysis_result = analyzer.analyze_requirements(requirements)
            
            if not analysis_result.get('success'):
                self.accept_result.setText(f"需求分析失败: {analysis_result.get('error')}")
                return
            
            # 运行测试
            test_manager = TestManager(project_dir)
            test_result = test_manager.run_tests()
            
            if not test_result.get('success'):
                self.accept_result.setText(f"测试执行失败: {test_result.get('error')}")
                return
            
            # 生成验收报告
            acceptance_manager = AcceptanceManager(project_dir)
            result = acceptance_manager.generate_acceptance_report(analysis_result, test_result)
            
            if result.get('success'):
                output = f"验收报告生成完成: {result.get('report_path')}\n"
                output += f"验收状态: {result.get('acceptance_status')}\n\n"
                output += "验收报告已生成: docs/acceptance_report.md"
                self.accept_result.setText(output)
            else:
                self.accept_result.setText(f"生成验收报告失败: {result.get('error')}")
        except Exception as e:
            self.accept_result.setText(f"生成验收报告时出错: {e}")
