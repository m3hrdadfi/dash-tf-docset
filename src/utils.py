import misaka
import os
import pygments
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
import shutil
import subprocess
import sys
from tqdm import tqdm


class HighlighterRenderer(misaka.HtmlRenderer):

    def blockcode(self, text, lang):
        if not lang:
            lang = 'text'
        try:
            lexer = get_lexer_by_name(lang, stripall=True)
        except:
            lexer = get_lexer_by_name('text', stripall=True)
        formatter = HtmlFormatter()

        return pygments.highlight(text, lexer, formatter)

    def table(self, header, body):
        return '<table class="table">\n' + header + '\n' + body + '\n</table>'


def run_task(cmd):
    result = []
    status = False

    try:
        print('run_task: {}'.format(cmd))
        with tqdm(unit='B', unit_scale=True, miniters=1) as pbar:
            cmd = cmd.split(' ')
            process = subprocess.Popen(cmd,
                                       bufsize=0,
                                       universal_newlines=True,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT)
            result = []

            while True:
                line = process.stdout.readline()
                result.append(line)
                pbar.update()
                sys.stdout.flush()

                if not line:
                    break

            process.stdout.close()
            return_code = process.wait()
            if return_code != 0:
                raise subprocess.CalledProcessError(return_code, cmd)
            else:
                status = True

        return ''.join(result), status
    except subprocess.CalledProcessError as e:
        sys.stderr.write(
            "common::run_command() : [ERROR]: output = {}, error code = {}\n".format(e.output, e.returncode))
        return ''.join(result), status


def pip_get_all_packages():
    # pkgs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
    pkgs, _ = run_task('pip freeze')
    pkgs = [pkg.split('==') for pkg in pkgs.split()]
    pkgs = [(pkg.lower().replace('-', '_'), version) for pkg, version in pkgs]
    return dict(pkgs)


def search_package(name, version=None):
    packages = pip_get_all_packages()
    if name in packages:
        if version:
            if not packages[name] == version:
                return False
        return True
    return False


def install_package(pkg, name, version=None):
    pkg = '{0}=={1}'.format(pkg, version) if pkg and version else '{0}'.format(pkg)
    # subprocess.call([sys.executable, '-m', 'pip', 'install', pkg])
    _, status = run_task('pip install {0}'.format(pkg))

    if not status:
        return False

    print('Evaluating ...')
    if search_package(name):
        return True

    return False


def copytree(source, destination):
    for item in os.listdir(source):
        if item.startswith('.'):
            continue

        file_path = os.path.join(source, item)

        if os.path.isdir(file_path):
            # shutil.copytree(source, destination, symlinks, ignore)
            new_destination = os.path.join(destination, item)
            os.makedirs(new_destination, exist_ok=True)
            copytree(file_path, new_destination)
        else:
            shutil.copy(file_path, destination)
