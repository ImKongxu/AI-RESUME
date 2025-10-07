import os
import json
import subprocess
import asyncio
import os

class DatabaseService:
    def __init__(self):
        # 创建数据目录
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "resume_data")
        os.makedirs(self.data_dir, exist_ok=True)
        # C程序路径
        self.c_db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "db")
        
    async def save_resume_data(self, resume_data: dict) -> bool:
        """
        调用C程序将数据保存到C语言数据库。

        约定的输入JSON结构：
        {
          "basic_info": {"id": int, "name": str, "email": str, "phone": str, "address": str, "linkedin": str, "github": str},
          "educations": [ {"id": int, "school": str, "degree": str, "major": str, "start_date": str, "end_date": str, "gpa": float, "description": str}, ... ],
          "experiences": [ {"id": int, "company": str, "position": str, "start_date": str, "end_date": str, "is_current": int, "description": str}, ... ],
          "skills": [ {"id": int, "skill_name": str, "proficiency": str, "category": str}, ... ],
          "projects": [ {"id": int, "project_name": str, "project_url": str, "start_date": str, "end_date": str, "description": str, "technologies": str}, ... ]
        }
        """
        try:
            # 规范化负载，确保包含所需键与默认空数组
            basic_info = resume_data.get('basic_info') or {}
            user_id = int(basic_info.get('id', 0) or 0)
            normalized = {
                'basic_info': {
                    'id': user_id,
                    'name': basic_info.get('name', '') or '',
                    'email': basic_info.get('email', '') or '',
                    'phone': basic_info.get('phone', '') or '',
                    'address': basic_info.get('address', '') or '',
                    'linkedin': basic_info.get('linkedin', '') or '',
                    'github': basic_info.get('github', '') or ''
                },
                'educations': resume_data.get('educations') or [],
                'experiences': resume_data.get('experiences') or [],
                'skills': resume_data.get('skills') or [],
                'projects': resume_data.get('projects') or []
            }
            if not user_id:
                return False
                
            # 转换为JSON字符串
            json_data = json.dumps(normalized, ensure_ascii=False)
            
            # 异步执行C程序，通过标准输入传递JSON数据
            proc = await asyncio.create_subprocess_exec(
                self.c_db_path,
                "save",
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=os.path.dirname(self.c_db_path)  # 设置工作目录为C程序所在目录
            )
            
            # 发送数据并等待完成
            stdout, stderr = await proc.communicate(input=json_data.encode('utf-8'))
            
            # 检查执行结果
            if proc.returncode == 0:
                print(f"数据保存成功: {stdout.decode('utf-8')}")
                return True
            else:
                print(f"C程序执行失败: {stderr.decode('utf-8')}")
                return False
        except Exception as e:
            print(f"保存数据时发生错误: {str(e)}")
            # 降级方案：如果C程序调用失败，保存为JSON文件
            try:
                file_path = os.path.join(self.data_dir, f"resume_{user_id}.json")
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(resume_data, f, ensure_ascii=False, indent=2)
                return True
            except:
                return False
                
    async def load_resume_data(self, user_id: int) -> dict:
        """调用C程序从C语言数据库加载数据"""
        try:
            # 异步执行C程序，请求指定用户ID的数据
            proc = await asyncio.create_subprocess_exec(
                self.c_db_path,
                "load",
                str(user_id),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=os.path.dirname(self.c_db_path)  # 设置工作目录为C程序所在目录
            )
            
            # 等待执行完成并获取输出
            stdout, stderr = await proc.communicate()
            
            # 检查执行结果
            if proc.returncode == 0:
                output = stdout.decode('utf-8')
                # 尝试解析JSON输出
            try:
                result = json.loads(output)
                # 检查返回的结果是否包含error字段
                if isinstance(result, dict) and 'error' in result:
                    print(f"C程序返回错误: {result['error']}")
                    return await self._load_from_json(user_id)
                return result
            except json.JSONDecodeError:
                print(f"C程序返回的数据不是有效的JSON: {output}")
                # 尝试从输出中提取有效的JSON部分
                try:
                    # 查找第一个'{'和最后一个'}'，提取JSON部分
                    json_start = output.find('{')
                    json_end = output.rfind('}') + 1
                    if json_start != -1 and json_end != -1:
                        json_part = output[json_start:json_end]
                        result = json.loads(json_part)
                        print(f"成功从混合输出中提取JSON: {result}")
                        return result
                except Exception:
                    print("无法从混合输出中提取有效的JSON")
                
                # 降级方案：尝试从JSON文件加载
                return await self._load_from_json(user_id)
            else:
                print(f"C程序执行失败: {stderr.decode('utf-8')}")
                # 降级方案：尝试从JSON文件加载
                return await self._load_from_json(user_id)
        except Exception as e:
            print(f"读取数据时发生错误: {str(e)}")
            # 降级方案：尝试从JSON文件加载
            return await self._load_from_json(user_id)
            
    async def _load_from_json(self, user_id: int) -> dict:
        """降级方案：从JSON文件加载数据"""
        try:
            file_path = os.path.join(self.data_dir, f"resume_{user_id}.json")
            if not os.path.exists(file_path):
                return {}
                
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}