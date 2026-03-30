#!/usr/bin/env python3
"""
Ray 客户端脚本 - 用于在 Ray 集群上执行任务
"""
import sys
import ray
import json

# Ray 集群地址
RAY_ADDRESS = "ray://100.74.227.40:10001"

def execute_task(task_input):
    """执行 Ray 任务"""
    try:
        # 连接 Ray 集群
        ray.init(address=RAY_ADDRESS, log_to_driver=False)
        
        # 解析输入
        try:
            task_data = json.loads(task_input)
        except:
            task_data = {"code": task_input}
        
        # 执行远程代码
        @ray.remote
        def remote_exec(code):
            import sys
            from io import StringIO
            
            # 捕获输出
            old_stdout = sys.stdout
            sys.stdout = buffer = StringIO()
            
            try:
                exec(code)
            except Exception as e:
                return {"error": str(e)}
            
            sys.stdout = old_stdout
            return {"output": buffer.getvalue()}
        
        # 执行并获取结果
        result = ray.get(remote_exec.remote(task_data.get("code", "")))
        
        ray.shutdown()
        
        return json.dumps(result, ensure_ascii=False)
    
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        task_input = " ".join(sys.argv[1:])
    else:
        task_input = sys.stdin.read()
    
    result = execute_task(task_input)
    print(result)
