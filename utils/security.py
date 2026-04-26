import os
import pathlib
from typing import Optional

class SecurityManager:
    """
    安全控制模块，用于限制文件系统操作范围和实现文件访问权限控制
    """
    
    def __init__(self, workspace_dir):
        """
        初始化安全管理器
        
        Args:
            workspace_dir: 工作空间目录
        """
        self.workspace_dir = pathlib.Path(workspace_dir).resolve()
    
    def check_file_access(self, file_path: str) -> bool:
        """
        检查文件访问权限
        
        Args:
            file_path: 文件路径
            
        Returns:
            bool: 是否允许访问
        """
        try:
            # 解析文件路径
            target_path = pathlib.Path(file_path).resolve()
            
            # 检查是否在工作空间目录内
            if not target_path.is_relative_to(self.workspace_dir):
                print(f"错误: 禁止访问工作空间以外的文件: {file_path}")
                return False
            
            return True
        except Exception as e:
            print(f"检查文件访问权限时出错: {e}")
            return False
    
    def check_directory_access(self, dir_path: str) -> bool:
        """
        检查目录访问权限
        
        Args:
            dir_path: 目录路径
            
        Returns:
            bool: 是否允许访问
        """
        try:
            # 解析目录路径
            target_path = pathlib.Path(dir_path).resolve()
            
            # 检查是否在工作空间目录内
            if not target_path.is_relative_to(self.workspace_dir):
                print(f"错误: 禁止访问工作空间以外的目录: {dir_path}")
                return False
            
            return True
        except Exception as e:
            print(f"检查目录访问权限时出错: {e}")
            return False
    
    def safe_open(self, file_path: str, mode: str = 'r') -> Optional[open]:
        """
        安全打开文件
        
        Args:
            file_path: 文件路径
            mode: 打开模式
            
        Returns:
            Optional[open]: 文件对象或None
        """
        if not self.check_file_access(file_path):
            return None
        
        try:
            return open(file_path, mode, encoding='utf-8')
        except Exception as e:
            print(f"打开文件时出错: {e}")
            return None
    
    def safe_mkdir(self, dir_path: str, exist_ok: bool = False) -> bool:
        """
        安全创建目录
        
        Args:
            dir_path: 目录路径
            exist_ok: 如果目录已存在是否报错
            
        Returns:
            bool: 是否创建成功
        """
        if not self.check_directory_access(dir_path):
            return False
        
        try:
            os.makedirs(dir_path, exist_ok=exist_ok)
            return True
        except Exception as e:
            print(f"创建目录时出错: {e}")
            return False
    
    def safe_remove(self, file_path: str) -> bool:
        """
        安全删除文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            bool: 是否删除成功
        """
        if not self.check_file_access(file_path):
            return False
        
        try:
            os.remove(file_path)
            return True
        except Exception as e:
            print(f"删除文件时出错: {e}")
            return False
    
    def safe_rename(self, src: str, dst: str) -> bool:
        """
        安全重命名文件或目录
        
        Args:
            src: 源路径
            dst: 目标路径
            
        Returns:
            bool: 是否重命名成功
        """
        if not self.check_file_access(src) or not self.check_file_access(dst):
            return False
        
        try:
            os.rename(src, dst)
            return True
        except Exception as e:
            print(f"重命名时出错: {e}")
            return False
    
    def safe_copy(self, src: str, dst: str) -> bool:
        """
        安全复制文件
        
        Args:
            src: 源文件路径
            dst: 目标文件路径
            
        Returns:
            bool: 是否复制成功
        """
        if not self.check_file_access(src) or not self.check_file_access(dst):
            return False
        
        try:
            import shutil
            shutil.copy2(src, dst)
            return True
        except Exception as e:
            print(f"复制文件时出错: {e}")
            return False
