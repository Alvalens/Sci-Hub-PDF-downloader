from bs4 import BeautifulSoup
import requests
import time
import os

def download_pdf_from_doi(doi, count):
    url = 'https://sci-hub.se/' + doi
    try:
        response = requests.get(url)
        response.raise_for_status()
        content = response.content

        soup = BeautifulSoup(content, 'html.parser')
        div = soup.find("div", {"id": "article"})

        if div is None:  # Check if the div element is found
            print(f"Div not found for {doi}")
            return False

        embed = div.find("embed")

        if embed and 'src' in embed.attrs:
            src = embed['src']
            if src.startswith('/download') or src.startswith('/tree'):
                link = "https://sci-hub.se" + src
            else:
                link = "https:" + src
            pdf_filename = f"{str(count).zfill(3)}-{doi.replace('/', '-')}.pdf"

            response = requests.get(link)
            response.raise_for_status()
            content = response.content

            if not os.path.exists('article'):
                os.mkdir('article')

            with open(os.path.join('article', pdf_filename), "wb") as f:
                f.write(content)

            return True
        else:
            print(f"PDF not found for {doi}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error for {doi}: {e}")
        return False
    except AttributeError:
        print(f"AttributeError for {doi}: 'NoneType' object has no attribute 'find'")
        return False

def main():
    count = 1
    with open('sdg-doi.txt', 'r') as f:
        for line in f:
            doi = line.strip()
            success = download_pdf_from_doi(doi, count)
            if success:
                print(f"Downloaded {doi} as {str(count).zfill(3)}-{doi.replace('/', '-')}.pdf")
            count += 1
            time.sleep(0.1)

if __name__ == "__main__":
    main()
