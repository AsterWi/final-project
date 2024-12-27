import requests
import json
import sqlite3

connection = sqlite3.connect('database.db')
cur = connection.cursor()

# cur.execute("""
#     CREATE TABLE links (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         link TEXT,
#         list TEXT
#     );
# """)

# Database
def delete(link):
    cur.execute(f"SELECT * FROM links WHERE link = '{link}'")
    result = cur.fetchone
    if result:
        cur.execute(f"DELETE FROM links WHERE link = '{link}';")  
    else:
        print("Link doesn't exist.")
    
def view():
    cur.execute("SELECT * FROM links;")
    links = cur.fetchall()
    for link in links:
        print(link)    

# Parse
def find(link):
    response = requests.get(link)
    response_text = response.text

    response_parse = response_text.split("<span>")

    res_parse_list = []

    for parse_elem in response_parse:
        if parse_elem.startswith("$"):
            for parse_elem2 in parse_elem.split("<"):
                if parse_elem2.startswith("$") and parse_elem2[1].isdigit():
                    res_parse_list.append(parse_elem2)               
    


    cur.execute(f"INSERT INTO links (link, list) VALUES ('{link}', '{json.dumps(res_parse_list)}')")
                            
    print(f"Results of search: {res_parse_list}")
    print("Results have been added to the database!")

# Interface
def menu():
    print("Select an option: ")
    print("Parse link for money values - 1; View database - 2; Delete link - 3")
    yoinks = int(input("Input here: "))
    match yoinks:
        case 1:
            yeezies = input("Link will be searched for crypto values. Input your link: ")
            find(yeezies)
        case 2:
            print("Viewing database.")
            view()
        case 3:
            wowzers = input("You can view database for existing links. Input link that will be deleted: ")
            delete(wowzers)

# Loop
i=0
print("Welcome to the Crypto Parser. This program will parse links for crypto values.")

while i==0:
    try:
        yowch = int(input("Go to select options? 0 - exit; 1 - proceed. Input: "))
    except (ValueError, TypeError):
        print("Error! Try again.")
    if yowch == 0:
        break
    else:
        menu()

connection.commit()
connection.close()