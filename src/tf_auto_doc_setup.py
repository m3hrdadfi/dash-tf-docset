import json
import os
import subprocess
import sys
from .tf_doc_setup import TFDocSetup
from .utils import run_task, install_package, search_package
from .dashing import DASHING


class TFAutoDocSetup(TFDocSetup):
    """ This class is designed to create DocSet for all versions of TensorFlow 2.x automatically."""

    def __init__(self, version, dir_path):
        """
        Initializing the DocSet automation based on which version of x in TensorFlow 2.x

        Args:
            version (str): What version of TensorFlow do you need?
            dir_path (str): Root dir to where the docs would be saved.
        """
        self.version = version
        self.dir_path = dir_path
        self.dir_path = os.path.join(self.dir_path, version)
        # checks if the dir_path exist or not
        os.makedirs(self.dir_path, exist_ok=True)

        # writes/reads information for such details like the number of tried
        self.INFO = self._setup(os.path.join(self.dir_path, self.INFO_FILE))
        self.TRIED = int(self.INFO.get('TRIED', 0))

        # initials the dir paths
        self.md_dir_path = self._check_dir_path(
            os.path.join(self.dir_path, 'md--{0}'.format(self.TRIED)))
        self.html_dir_path = self._check_dir_path(
            os.path.join(self.dir_path, 'html--{0}'.format(self.TRIED)))
        self.tf_dir_path = self._check_dir_path(
            os.path.join(self.dir_path, 'tf--{0}'.format(self.TRIED)))

        # configures the dashing
        self.DASHING_CONFIG = {
            'name': '{0} {1}'.format('TensorFlow', version),
            'package': '{0}{1}'.format('tensorflow', version),
            'index': 'index.html',
            'icon16x16': os.path.join('images', 'icon.png'),
            'icon32x32': os.path.join('images', 'icon@2x.png')
        }

    def _setup(self, info_path):
        """
        Writes/Reads the info.json file for the sake of knowing how many attempts have been made!

        Args:
            info_path (str): The name of the information file (default: info.json).

        Returns:
            info (dict): The information parameters!
        """
        info = self.INFO
        if os.path.exists(info_path):
            with open(info_path) as f:
                info = json.load(f)
        else:
            with open(info_path, 'w') as f:
                json.dump(info, f)

        return info

    def _update_info(self, info_path):
        self.INFO['TRIED'] = self.TRIED + 1
        with open(info_path, 'w') as f:
            json.dump(self.INFO, f)

    def _check_dir_path(self, dir_path):
        """
        Checks the `dir_path` version if it has been already made or not.

        Args:
            dir_path (str): The root dir to where the docs would be saved.

        Returns:
            new_dir_path (str): The new root dir to where the docs would be saved.
        """
        dir_path_split = dir_path.split('--')
        tried = int(dir_path_split[-1])

        if os.path.exists(dir_path) and len(os.listdir(dir_path)) > 0:
            tried += 1

        new_dir_path = '{0}--{1}'.format(dir_path_split[0], tried)
        os.makedirs(new_dir_path, exist_ok=True)
        return new_dir_path

    def _print(self, title, length=20, hashing=True):
        """
        A fancy way to print out information in a human-readable form.

        Args:
            title (str): The title of information.
            length (int): A way to handle the margin of `#`.
            hashing (bool): If it is True, it shows the `#` otherwise not.

        Returns:
            None
        """
        freedom = length - len(title)
        freedom = freedom // 2
        length = freedom * 2 + len(title) + 2
        bar = '#' * length

        if hashing:
            print('\n{0}\n{1}\n{2}\n'.format(bar, '#' + ' ' * freedom + title + ' ' * freedom + '#', bar))
        else:
            print('\n{0}\n'.format(title))

    def _install_tf_doc(self):
        """
        The first step is to install TensorFlow-docs in `https://github.com/tensorflow/docs`.

        Raises:
            Exception: If it could not install the `tensorflow-doc`.

        Returns:
            status (:list:`bool`)
        """
        status = [False] * 1

        if not search_package('tensorflow_docs', None):
            installed = install_package('git+{0}'.format(self.TF_DOC_URL), 'tensorflow_docs')
            if installed:
                status[0] = True
        else:
            self._print('The `tensorflow_docs` has already been installed!', hashing=False)
            status[0] = True

        return status

    def _install_tf(self, tf_version, tf_output, md_output):
        """
        The second step is to install TensorFlow->Docs and TensorFlow in `https://github.com/tensorflow/tensorflow`.

        Args:
            tf_version (str): The version of TensorFlow which is used
            tf_output (str): The root dir for clone of TensorFlow->Docs
            md_output (str): The root dir for output of TensorFlow->Docs in markdown format.

        Returns:
            status (:list:`bool`)
        """
        status = [False] * 3

        # print('tf_output', tf_output)
        # print('status', not os.path.exists(tf_output) or not len(os.listdir(tf_output)) > 0)
        if not os.path.exists(tf_output) or not len(os.listdir(tf_output)) > 0:
            # subprocess.call(['git', 'clone', '--branch', tf_version, self.TF_URL, tf_output])
            _, s = run_task('git clone --progress --branch {0} {1} {2}'.format(tf_version, self.TF_URL, tf_output))
            status[0] = s
        else:
            status[0] = False

        if not search_package('tensorflow', tf_version[1:].replace('-', '')):
            installed = install_package('tensorflow', 'tensorflow', tf_version[1:])
            if installed:
                status[1] = True

        else:
            self._print('The `tensorflow=={0}` has already been installed!'.format(tf_version), hashing=False)
            status[1] = True

        doc_path = os.path.join(tf_output, 'tensorflow', 'tools', 'docs')
        if doc_path not in sys.path:
            sys.path.insert(0, doc_path)

        # subprocess.call(['python', os.path.join(doc_path, 'generate2.py'), '--output_dir={0}'.format(md_output)])
        generate_py = 'generate2.py' if self.version[1] == '2' else 'generate.py'
        _, s = run_task('python {0} --output_dir={1}'.format(os.path.join(doc_path, generate_py),
                                                             self._sanitize_dir_path(md_output, abspath=True)))
        status[2] = s

        return status

    def run(self):
        """
        The procedure of auto-generating the DocSet for TensorFlow 2.x

        Returns:
            None
        """
        self._print('Installing tensorflow-docs', self.LENGTH)
        status = self._install_tf_doc()
        if not all(status):
            self._update_info(os.path.join(self.dir_path, self.INFO_FILE))
            raise Exception(
                'Some error has been occurred during installing {0}--{1}'.format('tensorflow_docs', self.TF_DOC_URL))

        self._print('Installing tensorflow & documents for TF-{0}'.format(self.version), self.LENGTH)
        status = self._install_tf(self.version, self.tf_dir_path, self.md_dir_path)
        if not all(status):
            self._update_info(os.path.join(self.dir_path, self.INFO_FILE))
            raise Exception(
                'Some error has been occurred during installing {0}=={1}'.format('tensorflow', self.version))

        self._print('Preparing documents for DocSet', self.LENGTH)

        if self.version[1] == '1':
            self.md_dir_path = os.path.join(self.md_dir_path, 'api_docs', 'python')

        self.md_to_html(self.md_dir_path, self.html_dir_path)
        dashing_cfg = json.loads(DASHING)
        for k, v in self.DASHING_CONFIG.items():
            dashing_cfg[k] = v

        with open(os.path.join(self.html_dir_path, 'dashing.json'), 'w') as fout:
            json.dump(dashing_cfg, fout)

        self._print('It is done!', hashing=False)
