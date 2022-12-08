import argparse

def main(args):
    clustering = dict()
    num_nodes = 0
    with open(args.input, 'r') as f:
        for edge in f:
            num_nodes += 1
            node, cluster, *_ = edge.strip().split(',')
            clustering[cluster] = clustering.get(cluster, []) + [node]
    num_singleton = sum(1 for nodes in clustering.values() if len(nodes) == 1)
    print(args.input, 'contains', len(clustering), 'clusters;', sum(1 for nodes in clustering.values() if len(nodes) > 1), 'are non-singleton; coverage is', \
        '{:.2f}%.'.format(100 * ((num_nodes - num_singleton) / num_nodes)))

if __name__=="__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input', type=str, required=True, help='input cluster')

    main(parser.parse_args())
