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


def read_tei_xml_text_list(tei_xml_path,
                           tag: typing.Union[list, str] = ['text'],
                           subtags: typing.Union[list, str] = ['p']
                           ):
    """
    read tei-format XML to list of text
    Args:
        tei_xml_path: the path of Tei-xml-path, is a format could be seen in https://tei-c.org/ for detail
        tag: the tag which contain text you interested in, first level
        subtags: second level tags, like p/s/head, etc

    Returns: a list of text

    """
    with open(tei_xml_path, 'r', encoding='utf-8', errors='replace') as tei:
        soup = bs4.BeautifulSoup(tei, 'xml')

    div_elements = soup.find_all(tag)

    # Initialize a list to store <s> pairs from all <div> elements
    s_pairs_list = []

    # Iterate through each <div> element
    for div in div_elements:
        # Find all <s> elements within the current <div>
        s_elements = div.find_all(subtags)

        # Extract and store <s> pairs as tuples in a list
        sentences = [s.get_text(strip=True) for s in s_elements]

        # Append the <s> pairs to the main list
        s_pairs_list.extend(sentences)

    return s_pairs_list


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

    for f in os.listdir(DIR_RESULT_XML):
        tmpl = read_tei_xml_text_list(os.path.join(DIR_RESULT_XML, f), ['div'], ['s'])
        print(tmpl)
