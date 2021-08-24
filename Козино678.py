import os #Библиотека для очистки конслои Windows
from ctypes import *
import time
import random

result = 0 # Результат
money = 0 # Сумма на  счету
valuta = 'руб.'  # Валюта игры
defaultMoney = 10000
startMoney = 0
playGame = True

windll.Kernel32.GetStdHandle.restype = c_ulong
h = windll.Kernel32.GetStdHandle(c_ulong(0xfffffff5))

# Изменение цвет текста.
def color(c): 

    windll.Kernel32.SetConsoleTextAttribute(h, c)
    
# Вывод приветствия    
def colorLine(c, s):

    os.system('cls') #очищакт консоль Windows
    
    color(c)
    
    print('*' * (len(s) + 2))
    print('' + s)
    print('*' * (len(s) + 2))

# ВВод ставки пользователя.
def getIntInput(minimum, maximum, message): 

    color(7)
    ret = -1
    
    while (ret < minimum or ret > maximum):
        st = input(message)
        if (st.isdigit()):
            ret = int(st)
        else:
            print('   Введите целое число!')
            
    return ret

# Ввод пользователя.   
def getInput(digit, message): 

    color(7)
    ret = ''
    
    while (ret == '' or not ret in digit):
        ret = input(message)
        
    return ret


# Сумма выигранных средств
def pobeda(result): 

    color(14)

    print(f'    Победа за тобой! Выигрыш составляет: {result} {valuta}')
    print(f'     У тебя на счету: {money}')

 # Сумма проигранных средст
def proigr(result):

    color(12)

    print(f'    К сожелению, проигрыш: {result} {valuta}')
    print(f'    У тебя на счету: {money} {valuta}')
    print('     Обязательно нужно отыгарться!!!')

    
# Метод считывания инфы с файла    
def loadMoney(): 

    try:
        f = open('money.dat', 'r')
        m = int(f.readline())
        f.close()
    except FileNotFoundError:
        print(f'Файл не существует, задано значение {defaultMoney} {valuta}')
        m = defaultMoney

    return m

# Метод записывает информаию в файла
def saveMoney(moneyToSave): 

    try:
        f = open('money.dat', 'w')
        f.write(str(moneyToSave))
        f.close()
    except:
        print('Ошибка создаия файла, нфше Казино закрывается!')
        quit(0) #Прерывание ивыходитв консоль
       
# Roulette ==================================
# Визуализация рулетки
def getRoulette(visible):
    # Задаем переменную
    tickTime = random.randint(100, 200) / 1000
    mainTime = 0
    number = random.randint(0, 38)
    increaseTickTime = random.randint(100, 110) / 100
    col = 1

    # ГЛАВНЫЙ цикл функции
    # Выполняется, пока пауза не станет 0.7 секунды или больше
    while (mainTime <  0.7):
        # Измененение цикла
        col += 1
        if (col >  15):
            col = 1

        # Увеличение времени паузы
        mainTime += tickTime
        tickTime *= increaseTickTime

        # Увеличение номера и вывода на экран
        color(col)
        number += 1
        if (number > 38):
            number = 0
            print()

        # Алгоритм обработкт 'скрытых'от
        # от пользователя чисел 37 и 38,
        # которые символизируют '00' и '000'
        printNumber = number
        if (number == 37):
            printNumber = '00'
        elif (number == 38):
            printNumber = '000'

        # Вывод на экран 
        print('Число >',
              printNumber,
              '*' * number,
              ' ' * (79 - number * 2),
              '*' * number)

        # Делаем паузу в зависимости от
        # перданного аргумента visible
        if (visible):
            time.sleep(mainTime)

    # Возвращаем выпавшее на рулетке число
    return number

