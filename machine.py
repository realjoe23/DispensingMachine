import tkinter as tk

class MaquinaExpendedora:
    def __init__(self, root):
        self.root = root
        self.root.title("Máquina Expendedora - Autómata Finito")
        self.root.geometry("450x550")
        self.root.configure(bg="#2C3E50")

        # Productos y precios
        self.inventario = {
            'a': ("cocacola", 10), 'b': ("fanta", 8), 'c': ("sprite", 20),
            'd': ("squirt", 4), 'e': ("sidral", 23), 'f': ("pepsi", 17),
            'g': ("agua", 3), 'h': ("sangria", 28), 'i': ("jarritos", 11),
            'j': ("topochico", 30)
        }

        # Estados
        self.estado_actual = 0      # 0 = q0, 1 = qpi,s, 2 = aceptacion, -1 = error
        self.saldo_acumulado = 0
        self.precio_objetivo = 0
        self.producto_elegido = ""
        self.mensaje_error = ""

        self.construir_interfaz()
        self.salida_moore()

    def construir_interfaz(self):
        self.pantalla = tk.Label(self.root, text="", bg="#ECF0F1", fg="#2C3E50", 
                                 font=("Courier", 12, "bold"), height=5, relief="sunken", justify="center")
        self.pantalla.pack(pady=20, padx=20, fill="x")

        frame_productos = tk.LabelFrame(self.root, text="Seleccione Producto ", bg="#2C3E50", fg="white", font=("Arial", 10, "bold"))
        frame_productos.pack(pady=10, padx=20, fill="x")
        
        row, col = 0, 0
        for codigo, datos in self.inventario.items():
            btn = tk.Button(frame_productos, text=f"[{codigo}] {datos[0].title()}\n${datos[1]}", 
                            width=12, bg="#3498DB", fg="white", font=("Arial", 9, "bold"),
                            command=lambda c=codigo: self.evaluar_transicion(c, 'producto'))
            btn.grid(row=row, column=col, padx=5, pady=5)
            col += 1
            if col > 1: 
                col = 0
                row += 1

        frame_monedas = tk.LabelFrame(self.root, text="Inserte Monedas ", bg="#2C3E50", fg="white", font=("Arial", 10, "bold"))
        frame_monedas.pack(pady=10, padx=20, fill="x")

        monedas = [1, 2, 5, 10]
        for i, m in enumerate(monedas):
            btn = tk.Button(frame_monedas, text=f"${m}", width=6, bg="#F1C40F", fg="black", font=("Arial", 12, "bold"),
                            command=lambda valor=m: self.evaluar_transicion(valor, 'moneda'))
            btn.grid(row=0, column=i, padx=8, pady=10)

        btn_reset = tk.Button(self.root, text="NUEVA TRANSACCIÓN / REINICIAR", bg="#E74C3C", fg="white", font=("Arial", 10, "bold"),
                              command=self.reiniciar_maquina)
        btn_reset.pack(pady=15)

    # delta: Q x Sigma -> Q
    def evaluar_transicion(self, entrada, tipo):
        if self.estado_actual in [-1, 2]:
            return 

        if tipo == 'producto':
            if self.estado_actual == 0:
                # q0 -> qpi,0
                self.producto_elegido = self.inventario[entrada][0]
                self.precio_objetivo = self.inventario[entrada][1]
                self.estado_actual = 1
            elif self.estado_actual == 1:
                # no doble selección
                self.mensaje_error = "ERROR."
                self.estado_actual = -1

        elif tipo == 'moneda':
            if self.estado_actual == 0:
                # no dinero antes de producto
                self.mensaje_error = "ERROR."
                self.estado_actual = -1
            elif self.estado_actual == 1:
                # qpi,s -> qpi,s+m
                self.saldo_acumulado += entrada
                
                # Aceptacion
                if self.saldo_acumulado >= self.precio_objetivo:
                    self.estado_actual = 2

        self.salida_moore()

    def salida_moore(self):
        if self.estado_actual == 0:
            texto = "[ESTADO q0]\nEsperando seleccion...\n-> Presione un botón"
        
        elif self.estado_actual == 1:
            faltante = self.precio_objetivo - self.saldo_acumulado
            texto = f"[ESTADO qpi,s]\nProducto: {self.producto_elegido.upper()}\nSaldo: ${self.saldo_acumulado} | Faltan: ${faltante}\n-> Inserte monedas (Botones amarillos)"
        
        elif self.estado_actual == 2:
            cambio = self.saldo_acumulado - self.precio_objetivo
            texto = f"¡TRANSACCIÓN EXITOSA! :)\nEntregando: {self.producto_elegido.upper()}\n"
            if cambio > 0:
                texto += f"Su cambio es: ${cambio}"
        
        elif self.estado_actual == -1:
            texto = f"[!] OPERACIÓN CANCELADA (q_error)\n{self.mensaje_error}\n"
            if self.saldo_acumulado > 0:
                texto += f"Devolviendo dinero: ${self.saldo_acumulado}"

        self.pantalla.config(text=texto)

    def reiniciar_maquina(self):
        self.estado_actual = 0
        self.saldo_acumulado = 0
        self.precio_objetivo = 0
        self.producto_elegido = ""
        self.mensaje_error = ""
        self.salida_moore()

if __name__ == "__main__":
    ventana_principal = tk.Tk()
    app = MaquinaExpendedora(ventana_principal)
    ventana_principal.mainloop()