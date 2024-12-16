#В форме функций задается ряд логических операций, принимающих два операнда

def conjunction (x, y):
 return x and y
	
def disjunction (x, y):
 return x or y

def strict_disjunction (x, y):
 return x != y

def equivalence(x, y):
 return x == y

def implication(x, y):
 return not x or y


#Функции логических операций связываются с их обозначениями в строке, задающей формулу
functions = {
    "&": conjunction,
    "v": disjunction,
    "->": implication,
    "=": equivalence,
    "(+)": strict_disjunction
}

#Обозначения операций в строке, задающей формулу, хранятся в массиве в порядке убывания приоритета
order = ["&", "v", "(+)", "->", "="]

#Функция возвращает строку, содержащую в алфавитном порядке все буквенные обозначения пропозициональных переменных в формуле exp
def getAllVars(exp):
    all_vars = ""
    for i in range(0, len(exp)):
        if exp[i].isalpha() and exp[i] == exp[i].upper() and exp[i] not in all_vars:
            all_vars = all_vars + exp[i]
    return ''.join(sorted(all_vars))

#Функция возвращает 1, если все пары скобок в формуле exp закрыты, нет лишних и недостающих, и 0 в противном случае
def isClosed(exp):
    return exp.count("(") == exp.count(")")

#Функция возвращает 1, если формула exp имеет пару внешних скобок (то есть пару, в которую она полностью заключена), и 0 в противном случае
def hasExternals(exp):
    if exp[0] != "(":
        return 0
    else:
        counter = 1
        pointer = 0
        while counter != 0:
            pointer+=1
            if exp[pointer] == "(":
                counter+=1
            elif exp[pointer] == ")":
                counter-=1
        if pointer == len(exp) - 1:
            return 1
        else:
            return 0


#Функция возвращает строку - вариант записи формулы exp без внешних скобок, если таковые имелись
def deleteExternal(exp):
    if exp[0] == "(" and exp[len(exp)-1] == ")":
        exp = exp[1:len(exp)-1]
    return exp

#Функция возвращает строку - вариант записи формулы exp без пробелов
def deleteAllSpaces(exp):
    return "".join(exp.split())

#Функция возвращает массив с двумя элементами - левой и правой частью выражения exp, разделенной операцией, имеющей наименьший приоритет выполнения в нем	
def divideExp(exp):
    parts = ["", ""]
    for i in range (len(order) - 1, -1, -1):
        cur_ind = len(exp)
        while cur_ind > 0:
            if exp.find(order[i], 0, cur_ind) == -1:
                break
            parts[1] = exp[exp.rfind(order[i], 0, cur_ind) + len(order[i]):len(exp)]
            parts[0] = exp[0:exp.rfind(order[i], 0, cur_ind)]
            if isClosed(parts[0]) and isClosed(parts[1]):
                if hasExternals(parts[0]):
                    parts[0] = deleteExternal(parts[0])
                if hasExternals(parts[1]):
                    parts[1] = deleteExternal(parts[1])
                #print("\t".join(parts))
                return parts;
            else:
                cur_ind = exp.rfind(order[i], 0, cur_ind)

#Функция возвращает строковое обозначение операции, имеющей наименьший приоритет выполнения в данном выражении exp
def getDividindSign(exp):
    for i in range (len(order) - 1, -1, -1):
        cur_ind = len(exp)
        while cur_ind > 0:
            if exp.find(order[i], 0, cur_ind) == -1:
                break
            part_1 = exp[exp.rfind(order[i], 0, cur_ind) + len(order[i]):len(exp)]
            part_2 = exp[0:exp.rfind(order[i], 0, cur_ind)]
            if isClosed(part_1) and isClosed(part_2):
                return order[i];
            else:
                cur_ind = exp.rfind(order[i], 0, cur_ind)  

#Функция возвращает значение переданного выражения exp, основываясь на значениях переменных, переданных в виде двоичного вектора code, и наборе обозначений переменных alphabet
def getValue(exp, code, alphabet):
    #print("Cur: ", exp)
    while (hasExternals(exp)):
        exp = deleteExternal(exp)
    if len(exp) == 1:
        return bool(code >> alphabet[::-1].find(exp[0]) & 1)
    elif exp[0] == "!" and (hasExternals(exp[1:]) or len(exp) == 2):
        return bool(not getValue(deleteExternal(exp[1:]), code, alphabet))
    else:
        parts = divideExp(exp)
        sign = getDividindSign(exp)
        return functions[sign](getValue(parts[0], code, alphabet), getValue(parts[1], code, alphabet))

