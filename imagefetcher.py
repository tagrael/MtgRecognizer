import json
import urllib.request
import time
import os
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def fetchImages(json_file_location, save_to_location):
    file = open(json_file_location, encoding='utf-8')
    json_data = json.load(file)
    file.close()
    print("Fetched " + str(len(json_data)) + " results")
    number = 1
    chunked_data = [json_data[i: i + 100] for i in range(0, len(json_data), 100)]
    failed_lines = []

    for index, chunk in enumerate(chunked_data):
        print("Downloading images " + str(index * 100) + " - " + str((index + 1) * 100) + "..." )
        for card in chunk:
            number = number + 1
            print(str(number) + "...")
            if 'image_uris' in card:
                if 'png' in card['image_uris']:
                    time.sleep(0.3)
                    image_uri = card['image_uris']['png']
                    cardname = card['name'].replace(" ", "_").replace("//", "And").replace("?", "_Qmark").replace("!", "_Exmark")
                    mtgo_id = card['oracle_id']
                    set_code = card['set'].upper()
                    if set_code == "CON":
                        set_code = "CONF"
                    image_name = str(mtgo_id) + '_' + set_code + '_' + cardname + '.png'

                    path = os.path.join(save_to_location, set_code)
                    os.makedirs(path, exist_ok=True)

                    full_file_name = os.path.join(path, image_name)
                    urllib.request.urlretrieve(image_uri, full_file_name)
                else:
                    failed_lines.append(number)
            else:
                failed_lines.append(number)

        print("Failed jsons: ")
        for x in failed_lines:
            print(x)


if __name__ == '__main__':

    JSON_FILE = 'json/unique-artwork-20201213102102.json'
    SAVE_LOCATION = os.path.join("E:", "Card_Images")

    print("Starting image fetching")
    fetchImages(JSON_FILE, SAVE_LOCATION)