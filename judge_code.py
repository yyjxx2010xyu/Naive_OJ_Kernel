#   所支持的语言
Language_List = ["gcc", "g++", "python"] 

#   题目的数据路径
PROBLEM_DIR = ".\\problem"

#   具体每一条Record存储在record文件夹中，record中文件名时Record_ID
RECORD_DIR = ".\\record"

#   每一个状态的结果
'''
Judge_Code = {
    "Waiting"               :   0,
    "Accepted"              :   1,
    "Time Limit Exceeded"   :   2,
    "Memory Limit Exceeded" :   3,
    "Wrong Answer"          :   4,
    "Runtime Error"         :   5,
    "Output Limit Exceeded" :   6,
    "Compile Error"         :   7,
    "Presentation Error"    :   8,
    "Illegal Code"          :   9,
    "System Error"          :   11,
    "Judging"               :   12,
}
'''
# 为了与forms-SubmitResultForm 保持一致
Judge_Code = {
    "Waiting"               :   "WAITING",
    "Accepted"              :   "AC",
    "Time Limit Exceeded"   :   "TLE",
    "Memory Limit Exceeded" :   "MLE",
    "Wrong Answer"          :   "WA",
    "Runtime Error"         :   "RE",
    "Output Limit Exceeded" :   "OLE",
    "Compile Error"         :   "CE",
    "Presentation Error"    :   "PE",
    "Illegal Code"          :   "IC",
    "System Error"          :   "SE",
    "Judging"               :   "JUDGING",
    "Unknown User"          :   "UU"
}


#   用户提交的源码文件
Source_Code = {
    "gcc":      "main.c",
    "g++":      "main.cpp",
    "python":   "main.py",
}

#   编译用户源码文件命令 Windows
Build_Cmd = {
    "gcc":      "gcc main.c -o main -Wall -lm -std=c99 --static -DONLINE_JUDGE",   #no -O2
    "g++":      "g++ main.cpp -o main",           #   no -O2  -Wall -lm --static -DONLINE_JUDGE
    "python":   "python -m compileall -b ",
}

#   运行时的命令 Linux
Build_Cmd_Linux = {
    "gcc":      "gcc main.c -o main -Wall -lm -std=c99 --static -DONLINE_JUDGE",   #no -O2
    "g++":      "g++ main.cpp -o main",           #   no -O2  -Wall -lm --static -DONLINE_JUDGE
    "python":   "python3 -m compileall -b ",
}

#   运行时的命令 Windows
Run_Cmd = {
    "g++":      "main",
    "gcc":      "main",
    "python":   "python main.pyc",
}

#   运行时的命令 Linux
Run_Cmd_Linux = {
    "g++":      "main",
    "gcc":      "main",
    "python":   "python3 main.pyc",
}

