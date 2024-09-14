import requests, re, webbrowser
'''A simple script to search libgen for books by ISBN and download them.
The script uses regular expressions to scrape the search results page and the download page 
for the file url. The file is then opened in the users default browser to download.
'''
def get_search_results(query):
    '''Get the search results page and scrape all html blocks containing the correct id=1234567... format.
    Args:
        query: the search query to be used in the search url, typically an ISBN number
    Returns:
        blocks: a list of strings containing the search results
    '''
    search_url = 'https://libgen.is/search.php?req=+'
    results_page = requests.get(search_url + query).text
    blocks = re.findall(r'id=\d*>(.*?)tr>', results_page, flags=re.S) #<tr> tags are used to separate search results
    return blocks
    
def display_blocks(blocks):
    '''Search blocks for book names, filetypes, and file sizes and display them to the user.'''
    for i in range(len(blocks)):
        name = re.search(r'(.*?)<', blocks[i]).group(1)
        tags = re.findall(r'nowrap>(.*)<', blocks[i]) #File type, size, and year are always after nowrap tags
        print(f'{i+1}) {name} | {tags[0]} | {tags[1]} | {tags[2]}')


def get_download_url(blocks, selection):
    '''Get the download url from the selected book.
    Args:
        blocks: a list of strings containing the search results
        selection: the index of the selected book
    Returns: 
        download_url: the url to the download page for the selected book
    '''
    download_url = re.search(r'(http://.*?)\'', blocks[selection]).group(1)
    return download_url
    
def get_file_url(download_url, file_type):
    '''Scrape the download page for the file url.
    Args:
        download_url: the url to the download page for the selected book
        file_type: the file type of the selected book
    Returns: 
        file_url: the url to the file to be downloaded, scraped from the download page
    '''
    download_page = requests.get(download_url).text
    file_url = re.search(r'(https://.*?{})'.format(file_type), download_page).group(1)
    return file_url
    
def download_file(file_url):
    '''Opens the file in the users default browser to download.'''
    webbrowser.open(file_url, new=0, autoraise=True)
    
def main():
    '''Main function to run the program.'''
    
    isbn = re.sub(r'\D', '', input('ISBN 13:')) #remove all non numeric charecters from isbn
    while len(isbn) != 13:
        isbn = re.sub(r'\D', '', input('Please enter a valid ISBN 13 number:'))
        print('Searching libgen for ISBN ' + isbn)
    blocks = get_search_results(isbn)
    display_blocks(blocks)
    selection = int(input("\nPick a number:"))-1
    download_url = get_download_url(blocks, selection)
    file_type = re.findall(r'nowrap>(.*)<', blocks[selection])[2] #file type is always after third nowrap tag
    file_url = get_file_url(download_url, file_type)
    print("Downloading file in browser...")
    download_file(file_url)

if __name__ == '__main__':
    main()
    