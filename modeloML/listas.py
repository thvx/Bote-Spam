diccionario={} 
lisb=[]

def llenardic(nom): #llena el diccionario(donde estan las direcciones con cuantas veces han spameado)
    if IsInLN(nom):
        pass
    elif nom in lisb:
        diccionario[nom]=diccionario.get(nom,0)+1
    else:
        diccionario[nom]=1

def llenarlb(nom):        
    lisb.append(nom)

def llenarln(nom):
    diccionario[nom]=5

def IsInLB(nom):
    return nom in diccionario
    
def IsInLN(nom):
    return nom not in lisb and diccionario.get(nom, 0) == 5

def menuListas():
    opcion=-1
    while opcion !=5:
        print("Seleccione una opción:")
        print("1. Añadir a Lista Blanca")
        print("2. Añadir a Lista negra")
        print("3. Quitar de Lista Blanca")
        print("4. Quitar de Lista negra")
        print("5. Salir")  
        opcion = int(input("Ingrese el número de la opción que desea seleccionar: "))

        if opcion == 5:
            break
        elif opcion == 4:
            nom=input("Ingrese la dirección de correo que desea quitar de la Lista Negra")
            if nom in diccionario:
                del(diccionario[nom])
        elif opcion == 3:
            nom=input("Ingrese la dirección de correo que desea quitar de la Lista Blanca")
            if nom in lisb:
                lisb.remove(nom)     
        elif opcion == 2:
            nom=input("Ingrese la dirección de correo que desea añadir a la Lista Negra")
            while nom in lisb:
                nom = input("La dirección ya está en la Lista Blanca. Ingrese otra dirección: ")
            llenarln(nom)
        elif opcion == 1:
            nom = input("Ingrese la dirección de correo que desea añadir a la Lista Blanca: ")
            while nom in lisb or (nom in diccionario and diccionario[nom] == 5):
                nom = input("La dirección ya está en la Lista o ha sido spam. Ingrese otra dirección: ")
            llenarlb(nom)



