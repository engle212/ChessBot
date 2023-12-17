import requests
import json
import chess.pgn
import io
import pandas as pd
import numpy as np
from datetime import date

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
    return pgn

def getMoves(game):
    moves = []
    for move in game.mainline_moves():
        moves.append(move.uci())
    # Even moves: white 
    # Odd moves: black
    return moves     

if __name__ == "__main__":
    #n = getNames(['GM', 'WGM', 'IM'])
    n = getNames(['IM'])
    url_list = getPGNurls(n.pop())
    for name in n:
        url_list.extend(getPGNurls(name))
    
    print('Creating DataFrame')

    vsList = []
    movesList = []
    for url in url_list:
        pgn = getPGN(url)
        game = chess.pgn.read_game(io.StringIO(pgn))

        versus = '{' + game.headers['White'] + '} vs {' + game.headers['Black'] + '}'

        moves = getMoves(game)

        vsList.append(versus)
        movesList.append(moves)
    
    pgn_df = pd.DataFrame()
    pgn_df['WhiteVsBlack'] = pd.Series(data=vsList)
    pgn_df['Moves'] = pd.Series(data=movesList, dtype='object')
    
    pgn_df.drop_duplicates(subset='WhiteVsBlack', inplace=True)

    print('DataFrame complete')

    print('Exporting data to CSV')

    # Export data to csv
    pgn_df.to_csv('ChessDataAccessed'+ date.today())

    print('Data successfully exported to CSV')

    #gameFile = open("test.pgn", "w", encoding="utf-8")
    #exporter = chess.pgn.FileExporter(gameFile)
    #game_string = game1.accept(exporter)

    



