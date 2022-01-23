from bs4 import BeautifulSoup
import requests
import json

artists = [
    ['/johnny-hallyday', 10],
    ['/kendji-girac', 2],
    ['/jean-jacques-goldman', 3],
    ['/claude-francois', 5],
    ['/charles-aznavour', 8],
    ['/francis-cabrel', 3],
    ['/georges-brassens', 4],
    ['/jacques-dutronc', 3],
    ['/alain-bashung', 4],
    ['/marc-lavoine', 3],
    ['/michel-polnareff', 3],
    ['/france-gall', 3],
    ['/sylvie-vartan', 6],
    ['/sheila', 4],
    ['/francoise-hardy', 5],
    ['/dalida', 6],
    ['/lio', 1],
    ['/mylene-farmer', 3],
    ['/zazie', 3],
    ['/vanessa-paradis', 3],
    ['/amel-bent', 3],
    ['/jenifer', 3],
    ['/christine-and-the-queens', 1],
    ['/aya-nakamura', 2],
    ['/vitaa-slimane', 2],
    ['/julien-dore', 2],
    ['/pierre-bachelet', 2],
    ['/calogero', 3],
    ['/renan-luce', 1],
    ['/eddy-mitchell', 6],
    ['/michel-berger', 3],
    ['/gilbert-montagne', 1],
    ['/pascal-obispo', 3],
    ['/alain-souchon', 3],
    ['/francis-lalanne', 2],
    ['/soprano', 3],
    ['/slimane', 1],
    ['/maitre-gims', 3],
    ['/pierre-perret', 3],
    ['/niska', 3],
    ['/pnl', 2],
    ['/jules', 1],
    ['/camelia-jordana', 1],
    ['/juliette-greco', 3],
    ['/veronique-sanson', 3],
    ['/keren-ann', 1],
    ['/angele', 2],
    ['/catherine-ringer', 1],
    ['/brigitte-fontaine', 3],
    ['/barbara', 3]
]

base_link = "https://www.paroles.net"

# Load songs from dictionary
with open("music.json") as file:
    data = json.load(file)

# Load songs file with names of the songs
with open("names.json") as file2:
    data_with_name = json.load(file2)

# Loop through all artists and number of web pages
for artist in range(len(artists)):
    print(artist)
    for p in range(1, artists[artist][1] + 1):
        if p == 1:
            link = artists[artist][0]
        else:
            link = f"{artists[artist][0]}-{p}"

        # Find main page and do soup
        source = requests.get(f"{base_link}{link}").text
        soup = BeautifulSoup(source, 'lxml')

        # Loop goes through every song in a list with a goal to scrape lyrics, clean text and past it to JSON file.
        for song in soup.find_all('td', class_="song-name"):

            # Some songs have different structure. They are rare. Loss of data is not important.
            try:
                link = song.p.a['href']
                song_name = str(song.p.a.text)
                if link[0] == "/":
                    print(song_name)
                    print(f"artist: {artist+1}", f"page: {p}", f"link: {link}")

                    # Find a song
                    song_page = requests.get(f"{base_link}{link}").text
                    soup_of_song = BeautifulSoup(song_page, 'lxml')

                    # Find lyrics and create a list with it
                    lyrics = []
                    for part in soup_of_song.find('div', class_="song-text"):
                        el_for_lyrics = part.text

                        el_for_lyrics = el_for_lyrics.replace("\r", "")
                        if el_for_lyrics != '\n\n':
                            el_for_lyrics = el_for_lyrics.replace("\n\n", "\n")
                            lyrics.append(el_for_lyrics)

                    # Clean your text to prepare export
                    lyrics.pop()
                    lyrics = lyrics[3:]
                    n = 0
                    for el in lyrics:
                        if el == '\n':
                            lyrics.pop(n)
                        n = n + 1
                    string_lyrics = ''.join(lyrics)

                    # Append song to a Song Dictionary
                    data['prompt'].append("")
                    data['completion'].append(f" {string_lyrics} END")

                    # Append song to a Song with Names Dictionary
                    data_with_name['prompt'].append(f"{string_lyrics} \n\n###\n\n")
                    data_with_name['completion'].append(f" {song_name} END")

            except:
                print("Error occured")
                pass

# Write here in a JSON file
with open("music.json", "w") as file:
    json.dump(data, file, ensure_ascii=False, indent=2)

with open("names.json", "w") as file2:
    json.dump(data_with_name, file2, ensure_ascii=False, indent=2)
