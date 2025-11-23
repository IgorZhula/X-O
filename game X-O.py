import random
import os
"эта функция создает файл с результатами если ее еще нет"
def create_stats_directory():
    if not os.path.exists("game_stats"):
        os.makedirs("game_stats")

"сохраняет результат игры в файл"
def save_game_result(winner, size):
    with open("game_stats/results.txt", "a", encoding="utf-8") as f:
        if winner == "X":
            f.write(f"Победил X на поле {size}x{size}\n")
        elif winner == "O":
            f.write(f"Победил O на поле {size}x{size}\n")
        else:
            f.write(f"Ничья на поле {size}x{size}\n")

"вывод игрового поля в консоль"
def print_board(board, size):
    print("\n   ", end="")
    for i in range(size):
        print(f" {i + 1} ", end="")
    print()

    for i in range(size):
        print(f"{i + 1} |", end="")
        for j in range(size):
            print(f" {board[i][j]} ", end="")
        print("|")

"функция для проверки победителя"
def check_winner(board, size):
    # Проверка строк
    for i in range(size):
        if board[i][0] != ' ' and all(board[i][j] == board[i][0] for j in range(size)):
            return board[i][0]

    # Проверка столбцов
    for j in range(size):
        if board[0][j] != ' ' and all(board[i][j] == board[0][j] for i in range(size)):
            return board[0][j]

    # Проверка диагоналей
    if board[0][0] != ' ' and all(board[i][i] == board[0][0] for i in range(size)):
        return board[0][0]

    if board[0][size - 1] != ' ' and all(board[i][size - 1 - i] == board[0][size - 1] for i in range(size)):
        return board[0][size - 1]

    return None

"проверка заполнености клетки"
def is_board_full(board, size):
    for i in range(size):
        for j in range(size):
            if board[i][j] == ' ':
                return False
    return True

"получения хода от игрока"
def get_player_move(board, size, player):
    while True:
        try:
            move = input(f"Игрок {player}, введите строку и столбец (например: 1 2): ")
            parts = move.split()
            if len(parts) != 2:
                print("Ошибка! Введите два числа через пробел")
                continue

            row = int(parts[0]) - 1
            col = int(parts[1]) - 1

            if row < 0 or row >= size or col < 0 or col >= size:
                print(f"Ошибка! Числа должны быть от 1 до {size}")
                continue

            if board[row][col] != ' ':
                print("Эта клетка уже занята!")
                continue

            return row, col

        except ValueError:
            print("Ошибка! Введите числа")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

"ход компьютера"
def get_computer_move(board, size):
    # поиск выиграшного хода
    for i in range(size):
        for j in range(size):
            if board[i][j] == ' ':
                board[i][j] = 'O'
                if check_winner(board, size) == 'O':
                    board[i][j] = ' '
                    return i, j
                board[i][j] = ' '

    # блокировка игрока
    for i in range(size):
        for j in range(size):
            if board[i][j] == ' ':
                board[i][j] = 'X'
                if check_winner(board, size) == 'X':
                    board[i][j] = ' '
                    return i, j
                board[i][j] = ' '

    # занятие центра если он свободен
    center = size // 2
    if board[center][center] == ' ':
        return center, center

    # случайный ход
    empty_cells = []
    for i in range(size):
        for j in range(size):
            if board[i][j] == ' ':
                empty_cells.append((i, j))

    return random.choice(empty_cells)


def play_game():
    """Основная функция игры"""
    create_stats_directory()

    while True:
        print("\n" + "=" * 40)
        print("       КРЕСТИКИ-НОЛИКИ")
        print("=" * 40)

        # Выбор режима игры
        while True:
            print("\nВыберите режим игры:")
            print("1 - Два игрока")
            print("2 - Против компьютера")
            try:
                mode = int(input("Ваш выбор (1 или 2): "))
                if mode in [1, 2]:
                    break
                else:
                    print("Ошибка! Введите 1 или 2")
            except:
                print("Ошибка! Введите число")

        # Выбор размера поля
        while True:
            try:
                size = int(input("\nВведите размер поля (3-5): "))
                if 3 <= size <= 5:
                    break
                else:
                    print("Ошибка! Размер должен быть от 3 до 5")
            except:
                print("Ошибка! Введите число")

        # Создание поля
        board = [[' ' for _ in range(size)] for _ in range(size)]

        # Случайно выбираем кто ходит первым
        current_player = random.choice(['X', 'O'])
        print(f"\nПервым ходит: {current_player}")

        while True:
            print_board(board, size)

            # Получаем ход
            if mode == 1 or current_player == 'X':
                # Ход человека
                row, col = get_player_move(board, size, current_player)
            else:
                # Ход компьютера
                print("\nКомпьютер думает...")
                row, col = get_computer_move(board, size)
                print(f"Компьютер походил: {row + 1} {col + 1}")

            # Делаем ход
            board[row][col] = current_player

            # Проверяем победу
            winner = check_winner(board, size)
            if winner:
                print_board(board, size)
                print(f"\n🎉 Победил {winner}!")
                save_game_result(winner, size)
                break

            # Проверяем ничью
            if is_board_full(board, size):
                print_board(board, size)
                print(f"\n🤝 Ничья!")
                save_game_result("Ничья", size)
                break

            # Меняем игрока
            current_player = 'O' if current_player == 'X' else 'X'

        # Предложение сыграть еще
        while True:
            again = input("\nХотите сыграть еще? (да/нет): ").lower()
            if again in ['да', 'д', 'yes', 'y']:
                break
            elif again in ['нет', 'н', 'no', 'n']:
                print("Спасибо за игру!")
                return
            else:
                print("Пожалуйста, введите 'да' или 'нет'")
if __name__ == "__main__":
    play_game()