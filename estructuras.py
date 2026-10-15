# estructuras.py
from collections import deque

# CLASE PILA (ESTRUCTURA LIFO)
class Pila:
    def __init__(self):
        self._elementos = []
        
    def apilar(self, elemento):
        self._elementos.append(elemento)
        
    def desapilar(self):
        if self.esta_vacia():
            raise IndexError("No se puede desapilar, lista vacia.")
        return self._elementos.pop()
        
    def esta_vacia(self):
        return len(self._elementos) == 0
        
    def ver_cima(self):
        if self.esta_vacia():
            raise IndexError("Lista vacia.")
        return self._elementos[-1]
        
    def __len__(self):
        return len(self._elementos)
        
    #PARA MOSTRAR LA PILA EN LA INTERFAZ SIN BORRAR DATOS
    def ver_todos_reversa(self):
        return reversed(self._elementos)


# CLASE COLA (ESTRUCTURA FIFO)
class Cola:
    def __init__(self):
        self._elementos = deque()
        
    def esta_vacia(self):
        return len(self._elementos) == 0
        
    def __len__(self):
        return len(self._elementos)
        
    def encolar(self, elemento):
        self._elementos.append(elemento)
        
    def desencolar(self):
        if self.esta_vacia():
            raise IndexError("No se puede desencolar, lista vacia.")
        return self._elementos.popleft()
        
    def ver_frente(self):
        if self.esta_vacia():
            raise IndexError("La lista vacia.")
        return self._elementos[0]  
        
    #MOSTRAR LA COLA EN LA INTERFAZ SIN BORRAR DATOS
    def ver_todos(self):
        return list(self._elementos)
