#!/usr/bin/env python
'''
SQL Introducción [Python]
Ejercicios de práctica
---------------------------
Autor: Ing.Jesús Matías González
Version: 1.1

Descripcion:
Programa creado para poner a prueba los conocimientos
adquiridos durante la clase
'''

__author__ = "Ing.Jesús Matías González"
__email__ = "ingjesusmrgonzalez@gmail.com"
__version__ = "1.1"

import sqlite3

import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Crear el motor (engine) de la base de datos
engine = sqlalchemy.create_engine("sqlite:///secundaria.db")
base = declarative_base()


class Tutor(base):
    __tablename__ = "tutor"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    
    def __repr__(self):
        return f"Tutor: {self.name}"


class Estudiante(base):
    __tablename__ = "estudiante"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    grade = Column(Integer)
    tutor_id = Column(Integer, ForeignKey("tutor.id"))

    tutor = relationship("Tutor")

    def __repr__(self):
        return f"Estudiante: {self.name}, edad {self.age}, grado {self.grade}, tutor {self.tutor.name}"


def create_schema():
    # Borrar todos las tablas existentes en la base de datos
    # Esta linea puede comentarse sino se eliminar los datos
    base.metadata.drop_all(engine)

    # Crear las tablas
    base.metadata.create_all(engine)


def fill():
    print('Completemos esta tablita!')
    print('...')
    # Llenar la tabla de la secundaria con al munos 2 tutores
    # Cada tutor tiene los campos:
    # id --> este campo es auto incremental por lo que no deberá completarlo
    # name --> El nombre del tutor (puede ser solo nombre sin apellido)

    # Crear la session
    Session = sessionmaker(bind=engine)
    session = Session()

    tutor1 = Tutor(name='Marcos Rojo')
    tutor2 = Tutor(name='Lautaro Martinez')
    tutor3 = Tutor(name='Diego Costas')

    session.add_all([tutor1, tutor2, tutor3])
    session.commit()

    # Agregar tutores
    
    # Llenar la tabla de la secundaria con al menos 5 estudiantes
    # Cada estudiante tiene los posibles campos:
    # id --> este campo es auto incremental por lo que no deberá completarlo
    # name --> El nombre del estudiante (puede ser solo nombre sin apellido)
    # age --> cuantos años tiene el estudiante
    # grade --> en que año de la secundaria se encuentra (1-6)
    # tutor --> el tutor de ese estudiante (el objeto creado antes)

     # Crear estudiantes

    estudiante1 = Estudiante(name = "Lucas Ocampos", age = 31, grade = 1, tutor_id = 1)
    estudiante2 = Estudiante(name = "Leonardo Ponzio", age = 44, grade = 2, tutor_id = 1)
    estudiante3 = Estudiante(name = "Antonio Rios", age = 64, grade = 3, tutor_id = 3)
    estudiante4 = Estudiante(name = "Victor Diaz", age = 21, grade = 2, tutor_id = 3)
    estudiante5 = Estudiante(name = "Marcos Acuña", age = 23, grade = 1, tutor_id = 3)
    estudiante6 = Estudiante(name = "Sebastian Saja", age = 45, grade = 3, tutor_id = 2)
    estudiante7 = Estudiante(name = "Diego Milito", age = 42, grade = 2, tutor_id = 2)

    session.add_all([estudiante1, estudiante2, estudiante3, estudiante4, estudiante5, estudiante6, estudiante7])
    session.commit()

    print('Tabla creada con exito ! ')
    print()

    # No olvidarse que antes de poder crear un estudiante debe haberse
    # primero creado el tutor.


def fetch():
    print('Comprobemos su contenido, ¿qué hay en la tabla?')
    # Crear una query para imprimir en pantalla
    # todos los objetos creados de la tabla estudiante.
    # Imprimir en pantalla cada objeto que traiga la query
    # Realizar un bucle para imprimir de una fila a la vez
    print()
    Session = sessionmaker(bind=engine)
    session = Session()
    consul_estudiante = session.query(Estudiante).all()
    for estudiante in consul_estudiante:
        print(estudiante)

    print('**Estos son todos los estudiantes de la tabla Estudiantes.**')
    print()

