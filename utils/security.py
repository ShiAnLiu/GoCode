import os
import json
import pathlib
from typing import Optional, TextIO, List, Dict, Any

def _is_relative_to(target: pathlib.Path, base: pathlib.Path) -> bool:
    try:
        target.relative_to(base)
        return True
    except ValueError:
        return False


class SecurityManager:
    """
    安全控制模块，用于限制文件系统操作范围和实现文件访问权限控制
    """
    
    def __init__(self, workspace_dir, config_path: str = None):
        """
        初始化安全管理器
        
        Args:
            workspace_dir: 工作空间目录
            config_path: 安全配置文件路径，默认为 config/security_config.json
        """
        self.workspace_dir = pathlib.Path(workspace_dir).resolve()
        self.config = self._load_config(config_path)
    
    def _load_config(self, config_path: str = None) -> Dict[str, Any]:
        """
        加载安全配置
        
        Args:
            config_path: 配置文件路径
            
        Returns:
            Dict: 安全配置
        """
        if config_path is None:
            config_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                '..', 'config', 'security_config.json'
            )
        
        default_config = {
            "allowed_directories": [],
            "blocked_directories": [],
            "max_file_size": 10485760,
            "allowed_file_extensions": [".py", ".txt", ".md", ".json", ".yaml", ".yml"],
            "blocked_file_extensions": [".exe", ".dll", ".bat", ".sh", ".pyc", ".pyd"]
        }
        
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    for key, value in default_config.items():
                        if key not in loaded:
                            loaded[key] = value
                    return loaded
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Failed to load security config: {e}")
        
        return default_config
    
    def _check_extension_allowed(self, file_path: str) -> bool:
        """
        检查文件扩展名是否允许
        
        Args:
            file_path: 文件路径
            
        Returns:
            bool: 是否允许访问
        """
        allowed = self.config.get("allowed_file_extensions", [])
        blocked = self.config.get("blocked_file_extensions", [])
        ext = pathlib.Path(file_path).suffix.lower()
        
        if blocked and ext in blocked:
            print(f"错误: 文件扩展名被禁止: {ext} ({file_path})")
            return False
        
        if allowed and ext not in allowed:
            print(f"错误: 文件扩展名不在允许列表中: {ext} ({file_path})")
            return False
        
        return True
    
    def _check_file_size(self, file_path: str) -> bool:
        """
        检查文件大小是否超限
        
        Args:
            file_path: 文件路径
            
        Returns:
            bool: 是否允许访问
        """
        max_size = self.config.get("max_file_size", 0)
        if max_size <= 0:
            return True
        
        try:
            file_size = os.path.getsize(file_path)
            if file_size > max_size:
                print(f"错误: 文件大小 ({file_size}) 超过限制 ({max_size}): {file_path}")
                return False
        except OSError:
            pass
        
        return True
    
    def _check_directory_restrictions(self, dir_path: str) -> bool:
        """
        检查目录是否在允许/禁止列表中
        
        Args:
            dir_path: 目录路径
            
        Returns:
            bool: 是否允许访问
        """
        target = pathlib.Path(dir_path).resolve()
        target_str = str(target).lower()
        
        blocked_dirs = self.config.get("blocked_directories", [])
        for blocked in blocked_dirs:
            if blocked and blocked.lower() in target_str:
                print(f"错误: 目录被禁止访问: {dir_path}")
                return False
        
        allowed_dirs = self.config.get("allowed_directories", [])
        if allowed_dirs:
            in_allowed = any(
                allowed.lower() in target_str 
                for allowed in allowed_dirs 
                if allowed
            )
            if not in_allowed:
                print(f"错误: 目录不在允许列表中: {dir_path}")
                return False
        
        return True
    
    def check_file_access(self, file_path: str) -> bool:
        """
        检查文件访问权限
        
        Args:
            file_path: 文件路径
            
        Returns:
            bool: 是否允许访问
        """
        try:
            target_path = pathlib.Path(file_path).resolve()
            
            if not _is_relative_to(target_path, self.workspace_dir):
                print(f"错误: 禁止访问工作空间以外的文件: {file_path}")
                return False
            
            if not self._check_extension_allowed(file_path):
                return False
            
            if os.path.exists(file_path) and not self._check_file_size(file_path):
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
            target_path = pathlib.Path(dir_path).resolve()
            
            if not _is_relative_to(target_path, self.workspace_dir):
                print(f"错误: 禁止访问工作空间以外的目录: {dir_path}")
                return False
            
            if not self._check_directory_restrictions(dir_path):
                return False
            
            return True
        except Exception as e:
            print(f"检查目录访问权限时出错: {e}")
            return False
    
    def safe_open(self, file_path: str, mode: str = 'r') -> Optional[TextIO]:
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
            if 'b' in mode:
                return open(file_path, mode)
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
