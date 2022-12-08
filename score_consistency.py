import argparse

def main(args):
    # Read in clusters
    new_cluster = dict()
    with open(args.cluster1, 'r') as f:
        for line in f:
            node, cluster, *_ = line.split(',')
            new_cluster[cluster] = new_cluster.get(cluster, []) + [node]
    og_cluster = dict()
    with open(args.cluster2, 'r') as f:
        for line in f:
            node, cluster, *_ = line.split(',')
            og_cluster[node] = cluster
    # Calculate consistency 
    volations = 0
    for cluster in new_cluster.values():
        contained_clusters = set()
        for node in cluster:
            contained_clusters.add(og_cluster[node])
            if len(contained_clusters) > 1:
                volations += 1
                break
    print(args.cluster1, 'had', volations, 'refinement consistency volations.')

if __name__=="__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-c1', '--cluster1', type=str, required=True, help="new cluster")
    parser.add_argument('-c2', '--cluster2', type=str, required=True, help="original cluster")

    main(parser.parse_args())
