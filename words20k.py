words20k = []
with open('test/20k.txt', 'r', encoding='utf-8') as file20k:
    for word in file20k:
        words20k.append(word.strip())