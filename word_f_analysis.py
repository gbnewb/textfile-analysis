import sys
import re
import json
from os import listdir


def text_analyse(textfile):
    result = {}
    word_count = 0
    word_counter = {}
    with open(textfile, encoding='utf-8') as fin:
        #'*** START' '*** END' is how Gutenberg project indicates the boundary of actual contents in plain text
        while True:
            if '*** START' in fin.readline():
                break
        
        for line in fin:
            if '*** END' in line:
                break
            #avoid lines indicating chapter either in contents or new chapters
            re_chapter = re.search(r'^[ \t]*chapter', line.lower())
            #Roman Numerals indicating chapters
            re_roman_numeral = re.search(r'^[ \t]*M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})\.', line)
            if (not re_chapter) and (not re_roman_numeral):
                line = line.strip().lower()
                line = re.sub(r'([^\w\s-]|_)', '', line)  #eliminating punctuations
                line = line.replace('--', ' ')
                
                for word in line.split():
                    if word:
                        word = word.lower()
                        word_count += 1
                        word_counter[word] = word_counter.get(word, 0) + 1
        
        result['word_count'] = word_count
        result['word_counter'] = word_counter                    
        result['frequency_rank'] = dict(sorted(word_counter.items(),
                                        key=lambda item:item[1], reverse=True))
        result['unique_count'] = len(word_counter)
    return result


def main():
    selection = []
    for f in listdir('text/'):
        if f.endswith('.txt'):
            selection.append(f)
    for i, x in enumerate(selection):
        print(f'{i}.', x.replace('.txt', ''))
    
    selected = int(input('Enter the file number: '))
    title = selection[selected].replace('.txt', '')
    out_filename = input('filename: ')
    use_json = input('Do you want to use JSON format? (otherwise use .txt) (Y/N):')
    analysis = text_analyse(f'text/{selection[selected]}')
    
    if use_json.lower() == 'y':
        with open(f'output/{out_filename}.json', 'w', encoding='utf-8') as f:
            json_output = {
                title: {'Word Count': analysis['word_count'],
                'Unique Word Count': analysis['unique_count'],
                'Frequency Count': analysis['frequency_rank']}
            }
            json.dump(json_output, f, ensure_ascii=False, indent=4)
    
    else:
        with open(f'output/{out_filename}.txt', 'w', encoding='utf-8') as sys.stdout:
            print('File:', selection[selected].replace('.txt', ''))
            print(f'Word Count: {analysis["word_count"]}')
            print(f'Unique Word Count: {analysis["unique_count"]}')
            print()
            print('{0:<20} {1:<10} {2}'.format('Word', 'Count', 'Percentage'))
            for word, count in analysis['frequency_rank'].items():
                print('{0:<20} {1:<10} {2:.4%}'.format(
                    word, count, count/analysis['word_count']))


if __name__ == '__main__':
    main()