#Функция возвращает строковое обозначение операции, имеющей наименьший приоритет выполнения в данном выражении exp
def getDividindSign(exp):
    for i in range (len(order) - 1, -1, -1):
        cur_ind = len(exp)
        while cur_ind > 0:
            if exp.find(order[i], 0, cur_ind) == -1:
                break
            part_1 = exp[exp.rfind(order[i], 0, cur_ind) + len(order[i]):len(exp)]
            part_2 = exp[0:exp.rfind(order[i], 0, cur_ind)]
            if isClosed(part_1) and isClosed(part_2):
                return order[i];
            else:
                cur_ind = exp.rfind(order[i], 0, cur_ind)  

#Функция возвращает значение переданного выражения exp, основываясь на значениях переменных, переданных в виде двоичного вектора code, и наборе обозначений переменных alphabet
def getValue(exp, code, alphabet):
    while (hasExternals(exp)):
        exp = deleteExternal(exp)
    if len(exp) == 1:
        return bool(code >> alphabet[::-1].find(exp[0]) & 1)
    elif exp[0] == "!" and (hasExternals(exp[1:]) or len(exp) == 2):
        return bool(not getValue(deleteExternal(exp[1:]), code, alphabet))
    else:
        parts = divideExp(exp)
        sign = getDividindSign(exp)
        return functions[sign](getValue(parts[0], code, alphabet), getValue(parts[1], code, alphabet))


#Возвращает двоичный вектор - последовательность нулей и единиц, значений таблицы истинности выражения exp с набором переменных alphabet по строкам сверху вниз
def getFinalColumn(exp, alphabet):
    exp = deleteAllSpaces(exp)
    final_column = 0
    for cur_code in range(0, 1<<len(alphabet)):
        final_column = (final_column << 1) + int(getValue(exp, cur_code, alphabet))
    return final_column

#Возвращает массив строк - дизъюнктов формы СКНФ выражения с набором переменных alphabet, значения таблицы истинности которого хранятся в двоичном векторе final_column
def getPCNF(final_column, alphabet):
    strings_amount = 2**len(alphabet)
    cur_string_code = strings_amount - 1
    PCNF = []
    while cur_string_code >= 0:
        if final_column>>(strings_amount - cur_string_code - 1) & 1 == 0:
            cur_disjunct = ""
            for i in range(0, len(alphabet)):
                if (cur_string_code>>(len(alphabet)-i-1)) & 1:
                    cur_disjunct = cur_disjunct + "!"
                cur_disjunct = cur_disjunct + alphabet[i] + "v"
            PCNF.append(cur_disjunct[0:len(cur_disjunct)-1])
        cur_string_code = cur_string_code - 1
    return PCNF

#Возвращает массив массивов строк - то есть массив форм СКНФ выражений, являющихся следствиями из выражения exp с набором переменных alphabet
def getPCNFsOfConsequences(exp, alphabet):
    origin_final_column_code = getFinalColumn(exp, alphabet)
    origin_PCNF = getPCNF(origin_final_column_code, alphabet)
    PCNFs_array = []
    PCNFs_array.append(origin_PCNF)
    cur_combination_code = 2**len(origin_PCNF) - 2
    while cur_combination_code >= 0:
        cur_PCNF = []
        for i in range(0, len(origin_PCNF)):
            if cur_combination_code>>(len(origin_PCNF) - i - 1) & 1:
                cur_PCNF.append(origin_PCNF[i])
        PCNFs_array.append(cur_PCNF)
        cur_combination_code = cur_combination_code - 1
    return PCNFs_array

#Возвращает -1, если дизьюнкты exp1 и exp2 не могут быть объединены в один методом склеивания, и индекс знака отрицания при "склеивающей" переменной в наиболее длинном дизъюнкте, если склеивание возможно:
def canBeGlued(exp1, exp2):
    if abs(len(exp1) - len(exp2)) != 1:
        return -1
    pointer = 0
    while pointer < min(len(exp1), len(exp2)):
        if exp1[pointer] == exp2[pointer]:
            pointer = pointer + 1
        elif exp1[pointer] == "!":
            exp1 = exp1[0:pointer] + exp1[pointer+1:len(exp1)]
            if (exp1 != exp2):
                return -1
            else:
                return pointer
        elif exp2[pointer] == "!":
            exp2 = exp2[0:pointer] + exp2[pointer+1:len(exp2)]
            if (exp1 != exp2):
                return -1
            else:
                return pointer
        else:
            return -1
    return -1

