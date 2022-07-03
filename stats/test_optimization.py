import ast

if __name__ == "__main__":
    f = open('/Users/danilamarius-cristian/PycharmProjects/pythonProject2/stats/raw_index.json')

    memmory_json = ast.literal_eval(f.read())
    f.close()


    j = 0
    for k in range(0, 50000):
        for i in memmory_json['hits']['hits']:
            print(j)
            j += 1