# %%
from grobid_client.grobid_client import GrobidClient
import os
import shutil
import typing
import re
import bs4


def delete_whole_dir(directory):
    """delete the whole dir..."""
    if os.path.exists(directory) and os.path.isdir(directory):
        shutil.rmtree(directory)


def list_to_file(input_list, a_file, mode="w", encoding="utf-8", errors='strict'):
    """Write a list to a file, each element in a line
    The strings need to have no line break "\n" or they will be removed

    Keyword Arguments:
        plain_validate {bool} -- check if the number of lines in the file
            equals the length of the list (default: {True}), Only Useful when not compress
        mode {str} -- the argument of open()
        compress {bool} -- whether to compress the output file as a gz file (default: {False})
        errors {str} -- codec error types, see https://docs.python.org/3/library/codecs.html#codec-base-classes
    """
    open_mode = mode

    with open(a_file, mode, 8192000, encoding=encoding, newline="\n", errors=errors) as f:
        for e in input_list:
            e = str(e).replace("\n", " ").replace("\r", " ")
            f.write("{}\n".format(e))


# %%
if __name__ == '__main__':
    DIR_ROOT = os.path.abspath(os.path.dirname(__file__))

    DIR_INPUT_SAMPLE = os.path.join(DIR_ROOT, 'samplepdf')

    DIR_RESULT_XML = os.path.join(DIR_ROOT, 'resultxml')

    DIR_RESULT_TXT = os.path.join(DIR_ROOT, 'xmltotxt')

    delete_whole_dir(DIR_RESULT_XML)

    client = GrobidClient(config_path=os.path.join(DIR_ROOT, 'config.json'))
    client.process("processFulltextDocument",
                   DIR_INPUT_SAMPLE,
                   DIR_RESULT_XML,
                   n=os.cpu_count(),
                   segment_sentences=True)

    for n in os.listdir(DIR_RESULT_XML):
        os.rename(
            os.path.join(DIR_RESULT_XML, n),
            os.path.join(DIR_RESULT_XML,
                         re.search(r'^(.+)\.grobid\.tei\.xml$', n
                                   ).groups()[0]+'.xml'
                         )
        )