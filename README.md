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
3. **Validar que exista la posición**
   - Si `symbol` no está en `positions`, se lanza `AllocationError`.
4. **Calcular el valor objetivo del activo**
   - `target_value = total_value * target_pct`
5. **Calcular el valor actual del activo**
   - `current_value = positions[symbol].get_value()`
6. **Calcular la diferencia (lo que falta o sobra)**
   - `difference = target_value - current_value`
7. **Decidir BUY / SELL según el signo de la diferencia**
   - Si `difference > 0`: falta dinero para alcanzar el objetivo ⇒ `BUY[symbol] = difference`
   - Si `difference < 0`: hay exceso ⇒ `SELL[symbol] = abs(difference)`
   - Si `difference == 0`: ya está en objetivo ⇒ no se agrega ninguna acción.
8. **Devolver el resultado**
   - Se devuelve un diccionario con la forma:
     - `{"BUY": {...}, "SELL": {...}}`
   - Los montos están expresados en **dinero** (base dólares), no en cantidad de acciones.
