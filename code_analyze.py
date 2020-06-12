import os
import linecache
import judge_config

'''
Input:  
    Code_Dir    提交目录
    Language    语言

Output:
    Source_List 源文件列表名

Func:
    返回提交目录下的所有源文件名
'''

def Scan_Dir(Code_Dir, Language):
    Source_Dir = os.walk(Code_Dir)
    Source_List = []
    for _ , _ , files in Source_Dir:
        for file in files:
            for suffix in judge_config.Language_Suffix[Language]:
                if file.endswith(suffix):
                    Source_List.append(file)
    return Source_List

'''
Input:  
    Code_Dir        提交目录
    Language        语言

Output:
    Line_Code       代码行数
    Line_Comment    注释行数
    Line_Blank      空白行数

Func:
    统计提交目录下的所有源文件的注释情况
'''
def Count_Comment(Code_Dir, Language):
    Code_List = Scan_Dir(Code_Dir, Language)
    Line_Code, Line_Comment, Line_Blank = 0, 0, 0
    for Code_Name in Code_List:
        Code_Path = os.path.join(Code_Dir, Code_Name)
        linecache.clearcache()
        try:
            Lines = linecache.getlines(Code_Path)
        except Exception as e:
            print("Unable to open the file")
            return 0

        for Line in Lines:
            Line = Line.strip() 
            if Line == "" and not Multi_Comment:
                Line_Blank += 1
                continue
            if Line.startswith(judge_config.Single_Comment[Language]):
                Line_Comment += 1
                continue
            for Comment_Begin, _ in judge_config.Multi_Comment[Language]:
                if Line.startswith(Comment_Begin):
                    Multi_Comment = True
            if not Multi_Comment:
                Line_Code += 1
            else:
                Line_Comment += 1
            for _, Comment_End in judge_config.Multi_Comment[Language]:
                if Line.endswith(Comment_End):
                    Multi_Comment = False
    return Line_Code, Line_Comment, Line_Blank
            

if __name__ == "__main__":

    #Code_List = Scan_Dir(".\\record\\RCPP_AC", "g++")    
    #print(Code_List)
    Line_Code, Line_Comment, Line_Blank = Count_Comment(".\\record\\RCPP_AC", "g++")

    print("Line_Code: ", Line_Code)
    print("Line_Comment: ", Line_Comment)
    print("Line_Blank: ", Line_Blank)
