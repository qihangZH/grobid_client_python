# %%
from grobid_client.grobid_client import GrobidClient
import os
import shutil
import typing
import bs4


def delete_whole_dir(directory):
    """delete the whole dir..."""
    if os.path.exists(directory) and os.path.isdir(directory):
        shutil.rmtree(directory)


def read_tei_xml_text_list(tei_xml_path,
                           tag: typing.Union[list, str] = ['div'],
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
    with open(tei_xml_path, 'r') as tei:
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
