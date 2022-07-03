from sklearn import tree
import ast
import json

# just for testing
if __name__ == "__main__":
    with open("/Users/danilamarius-cristian/PycharmProjects/pythonProject2/stats/data_german.json", "r") as f:
        stats_memory = json.loads(f.read())

    max_stats = 0
    stats_max = None

    for entry in stats_memory:
        if len(entry['stats']) > max_stats:
            max_stats = len(entry['stats'])
            stats_max = entry['stats']

    print(max_stats)
    print(stats_max)

    stats_wrong = 0
    stats_correct = 0

    features = []
    diagnosis = []
    stats_classes = []


    for entry in stats_memory:
        features = set(list(features) + list(entry['stats'].keys()))
        diagnosis = set(list(diagnosis) + [entry['diagnosis']])

        for stat in entry['stats']:
            stats_classes = set(list(stats_classes) + [entry['stats'][stat]])


    # print(stats_wrong)
    # print(stats_correct/34)

    features = list(features)
    print(features)
    print(len(features))

    print("Diagnosis")
    print(list(diagnosis))

    stats_classes = list(stats_classes)

    # Also append the placeholder class in case we do not have a feature
    stats_classes.append('X')

    print(stats_classes)


    # map the string disease to integers values to match trhe requirement by sklearn decision tree
    diagnosis_map = {}
    diag_index = 0
    for diag in diagnosis:
        diagnosis_map[diag] = diag_index
        diag_index += 1

    print(diagnosis_map)

    # also map the possible feature values to integer values to match the same requirement imposed by sklearn
    classes_map = {}
    class_index = 0
    for cls in stats_classes:
        classes_map[cls] = class_index
        class_index += 1

    X = []
    Y = []

    for entry in stats_memory:
        x_f = []
        for feature in features:
            if feature in entry['stats']:
                x_f.append(classes_map[entry['stats'][feature]])
            else:
                x_f.append(classes_map['X'])

        X.append(x_f)
        Y.append(diagnosis_map[entry['diagnosis']])


    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(X, Y)


    print("=========== PREDICTION ===========")
    print(clf.predict([X[10]]))
    print(Y[10])
    print(clf.predict([X[200]]))
    print(Y[200])
    print(diagnosis_map)
    print("=========== PREDICTION ===========")

    from sklearn.tree import plot_tree
    import matplotlib.pyplot as plt

    plt.figure()
    plot_tree(clf, filled=True)
    plt.title("Decision tree trained on all the iris features")
    plt.show()




