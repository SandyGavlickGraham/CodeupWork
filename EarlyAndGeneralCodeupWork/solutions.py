# Sandy Graham's Python Assessment for Codeup

# 1.)
def isnegative(number):
    return number < 0

# 2.)
def count_evens(list_of_numbers):
    count = 0
    for number in list_of_numbers:
        if number % 2 == 0:
            count += 1
    return count

def zachs_count_evens(numbers):
    even_numbers = [n for n in numbers if n % 2 == 0]
    return len(even_numbers)

# 3.)
def increment_odds(list_of_numbers):
    new_list = []
    for number in list_of_numbers:
        if number % 2 == 0:
            new_list.append(number)
        else:
            new_list.append(number+1)
    return new_list

def zachs_inc_odds(xs): # adding an s after a variable indicates a list
    return[x + 1 if x % 2 == 1 else x for x in xs]

# 4.)
def average(list_of_numbers):
    return sum(list_of_numbers)/len(list_of_numbers)

# 5.)
def name_to_dict(name_string):
    name_list = name_string.split(' ')
    name_dict = {
        'first_name': name_list[0],
        'last_name': name_list[1],
        }
    return name_dict

def zachs_name_to_dict(name: str) -> dict:
    'doc string here: str -> dict'
    first_name, last_name = name.split(' ')
    return {'first_name': first_name, 'last_name': last_name}

# 6.) -- missed! This is the answer Zach gave me
def capitalize_names(names):
    # This one changes the original list and returns the original list 
    for name in names:
        name['first_name'] = name['first_name'].capitalize()
        name['last_name'] = name['last_name'].capitalize()
    return(names)

def zachs_cap_names(people: list) -> list:
    capitalized = []
    for person in people:
        print('person = ', person)
        capitalized.append({
            'first_name': person['first_name'].title(),
            'last_name': person['last_name'].title(),
        })
    return capitalized

def iterate_through_dict(people):
    capitalized_names = []
    for person in people: # iterate through the list
        print('person = ', person)
        d = {}
        for k in person.keys(): # bounce throught the keys in the input dictionary
            print('k = ', k, ',  person[k].title() = ', person[k].title())
            d[k] = person[k].title()
            capitalized_names.append(d)
    return capitalized_names

# 7.)
def count_vowels(word):
    count = 0
    for letter in word:
        if letter in ['a','e','i','o','u']:
            count += 1
    return count

# 8.)
def analyze_word(word):
    vowel_count = 0
    letter_count = 0
    
    for letter in word:
        letter_count += 1
        if letter in ['a','e','i','o','u']:
            vowel_count += 1
    
    word_dict = {'word': word, 'n_letters': letter_count, 'n_vowels': vowel_count}

    return(word_dict)
     