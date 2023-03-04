import random
import requests
from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=["GET"])
def handler():
    option = request.form.get("FUNCTION")
    if option:
        try:
            if option == "random_username":
                from_index = request.form.get("from_index")
                to_index = request.form.get("to_index")
                return random_username(int(from_index), int(to_index))
            
            elif option == "random_list_usernames":
                from_index = request.form.get("from_index")
                to_index = request.form.get("to_index")
                return random_list_usernames(int(from_index), int(to_index))
            
            elif option == "random_email_generator":
                length = request.form.get("length")
                include_nums = request.form.get("include_nums")
                include_additional_symbols = request.form.get("include_additional_symbols")
                domain = request.form.get("domain")
                return random_email_generator(int(length), bool(include_nums), bool(include_additional_symbols), domain)
            
            elif option == "random_real_email_generator":
                add_nums = request.form.get("add_nums")
                add_additional_symbols = request.form.get("add_additional_symbols")
                domain = request.form.get("domain")
                return random_real_email_generator(bool(add_nums), bool(add_additional_symbols), domain)
            
            elif option == "random_pass_generator":
                length = request.form.get("length")
                include_nums = request.form.get("include_nums")
                include_additional_symbols = request.form.get("include_additional_symbols")
                return random_pass_generator(int(length), bool(include_nums), bool(include_additional_symbols))
            
            else:
                return "Didnt understand you"

        except Exception as e:
            return "Got an error:\n\n" + str(e) + \
                   '\n\nCommon mistakes:\nInvalid declaration of arguments'

    return "No command - no action"


def random_username(from_index: int, to_index: int) -> str:
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    response = requests.get('https://raw.githubusercontent.com/danielmiessler/SecLists/'
                            'master/Usernames/xato-net-10-million-usernames.txt')
    text = response.content.decode('cp1251')
    usernames = text[:100000].splitlines()[from_index:to_index]
    user = random.choice(usernames) + random.choice(usernames)
    for i in range(random.randint(0, 5)):
        user += str(random.choice(numbers))
    return user


def random_list_usernames(from_index: int, to_index: int) -> list:
    response = requests.get('https://raw.githubusercontent.com/danielmiessler/SecLists/'
                            'master/Usernames/xato-net-10-million-usernames.txt')
    text = response.content.decode('cp1251')
    usernames = text[:100000].splitlines()[from_index:to_index]
    return usernames


def random_email_generator(length: int, include_nums: bool, include_additional_symbols: bool, domain):
    """
    specify domain with @ (ex.: @gmail.com)
    """
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
               's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    additional_symbols = ['.', '-']
    final_email = random.choice(letters)
    all_chars = letters.copy()
    if include_nums:
        all_chars += numbers
    if include_additional_symbols:
        all_chars += additional_symbols + additional_symbols
    for i in range(length):
        final_email += str(random.choice(all_chars))

    return final_email + domain


def random_real_email_generator(add_nums: bool, add_additional_symbols: bool, domain):
    """
    add_nums: bool or int ;

    add_additional_symbols: bool or int ;

    specify domain with @ (ex.: @gmail.com)
    """
    response = requests.get('https://raw.githubusercontent.com/danielmiessler/SecLists/'
                            'master/Usernames/xato-net-10-million-usernames.txt')
    text = response.content.decode('cp1251')
    usernames = text[:100000].splitlines()
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    additional_symbols = ['.', '-']
    final_email = random.choice(usernames) + random.choice(usernames)
    random_indexes = []
    if add_additional_symbols:
        for i in range(random.randint(1, 4)):
            for j in range(30):
                random_index = random.randint(1, len(final_email) - 3)
                if random_index not in random_indexes and random_index + 1 not in random_indexes and \
                        random_index - 1 not in random_indexes:
                    final_email = f"{final_email[:random_index]}" \
                                  f"{random.choice(additional_symbols)}{final_email[random_index + 1:]}"
                    random_indexes.append(random_index)
                    break

    if add_nums:
        for i in range(random.randint(1, 5)):
            final_email += str(random.choice(numbers))

    return final_email + domain


def random_pass_generator(length: int, include_nums: bool, include_special_symbols: bool):
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
               's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
               'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    symbols = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "~", "`"]
    final_pass = ""
    all_chars = letters.copy()
    if include_nums:
        all_chars += numbers + numbers
    if include_special_symbols:
        all_chars += symbols

    for i in range(length):
        final_pass += str(random.choice(all_chars))

    return final_pass



def main():
    app.run(host='0.0.0.0', port=os.getenv("PORT", 3000))

if __name__ == '__main__':
    main()


