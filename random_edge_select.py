import argparse
import random
random.seed(0)

def main(args):
    if args.output is None:
        name, extention = args.input.rsplit('.', 1)
        args.output = "{}-{:d}.{}".format(name, int(args.probability * 100), extention)
        remainder = "{}-{:d}-remainder.{}".format(name, int(args.probability * 100), extention)
    with open(args.input, 'r') as fi, open(remainder, 'w') as r, open(args.output, 'w') as fo:
        edge_count = 0
        for edge in fi:
            if random.random() < args.probability:
                edge_count += 1
                fo.write(edge)
            else:
                r.write(edge)
        print(edge_count, 'edges selected.')


if __name__=="__main__":
    def prob(f):
        try:
            f = float(f)
        except ValueError:
            raise argparse.ArgumentTypeError("%r not a floating-point literal" % (f,))
        if f < 0.0 or f > 1.0:
            raise argparse.ArgumentTypeError("%r not in range [0.0, 1.0]"%(f,))
        return f

    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input', type=str, required=True, help="input edge list")
    parser.add_argument('-o', '--output', type=str, help="output file name")
    parser.add_argument('-p', '--probability', type=prob, required=True, help="probability of retaining an edge")

    main(parser.parse_args())
