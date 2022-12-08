import argparse
import pandas as pd
import numpy as np
from tqdm import tqdm

def main(args):
    # Get list of nodes
    clusters = pd.read_csv(args.input_cluster, names=['cluster', 'node'], sep=' ')
    nodes = clusters.loc[clusters['cluster'].isin(args.clusters)]['node']
    print(len(nodes), 'nodes extracted.')
    node_map = dict() #{node:i for i, node in enumerate(nodes)}
    # Write list of nodes
    with open(args.output_prefix + '-map.csv', 'w') as out_map:
        for i, node in enumerate(nodes):
            node_map[np.int64(node)] = i
            out_map.write('{:d},{:d}\n'.format(i,node))
    # Extract edges from dataset edgelist
    edge_count = 0
    dataset_size = sum(1 for _ in open(args.dataset, 'r')) - 1
    with open(args.dataset, 'r') as in_edges, open(args.output_prefix + '-edges.csv', 'w') as out_el:
        for edge in tqdm(in_edges, total=dataset_size):
            try:
                citing, cited = map(np.int64, edge.split(','))
                if citing in nodes.values and cited in nodes.values:
                    edge_count += 1
                    out_el.write('{:d},{:d}\n'.format(node_map[citing], node_map[cited]))
            except ValueError:
                continue
    print(edge_count, 'edges extracted.')


if __name__=="__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input-cluster', type=str, required=True,
                        help='input clustering')
    parser.add_argument('-d', '--dataset', type=str, required=True,
                        help='dataset edgelist')
    parser.add_argument('-c', '--clusters', type=int, nargs='+', required=True,
                        help='clusters to be extracted')
    parser.add_argument('-o', '--output-prefix', type=str, required=True,
                        help='output filename')

    main(parser.parse_args())                    
