# Libraries
from pathlib import Path


def load_file_with_all_captions(filepath):
    """

    Parameters
    ----------

    Returns
    --------
    """
    import json
    with open(str(filepath), "r") as f:
        captions = json.load(f)
    return captions


def load_captions_from_posts_file():
    """"""
    pass


def load_captions_by_shortcode(shortcode_list, path):
    """

    Parameters
    ----------

    Returns
    --------
    """
    d = {}
    for i,s in enumerate(shortcode_list):
        path_caption = Path(path) / s / 'caption.txt'

        # Check if path exists
        if not path_caption.exists():
            print("[Warning] The shortcode does not exist: <%s>" % s)
            continue

        # Load
        with open(str(path_caption), "r") as f:
            data = f.read()
        if data is not None:
            d[s] = data

    # Return
    return d