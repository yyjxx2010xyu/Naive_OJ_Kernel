import os
import logging
import subprocess
import datetime
import time
import re
import psutil
import platform
import shlex
import sys

from judge_code import *


#   logging config
logging.basicConfig(level=logging.DEBUG,
                    filename='output.log',
                    datefmt='%Y/%m/%d %H:%M:%S',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(module)s - %(message)s')

#   SYS_TYPE == "Windows"
#   SYS_TYPE == "Linux"
SYS_TYPE = platform.system()

#   最大的输出长度否则OLE
MAX_OUTPUT = 1000000

'''
Input:  
    Problem_ID      题目编号

Output:
    Time_Limit      时间限制
    Memory_Limit    内存限制

Func:
   由Mysql得到 Time_Limit, Memory_Limit
'''

def Get_ProblemLimit(Problem_ID):

    problem = Problem.query.get(Problem_ID)
    Time_Limit = problem.Time_Limit
    Memory_Limit = problem.Memory_Limit
    #print(Time_Limit, Memory_Limit)
    return Time_Limit, Memory_Limit

'''
Construct Path 组成路径函数，具体的位置设定如下

Construct_Problem_Input_Path
Example:    .\problem\P1000\Input\input0.txt

Construct_Problem_Output_Path
Example:    .\problem\P1000\Output\output0.txt

Construct_Record_Path
Example:    .\record\R10000\ user0.txt
'''
def Construct_Problem_Input_Path(Problem_ID, Test_ID):
    Path = os.path.join(PROBLEM_DIR, str(Problem_ID), "Input", 'input%d.txt' % Test_ID)
    return Path
def Construct_Problem_Output_Path(Problem_ID, Test_ID):
    Path = os.path.join(PROBLEM_DIR, str(Problem_ID), "Output", 'output%d.txt' % Test_ID)
    return Path
def Construct_Record_Path(Record_ID, Test_ID):
    Path = os.path.join(RECORD_DIR, str(Record_ID), 'user%d.txt' % Test_ID)
    return Path

'''
Input:
    Record_ID       提交编号
    Language        程式语言
    
Output:
    Bool()        
        True        存在标号为Record_ID的提交
        False       不存在

Func:
    判断Record文件夹是否存在
'''
def Exist_Record(Record_ID, Language):
    Code_Path =  os.path.join(RECORD_DIR, str(Record_ID), Source_Code[Language])
    try:
        with open(Code_Path) as file:
            pass
    except IOError as e:
        print("Error:   Record Not Exist!!!")
        return False
    return True

'''
Input:
    Record_ID       提交编号
    Language        程式语言
    
Output:
    Bool()        
        True        不合法程式
        False       合法程式

Func:
    判断程序内是否有GOTO，是否有freopen等直接系统文件函数。
    内部设置了List Illegal_Keywords用于添加关键字
'''
def Illegal_Code(Record_ID, Language):

    Illegal_Keywords = ["goto", "freopen"]
    Code_Path =  os.path.join(RECORD_DIR, str(Record_ID), Source_Code[Language])
    with open(Code_Path, "r", encoding="UTF-8") as file:
        Code = file.read()


    for keyword in Illegal_Keywords:
        if Code.find(keyword) != -1:
            #if __debug__:
            #    print("Find Keyword : %s" % keyword, Code.find(keyword))
            logging.info("Find Keyword : %s  %d" % (keyword, Code.find(keyword)))
            return True
    return False

'''
Input:
    Problem_ID  题目编号

Output:
    count       数据点计数

Func:
    统计有多少个测试数据点       
'''
def Test_Count(Problem_ID):
    
    Probelm_Path = os.path.join(PROBLEM_DIR, str(Problem_ID), "Input")
    try:
        Files = os.listdir(Probelm_Path)
    except OSError as err:
        logging.error(err)
        return 0
    
    count = 0
    for item in Files:
        if item.endswith(".txt"):
            count += 1
    
    return count

'''
Input:
    Problem_ID  题目编号
    Record_ID   提交编号
    Test_ID     测试点编号

Output:
    string()
        "Accepted"              :   正确
        "Presentation Error"    :   格式错误
        "Output Limit Exceeded" :   输出超限
        "Wrong Answer"          :   错误

Func:
    比对程序运行结果和标准答案的区别
    TODO:默认忽略行末空格和换行，目前只做了简单的比较
'''

def Diff(Problem_ID, Record_ID, Test_ID):
    output_path = Construct_Problem_Output_Path(Problem_ID, Test_ID)
    user_path =  Construct_Record_Path(Record_ID, Test_ID)
    
    with open(output_path, "r", encoding="UTF-8") as file:
        output_data = file.read()
    with open(user_path, "r", encoding="UTF-8") as file:
        user_data = file.read()

    '''
    if __debug__:
        print("Output Data", output_data)
        print("User Data:", user_data)
    '''

    if len(user_data) > MAX_OUTPUT:
        return "Output Limit Exceeded"
    if output_data == user_data:
        return "Accepted"
    if output_data.split() == user_data.split():
        return "Presentation Error"        
    
    return "Wrong Answer"
   
'''

Func:
    杀死已经超时的进程
    有了Process.kill()，这个函数就不再使用了。
'''
def Kill_PID(pid):
    if SYS_TYPE == "Windows":
        os.popen("taskkill.exe /f /pid:" + str(pid))
    if SYS_TYPE == "Linux":
        os.popen("kill -9" + str(pid))


'''
Input:
    Record_ID       提交编号
    Problem_ID      题目编号
    Test_ID         测试点编号
    Time_Limit      时间限制
    Memory_Limit    内存限制
    Langugae        程式语言

Output:
    Time_Consume    时间消耗
    Memory_Consume  内存消耗

Func:
    在运行时记录程序的时间内存消耗，
    完成基于Python的内核，初步测量内存和时间
    TODO:   完成基于C的OJ内核（更准确
'''
def Test(Record_ID, Problem_ID, Test_ID, Time_Limit, Memory_Limit, Language):
    if SYS_TYPE == "Windows":
    	Cmd = Run_Cmd[Language]
    if SYS_TYPE == "Linux":
    	Cmd = Run_Cmd_Linux[Language]
    
    Return_Code = 0
    Time_Consume = 0
    Memory_Consume = 0
    
    input_path = Construct_Problem_Input_Path(Problem_ID, Test_ID)
    input_data = open(input_path, "rb")

    
    user_path = Construct_Record_Path(Record_ID, Test_ID) 
    user_data = open(user_path, "wb")
    
    Compile_DIR = os.path.join(RECORD_DIR, str(Record_ID))  
    Compile_EXE = os.path.join(RECORD_DIR, str(Record_ID), Cmd)     
	
    if SYS_TYPE == "Windows":
        WinStartUpInfo = subprocess.STARTUPINFO()
        WinStartUpInfo.dwFlags = subprocess.CREATE_DEFAULT_ERROR_MODE | subprocess.IDLE_PRIORITY_CLASS | subprocess.CREATE_NO_WINDOW | subprocess.CREATE_BREAKAWAY_FROM_JOB
        
    if Language in ["gcc", "g++"]:
        if SYS_TYPE == "Windows":
            Process = subprocess.Popen( [Compile_EXE],
                                        shell = False,      #   如果Shell = True 那么它会通过cmd来启动，其中的PID也是Cmd，导致测不出来内存
                                        stdin = input_data, 
                                        stdout = user_data, 
                                        stderr = subprocess.PIPE,
                                        startupinfo = WinStartUpInfo)
        else:
            Process = subprocess.Popen( [Compile_EXE],
                                        shell = False,      #   如果Shell = True 那么它会通过cmd来启动，其中的PID也是Cmd，导致测不出来内存
                                        stdin = input_data, 
                                        stdout = user_data, 
                                        stderr = subprocess.PIPE)
    if Language in ["python"]:
        if SYS_TYPE == "Windows":
            Process = subprocess.Popen( Cmd,
                                        cwd = Compile_DIR, 
                                        shell = False,      #   如果Shell = True 那么它会通过cmd来启动，其中的PID也是Cmd，导致测不出来内存
                                        stdin = input_data, 
                                        stdout = user_data, 
                                        stderr = subprocess.PIPE,
                                        startupinfo = WinStartUpInfo)
        else:
            Process = subprocess.Popen( shlex.split(Cmd),   #   很迷惑的一个bug，理论上应该是这样的，但是在Windows上得像上面一样
                                        cwd = Compile_DIR, 
                                        shell = False,      #   如果Shell = True 那么它会通过cmd来启动，其中的PID也是Cmd，导致测不出来内存
                                        stdin = input_data, 
                                        stdout = user_data, 
                                        stderr = subprocess.PIPE)


    start_time = time.perf_counter_ns()
    while True:
        #time.sleep(0.0001)
        Return_Code = Process.poll()
        #print(Return_Code)
        if Return_Code is not None:
        	break
        #   Checking TLE
        end_time = time.perf_counter_ns()

        Time_Consume = (end_time - start_time) / 1000000000.0
	
        #   Process Finished
        if psutil.pid_exists(Process.pid) == False:
            if Return_Code is None:
                Return_Code = Process.poll()
            #print("Return Code:", Return_Code)
            break
        
        #if __debug__:
        #    print(Process.pid)

        #   Setting TLE
        if  Time_Consume > Time_Limit:
            #   Kill Task
            Process.kill()
            #input_data.close()
            #user_data.close()
            return Time_Consume, Memory_Consume , Return_Code

        #   Process finished during this code
        #   程序很可能就运行结束，在统计的过程中，因而统计时可能会报错
        try:
            #   Checking MLE
            Psu_Process = psutil.Process(Process.pid)
            Memory_Consume = Psu_Process.memory_info().rss  / 1024 / 1024
            #print("rss:",  Psu_Process.memory_info().rss,"vms:",  Psu_Process.memory_info().vms)
            #print(Psu_Process.memory_info())
        except  Exception as e:
            if Return_Code is None:
                Return_Code = Process.poll()
            break

       
        #   Setting MLE
        if Memory_Consume > Memory_Limit:
            #   Kill Task
            Process.kill()
            #input_data.close()
            #user_data.close()
            return Time_Consume, Memory_Consume, Return_Code

        '''
        最原始的想法，但是在资料搜索的时候发现了psutil
        #   Checking MLE
        Cat_Cmd = "cat /proc/%d/status" % Process.pid
        Cat_Ret = os.popen(Cat_Cmd).read()
        
        #   Search VmPeak:
        Cat_Patten = re.compile(r'VmPeak:(.*)\d+KB')
        Cur_Memory = Cat_Patten.findall(Cat_Ret)
        '''

    '''
    data = Process.stdout.read()
    user_data.write(data)
    
    Process.stdout.close()
    input_data.close()
    user_data.close()
    '''
    if Return_Code is None:
        Return_Code = 0
    return Time_Consume, Memory_Consume, Return_Code

'''
Input:  
    Student_ID      学生编号
    Problem_ID      题目编号
    Record_ID       提交编号
    Language        程式语言
    Time_Limit      时间限制
    Memory_Limit    内存限制
    Info            初始化的Info

Output:
    Info            记录过Max_Time和Max_Memory的Info

Func:
    总的测试模块 1. 测试程序的时间消耗和内存消耗
                2. 计算程序的正确性和返回值
                3. 统计每个点的运行结果，统计总的分数，存储在List中
'''
    
def Judge(Student_ID, Problem_ID, Record_ID, Language, Time_Limit, Memory_Limit, Info):
    
    
    Count = Test_Count(Problem_ID)
    
    Max_Time = 0
    Max_Memory = 0
    
    #   Bias 因为Get_ProblemLimit还没写
    # Time_Limit = 2          #   2S
    # Memory_Limit = 100      #   100MB
    Extra_Time = 0
    Extra_Memory = 0


    for Test_ID in range(Count):
        Time_Consume, Memory_Consume, Return_Code = Test(  Record_ID,
                                                                Problem_ID,
                                                                Test_ID,
                                                                Time_Limit + Extra_Time,
                                                                Memory_Limit + Extra_Memory,
                                                                Language)
        #   时间或内存超限
        '''
        if __debug__:
            print("Consume  Time: ", Time_Consume, "Memory: ", Memory_Consume)
            print("Limit    Time: ", Time_Limit, "Memory: ", Memory_Limit)
        '''

        if Time_Consume > Time_Limit:
            Info["Judge_Result"].append(Judge_Code["Time Limit Exceeded"])
            continue
        if Memory_Consume > Memory_Limit:
            Info["Judge_Result"].append(Judge_Code["Memory Limit Exceeded"])
            continue
        if Return_Code != 0:
            Info["Judge_Result"].append(Judge_Code["Runtime Error"])
            continue

        #   记录花费最长的时间和最多内存
        if Max_Time < Time_Consume:
            Max_Time = Time_Consume
        if Max_Memory < Memory_Consume:
            Max_Memory = Memory_Consume
        
        
        Diff_Ret = Diff(Problem_ID, Record_ID, Test_ID)
        
        Info['Judge_Result'].append(Judge_Code[Diff_Ret])
        
        logging.info(Info)
    
    Info["Time_Consume"] = Max_Time
    Info["Memory_Consume"] = Max_Memory
    return Info
        
'''
Input:
    Record_ID       提交编号
    Language        程式语言

Output:
    bool()
        True        编译成功
        False       编译错误

Func:
    编译程序，并记录编译信息到error.log中
'''
def Compile(Record_ID, Language):
    Compile_Dir = os.path.join(RECORD_DIR, str(Record_ID))
    
    if Language not in Build_Cmd.keys():
        return False
    
    if SYS_TYPE == "Windows":
    	Build_Command = Build_Cmd[Language]
    if SYS_TYPE == "Linux":
    	Build_Command = Build_Cmd_Linux[Language]
    	
    Popen_Ret = subprocess.Popen(
        Build_Command,
        shell = True,
        cwd = Compile_Dir,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE)
    
    Out, Err = Popen_Ret.communicate()  # 获取编译错误信息
    
    #if __debug__:
    #    print("Out: ", Out, "Err: ", Err)
    
    Err_Path = os.path.join(RECORD_DIR, str(Record_ID), 'error.log')
    f = open(Err_Path, 'wb')
    if Err != b"":
        f.write(Err)
    if Err != b"":
        f.write(Out)
    f.close()
    
    # 编译成功
    if Popen_Ret.returncode == 0:  
        return True
    
    return False

def Check_Headline(Record_ID, Language):
    Code_Path =  os.path.join(RECORD_DIR, str(Record_ID), Source_Code[Language])
    with open(Code_Path, "r", encoding="UTF-8") as file:
        Code = file.read()
    
    pattern = re.compile(r'/* (?P<number>\d{7}) (?P<class>[\u4e00-\u9fa5]{1}\d{1}[\u4e00-\u9fa5]{1}) (?P<name>[\u4e00-\u9fa5]{2,3})')
    res = re.findall(pattern, Code)
    if len(res) == 1 and len(res[0]) == 3:
        return False
    
    pattern = re.compile(r'// (?P<number>\d{7}) (?P<class>[\u4e00-\u9fa5]{1}\d{1}[\u4e00-\u9fa5]{1}) (?P<name>[\u4e00-\u9fa5]{2,3})')
    res = re.findall(pattern, Code)
    if len(res) == 1 and len(res[0]) == 3:
        return False

    return True

'''
Input:
    Student_ID      学生编号
    Problem_ID      题目编号
    Record_ID       提交编号
    Language        程式语言
    Time_Limit      时间限制
    Memory_Limit    内存限制

Output:
    Judge_Ret
        Info = {
        "Student_ID": Student_ID,       //  学生编号 
        "Problem_ID": Problem_ID,       //  题目编号
        "Record_ID": Record_ID,         //  提交编号
        "Time_Consume": 0,              //  时间消耗
        "Memory_Consume": 0,            //  内存消耗
        "Judge_Result": [],             //  评测结果 List
        }

Func:
    对于用的一次提交进行评测
'''
def Run_Code(Student_ID, Problem_ID, Record_ID, Language, Time_Limit, Memory_Limit, Enable_HeadLine):
    
    Info = {
        "Student_ID": Student_ID,
        "Problem_ID": Problem_ID,
        "Record_ID": Record_ID,
        "Time_Consume": 0,
        "Memory_Consume": 0,
        "Judge_Result": [],
    }
    if Exist_Record(Record_ID, Language) == False:
        Info["Judge_Result"].append(Judge_Code["Compile Error"])
        return Info

    if Illegal_Code(Record_ID, Language):
        Info["Judge_Result"].append(Judge_Code["Illegal Code"])
        return Info

    if Enable_HeadLine and Check_Headline(Record_ID, Language):
        Info["Judge_Result"].append(Judge_Code["Illegal Code"])
        return Info

    Compile_Ret = Compile(Record_ID, Language)

    #   编译错误
    if Compile_Ret == False:
        Info["Judge_Result"].append(Judge_Code["Compile Error"])
        logging.info(Info)
        return Info
    
    Judge_Info = Judge(
        Student_ID, 
        Problem_ID, 
        Record_ID, 
        Language,
        Time_Limit,
        Memory_Limit,
        Info)
    
    logging.info(Judge_Info)

    if len(Info["Judge_Result"]) == 0:
        Info["Judge_Result"].append(Judge_Code["System Error"])
    return Judge_Info

'''
func 如何获得任务现在还没想好
'''
'''
def Get_Task():    
    Run(Student_ID, Problem_ID, Record_ID, Language)
'''
def Get_Task():
    print(__file__)
    while True:
        recordList = Record.query.filter(Record.Status=='WAITING').all()
        # print (recordList)
        if recordList == []:
            break
        for record in recordList:
            record.Status = "JUDGING"
            db.session.commit()
            Time_Limit, Memory_Limit = Get_ProblemLimit(record.Problem_ID)
            Info = Run_Code(record.Student_ID,record.Problem_ID,record.Record_ID,SuffixCommand[record.Language], Time_Limit, Memory_Limit, 1)
            print (Info["Judge_Result"])
            for result in Info["Judge_Result"]:
                if result != "AC":
                    record.Status = result
                    break
            if record.Status == "JUDGING" or record.Status == "WAITING":
                record.Status = "AC"
            db.session.commit()
        time.sleep(1)

    
if __name__ == "__main__":
    
    Info = Run_Code("100000", "P1000", "RCPP_AC", "g++", 1, 128)
    print(Info["Judge_Result"])
    pass
