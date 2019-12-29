import argparse
from src.tf_auto_doc_setup import TFAutoDocSetup


def main(dir_path, version):
    tf_auto_doc_setup = TFAutoDocSetup(version, dir_path)
    tf_auto_doc_setup.run()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='TF DocSet Generator')
    parser.add_argument(
        '-d',
        '--dir_path',
        required=True,
        type=str,
        help='Root dir to where the docs would be saved.')
    parser.add_argument(
        '-v',
        '--version',
        required=False,
        type=str,
        default='v2.0.0',
        help='What version of TensorFlow do you need?')
    args = parser.parse_args()
    main(args.dir_path, args.version)
