import sys
import re
import json
from os import listdir
from words20k import words20k


def text_analyse(textfile, look_for_outliner=False, outliner_data=words20k):
    result = {}
    result['word_count'] = 0
    result['word_counter'] = {}
    result['outliners'] = set()
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
                    word = word.lower()
                    if word:
                        result['word_count'] += 1
                        result['word_counter'][word] = result['word_counter'].get(word, 0) + 1
                        if look_for_outliner == True:
                            if word not in outliner_data:
                                result['outliners'].add(word)
                            
        result['frequency_rank'] = dict(sorted(result['word_counter'].items(), key=lambda item:item[1], reverse=True))
        result['unique_count'] = len(result['word_counter'])
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
            json_output={
                title: {'Word Count': analysis['word_count'],
                'Unique Word Count': analysis['unique_count'],
                'Frequency Count': analysis['frequency_rank'],
                'Number of Words Not Found in the 20k Word List': len(analysis['outliners']),
                'Words Not Found in the 20k Word List': list(analysis['outliners'])}
            }
            json.dump(json_output, f, ensure_ascii=False, indent=4)
    else:
        with open(f'output/{out_filename}.txt', 'w', encoding='utf-8') as sys.stdout:
            print('File:', selection[selected].replace('.txt', ''))
            print(f'Word Count: {analysis["word_count"]}', f'Unique Word Count: {analysis["unique_count"]}', sep='\n')
            print()
            print('{0:<20} {1:<10} {2}'.format('Word', 'Count', 'Percentage'))
            [print('{0:<20} {1:<10} {2:.4%}'.format(word, count, count/analysis['word_count'])) for word, count in analysis['frequency_rank'].items()]
            print()
            print('Words not in the most frequent 20k English words:')
            [print(x) for x in analysis['outliners']]
if __name__=='__main__':
    main()