import argparse
import random
import os
from tqdm import tqdm
from math import comb
from collections import Counter
random.seed(0)

def main(args):
    clustering = dict()
    cluster_map = dict()
    with open(args.clustering, 'r') as f:
        for line in f:
            n, c, *_ = line.strip().split(',')
            assert isinstance(n, str)
            clustering.setdefault(c, []).append(n)
            assert len(clustering.get(c)) != 0
            cluster_map[n] = c
        #cluster_map = {parts[0]:parts[1] for line in f if (parts := line.strip().split(','))}

    #connections = {n1:{n2:False for n2 in clustering} for n1 in tqdm(clustering, desc="init")}
    
    name, extension = args.clustering.rsplit(os.sep, 1)[-1].rsplit('.', 1)
    output_name = "{}-{}-edges-{}-{}.{}".format(args.output, name, str(args.multiplier).replace('.','_'), \
        'removed' if args.remove else 'added', extension)

    connections = dict()
    n_edges = Counter()
    file_len = len(open(args.edge_list, 'r').readlines())
    n_external = file_len - sum(n_edges.values())
    edges_to_keep = [True] * n_external
    if args.remove:
        for i in random.sample(edges_to_keep, int(n_external * args.multiplier)):
            edges_to_keep[i] = False
    removed = 0
    with open(args.edge_list, 'r') as fi, open(output_name, 'w') as fo:
        for line in tqdm(fi, total=file_len, desc="build adjacency"):            
            n1, n2 = line.strip().split('\t')
            connections.setdefault(n1, dict())[n2] = True
            connections.setdefault(n2, dict())[n1] = True
            if cluster_map[n1] == cluster_map[n2]:
                n_edges[cluster_map[n1]] += 1
            elif not edges_to_keep[removed]:
                removed += 1
                continue            
            fo.write(line)
            
        if not args.remove:
            for cluster, nodes in clustering.items():
                num_to_add = int(n_edges[cluster] * args.multiplier)
                added = 0
                if comb(len(nodes), 2) < num_to_add + n_edges[cluster]:
                    num_to_add = comb(len(nodes), 2) - n_edges[cluster]
                print(num_to_add, 'edges to add to cluster', cluster)
                with tqdm(total=num_to_add, desc='cluster {}'.format(cluster)) as pbar:
                    while added < num_to_add:
                        n1, n2 = random.sample(nodes, 2)
                        #print(type(n1), type(n2), n1, n2)
                        if not connections.get(n1, dict()).get(n2, dict()):
                            fo.write('{}\t{}\n'.format(n1,n2))
                            connections.setdefault(n1, dict())[n2] = True
                            connections.setdefault(n2, dict())[n1] = True
                            added += 1
                            pbar.update(1)

        # for n1, n2 in tqdm(combinations(clustering, 2), total=comb(len(clustering), 2)):
        #     if connections[n1].get(n2, False) or (random.random() < args.probability and clustering[n1] == clustering[n2]):
        #         f.write('{}\t{}\n'.format(n1, n2)) 


if __name__ == "__main__":
    def mult(f):
        try:
            f = float(f)
        except ValueError:
            raise argparse.ArgumentTypeError("%r not a floating-point literal" % (f,))
        if f < 0.0:
            raise argparse.ArgumentTypeError("%r not greater then 0.0"%(f,))
        return f

    parser = argparse.ArgumentParser()

    parser.add_argument('-e', '--edge-list', type=str, required=True, help='edge list file')
    parser.add_argument('-c', '--clustering', type=str, required=True, help='clustering file')
    parser.add_argument('-o', '--output', type=str, default="", help='output file name prefix')
    parser.add_argument('-m', '--multiplier', type=mult, required=True, help="multipier")
    parser.add_argument('-r', '--remove', action='store_true', help='remove edges')

    main(parser.parse_args())