#Возвращает дизьюнкт - результат склеивания дизъюнктов exp1 и exp2 при индексе знака отрицания при "склеивающей" переменной, равном pointer
def returnGlued(exp1, exp2, pointer):
    if (len(exp1) > len(exp2)):
        if (pointer == len(exp2) - 1):
            return exp2[0:pointer-1] + exp2[pointer+1:len(exp2)]
        else:
            return exp2[0:pointer] + exp2[pointer+2:len(exp2)]

    else:
        if (pointer == len(exp1) - 1):
            return exp1[0:pointer-1] + exp1[pointer+1:len(exp1)]
        else:
            return exp1[0:pointer] + exp1[pointer+2:len(exp1)]

#Возвращает массив строк - дизъюнктов формы КНФ после склеивания дизъюнктов СКНФ некоего выражения, хранящейся в массиве PCNF
def simplifyPCNF (PCNF):
    first_pointer = 0
    while (first_pointer < len(PCNF)):
        second_pointer = 0
        while (second_pointer < len(PCNF)):
            p = canBeGlued(PCNF[first_pointer], PCNF[second_pointer])
            if (first_pointer == second_pointer):
                second_pointer = second_pointer + 1
                continue
            elif (p != -1):
                PCNF[first_pointer] = returnGlued(PCNF[first_pointer], PCNF[second_pointer], p)
                PCNF.pop(second_pointer)
                second_pointer = 0
            elif (PCNF[first_pointer] == PCNF[second_pointer]):
                PCNF.pop(second_pointer)
                second_pointer = second_pointer + 1
            else:
                second_pointer = second_pointer + 1
        first_pointer = first_pointer + 1
    return PCNF

#Возвращает массив массивов строк - массив форм КНФ после склеивания дизъюнктов СКНФ неких выражений, хранящихся в массиве PCNFs_array
def simplifyArrayOfPCNFs (PCNFs_array):
    for i in range (0, len(PCNFs_array)):
        PCNFs_array[i] = simplifyPCNF(PCNFs_array[i])
    return PCNFs_array

#Выводит на экран массив форм КНФ неких выражений, хранящихся в массиве CNFs_array
def printArrayOfCNFs (CNFs_array):
    for i in range (0, len(CNFs_array)):
        print("(" + ") & (".join(CNFs_array[i]) + ")")
    


            
print("Здравствуйте! С помощью этой программы вы можете получить все возможные следствия из посылок, вводимых с клавиатуры, как в виде СКНФ, так и в сокращенной КНФ.")
print("Вводя посылки, соблюдайте несколько простых правил:")
print("\t 1) Обозначайте каждую переменную одной заглавной буквой латинского алфавита")
print("\t 2) Убедитесь, что операторы в вашей формуле не идут подряд, а все скобки закрыты")
print("\t 3) Не вставляйте в строку посторонних символов, кроме знаков операций, названий переменных, скобок и пробелов")
print("Для обозначения операций используйте следующие последовательности: ! - отрицание, & - конъюнкция, v - дизъюнкция, (+) - исключающее или, -> - импликация, = - эквивалентность.")
print("Перед началом работы введите perfect, если хотите получить следствия в форме СКНФ, и short, если хотите, чтобы записи следствий были сокращены по закончу склеивания (по умолчанию применяется настройка perfect).")
format = input().lower()
print("Теперь можете вводить посылки, из которых хотите получить следствия. Для того, чтобы получить следствия, нажмите Enter, оставив последнюю строку пустой. После вывода следствий на экран вы можете начать ввод нового множества посылок (настройки вывода останутся прежними). Для прекращения цикла ввода введите  quit.")
cur_premise = input()
while cur_premise != "quit":
    premises = []
    while cur_premise != "":
        premises.append(cur_premise)
        cur_premise = input()
    ex = "(" + ") & (".join(premises) + ")"
    
    if format == "short":
        printArrayOfCNFs(simplifyArrayOfPCNFs(getPCNFsOfConsequences(ex, getAllVars(ex))))
    else:
        printArrayOfCNFs(getPCNFsOfConsequences(ex, getAllVars(ex)))

    cur_premise = input()
