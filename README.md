检查报告结构化 服务

## v1.py 
### 每个seg中, 统一放入一个 stack 进行拼接
### stack_v1 = [['关节'], ['囊', '周围软组织'], ['无'], ['明显肿胀']]

## v2.py
### stack 结构和v1不同.
### stack_v2 = [['symptom_pos', ['双']],
###            ['symptom_obj', ['膝关节部']],
###            ['object_part', ['诸骨']],
###            ['exam_result', ['骨质密度未见异常', '形态未见异常']]]


## v3.py 
### 根据100个样本统计结果, 定义多种情况

## v4.py
### 与v1, v2区别
### v1, v2获取将所有项后统一放入一个stack
### v4 分为多个不同stack (ppo_stack, ir, exam_stack等)

## v5.py
### 新的处理方式, 和后面v6方式相同, 建议使用v6进行测试.

## v6.py
### 当前最新版本， 建议按此脚本测试.
### python v6.py xxx (xxx可取0-99, 来源data/v6_test_data.py)

# data/samples.py
### 测试用数据.