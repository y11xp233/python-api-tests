import pytest
import subprocess   #引入子进程模块，让你在 Python 脚本里直接运行外部命令
import sys
import os  #引入 Python 自带的 操作系统接口模块。它能让你在 Python 脚本里读写环境变量、拼接文件路径、执行系统命令等。

def run_tests():
    """运行所有接口和数据库验证用例，生成 Allure 报告"""
    print("=" * 50)
    print("开始运行自动化测试...")
    print("=" * 50)

    '''运行测试并生成 allure 原始数据,pytest.main(...) 执行完后，会返回一个数字，存到变量 result 里。这个数字叫退出码。
    退出码   0	所有测试都通过了；
            1	至少有一个测试失败了（断言没通过）
            2	测试过程中出现了错误（比如 Python 语法错误、找不到模块等）'''
    result = pytest.main([
        "-v",
        "--alluredir=./allure-results",
        "--clean-alluredir"
    ])

    # 2. 复制环境配置文件
    subprocess.run(["copy", "environment.properties", ".\\allure-results\\"], shell=True)

    # 3. 生成 HTML 报告      
    # os.environ一个字典，里面装着你电脑上的所有环境变量   
    # os.path.join(路径A, 路径B),把路径A和路径B智能拼接成一个完整的路径。
    #allure_cmd = os.path.join(os.environ["ALLURE_HOME"], "bin/allure.bat") ——这条没错但我系统太乱了导致找不到路径
    allure_cmd = r"E:\MyTestLearning\tools\allure\allure-2.33.0\bin\allure.bat"  #我直接把路径写死，系统就不用自己找了
    subprocess.run([allure_cmd, "generate", "./allure-results", "-o", "./allure-report", "--clean"])

    print("=" * 50)
    if result == 0:
        print("✅ 所有测试通过！")
    else:
        print("❌ 部分测试未通过，请查看 Allure 报告了解详情。")
    print("通过以下命令打开报告：")
    print("  allure open ./allure-report")
    print("=" * 50)
    return result

if __name__ == "__main__":
    sys.exit(run_tests())
    '''
    退出程序，并把 run_tests() 的返回值作为程序的退出码;
    sys.exit(run_tests()) 就是“测试跑完后,用一个数字告诉操作系统最终是成功还是失败”。如果所有测试通过(result == 0),run_tests() 返回 0,
    sys.exit(0) 表示“正常退出”。如果有测试失败(result != 0),run_tests() 返回非 0 值,sys.exit(非0) 表示“有错误”。以后如果你把
    py run_all_tests.py 集成到 Jenkins 或 GitLab CI 里,CI 系统会根据这个退出码判断本次测试是成功还是失败，决定要不要阻止代码合并。
    
    '''