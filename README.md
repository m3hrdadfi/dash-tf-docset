# dash-tf-docset
Dash DocSet for TensorFlow 2.x and 1.x

![screenshot](/vendors/screenshot.png)

View TensorFlow docs in the [dash](https://kapeli.com/dash)/[zeal](https://github.com/zealdocs/zeal) offline docset browser.

To use, you can add this feed in Dash/Zeal:

```
https://raw.githubusercontent.com/m3hrdadfi/dash-tf-docset/master/TensorFlow.xml
```

Or download the latest release [here](https://github.com/m3hrdadfi/dash-tf-docset/releases).

## Installation:
1. `pip install -r requirements.txt`

## Supported versions/Pre-requisites.

| Python        |
| -------------:|
| 3.6           |
| 3.7           |
| 3.8           |


## Usage:

The code handles both manual and auto-generating techniques.
**Before going any further install [Dashing Generator](https://github.com/technosophos/dashing) by Technosophos**

### Manual

In the manual section, you can generate the Dash DocSet for your TensorFlow version which created by [Contribute to the TensorFlow documentation](https://www.tensorflow.org/community/contribute/docs) in markdown format by the following templates:

``` python
python gen.py -i {DIR_PATH} -o {DIR_PATH} -v {TENSORFLOW_VERSION}
```

The sample command for generating DocSet for TensorFlow v1.13.0 in `./v1.13.0/html` in which already made in markdown format in `./v1.13.0/markdown`:

``` python
python gen.py -i ./v1.13.0/markdown ./v1.13.0/html -v 1.13.0
```

### Automatically

In the automatic plan, you can generate your specific version of TensorFlow for your Dash DocSet using this command

``` python
python gen2.py -d {DIR_PATH} -v {TENSORFLOW_VERSION}
```

The sample command for generating DocSet for TensorFlow v2.0.0:

``` python
python gen2.py -d ./output -v v2.0.0
```

And finally for both manual and automatic parts after generating HTML output use this command to generate your custom Dash DocSet:
``` bash
cd to_your_generated_html_directory
dashing build
```

## Credits

This code uses some of the functionalities of  [gen_tf_docset](https://github.com/reuben/gen_tf_docset/) by [Reuben Morais](https://github.com/reuben). I thank the authors for his efforts.

## License

Copyright (C) 2019, Mehrdad Farahani
Licensed under the MIT license, see LICENSE file for details.

Copyright (C) 2019, Reuben M
orais
Licensed under the Mozilla Public License, version 2.0, see LICENSE file for details.
