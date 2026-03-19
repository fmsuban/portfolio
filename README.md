# Módulo de reequilibrio de cartera

## Visión general

Este módulo modela una cartera de acciones y proporciona un mecanismo de reequilibrio basado en una asignación objetivo.

## Decisiones de diseño

- Separación de responsabilidades:
  - Stock: representa una posición (acción) con los datos de precio y cantidad.
  - Portfolio: orquesta la lógica del manejo de Stock.
  - Rebalance: función pura para cálculos.
- Se incluye validación de la asignación
- El balanceo devuelve acciones basadas en precio, se puede deducir la correspondiente cantidad de acciones.
- El modelo contempla la posibilidad de compra de fraccion de stocks. si se desea balancer en base a numeros enteros la problematica cambia radicalmente ya que es probable que nose pueda rebalacear manteniendo el mismo valor de total de portfolio

## Supuestos

- Los precios se proporcionan externamente
- No se consideran costos de transacción
- Se permiten acciones fraccionarias
