# Ziel: Wir wollen analysieren, welche Arten von Apps in den App Stores besonders beliebt sind, damit wir profitable App-Ideen für uns ableiten können.
# Dabei konzentrieren wir uns auf kostenlose, englische Apps.

import csv

# 🗂️ Schritt 1: Daten einlesen
def load_data(filename):
    with open(filename, encoding='utf8') as file:
        return list(csv.reader(file))

android_data = load_data('googleplaystore.csv')
ios_data = load_data('AppleStore.csv')

android_header, android = android_data[0], android_data[1:]
ios_header, ios = ios_data[0], ios_data[1:]

# 🧹 Schritt 2: Fehlerhafte Zeile bei Google Play entfernen (bekannter Fehler)
del android[10472]  # Zeile mit falschem Datenformat

# 🧹 Schritt 3: Doppelte Apps bereinigen (nur höchste Reviews behalten)
def remove_duplicates(dataset, name_index, reviews_index):
    reviews_max = {}
    for row in dataset:
        name = row[name_index]
        reviews = float(row[reviews_index])
        if name not in reviews_max or reviews > reviews_max[name]:
            reviews_max[name] = reviews

    cleaned_data = []
    added_names = set()

    for row in dataset:
        name = row[name_index]
        reviews = float(row[reviews_index])
        if reviews == reviews_max[name] and name not in added_names:
            cleaned_data.append(row)
            added_names.add(name)

    return cleaned_data

android_clean = remove_duplicates(android, 0, 3)

# 🗑️ Schritt 4: Nur englische Apps behalten
def is_english(string):
    non_ascii = sum(1 for char in string if ord(char) > 127)
    return non_ascii <= 3

android_english = [app for app in android_clean if is_english(app[0])]
ios_english = [app for app in ios if is_english(app[1])]

# 🆓 Schritt 5: Nur kostenlose Apps behalten
android_free = [app for app in android_english if app[7] == '0']
ios_free = [app for app in ios_english if app[4] == '0.0']

# 📊 Schritt 6: Häufigkeitstabellen berechnen (prozentual)
def freq_table(dataset, index):
    table = {}
    for row in dataset:
        key = row[index]
        table[key] = table.get(key, 0) + 1

    table_percentages = {key: (value / len(dataset)) * 100 for key, value in table.items()}
    return table_percentages

# 📊 Schritt 7: Durchschnittliche Nutzerbewertungen pro iOS-Genre
print("\n--- Durchschnittliche Nutzerbewertungen (iOS Genres) ---")
genres_ios = freq_table(ios_free, -5)

for genre in genres_ios:
    total_reviews = sum(float(app[5]) for app in ios_free if app[-5] == genre)
    count = sum(1 for app in ios_free if app[-5] == genre)
    avg_reviews = total_reviews / count
    print(f"{genre}: {avg_reviews:.2f}")

# 📊 Schritt 8: Durchschnittliche Installationen pro Google Play Kategorie
print("\n--- Durchschnittliche Installationen (Google Play Kategorien) ---")
categories_android = freq_table(android_free, 1)

for category in categories_android:
    installs_list = [
        float(app[5].replace(',', '').replace('+', ''))
        for app in android_free if app[1] == category
    ]
    if installs_list:
        avg_installs = sum(installs_list) / len(installs_list)
        print(f"{category}: {avg_installs:.2f}")
