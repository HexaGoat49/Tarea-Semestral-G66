### ENTRADAS ###

# Crea un numero entero en un intervalo maximo y minimo
def valid(mn, MX, txt):
    v = mn - 1
    while v < mn or v > MX:
        v = int(input(txt))
    return v

# Crea un string sin espacios y con un maximo de caracteres
def no_space(txt, MX):
    out = ""
    while out == "":
        out = input(txt)
        if len(out) > MX:
            out = ""
        for c in out:
            if c == " ":
                out = ""
    return out

# Crea una nueva lista con N elementos
def add_list(N, txt1, txt2):
    k = valid(0, 10, txt1)
    req = []
    for r in range(k):
        req.append(input(txt2.format(k)))
    return req

num_cursos = valid(0, 100, "Ingresar numero de cursos: ") 
num_salas = valid(0, 100, "Ingresar numero de salas: ")
cursos = []
salas = []
nuevo = []

# Id, num, ini, fin, req 
for i in range(num_cursos):
    nuevo = []
    print("--- CURSO {} ---------------".format(i+1))
    
    nuevo.append(no_space("Ingresar identificador: ", 9))
    nuevo.append(valid(1, 500, "Ingresar numero de estudiantes: "))
    nuevo.append(valid(1, 24, "Ingresar bloque inicial: "))
    nuevo.append(valid(nuevo[2], 24, "Ingresar bloque final del curso: "))
    nuevo.append(add_list(10, "Ingresar numero de requisitos: ", "Ingresar requisito {}: "))
    
    cursos.append(nuevo)

# Id, max, car 
for i in range(num_salas):
    nuevo = []
    print("--- SALA {} ---------------".format(i+1))
    
    nuevo.append(no_space("Ingresar identificador: ", 9))
    nuevo.append(valid(1, 500, "Ingresar numero maximo de estudiantes: "))
    nuevo.append(add_list(10, "Ingresar numero de caracteristicas: ", "Ingresar caracteristica {}: "))
    
    salas.append(nuevo)
    
### ALGORITMO ###

# Esta funcion devuelve la lista de todos las salas que cumplen con la condicion de alumno y la de requisitos
def posibles(curso):
    
    global salas
    
    pos = []
    for i in range(len(salas)):
        sala = salas[i]
        
        # Añadir a posibles si cumple la capacidad
        if sala[1] >= curso[1]:
            pos.append(i)
            
            # Quitar de posibles si no tiene los requisitos
            for r in curso[4]:
                if r not in sala[2]:
                    pos.remove(i)
            
    return pos

# Añadir [como indice 5] la salida de posibles() a cada curso
for c in cursos:
    c.append(posibles(c))

# Esta funcion devuelve un booleano que dice si 2 cursos tienen topon de horario
def topon(c1, c2):
    return c1[2] < c2[3] and c1[3] > c2[2]

# Esta funcion lee una lista L de listas B, y devuelve la lista B con el menor valor de indice index
def optimo(L, index):
    
    P = []
    for B in L:
        P.append(B[index])
    P.sort()
    m = P[0]
    
    for B in L:
        if m == B[index]:
            return B
        

# Esta funcion calcula para cada curso, una lista "D"
# Esta lista contiene otras listas K cada una con 3 numeros
# El primero es en indice del curso
# El segundo es el indice de una sala de su lista de posibles
# El tercero es cuantos topones tiene el curso en esa sala
# Por ejemplo si un curso tiene 2 topones es que hay 2 cursos mas que tienen topon de horario con ese curso
# La funcion solamente va a devolver la lista K que tenga el menor numero de topones
def candidato(curso):
    
    global cursos
    D = []
    for s in curso[5]:
        v = 0
        
        # Primero se obtienen los cursos (distintos al de la funcion) que tienen la sala s
        for c in cursos:
            if s in c[5] and c != curso and topon(curso, c):
                    v += 1
        # Se genera una lista K con 3 numeros
        D.append([cursos.index(curso), s, v])
        
    # Si D esta vacio se devuelve None
    if len(D) == 0:
        return None
    # Si no, se devuelve el "mejor" elemento de D
    else:
        return optimo(D, 2)

# Mejor es una lista K
mejor = []
# Esta funcion calcula los candidatos (6to indice) de cada curso y calcula el mejor
def calcular():
    global mejor
    
    M = []
    for c in cursos:
        c[6] = candidato(c)
        if c[6] != None:
            M.append(c[6])
    
    if len(M) != 0:
        mejor = optimo(M, 2)
        
    else:
        mejor = None


# Esta funcion elige a la sala y al curso como un par valido
# Nota, "curso" es una lista tipo curso y "sala" un indice de la sala
elegidos = []
def elegir(curso, sala):
    
    global cursos
    global salas
    global mejor
    
    # Primero, se añade [(ID de curso), (ID de sala)] a elegidos
    elegidos.append([curso[0], salas[sala][0]])
    
    # Segundo, se quita esta sala como sala posible a todos cursos que tengan topon en la sala con el curso c
    for c in cursos:
        # Si es sala posible en c y hay topon entre c y curso
        if sala in c[5] and topon(curso, c):
            c[5].remove(sala)
    
    # Tercero, se elimina este curso de la lista de cursos
    cursos.remove(curso)
    
    # Cuarto, a todos los cursos se recalculan los candidatos
    calcular()

# Primero se calculan los candidatos
# Añadir un indice 6 a los cursos
for c in cursos:
    c.append([])
calcular()

# Se elige al mejor candidato si existe
while mejor != None:
    elegir(cursos[mejor[0]], mejor[1]) 


### SALIDAS ###

print("--- SALIDA ---------------")
print(len(elegidos), "cursos tienen salas:")
for e in elegidos:
    print(e[0], e[1])

print(len(cursos), "no tienen salas:")
for c in cursos:
    print(c[0])
    
