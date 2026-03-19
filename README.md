# Módulo de reequilibrio de cartera

## Visión general

Este módulo modela una cartera de acciones y proporciona un mecanismo de reequilibrio basado en una asignación objetivo.

## Decisiones de diseño

- Separación de responsabilidades:
  - Stock: representa una posición (acción) con los datos de precio y cantidad.
  - Portfolio: orquesta la lógica del manejo de Stock.
  - Rebalance: función pura para cálculos.
- El balanceo devuelve acciones basadas en precio, se puede deducir la correspondiente cantidad de acciones.
- El modelo contempla la posibilidad de compra de fraccion de stocks. si se desea balancer en base a numeros enteros la problematica cambia radicalmente ya que es probable que nose pueda rebalacear manteniendo el mismo valor de total de portfolio

## Supuestos

- Los precios se proporcionan externamente
- No se consideran costos de transacción
- Se permiten acciones fraccionarias

## Logica de rebalanceo.

El rebalanceo busca ajustar la cartera a una `target_allocation` (asignación objetivo) calculando cuánto debería comprar (BUY) o vender (SELL) para cada accion.

Paso a paso:

1. **Calcular el valor total de la cartera**
   - Se suman los valores actuales de todas las acciones del diccionario `positions`.
   - El valor actual de cada `Stock` es `shares * price`.
2. **Recorrer cada símbolo de la asignación objetivo**
   - Para cada `symbol` y su porcentaje `target_pct` en `target_allocation`:
     - **3. Validar que exista la posición**
       - Si `symbol` no está en `positions`, se lanza `AllocationError`.
     - **4. Calcular el valor objetivo del activo**
       - `target_value = total_value * target_pct`
     - **5. Calcular el valor actual del activo**
       - `current_value = positions[symbol].get_value()`
     - **6. Calcular la diferencia (lo que falta o sobra)**
       - `difference = target_value - current_value`
     - **7. Decidir BUY / SELL según el signo de la diferencia**
       - Si `difference > 0`: falta dinero para alcanzar el objetivo ⇒ `BUY[symbol] = difference`
       - Si `difference < 0`: hay exceso ⇒ `SELL[symbol] = abs(difference)`
       - Si `difference == 0`: ya está en objetivo ⇒ no se agrega ninguna acción.
     - **8. Devolver el resultado**
       - Se devuelve un diccionario con la forma: `{"BUY": {...}, "SELL": {...}}`
       - Los montos están expresados en **dinero** (base dólares), no en cantidad de acciones.

## Uso de LLM

Se utilizó un LLM para apoyar el desarrollo de este módulo. El flujo fue el siguiente:

- **1. Generación del esquema inicial**
  - Se le pasó al modelo la descripción del problema y se obtuvo una primera versión de la solución.

- **2. Refactorización por responsabilidades**
  - Se pidió al modelo separar la estructura en distintos archivos según su responsabilidad (`stock`, `portfolio`, `rebalance`, `exceptions`).

- **3. Generación de tests básicos**
  - El modelo propuso algunos tests iniciales, que luego se extendieron y ajustaron manualmente.

- **4. Correcciones manuales posteriores**
  - El LLM trataba símbolos sin posición como si tuvieran valor `0`, en lugar de lanzar un error: se corrigió para que se dispare `AllocationError` cuando falta una posición.
  - Se ajustó la forma de validar el balance considerando errores de punto flotante: al trabajar con decimales, el nuevo valor total de la cartera puede no ser exactamente igual al original (por ejemplo, `0.9999999 != 1.0`), por lo que se usa un redondeo/tolerancia apropiada.
