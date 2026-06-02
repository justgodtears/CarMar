from logging import raiseExceptions

import httpx
import ssl
import zipfile
from pathlib import Path

from httpx import HTTPError

# Low security context for CEPIK API
ssl_context = ssl.create_default_context()
ssl_context.set_ciphers('DEFAULT:@SECLEVEL=1')

PATH = "data/batch"
URL = "https://api.cepik.gov.pl/pliki"



def batch_data_links(url: str, params=None):
    """
    Function fetches all links to downloadable data files.
    Args:
        url: URL of batch data endpoint.
        params: Can be none, parameters of query.

    Returns:
        List of links to downloadable data files.

    """
    links_list = []
    with httpx.Client(verify=ssl_context) as client:
        r = client.get(url, params=params)
        response = r.json()["data"]
        for link in response:
            links_list.append(link["attributes"])

    download_links = []
    for download_link in links_list:
         download_links.append(download_link["url-do-pliku"])

    meta_data_links = []
    for meta_link in links_list:
        meta_data_links.append(meta_link["url-do-metadanych-pliku"])

    return download_links, meta_data_links


def download_batch_files(data_link: list, metadata_link: list, path_dir):
    """
    Function downloads batch files from list of links
    Args:
        data_link: List of links to download.
        metadata_link: List of links to download metadata.
        path_dir: Directory to save batch files.

    Returns:
        CSV Files saved in directory from parameter.

    """
    save_dir = Path(path_dir)
    save_dir.mkdir(exist_ok=True)

    all_links = data_link + metadata_link

    for link in all_links:
        filename = link.split("/")[-1]
        filepath = save_dir / filename

        with httpx.stream("GET", link, verify=ssl_context) as response:
            response.raise_for_status()
            with open(filepath, "wb") as f:
                for chunk in response.iter_bytes(chunk_size=8192):
                    f.write(chunk)

        if filepath.suffix == ".zip":
            with zipfile.ZipFile(filepath, "r") as z:
                z.extractall(save_dir)
            filepath.unlink()
            print(f"Unpacked: {filename}")
        else:
            print(f"Saved: {filepath}")


if __name__ == "__main__":
    print("")