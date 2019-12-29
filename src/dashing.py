DASHING = """{
    "name": "{tf_name}",
    "package": "{tf_package}",
    "index": "{tf_index}",
    "externalURL": "https://www.tensorflow.org/",
    "selectors": {
        "h1:first-of-type": [
            {
                "type": "Module",
                "requiretext": "Module: ",
                "regexp": "Module: ",
                "replacement": ""
            },
            {
                "type": "Function"
            }
        ],
        "h3": {
            "type": "Method",
            "attr": "id"
        }
    },
    "ignore": [
        "Aliases:", "", "References", "Arguments", "Returns"
    ],
    "icon32x32": "{tf_icon32}",
    "icon16x16": "{tf_icon16}"
}"""