import json


class JsonLoader(object):
    """
    JsonLoader 类, 读取初始 goldset.json 数据中的文本 text 和标注 target.
    """

    def __init__(self,
                 json_file_path="/users/hk/dev/ExamStandard/data/",
                 json_file_name="goldset_93.json"):
        self.file_path = json_file_path
        self.file_name = json_file_name

    # 读取json数据
    def load_file(self):
        print(self.file_path)
        loaded_file = []
        line_count = 0
        count = 0
        print('Source file: {}'.format(self.file_name))

        with open(self.file_path + self.file_name, 'r', encoding='utf-8') as f:
            for line in f:
                line_count = line_count + 1
                if line_count % 1000 == 0:
                    print('line --- {}'.format(line_count))
                try:
                    dic = json.loads(line)
                    loaded_file.append(dic)
                    count = count + 1
                except Exception as e:
                    print(e)
                    print('error line: {}'.format(line))
        print('Read source file finished: total={}, valid={}\n'.format(line_count, count))

        return loaded_file
