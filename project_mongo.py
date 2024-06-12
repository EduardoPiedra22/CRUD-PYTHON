from pymongo import MongoClient
#Eduardo Piedra
#Rafael Briceño

# Conectar a MongoDB
client = MongoClient("mongodb://localhost:27017/")
autos = client["Autos"]
collection = autos["collectionAutos"]

# Creamos nuestra funcion que inicializara al ejecutar el script
def main_menu():
    while True:
        print("**** Menu Principal ****")
        print("1. Registrar ")
        print("2. Consultar ")
        print("3. Modificar ")
        print("4. Eliminar ")
        print("5. Salir")
        # realizamos manejo de errores por si un usuario introduce una opcion no valida    
        try:
            opcion = int(input("Introduce la opción: "))
            # dependiendo de la opcion seleccionada se llamara a diferentes funciones
            if opcion == 1:
                registrar()
            elif opcion == 2:
                consultar()
            elif opcion == 3:
                modificar()
            elif opcion == 4:
                eliminar()
            elif opcion == 5:
                print("Saliendo del programa...")
                break
            else:
                print("Debe introducir una opción válida")
        # Monstramos el mensaje de error
        except ValueError:
            print("Debe introducir solo números enteros")
            
#funcion para registrar
def registrar():
    while True:
        print("*** Menu de Registro ***")
        print("1. Registrar Auto")
        print("2. Agregar campos extras")
        print("3. Volver al menú anterior")
        #manejo de errores
        try:
            opcion = int(input("Introduce tu opción: "))
            if opcion == 1:
                #Solicitamos los valores de nuestras llaves para armas nuestro diccionario
                placa = input("Placa del auto: ")
                marca = input("Marca del auto: ")
                modelo = input("Modelo del auto: ")
                year = input("Año de fabricación: ")
                # Creamos el diccionario
                documento = {
                    "_id": placa,
                    "marca": marca,
                    "modelo": modelo,
                    "year": year
                }
                #Insertamos en nuestra collection
                collection.insert_one(documento)
                #enviamos mensaje de exito
                print("Se ha agregado a la colección")
                
            elif opcion == 2:
                campos()
            elif opcion == 3:
                break
            else:
                print("Debe introducir una opción válida")
        #mostramos si hay un error
        except ValueError:
            print("Debes introducir solo números enteros")
            
#Sub menu si se desea agregar un campo extra a nuestra collection
def campos():
    print("*** Agregar campos extras ***")
    # Solicitamos la placa del auto que se desea realizar la agregacion 
    try:
        placa = input("Introduce la placa del auto al que deseas agregar el campo: ")
        # Buscamos el documento por la placa
        documento = collection.find_one({"_id": placa})
        
        #si se encuentra
        if documento:
            #solicitamos la clave y el valor
            campo = input("Introduce el nombre del campo extra: ")
            valor = input(f"Introduce el valor para {campo}: ")
            
            # Agregamos el nuevo campo al documento
            documento[campo] = valor

            # Actualizamos el documento en la colección
            collection.update_one({"_id": placa}, {"$set": documento})

            print(f"Se ha agregado el campo '{campo}' con el valor '{valor}' al auto con placa '{placa}'.")
            
        #si no se encuentra la placa mostramos mensaje 
        else:
            print(f"No se encontró ningún auto con la placa '{placa}'.")
    except:
        print ("Introduce una opcion valida")     
    
