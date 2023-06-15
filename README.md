# PID controller

Controlador PID em Python

## Módulos

### Model

Módulo que representa as leis físicas que regem o comportamento do sistema. 
Cada arquivo desse módulo tem por objetivo modelar um sistema ou subsistema diferente.

Atualmente, os modelos implementados são:

- **tank_model**: Tanque com resistência para controle de temperatura de um fluido

### Controller

Módulo que realiza o controle dos sistemas representados em **Model**. 
O controlador implementado é um controlador PID Digital, que é regido pela seguinte 
equação de controle:


$$
 Q = \overline{Q} + K_c \left( e(k) + \frac{1}{\tau_i} \sum_{i=1}^{k}e(k)\Delta T + \tau_d \left( \frac{e(k) - e(k-1)}{\Delta T}\right)\right)
$$

### Simulation

### Data

### Demo