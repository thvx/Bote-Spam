diccionario={} 
lisb=[]

def llenardic(nom): #llena el diccionario(donde estan las direcciones con cuantas veces han spameado)
    if IsInLN(nom):
        pass
    elif(nom in lisn):
        diccionario[nom]=diccionario[nom]+1
    else:
        diccionario[nom]=1
def llenarlb(nom):        
    lisb.append(nom)
def llenarln(nom):
    diccionario[nom]=5
def IsInLB(nom):
    if nom in diccionario:
        return True
    else return False
def IsInLN(nom):
    if nom not in lisb:
        return False
    if(diccionario[nom]==5):
        return True
    else:
        return False

def menuListas():
    opcion=-1
    print("Seleccione una opción:")
    print("1. Añadir a Lista Blanca")
    print("2. Añadir a Lista negra")
    print("3. Quitar de Lista Blanca")
    print("4. Quitar de Lista negra")
    print("5. Salir")  
    while opcion < 0 and opcion > 6:
        if opcion == 5:
            break
        elif opcion == 4:
            nom=input("Ingrese la dirección de correo que desea quitar de la Lista Negra")
            del(diccionario[nom])
        elif opcion == 3:
            nom=input("Ingrese la dirección de correo que desea quitar de la Lista Blanca")
            lisb.pop(nom)     
        elif opcion == 2:
            nom=input("Ingrese la dirección de correo que desea añadir a la Lista Negra")
            while(nom in lisb):
            llenarln(nom)
        elif opcion == 1:
            nom=input("Ingrese la dirección de correo que desea añadir a la Lista Blanca")
            while(nom in lisb or nom is in diccionario and diccionario[nom]==5):
                nom=input("Ingrese una direccion que no se encuentre ya en la lista")
            llenarlb(nom)