# Consultas
def consultar():
    while True:
        print ("***Menu de Consultas***")
        print ("1. Listado general")
        print("2. Consulta de un auto especifico")
        print ("3. Salir al menu anterior")
        try:
            
            opcion = int(input("Introduce tu opcion: "))
            if opcion ==1:
                print("*** Listado de Autos ***")
                
                consult = list(collection.find())
                
                #verificamos que el listado  este vacio
                if not consult:
                    print("La lista está vacía, debe agregar un auto.")
                #de lo contrario
                else:
                    print("Información de los  Autos:")               
                    for auto in consult:

                        
                        
                        #Iteramos sobre la clave y el valor en cada registros
                        for campo, valor in auto.items():
                            
                            #con capitalize() hacemos la primera letra de cada palabra mayuscula.
                            #tambien le damos formato a la imprecion
                            print(f"{campo.capitalize()}: {valor}")
                        print()  # Agregamos una línea en blanco entre cada auto

                    
            #Consulta especifica
            elif opcion == 2:
                
                #Solicitamos la clave
                placa = input("Introduce la placa del auto que deseas consultar: ")
                
                #Buscamos por dicha clave
                resultado = collection.find_one({"_id": placa})
                
                #Si se encuentra
                if resultado:
                    print("*** Información del Auto ***")
                    #iteramos sobre cada clave, valor en el resultado obtenido
                    for campo, valor in resultado.items():
                        
                        #Damos Forma a la imprecion
                        print(f"{campo.capitalize()}: {valor}")
                        
                # Si no se encuentra mostramos mensaje de error
                else:
                    print(f"No se encontró ningún auto con la placa {placa}.")
            #opcion salir
            elif opcion == 3:
                break
            
            elif opcion >= 4:
                print ("Introduce una opcion valida")
        except ValueError:
            print ("Solo puedes introducir numeros enteros")
        
        
        
        
def modificar():
    while True:
        print("*** Modificar Auto ***")
        
        #solicitamos valor de auto a modificar
        placa = input("Introduce la placa del auto que deseas modificar: ")
            #buscamos
        resultado = collection.find_one({"_id": placa})
            #si se encuentra
        if resultado:
                print("*** Modificar Auto ***")
                print("Campos disponibles:")
                #Inicializamos un contador
                contador = 1
                print ("0. Salir")
                
                # Iteramos el objeto obtenido
                for campo in resultado:
                    # Damos forma al print (esto es para que el menu se imprimo conforme la cantidad
                    # de campos que tenga el registro o objeto )
                    print (f"{contador}. {campo}: ")
                    
                    #sumamos +1 al contador para que por cada campo se sume 1 y se imprima cada opcion con
                    # numero distinto
                    contador += 1
                
                #Solicitamos opcion
                opcion = int(input("Selecciona el número del campo que deseas modificar: "))
                
                #salimos en caso de ser 0
                if opcion == 0:
                    break
                #verificamos que la opcion sea valida 
                if 1 <= opcion <= contador - 1:
                    #obtenemos la lista de las claves con .key() de nuestro objeto 
                    # (con [opcion - 1] le decimos (la variable opcion lleva nuestro numero seleccionado)
                    # y con el -1 le decimos que a la opcion le reste 1 numero ya que sabemos que la indexacion de 
                    #python comienza con 0
                    campo_seleccionado = list(resultado.keys())[opcion - 1]
                    
                    #Solicitamos nuevo valor para la clave
                    nuevo_valor = input(f"Introduce el nuevo valor para {campo_seleccionado}: ")
                    
                    # Actualizamos el campo en el documento
                    collection.update_one({"_id": placa}, {"$set": {campo_seleccionado: nuevo_valor}})
                    
                    #mostramos mensaje de exito
                    print(f"El campo '{campo_seleccionado}' ha sido modificado correctamente.")
                    break
                # de lo contrario mostraremos un error
                else:
                    print("Opción inválida.")
                    
            #si no se encuentra mostramos mensaje de error   
        else:
                print(f"No se encontró ningún auto con la placa {placa}.")
            
# Eliminar
def eliminar():
    print("*** Eliminar Auto ***")
    placa = input("Ingrese la placa del auto que desea eliminar: ") 
    
    # Buscamos el auto
    resultado = collection.find_one({"_id": placa})
    # si encontramos
    if resultado:
        #eliminamos y mostramos mensaje de exito
        collection.delete_one({"_id": placa})
        print (f"se ha aliminado el auto con la placa:  {placa} ")
        
    #si no se encuentra un auto mostramos mensaje de error
    else:
        print ("Auto no encontrado")

#Ejecutamos el Script 
if __name__ == "__main__":
    main_menu()
