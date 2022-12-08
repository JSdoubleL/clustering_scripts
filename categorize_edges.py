import argparse

def main(args):
    clustering = dict()
    with open(args.clustering, 'r') as f:
        for line in f:
            node, cluster, *_ = line.split(',')
            clustering[node] = cluster

    with open(args.output_prefix + '-in-edges.csv', 'w') as in_edges,  \
        open(args.output_prefix + '-out-edges.csv', 'w') as out_edges, \
        open(args.edges, 'r') as f:
        for edge in f:
            n1, n2 = edge.strip().split('\t')
            try:
                if clustering[n1] == clustering[n2]:
                    in_edges.write(edge)
                else:
                    out_edges.write(edge)
            except KeyError:
                continue


if __name__=="__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-e', '--edges', type=str, required=True, help="edges list file (tab separated)")
    parser.add_argument('-c', '--clustering', type=str, required=True, help="clustering file (csv)")
    parser.add_argument('-o', '--output-prefix', type=str, required=True, help="output prefix")

    main(parser.parse_args())