# Игра Рулетка
def roulette(): 
    # Получаем возможность изменеия глобальной переменной money
    global money

    # Маркер главного цикла метода рулетки
    playGame = True

    # Главный цикл рулетки
    while (playGame and money > 0):
        # Вывод меню игры
        colorLine(3, 'ДОБРО ПОЖАЛОВАТЬ НА ИГРУ РУЛЕТКА')
        
        color(14)
        print(f'\n У тебя на счету: {money} {valuta}')
        
        color(11)        
        print(' Ставлю на...')
        print('     1. Чётное (выигрыш 1:1)')
        print('     2. Нечётное (выигрыш 1:1)')
        print('     3. Дюжина (выигрыш 3:1)')
        print('     4. Число (выигрыш 36:1)')
        print('     0. Возврат в предыдущее меню')

        # Ввод значения: выбор пункта меню
        x = getInput('01234', '     Твой выбор? ')

        # Маркер: нужно ли нам играть в рулетку?
        # Будет True в том случае, когда пользователь
        # ввёл пралные значения
        playRoulette = True

        # Если игра - дюжина, спрашиваем диапазон чисел
        if (x == '3'):
            color(2)
            print()
            print(' Выбери число:...')
            print('     1. От 1 до 12')
            print('     2. От 13 до 24')
            print('     3. От 25 до 36')
            print('     0. Назад')

            # Выбор пункта меню 'дюжины'
            duzhina = getInput('0123', '     Твой выбор?')

            # Задаем текст диапазона для вывода в последующем коде
            if (duzhina == '1'):
                textDuzhina = 'от 1 до 12'
            elif (duzhina == '2'):
                textDuzhina = 'от 13 до 24'
            elif (duzhina == '3'):
                textDuzhina = 'от 25 до 36'
            elif (duzhina == '0'):
                playRoulette = False
        # Если человек играет ставкой на число, то представляем ввод числа        
        elif (x == '4'):
            chislo = getIntInput(0, 36, '     На какое число ставишь? (0..36): ')

        # Если пользователь ввел 0 в меню рулетки, то возвращаемся в оссновной цикл программы (главнное меню игры)
        color(7)
        if (x == '0'):
            return 0
        
        # Если продолжаем играть (не ввуден 0)
        if (playRoulette):             
            stavka = getIntInput(0, money, f'     Сколько поставишь? (не больше {money}):')
            if (stavka == 0):
                return 0

            # Анимация рулетки и получение номера
            number = getRoulette(True)

            # Выаодим полученное число
            print()
            color(11)

            # В зависимости от значения number формеруем вывод
            if (number < 37):
                print(f'     Выпало число {number}! ' + '*' * number)
            else:
                if (number == 37):
                    printNumber == '00'
                elif (number == 38):
                    printNumber == '000'
                print(f'     Выпало число: {printNumber}!')

                
            # Прверяем ставки и результат
            if (x == '1'):
                print('     Ты ставил на ЧЕРНОЕ!')
                if (number <  37 and number % 2 == 0):
                    money += stavka
                    pobeda(stavka)
                else:
                    money -= stavka
                    proigr(stavka)                    
            elif (x == '2'):
                if (number <  37 and number % 2 != 0):
                    money += stavka
                    pobeda(stavka)
                else:
                    money -= stavka
                    proigr(stavka)

            elif (x == '3'):
                print(f'    Ставка сделана на диапазон чисел {textDuzhina}.')
                winDuzhina = ''
                if (number > 0 and number < 13):
                    winDuzhina = '1'
                elif (number >12 and number < 25):
                    winDuzhina = '2'
                elif (number >26 and number < 37):
                    winDuzhina = '3'

                if (duzhina == winDuzhina):
                    money += stavka * 2
                    pobeda(stavka * 3)
                else:
                    money -= stavka
                    proigr(stavka)
                    
            elif (x == '4'):
                print(f'    Ставка сделана на число {chislo}')
                if (number == chislo):
                    money += stavka * 35
                    pobeda(stavka * 36)
                else:
                    money -= stavka
                    pobeda(stavka)

            # Ждем нажатие Enter и продолжаем
            print()
            input(' Нажмите Enter для продолжения...')


   

    
    

    

