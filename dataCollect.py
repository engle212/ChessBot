import requests
import json
import chess.pgn
import io

def getNames(titles):
    nameSet = set()
    for t in titles:
        # Get list of usernames in title t
        url = "https://api.chess.com/pub/titled/" + t
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        r = requests.get(url, headers=headers)
        
        if r.status_code != 200:
            print(r)
        else:
            print("Successfully retrieved list of names in title: " + t)
            names = r.json()['players']
            # Add names to set
            nameSet.update(names)
    return nameSet

def getPGNurls(name):
    archives = []
    url = "https://api.chess.com/pub/player/" + str(name) + "/games/archives"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print(r)
    else:
        archives = r.json()['archives']
        archives = [a + '/pgn' for a in archives]
    return archives

def getPGN(url):
    pgn = ''
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36', 
               'Content-Type': 'application/x-chess-pgn',
               'Content-Disposition': 'attachment; filename="ChessCom_username_YYYMM.pgn'}
    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print(r)
    else:
        pgn = r.text
    return io.StringIO(pgn)

if __name__ == "__main__":
    n = getNames(['GM', 'WGM', 'IM'])
    url_list = getPGNurls(n.pop())

    pgn = getPGN(url_list[0])
    
    game1 = chess.pgn.read_game(pgn)

    gameFile = open("test.pgn", "w", encoding="utf-8")
    exporter = chess.pgn.FileExporter(gameFile)
    game_string = game1.accept(exporter)

    



