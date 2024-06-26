import socket
import json

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 65432

def transmitRequest(socket_client, request_message):
    socket_client.send(request_message.encode('utf-8'))
    length_response_str = socket_client.recv(10).decode('utf-8').strip()
    print(f"Received response length string: '{length_response_str}'")
    length_response = int(length_response_str)
    print(f"Received response length: {length_response}")
    data_response = b""
    while len(data_response) < length_response:
        part_data = socket_client.recv(length_response - len(data_response))
        data_response += part_data

    return json.loads(data_response.decode('utf-8'))

def searchNewsHeadlines(socket_client):
    while True:
        print("Search headlines menu:")
        print("1. Search for keywords")
        print("2. Search by category")
        print("3. Search by country")
        print("4. List all new headlines")
        print("5. Back to the main menu")
        choice_option = input("Select an option: ")

        if choice_option == '1':
            search_keyword = input("Enter keyword: ")
            query_params = {'q': search_keyword}
            data_news = transmitRequest(socket_client, f'get_news|everything|{json.dumps(query_params)}')
            displayResults(data_news)
        elif choice_option == '2':
            search_category = input("Enter category (e.g., business, entertainment, general, health, science, sports, technology): ")
            query_params = {'category': search_category}
            data_news = transmitRequest(socket_client, f'get_news|top-headlines|{json.dumps(query_params)}')
            displayResults(data_news)
        elif choice_option == '3':
            search_country = input("Enter country code (e.g., au, nz, ca, ae, sa, gb, us, eg, ma): ")
            query_params = {'country': search_country}
            data_news = transmitRequest(socket_client, f'get_news|top-headlines|{json.dumps(query_params)}')
            displayResults(data_news)
        elif choice_option == '4':
            data_news = transmitRequest(socket_client, 'get_news|top-headlines|{}')
            displayResults(data_news)
        elif choice_option == '5':
            break
        else:
            print("Invalid input. Please enter again.")

def retrieveSourcesList(socket_client):
    while True:
        print("List of sources menu:")
        print("1. Search by category")
        print("2. Search by country")
        print("3. Search by language")
        print("4. List all")
        print("5. Back to the main menu")
        choice_option = input("Select an option: ")

        if choice_option == '1':
            search_category = input("Enter category (e.g., business, entertainment, general, health, science, sports, technology): ")
            query_params = {'category': search_category}
            data_sources = transmitRequest(socket_client, f'get_news|sources|{json.dumps(query_params)}')
            displaySources(data_sources)
        elif choice_option == '2':
            search_country = input("Enter country code (e.g., au, nz, ca, ae, sa, gb, us, eg, ma): ")
            query_params = {'country': search_country}
            data_sources = transmitRequest(socket_client, f'get_news|sources|{json.dumps(query_params)}')
            displaySources(data_sources)
        elif choice_option == '3':
            search_language = input("Enter language code (e.g., ar, en): ")
            query_params = {'language': search_language}
            data_sources = transmitRequest(socket_client, f'get_news|sources|{json.dumps(query_params)}')
            displaySources(data_sources)
        elif choice_option == '4':
            data_sources = transmitRequest(socket_client, 'get_news|sources|{}')
            displaySources(data_sources)
        elif choice_option == '5':
            break
        else:
            print("Invalid input. Please enter again.")

def displayResults(data_news):
    if data_news['status'] == 'ok':
        for idx, article in enumerate(data_news['articles']):
            print(f"{idx+1}. {article['title']}")
        article_choice = int(input("Select an article number for details: "))
        if 1 <= article_choice <= len(data_news['articles']):
            selected_article = data_news['articles'][article_choice-1]
            print(f"Title: {selected_article['title']}")
            print(f"Description: {selected_article['description']}")
            print(f"Source: {selected_article['source']['name']}")
            print(f"URL: {selected_article['url']}")
    else:
        print('Failed to fetch news.')

def displaySources(data_sources):
    if data_sources['status'] == 'ok':
        for idx, source in enumerate(data_sources['sources']):
            print(f"{idx+1}. {source['name']} ({source['country']})")
    else:
        print('Failed to fetch sources.')

if __name__ == '__main__':
    username_client = input("Enter your name: ")
    socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_client.connect((SERVER_HOST, SERVER_PORT))
    socket_client.send(username_client.encode('utf-8'))
    
    while True:
        print("Main menu:")
        print("1. Search headlines")
        print("2. List of sources")
        print("3. Quit")
        choice_option = input("Select an option: ")

        if choice_option == '1':
            searchNewsHeadlines(socket_client)
        elif choice_option == '2':
            retrieveSourcesList(socket_client)
        elif choice_option == '3':
            break
        else:
            print("Invalid input. Please enter again.")
    
    socket_client.close()
