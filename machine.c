#include <stdio.h>
#include <string.h>

typedef struct {
  char code;
  char product[15];
  int price;
} Products;

int main() {
  printf("=======================================\n");
  printf("   MAQUINA EXPENDEDORA DE REFRESCOS  \n");
  printf("=======================================\n");

  // productos y precios
  Products machine[10] = {{'a', "cocacola", 10}, {'b', "fanta", 8},
                          {'c', "sprite", 20},   {'d', "squirt", 4},
                          {'e', "sidral", 23},   {'f', "pepsi", 17},
                          {'g', "agua", 3},      {'h', "sangria", 28},
                          {'i', "jarritos", 11}, {'j', "topochico", 30}};

  // Estados
  int estado_actual = 0;
  int saldo_acumulado = 0;         // s
  int precio_objetivo = 0;         // precio(x)
  char producto_elegido[15] = "";  // x
  int total_productos = sizeof(machine) / sizeof(machine[0]);

  printf("\n-- MENU --\n");
  for (int i = 0; i < total_productos; i++) {
    printf(" [%c] %-10s | $%i\n", machine[i].code, machine[i].product,
           machine[i].price);
  }
  printf("---------------------------------------\n");

  do {
    // salidas MOORE: lambda(q) depende solo del estado actual
    if (estado_actual == 0) {
      // lambda(q0) = Esperar
      printf("\n[ESTADO q0]: Esperando seleccion.\n");
      printf("-> Seleccione un producto (a - j): ");
    } else if (estado_actual == 1) {
      // lambda(q(x,s)) = Faltan(precio(x) - s)
      int faltante = precio_objetivo - saldo_acumulado;
      printf("\n[ESTADO qx,s]: Seleccion: %s | Saldo: $%i | Faltan: $%i\n",
             producto_elegido, saldo_acumulado, faltante);
      printf("-> Ingrese moneda (1, 2, 5, 10): ");
    }

    char entrada[20];
    if (scanf("%19s", entrada) != 1) {
      break;
    }

    // clasificar el simbolo
    int es_producto = 0;
    int es_moneda = 0;
    int valor_moneda = 0;
    char codigo_producto = '\0';

    // producto o moneda
    if (strlen(entrada) == 1 && entrada[0] >= 'a' && entrada[0] <= 'j') {
      es_producto = 1;
      codigo_producto = entrada[0];
    } else if (strcmp(entrada, "1") == 0) {
      es_moneda = 1;
      valor_moneda = 1;
    } else if (strcmp(entrada, "2") == 0) {
      es_moneda = 1;
      valor_moneda = 2;
    } else if (strcmp(entrada, "5") == 0) {
      es_moneda = 1;
      valor_moneda = 5;
    } else if (strcmp(entrada, "10") == 0) {
      es_moneda = 1;
      valor_moneda = 10;
    }

    // Funcion de transicion
    if (es_producto) {
      if (estado_actual == 0) {
        int indice = codigo_producto - 'a';
        strcpy(producto_elegido, machine[indice].product);
        precio_objetivo = machine[indice].price;
        estado_actual = 1;
      } else if (estado_actual == 1) {
        // solo se permite una seleccion:
        estado_actual = -1;
      }
    } else if (es_moneda) {
      if (estado_actual == 0) {
        // no se puede insertar dinero antes de seleccionar
        estado_actual = -1;
      } else if (estado_actual == 1) {
        // q(x,s) --> q(x,s+m)
        saldo_acumulado += valor_moneda;

        // aceptacion
        if (saldo_acumulado >= precio_objetivo) {
          estado_actual = 2;
        }
      }
    } else {
      // simbolo que no esta en el alfabeto
      printf("\n[!] Entrada no reconocida.\n");
    }

  } while (estado_actual != -1 && estado_actual != 2);

  // salidas MOORE de los estados finales
  printf("\n=======================================\n");
  if (estado_actual == 2) {
    int cambio = saldo_acumulado - precio_objetivo;
    printf(":) Transaccion Exitosa! (Estado Final)\n");
    printf("Entregando producto: %s\n", producto_elegido);
    if (cambio > 0) {
      // si el dinero es mayor da cambio
      printf("Su cambio es: $%i\n", cambio);
    }
  } else if (estado_actual == -1) {
    // lambda(q(error,s)) = Devolver(s)
    printf(":( Operacion Cancelada (Estado error).\n");
    if (saldo_acumulado > 0) {
      printf(" Devolviendo dinero: $%i\n", saldo_acumulado);
    }
  } else {
    printf(":( Cadena rechazada (Estado no aceptor).\n");
    if (saldo_acumulado > 0) {
      printf(" Saldo insuficiente. Devolviendo dinero: $%i\n", saldo_acumulado);
    }
  }
  printf("=======================================\n");

  return 0;
}