# Dice ======================================
# Игра в кости
def dice():
    global money
    playGame = True

    while (playGame):

        print()
        colorLine(3, 'ДОБРО ПОЖАЛОВАТЬ НА ИГРУ КОСТИ!')
        color(14)
        print(f'\n У тебя на счету {money} {valuta}\n')

        color(7)
        stavka = getIntInput(0, money, f'     Сделай ставку в пределах:{money} {valuta}: ')
        if (stavka == 0):
            return 0
        

        playRound = True
        control = stavka
        oldResult = getDice()
        firstPlay = True

        while (playRound and stavka > 0 and money > 0):
            
            if (stavka > money):
                stavka = money

            color(11)
            print(f'    В твоем распаряжении: {stavka} {valuta}')
            color(12)
            print(f'   Текущая сумма чисел на костях: {oldResult}')
            color(11)
            print('\n   Сумма числе на гранях будет больше, меньше или равно?')
            color(7)
            x = getInput('0123', '   Введи 1 - больше, 2 - меньше, 3 - равно или 0 - выход:')

            if (x != 0):
                firstPlay = False
                if (stavka > money):
                    stavka = money

            money -= stavka
            diceResult = getDice()

            win = False
            if (oldResult > diceResult):
                if (x == '2'):
                    win = True
            elif (oldResult < diceResult):
                if (x == '1'):
                    win = True

            if (not x == '3'):
                if (win):
                    money += stavka + stavka // 5
                    pobeda(stavka // 5)
                    stavka += stavka // 5
                else:
                    stavka = control
                    proigr(stavka)
            elif (x == '3'):
                if (oldResult == diceResult):
                    money += stavka * 3
                    poberda(stavka * 2)
                    stavka *= 3
                else:
                    stavka = control
                    proigr(stavka)
                        
            oldResult = diceResult

        else:
            # Если выход на первой ставке
            if (firstPlay):
                money -= stavka
                playRound = False
                

                    
# Анимация кубиков игры в кости
def getDice():
    count =random.randint(3, 8)
    sleep = 0

    while (count > 0):
        color(count + 7)
        x = random.randint(1, 6)
        y = random.randint(1, 6)
        print(' ' * 10, '----- -----')
        print(' ' * 10, f'| {x} | | {y} |')
        print(' ' * 10, '----- -----')
        time.sleep(sleep)
        sleep += 1 / count
        count -= 1
        return x + y
        

# Hand Bandit==================================

# Однорукий бандит...
def oneHandBandit():
    global money
    playGame = True
    while (playGame):
        colorLine(3, 'ДОБРО ПОЖАЛОВАТЬ НА ИГРУ В ОДНОРУКОГО БАНДИТА!')
        color(14)
        print(f'\n У тебя на счету {money} {valuta}\n')
        color(5)
        print('Правила игры:')
        print('     1. При совпвдении 2-х числе ставка не списывается.')
        print('     2. При совпадении 3-х чисел выигрыш 2:1.')
        print('     3. При совпадении 4-х чисел выигрыш 5:1.')
        print('     4. При совадении 5-ти чисел выигрыш 10:1.')
        print('     0. Ставка 0 для завершения игры\n')

        stavka = getIntInput(0, money, f'     Введите ставку от 0 до {money}')
        if (stavka == 0):
            return 0
        money -= stavka
        money += getOHBRes(stavka)

        if (money <= 0):
            playGame = False

# Анимация однорукого бандита.
def getOHBRes(stavka):
    res = stavka
    d1 = 0
    d2 = 0
    d3 = 0
    d4 = 0
    d5 = 0
    getD1 = True
    getD2 = True
    getD3 = True
    getD4 = True
    getD5 = True
    
    col = 10

    while (getD1
           or getD2
           or getD3
           or getD4
           or getD5):
        
        if (getD1):
            d1 += 1
        if (getD2):
            d2 -= 1
        if (getD3):
            d3 += 1
        if (getD4):
            d4 -= 1
        if (getD5):
            d5 += 1
            
        if (d1 > 9):
            d1 = 0
        if (d2 < 0):
            d2 = 9
        if (d3 > 9):
            d3 = 0
        if (d4 < 0):
            d4 = 9
        if (d5 > 9):
            d5 = 0

        if (random.randint(0, 20) == 1):
            getD1 = False
        if (random.randint(0, 20) == 1):
            getD2 = False
        if (random.randint(0, 20) == 1):
            getD3 = False
        if (random.randint(0, 20) == 1):
            getD4 = False
        if (random.randint(0, 20) == 1):
            getD5 = False

        time.sleep(0.1)
        color(col)
        col += 1
        if (col > 15):
            col = 10

        # Строка со знаком %, оформление
        print('     ' + '%' * 10)
        print('     {d1} {d2} {d3} {d4} {d5}')

    msxCount = getMaxCount(d1, d1, d2, d3, d4, d5)

    if (maxCount < getMaxCount(d2, d1, d2, d3, d4, d5)):
        maxCount = getMaxCount(d2, d1, d2, d3, d4, d5))
    if (maxCount < getMaxCount(d3, d1, d2, d3, d4, d5)):
        maxCount = getMaxCount(d3, d1, d2, d3, d4, d5))
    if (maxCount < getMaxCount(d4, d1, d2, d3, d4, d5)):
        maxCount = getMaxCount(d4, d1, d2, d3, d4, d5))
    if (maxCount < getMaxCount(d5, d1, d2, d3, d4, d5)):
        maxCount = getMaxCount(d5, d1, d2, d3, d4, d5))
        
        
        
    


# Анализ совкадения чисел в бандите
#def getMaxCount(digit, v1, v2, v3, v4, v5): 

#=============================================================

    

def main(): #  Диспечер стартово Меню проги. ...
    
    global money, playGame

    money = loadMoney()
    startMoney = money

    while (playGame and money >  0):

        colorLine(10, 'Приветствую тебя в нашем козинодружище!!')
        color(14)
        print(f' У тебя на счету {money} {valuta}')

        color(6)
        print(' Ты можешь сыграть:')
        print('     1. Рулетка')
        print('     2. Кости')
        print('     3. Однорукий бандит')
        print('     0. Выход. Ставка 0 в играх - выход.')
        color(7)

        x = getInput('0123', '     Твой выбор?')

        if (x == '0'):
            playGame = False
        elif (x == '1'):
            roulette()
        elif (x  == '2'):
            dice()
        elif (x == '3'):
            oneHandBandit()

    colorLine(12, 'Жаль что ты покидаешь нас, но возвращайся скорей!!!')
    color(13)
    if (money <= 0):
        print(' Упс, ты остался без денег. Возбми микрокредит ивовращяйся скорей!!!')

    color(11)
    if(money > startMoney):
        print(' Ну чтож, поздравляюс прибылью!')
        print(f' На начало игрыу тебя было: {startMomey} {valuta}')
        print(f' Сейчас уже: {money} {voluta}, играй еще и приумножай!')
    else:
        print(f' К сожелению ты проиграл {startMoney - money} {valuta}')
        print(' В следующий раз все обязательно получится!')

    saveMoney(money)

    color(7)
    quit(0)
        
        
main()
            

            

            
            
        

        
        

    

    
            
            
            
        

            
            

    




 
        
    

        
        
   
                
 
    

            
            
            

    
        
        
    
                
                
        

   
    
    
         
    
    
            
        
        
    


    
     
   
     
  
        



