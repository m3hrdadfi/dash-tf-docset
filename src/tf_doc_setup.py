import collections
import fnmatch
import misaka
import os
import shutil
from tqdm import tqdm
from .utils import HighlighterRenderer
from .utils import copytree


class TFDocSetup:
    """ This class is designed to create DocSet for all versions of TensorFlow 2.x automatically."""
    ASSETS_PATH = os.path.abspath(os.path.join('assets'))
    ASSETS_MAP = {
        'css': ['style.css', 'override.css'],
        'images': ['icon.png', 'icon@2x.png'],
        'js': ['math.js', 'main.js']
    }
    TF_URL = 'https://github.com/tensorflow/tensorflow'
    TF_DOC_URL = 'https://github.com/tensorflow/docs'
    INFO_FILE = 'info.json'
    INFO = {'TRIED': 0}
    LENGTH = 70
    DASHING_CONFIG = {}
    STYLE_RELACER = '<p>page_type: reference<br>\n<style>{% include &quot;site-assets/css/style.css&quot; %}</style>'

    def _sanitize_dir_path(self, dir_path, abspath=False):
        """
        Cleans the `dir_path` suitable for our procedures.
        Args:
            dir_path (str): The root dir to where the docs would be saved.
            abspath (bool): If it is True, the new_dir_path return in absolute path format

        Returns:
            dir_path (str): The cleanised one.
        """
        # dir_path = os.path.abspath(os.path.join(dir_path))
        # dir_path = dir_path.split('/')
        # dir_path = dir_path.replace('.', '-')

        if abspath:
            dir_path = os.path.abspath(os.path.join(dir_path))

        return dir_path

    def _print(self, title, length=20, signature=True):
        """
        A fancy way to print out information in a human-readable form.

        Args:
            title (str): The title of information.
            length (int): A way to handle the margin of `#`.
            signature (bool): If it is True, it shows the `#` otherwise not.

        Returns:
            None
        """
        freedom = length - len(title)
        freedom = freedom // 2
        length = freedom * 2 + len(title) + 2
        bar = '#' * length

        if signature:
            print('\n{0}\n{1}\n{2}\n'.format(bar, '#' + ' ' * freedom + title + ' ' * freedom + '#', bar))
        else:
            print('\n{0}\n'.format(title))

    def md_to_html(self, md_dir_path, html_dir_path):
        """
        Converts the markdown format of TensorFlow-Doc into HTML format, which is suitable by DocSet Dashing.

        Args:
            md_dir_path: The root dir with TensorFlow generated markdown docs
            html_dir_path: The root dir to save rendered HTML files.

        Returns:
            None
        """
        renderer = HighlighterRenderer(flags=('hard-wrap',))
        extensions = (
            'tables',
            'fenced-code',
            'footnotes',
            'autolink',
            'strikethrough',
            'underline',
            'highlight',
            'quote',
            'superscript',
            'math',
            'no-intra-emphasis',
            'space-headers',
            'math-explicit',
            'disable-indented-code')
        renderer = misaka.Markdown(renderer, extensions=extensions)

        # converted filename -> number of (case sensitive) conflicts
        case_sensitive_conflicts = collections.defaultdict(int)

        # copy whole assets
        copytree(self.ASSETS_PATH, html_dir_path)

        root_len = len(md_dir_path)
        for root, dirnames, filenames in tqdm(os.walk(md_dir_path)):
            for filename in fnmatch.filter(filenames, '*.md'):
                md_file = os.path.join(root, filename)
                out_file = os.path.splitext(md_file)[0] + '.html'

                # Remove markdown root from path and append to HTML output root
                # Also strip path separators since
                #   os.path.join('foo', '/bar') == '/bar'
                out_file = os.path.join(html_dir_path, out_file[root_len:].strip(os.sep))

                # If destination folder does not exist, create it
                out_dir = os.path.dirname(out_file)
                if not os.path.exists(out_dir):
                    os.makedirs(os.path.dirname(out_file))

                # If the same file name (case insensitive) has already been
                # written to this folder, add a suffix to make it different to
                # avoid problems in case insensitive filesystems
                if case_sensitive_conflicts[out_file.lower()] > 0:
                    start, ext = os.path.splitext(out_file)
                    out_file = '{start}_{num}{ext}'.format(
                        start=start,
                        num=case_sensitive_conflicts[out_file.lower()],
                        ext=ext)

                case_sensitive_conflicts[out_file.lower()] += 1

                # Render Markdown and write it
                with open(md_file, 'r') as fin, open(out_file, 'w') as fout:
                    rendered = renderer(fin.read())
                    depth_path = '../' * (len(out_file.split(os.sep)) - 5)

                    # Replace initial metadata with link to our style
                    css, js = '', ''
                    for asset_name, asset_paths in self.ASSETS_MAP.items():
                        for asset_path in asset_paths:

                            if asset_name == 'css':
                                asset_path = '{0}{1}/{2}'.format(depth_path, asset_name, asset_path)
                                css += f'<link rel="stylesheet" href="{asset_path}" />\n'

                            if asset_name == 'js':
                                asset_path = '{0}{1}/{2}'.format(depth_path, asset_name, asset_path)
                                js += f'<script src="{asset_path}"></script>\n'

                    if rendered[:len(self.STYLE_RELACER)] == self.STYLE_RELACER:
                        rendered = rendered[len(self.STYLE_RELACER):] + '<p>'
                    rendered = css + rendered + js

                    # replace .md link with .html
                    rendered = rendered.replace('.md', '.html')
                    fout.write(rendered)

        shutil.copy(os.path.join(md_dir_path, '_toc.yaml'), html_dir_path)

    def run(self):
        raise NotImplementedError
