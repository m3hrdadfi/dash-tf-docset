import json
import os
from .tf_doc_setup import TFDocSetup
from .dashing import DASHING


class TFManualDocSetup(TFDocSetup):
    """ This class is designed to create DocSet for all versions of TensorFlow 2.x automatically."""

    def __init__(self, md_dir_path, html_dir_path, version=''):
        """
        Initializing the DocSet automation based on which version of x in TensorFlow 2.x

        Args:
            md_dir_path (str): The root dir with generated markdown docs
            html_dir_path (str): The root dir to save rendered HTML files
        """

        self.md_dir_path = os.path.join(md_dir_path)
        self.html_dir_path = os.path.join(html_dir_path)
        os.makedirs(self.html_dir_path, exist_ok=True)

        # configures the dashing
        self.DASHING_CONFIG = {
            'name': '{0} {1}'.format('TensorFlow', version),
            'package': '{0}{1}'.format('tensorflow', version),
            'index': 'index.html',
            'icon16x16': os.path.join('images', 'icon.png'),
            'icon32x32': os.path.join('images', 'icon@2x.png')
        }

    def run(self):
        """
        The procedure of manual-generating the DocSet for TensorFlow 2.x

        Returns:
            None
        """

        self._print('Preparing documents for DocSet [Manual]', self.LENGTH)
        self.md_to_html(self.md_dir_path, self.html_dir_path)
        dashing_cfg = json.loads(DASHING)
        for k, v in self.DASHING_CONFIG.items():
            dashing_cfg[k] = v

        with open(os.path.join(self.html_dir_path, 'dashing.json'), 'w') as fout:
            json.dump(dashing_cfg, fout)

        self._print('It is done!', signature=True)
