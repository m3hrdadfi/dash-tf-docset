import argparse
from src.tf_manual_doc_setup import TFManualDocSetup


def main(md_dir_path, html_dir_path, version):
    tf_manual_doc_setup = TFManualDocSetup(md_dir_path, html_dir_path, version)
    tf_manual_doc_setup.run()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='TF DocSet Generator')
    parser.add_argument(
        '-i',
        '--md_dir_path',
        required=True,
        type=str,
        help='The root dir with generated markdown docs.')
    parser.add_argument(
        '-o',
        '--html_dir_path',
        required=True,
        type=str,
        help='The root dir to save rendered HTML docs.')
    parser.add_argument(
        '-v',
        '--version',
        required=False,
        default='',
        type=str,
        help='What version of TensorFlow do you need?')
    args = parser.parse_args()
    main(args.md_dir_path, args.html_dir_path, args.version)
