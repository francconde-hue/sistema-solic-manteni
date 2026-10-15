# logica.py
import random
from estructuras import Pila, Cola

class AdministradorMantenimiento:
    def __init__(self):
        # Instanciar usando los nombres de clase
        self.pila_urgentes = Pila()
        self.cola_regulares = Cola()
        
        #TECNICOS FICTICIOS
        self.tecnicos = ["Ing. Alice Vega", "Tec. Carlos Ruiz", "Ing. Diego López", "Tec. Elena Gómez"]
        self.contador_solicitud = 1

    def registrar_solicitud(self, equipo, descripcion, observaciones, puntos_urgencia):
        if not observaciones:
            observaciones = "Ninguna."
            
        solicitud = {
            "id": self.contador_solicitud,
            "equipo": equipo,
            "descripcion": descripcion,
            "observaciones": observaciones
        }
        
        self.contador_solicitud += 1

        #CLASIFICACIÓN DE PRIORIDAD SEGÚN EL DIAGNÓSTICO
        if puntos_urgencia >= 2:
            #AQUÍ SE ASIGNA EL ENCARGADO Y EL TIEMPO PARA CASOS URGENTE
            solicitud["prioridad"] = "URGENTE"
            solicitud["tiempo_reaccion"] = f"{random.randint(5, 15)} minutos"
            solicitud["tecnico"] = random.choice(self.tecnicos)
            
            #SE ALMACENA EN LA PILA DE EMERGENCIAS (LIFO)
            self.pila_urgentes.apilar(solicitud)
            return solicitud, True
        else:
            #AQUÍ SE CONFIGURA EL TIEMPO DE ESPERA PARA CASOS NO URGENTES
            solicitud["prioridad"] = "REGULAR"
            solicitud["tiempo_reaccion"] = f"{random.randint(1, 4)} horas"
            solicitud["tecnico"] = "En espera de asignación"
            
            #SE ALMACENA EN LA COLA DE ESPERA GENERAL (FIFO)
            self.cola_regulares.encolar(solicitud)
            return solicitud, False

    def atender_siguiente(self):
        #CONTROL DE ATENCIÓN PRIORIZANDO LAS EMERGENCIAS
        
        #SI HAY URGENCIAS EN LA PILA SE ATIENDEN DE PRIMERAS
        if not self.pila_urgentes.esta_vacia():
            caso = self.pila_urgentes.desapilar()
            return caso, "URGENTE"
            
        #SI NO HAY URGENCIAS SE PROCEDE A ATENDER LA COLA GENERAL
        elif not self.cola_regulares.esta_vacia():
            caso = self.cola_regulares.desencolar()
            
            #ASIGNACIÓN DEL TÉCNICO AL MOMENTO DE PASAR A ATENCIÓN
            caso["tecnico_asignado"] = random.choice(self.tecnicos)
            return caso, "REGULAR"
            
        # # NO CASOS PENDIENTE
        return None, "VACIO"
