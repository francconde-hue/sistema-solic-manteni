# interfaz.py
import tkinter as tk
from tkinter import messagebox, ttk
from logica import AdministradorMantenimiento

class InterfazMantenimientoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Mantenimiento de Laboratorio (POO)")
        self.root.geometry("700x680")
        
        # Instanciar controlador/lógica del negocio
        self.admin = AdministradorMantenimiento()
        self.crear_widgets()

    def crear_widgets(self):
        #Formulario de Entrada
        frame_form = ttk.LabelFrame(self.root, text=" Nueva Solicitud de Mantenimiento ", padding=10)
        frame_form.pack(fill="x", padx=15, pady=10)
        
        ttk.Label(frame_form, text="Equipo / Área:").grid(row=0, column=0, sticky="w", pady=4)
        self.entry_equipo = ttk.Entry(frame_form, width=30)
        self.entry_equipo.grid(row=0, column=1, sticky="w", pady=4)
        
        ttk.Label(frame_form, text="Descripción corta:").grid(row=1, column=0, sticky="w", pady=4)
        self.entry_desc = ttk.Entry(frame_form, width=50)
        self.entry_desc.grid(row=1, column=1, sticky="w", pady=4)
        
        #CUADRO DE OBSERVACIONES ADICIONALES
        ttk.Label(frame_form, text="Observaciones adicionales:").grid(row=2, column=0, sticky="nw", pady=4)
        self.txt_observaciones = tk.Text(frame_form, width=50, height=4, font=("Arial", 10))
        self.txt_observaciones.grid(row=2, column=1, sticky="w", pady=4)
        
        #preguntsas para Diagnóstico
        frame_preguntas = ttk.LabelFrame(self.root, text=" Cuestionario de Diagnóstico ", padding=10)
        frame_preguntas.pack(fill="x", padx=15, pady=5)
        
        self.var_p1 = tk.BooleanVar()
        self.var_p2 = tk.BooleanVar()
        self.var_p3 = tk.BooleanVar()
        
        ttk.Checkbutton(frame_preguntas, text="¿Hay riesgo de seguridad biológica, química o eléctrica inmediato?", variable=self.var_p1).pack(anchor="w")
        ttk.Checkbutton(frame_preguntas, text="¿El problema detiene por completo los experimentos en curso?", variable=self.var_p2).pack(anchor="w")
        ttk.Checkbutton(frame_preguntas, text="¿Involucra pérdida de datos críticos o daños a equipos de alto costo?", variable=self.var_p3).pack(anchor="w")
        
        btn_ingresar = ttk.Button(self.root, text="Registrar Solicitud", command=self.ejecutar_registro)
        btn_ingresar.pack(pady=10)
        
        # --- Listas de Visualización de Datos ---
        frame_listas = ttk.Frame(self.root, padding=10)
        frame_listas.pack(fill="both", expand=True, padx=15, pady=5)
        
        frame_pila = ttk.LabelFrame(frame_listas, text=" PILA: Casos Urgentes (LIFO) ")
        frame_pila.pack(side="left", fill="both", expand=True, padx=5)
        self.lista_pila = tk.Listbox(frame_pila, bg="#ffe6e6")
        self.lista_pila.pack(fill="both", expand=True)
        
        frame_cola = ttk.LabelFrame(frame_listas, text=" COLA: Casos Regulares (FIFO) ")
        frame_cola.pack(side="right", fill="both", expand=True, padx=5)
        self.lista_cola = tk.Listbox(frame_cola, bg="#e6f2ff")
        self.lista_cola.pack(fill="both", expand=True)
        
        btn_atender = ttk.Button(self.root, text="Atender Próximo Caso", command=self.ejecutar_atencion)
        btn_atender.pack(pady=10)

    def ejecutar_registro(self):
        equipo = self.entry_equipo.get().strip()
        descripcion = self.entry_desc.get().strip()
        observaciones = self.txt_observaciones.get("1.0", tk.END).strip()
        
        if not equipo or not descripcion:
            messagebox.showwarning("Campos vacíos", "Por favor, completa el equipo y su descripción.")
            return
            
        puntos = sum([self.var_p1.get(), self.var_p2.get(), self.var_p3.get()])
        solicitud, es_urgente = self.admin.registrar_solicitud(equipo, descripcion, observaciones, puntos)
        
        if es_urgente:
            messagebox.showinfo("Clasificación: URGENTE", 
                                f"Caso Crítico #{solicitud['id']}.\n"
                                f"Técnico Asignado: {solicitud['tecnico']}\n"
                                f"Tiempo de reacción: {solicitud['tiempo_reaccion']}")
        else:
            messagebox.showinfo("Clasificación: REGULAR", 
                                f"Caso Regular #{solicitud['id']}.\n"
                                f"Añadido a la cola de espera general (⏱️ {solicitud['tiempo_reaccion']}).")
        
        self.limpiar_formulario()
        self.actualizar_pantalla()

    def ejecutar_atencion(self):
        caso, tipo = self.admin.atender_siguiente()
        
        if tipo == "URGENTE":
            messagebox.showinfo("Atendiendo Emergencia", 
                                f"🚨 ¡ATENCIÓN INMEDIATA! 🚨\n\n"
                                f"ID: #{caso['id']} - {caso['equipo']}\n"
                                f"Encargado: {caso['tecnico']}\n"
                                f"Problema: {caso['descripcion']}\n\n"
                                f"📝 Observaciones:\n{caso['observaciones']}")
        elif tipo == "REGULAR":
            messagebox.showinfo("Atendiendo Caso Regular", 
                                f"📋 Atendiendo por orden de llegada (FIFO):\n\n"
                                f"ID: #{caso['id']} - {caso['equipo']}\n"
                                f"Técnico asignado ahora: {caso['tecnico_asignado']}\n"
                                f"Problema: {caso['descripcion']}\n\n"
                                f"📝 Observaciones:\n{caso['observaciones']}")
        else:
            messagebox.showinfo("Todo al día", "No hay solicitudes pendientes.")
            
        self.actualizar_pantalla()

    def actualizar_pantalla(self):
        self.lista_pila.delete(0, tk.END)
        self.lista_cola.delete(0, tk.END)
        
        # # VISTA DE LA PILA: EL ÚLTIMO EN ENTRAR SERÁ EL PRIMERO EN SALIR
        for caso in self.admin.pila_urgentes.ver_todos_reversa():
            self.lista_pila.insert(tk.END, f"#{caso['id']} - {caso['equipo']} (⏱️ {caso['tiempo_reaccion']})")
            
        #VISTA DE LA COLA: ORDEN DE LLEGADA
        for caso in self.admin.cola_regulares.ver_todos():
            self.lista_cola.insert(tk.END, f"#{caso['id']} - {caso['equipo']} (En espera)")

    def limpiar_formulario(self):
        self.entry_equipo.delete(0, tk.END)
        self.entry_desc.delete(0, tk.END)
        self.txt_observaciones.delete("1.0", tk.END)
        self.var_p1.set(False)
        self.var_p2.set(False)
        self.var_p3.set(False)

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazMantenimientoApp(root)
    root.mainloop()
