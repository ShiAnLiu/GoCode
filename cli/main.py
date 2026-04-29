import argparse
import os
import sys
from core.project_init import ProjectInitializer
from core.requirement_analysis import RequirementAnalyzer
from core.resource_acquisition import ResourceAcquirer
from core.development import DevelopmentManager
from core.testing import TestManager
from core.acceptance import AcceptanceManager
from utils.security import SecurityManager

def main():
    """
    命令行主入口
    """
    # 创建参数解析器
    parser = argparse.ArgumentParser(description='gocode - 代码编程工具')
    
    # 子命令解析器
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # init 命令 - 初始化项目
    init_parser = subparsers.add_parser('init', help='初始化新项目')
    init_parser.add_argument('--workspace', required=True, help='工作空间目录')
    init_parser.add_argument('--project-name', required=True, help='项目名称')
    
    # analyze 命令 - 分析需求
    analyze_parser = subparsers.add_parser('analyze', help='分析需求')
    analyze_parser.add_argument('--requirements', required=True, help='需求文本')
    analyze_parser.add_argument('--output', default='requirements_analysis.md', help='输出文件')
    
    # acquire 命令 - 获取资源
    acquire_parser = subparsers.add_parser('acquire', help='获取资源')
    acquire_parser.add_argument('--requirements', required=True, help='需求文本')
    acquire_parser.add_argument('--output-dir', default='resources', help='资源输出目录')
    
    # develop 命令 - 开发实施
    develop_parser = subparsers.add_parser('develop', help='开发实施')
    develop_parser.add_argument('--project-dir', required=True, help='项目目录')
    develop_parser.add_argument('--requirements', required=True, help='需求文本')
    
    # test 命令 - 运行测试
    test_parser = subparsers.add_parser('test', help='运行测试')
    test_parser.add_argument('--project-dir', required=True, help='项目目录')
    
    # accept 命令 - 生成验收报告
    accept_parser = subparsers.add_parser('accept', help='生成验收报告')
    accept_parser.add_argument('--project-dir', required=True, help='项目目录')
    accept_parser.add_argument('--requirements', required=True, help='需求文本')
    
    # gui 命令 - 启动图形界面
    gui_parser = subparsers.add_parser('gui', help='启动图形界面')
    
    # 解析参数
    args = parser.parse_args()
    
    # 执行命令
    if args.command == 'init':
        handle_init(args)
    elif args.command == 'analyze':
        handle_analyze(args)
    elif args.command == 'acquire':
        handle_acquire(args)
    elif args.command == 'develop':
        handle_develop(args)
    elif args.command == 'test':
        handle_test(args)
    elif args.command == 'accept':
        handle_accept(args)
    elif args.command == 'gui':
        handle_gui(args)
    else:
        parser.print_help()

def handle_init(args):
    """
    处理init命令
    """
    try:
        # 初始化项目
        initializer = ProjectInitializer(args.workspace, args.project_name)
        success = initializer.initialize()
        
        if success:
            print(f"项目初始化成功: {os.path.join(args.workspace, args.project_name)}")
        else:
            print("项目初始化失败")
    except Exception as e:
        print(f"初始化项目时出错: {e}")

def handle_analyze(args):
    """
    处理analyze命令
    """
    try:
        # 分析需求
        analyzer = RequirementAnalyzer()
        analysis_result = analyzer.analyze_requirements(args.requirements)
        
        if analysis_result.get('success'):
            # 生成需求文档
            output_path = os.path.join(os.getcwd(), args.output)
            analyzer.generate_requirement_document(analysis_result, output_path)
            print(f"需求分析完成，文档已生成: {output_path}")
        else:
            print(f"需求分析失败: {analysis_result.get('error')}")
    except Exception as e:
        print(f"分析需求时出错: {e}")

def handle_acquire(args):
    """
    处理acquire命令
    """
    try:
        # 获取资源
        acquirer = ResourceAcquirer()
        result = acquirer.acquire_resources(args.requirements, args.output_dir)
        
        if result.get('success'):
            print(f"资源获取完成")
            print(f"网络获取的资源: {len(result.get('network_resources', []))}")
            print(f"创作的资源: {len(result.get('created_resources', []))}")
            print(f"用户提供的资源: {len(result.get('user_provided_resources', []))}")
        else:
            print(f"资源获取失败: {result.get('error')}")
    except Exception as e:
        print(f"获取资源时出错: {e}")

def handle_develop(args):
    """
    处理develop命令
    """
    try:
        # 分析需求
        analyzer = RequirementAnalyzer()
        analysis_result = analyzer.analyze_requirements(args.requirements)
        
        if not analysis_result.get('success'):
            print(f"需求分析失败: {analysis_result.get('error')}")
            return
        
        # 开发实施
        manager = DevelopmentManager(args.project_dir)
        result = manager.develop(analysis_result)
        
        if result.get('success'):
            print(f"开发实施完成")
            print(f"实现的模块数: {len(result.get('modules', []))}")
        else:
            print(f"开发实施失败: {result.get('error')}")
    except Exception as e:
        print(f"开发实施时出错: {e}")

def handle_test(args):
    """
    处理test命令
    """
    try:
        # 运行测试
        test_manager = TestManager(args.project_dir)
        result = test_manager.run_tests()
        
        if result.get('success'):
            print(f"测试执行完成")
            print(f"单元测试: {'通过' if result.get('unit_tests', {}).get('success') else '失败'}")
            print(f"边界条件测试: {'通过' if result.get('boundary_tests', {}).get('success') else '失败'}")
            print(f"系统集成测试: {'通过' if result.get('integration_tests', {}).get('success') else '失败'}")
        else:
            print(f"测试执行失败: {result.get('error')}")
    except Exception as e:
        print(f"运行测试时出错: {e}")

def handle_accept(args):
    """
    处理accept命令
    """
    try:
        # 分析需求
        analyzer = RequirementAnalyzer()
        analysis_result = analyzer.analyze_requirements(args.requirements)
        
        if not analysis_result.get('success'):
            print(f"需求分析失败: {analysis_result.get('error')}")
            return
        
        # 运行测试
        test_manager = TestManager(args.project_dir)
        test_result = test_manager.run_tests()
        
        if not test_result.get('success'):
            print(f"测试执行失败: {test_result.get('error')}")
            return
        
        # 生成验收报告
        acceptance_manager = AcceptanceManager(args.project_dir)
        result = acceptance_manager.generate_acceptance_report(analysis_result, test_result)
        
        if result.get('success'):
            print(f"验收报告生成完成: {result.get('report_path')}")
            print(f"验收状态: {result.get('acceptance_status')}")
        else:
            print(f"生成验收报告失败: {result.get('error')}")
    except Exception as e:
        print(f"生成验收报告时出错: {e}")

def handle_gui(args):
    """
    处理gui命令
    """
    try:
        # 启动图形界面
        from gui.main_window import MainWindow
        import sys
        from PySide6.QtWidgets import QApplication
        
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f"启动图形界面时出错: {e}")

if __name__ == '__main__':
    main()