def search_by_tutor(tutor):
    print('Operación búsqueda!')
    # Esta función recibe como parámetro el nombre de un posible tutor.
    # Crear una query para imprimir en pantalla
    # aquellos estudiantes que tengan asignado dicho tutor.

    # Para poder realizar esta query debe usar join, ya que
    # deberá crear la query para la tabla estudiante pero
    # buscar por la propiedad de tutor.name

    Session = sessionmaker(bind=engine)
    session = Session()
    estudiantes = (session.query(Estudiante).join(Tutor).filter(Tutor.name == tutor).all())

    if estudiantes:
        print(f"Estudiantes asignados a {tutor}:")
        for estudiante in estudiantes:
            print(f"- {estudiante.name}")
    else:
        print("No se encontraron estudiantes con ese tutor.")
    print()
        


def modify(estudiante_nombre, nuevo_tutor_nombre):
    print('Modificando la tabla')
    print()
    # Deberá actualizar el tutor de un estudiante, cambiarlo para eso debe
    # 1) buscar con una query el tutor por "tutor.name" usando name
    # pasado como parámetro y obtener el objeto del tutor
    # 2) buscar con una query el estudiante por "estudiante.id" usando
    # el id pasado como parámetro
    # 3) actualizar el objeto de tutor del estudiante con el obtenido
    # en el punto 1 y actualizar la base de datos

    # TIP: En clase se hizo lo mismo para las nacionalidades con
    # en la función update_persona_nationality

    Session = sessionmaker(bind=engine)
    session = Session()
    estudiante_obj = session.query(Estudiante).filter(Estudiante.name == estudiante_nombre).first()
    tutor_obj = session.query(Tutor).filter(Tutor.name == nuevo_tutor_nombre).first()
    estudiante_obj.tutor_id = tutor_obj.id
    session.commit()
    print(f"Estudiante {estudiante_obj.name} ahora tiene como tutor a {tutor_obj.name}")
    print()

def count_grade(grade):
    print('Estudiante por grado')
    # Utilizar la sentencia COUNT para contar cuantos estudiante
    # se encuentran cursando el grado "grade" pasado como parámetro
    # Imprimir en pantalla el resultado

    # TIP: En clase se hizo lo mismo para las nacionalidades con
    # en la función count_persona

    Session = sessionmaker(bind=engine)
    session = Session()

    conteo = session.query(Estudiante).filter(Estudiante.grade == grade).count()
    print('Estudiantes en grado:', grade, 'encontradas:', conteo)

if __name__ == '__main__':
    print("Bienvenidos a otra clase con Python")
    create_schema()   
    
    fill()
    
    fetch()

    print('Para revisar que estudiantes estan asignados a cada tutor ingresa el nombre del tutor')
    print('Recordemos que valores tenemos en la tabla "Tutor"')
    Session = sessionmaker(bind=engine)
    session = Session()
    consul_tutor = session.query(Tutor.id, Tutor.name).all()
    tutor_nombres = [tutor.name for tutor in consul_tutor]
    for tutor in consul_tutor:
        print(tutor)
    while True:
        ingreso_manual = input('Ingresa el nombre del tutor que quieres consultar (Conviene copiar y pegar): ')
        if ingreso_manual not in tutor_nombres:
            print("Por favor, ingresa uno de los nombres de tutor mostrados arriba.")
            continue
        break
    print()
    search_by_tutor(ingreso_manual)

    print('Teniendo en cuenta el listado de tutores demostrado recientemente, vamos a modificar al tutor de Sebastian Saja')
    nuevo_tutor = input('Ingrese el nombre del nuevo tutor: ')
    modify("Sebastian Saja", nuevo_tutor)

    fetch()
    
    
    while True:
        try:
            entrada_grade = input('Ingresa el grade por el que quieres consultar, los disponibles son 1, 2 y 3: ')
            if entrada_grade not in ['1', '2', '3']:
                print("Por favor, ingresa solo 1, 2 o 3.")
                continue
            entrada_grade = int(entrada_grade)
            break
        except ValueError:
            print("Entrada inválida. Debe ser un número (1, 2 o 3).")
    count_grade(entrada_grade)

    print('Fin del trabajo. Gracias')
    