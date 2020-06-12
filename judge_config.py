
#   相应语言的源代码的后缀名
Language_Suffix = {
    "gcc"       :       [".c", ".h"]            , 
    "g++"       :       [".cpp", ".h", ".hpp"]  , 
    "python"    :       [".py"]                 ,
}

Single_Comment = {
    "gcc"       :       "//", 
    "g++"       :       "//",
    "python"    :       "#" ,
}

Multi_Comment = {
    "gcc"       :       [["/*", "*/"]]                      , 
    "g++"       :       [["/*", "*/"]]                      ,
    "python"    :       [["'''", "'''"], ['"""', '""""']]   ,
}