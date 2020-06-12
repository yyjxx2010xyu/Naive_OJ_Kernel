import unittest
import warnings
import time

from judge import *
from judge_code import *

Student_ID = "10000"
Problem_ID = "1"

Test_Code_Status = [
    "Accepted",
    "Time Limit Exceeded",
    "Memory Limit Exceeded",
    "Wrong Answer",
    "Runtime Error",
    "Output Limit Exceeded",
    "Compile Error",
    "Presentation Error",
    "Illegal Code",
]

Test_Record =   {
    "g++":      {
        "Accepted"              :   "RCPP_AC"   ,
        "Time Limit Exceeded"   :   "RCPP_TLE"  ,
        "Memory Limit Exceeded" :   "RCPP_MLE"  ,
        "Wrong Answer"          :   "RCPP_WA"   ,
        "Runtime Error"         :   "RCPP_RE"   ,
        "Output Limit Exceeded" :   "RCPP_OLE"  ,
        "Compile Error"         :   "RCPP_CE"   ,
        "Presentation Error"    :   "RCPP_PE"   ,
        "Illegal Code"          :   "RCPP_IC"   ,
    },
    "gcc":      {
        "Accepted"              :   "RC_AC"     ,
        "Time Limit Exceeded"   :   "RC_TLE"    ,
        "Memory Limit Exceeded" :   "RC_MLE"    ,
        "Wrong Answer"          :   "RC_WA"     ,
        "Runtime Error"         :   "RC_RE"     ,
        "Output Limit Exceeded" :   "RC_OLE"    ,
        "Compile Error"         :   "RC_CE"     ,
        "Presentation Error"    :   "RC_PE"     ,
        "Illegal Code"          :   "RC_IC"     ,
    },
    "python":   {
        "Accepted"              :   "RPY_AC"   ,
        "Time Limit Exceeded"   :   "RPY_TLE"  ,
        "Memory Limit Exceeded" :   "RPY_MLE"  ,
        "Wrong Answer"          :   "RPY_WA"   ,
        "Runtime Error"         :   "RPY_RE"   ,
        "Output Limit Exceeded" :   "RPY_OLE"  ,
        "Compile Error"         :   "RPY_CE"   ,
        "Presentation Error"    :   "RPY_PE"   ,
        "Illegal Code"          :   "RPY_IC"   ,
    }
}


class TestJudgeModule(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter('ignore', ResourceWarning)

    def test_Judge(self):
        for Language in Language_List:
            for Test_Status in Test_Code_Status:
                Info = Run_Code(Student_ID, Problem_ID, Test_Record[Language][Test_Status], Language, 10, 128, 0)
                print("Test Lang: %s Test Status: %s" % (Language, Test_Status), "Info : ", Info["Judge_Result"])
                self.assertTrue(Info["Judge_Result"][0] == Judge_Code[Test_Status])
                time.sleep(0.2)

if __name__ == "__main__":
    unittest.main()
