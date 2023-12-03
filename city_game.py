import random


def user_answer():
    if previous_city:
        last_letter = previous_city[-1].lower()
        if last_letter in exclude_letters:
            print("Город заканчивается на букву, на которую нельзя назвать город. Введите город на первую букву предыдущего слова: ")
            city = input("Введите название города, для выхода из игры - выход: ").title()
            return city
    city = input("Введите название города: ").title()
    return city

def comp_answer(previous_city, answers=None):
    last_letter = previous_city[-1].lower()
    if last_letter in exclude_letters:
        cities = [city for city in cities_list if city[0].lower() == previous_city[0].lower()]
    else:
        cities = [city for city in cities_list if city[0].lower() == previous_city[-1]]
    unused_cities = [city for city in cities if city not in answers]
    current_city = random.choice(unused_cities)
    return current_city

def save_game(game):
    with open("C:\\Users\\Полина\\Desktop\\answers.txt", 'w', encoding="utf-8") as f:
        f.write(game + '\n')

if __name__ == "__main__":
    with open("C:\\Users\\Полина\\Desktop\\cities.txt", 'r', encoding='utf-8') as f:
        cities_list = f.read().splitlines()

    answers = []
    previous_city = ""
    exclude_letters = ["ы", "ь", "ъ"]

    def play_game():

        global user_attempts
        user_attempts = 0

        while True:
            user_city = user_answer()
            if user_city.lower() == "выход":
                print("Игра закончена.")
                break

            if not user_city:
                print("Вы не ввели город. Попробуйте еще раз:")
                continue

            if user_city not in cities_list:
                user_attempts += 1
                print("Такого города не существует. Попробуйте еще раз.")
                if user_attempts >= 5:
                    print("Ваша попытки закончились. Игра проиграна.")
                    save_game("Поражение игрока")
                    break
                continue

            if user_city in answers:
                user_attempts += 1
                print("Такой город уже был. Попробуйте еще раз.")
                if user_attempts >= 5:
                    print("Ваша попытки закончились. Игра проиграна.")
                    save_game("Поражение игрока")
                    break
                continue

            if answers and user_city[0].lower() != answers[-1][-1].lower() and answers[-1][-1].lower() \
                not in exclude_letters:
                user_attempts += 1
                print("Город должен называться с последней буквы предыдущего города. Попробуйте еще раз.")
                if user_attempts >= 5:
                    print("Ваша попытки закончились. Игра проиграна.")
                    save_game("Поражение игрока")
                    break
                continue

            answers.append(user_city)
            previous_city = user_city
            save_game("Пользователь:" + user_city)
            comp_city = comp_answer(previous_city, answers)
            if not comp_city:
                print("Компьютер не смог найти подходящий город. Вы победили!")
                save_game("Поражение компьютера")
                break

            answers.append(comp_city)
            save_game("Компьютер:" + comp_city)
            print("Компьютер:" + comp_city)
    play_game()
