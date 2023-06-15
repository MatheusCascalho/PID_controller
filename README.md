# PID controller

Controlador PID em Python

## Módulos

### Model

Módulo que representa as leis físicas que regem o comportamento do sistema. 
Cada arquivo desse módulo tem por objetivo modelar um sistema ou subsistema diferente.

Atualmente, os modelos implementados são:

- **tank_model**: Tanque com resistência (r) para controle de temperatura de um fluido (f). O comportamento dinâmico desse modelo
  pode ser descrito pelas equações diferenciais abaixo:
  
$$
 \frac{dT_f}{dt} = \frac{\rho q c_p (T_f - T) + h_r A_r (T_r - T)}{\rho V c_p}
$$

$$
 \frac{dT_r}{dt} = \frac{Q + h_r A_r (T_r - T)} {\rho_r V_r c_{p_r}}
$$

  onde:
  - Q: potência elétrica da resistência;
  - h: coeficiente convectivo;
  - $\rho$: densidade do material;
  - T: temperatura;
  - A: área superficial;
  - q: vazão volumétrica;
  - $c_p$: calor específico;

  A figura 1 apresenta o um diagrama com a representação do modelo.

  [![Fig. 1](/img/tanque.png)](https://youtu.be/0jZT7yYJ9p8)
  Figura 1: Representação do modelo. Imagem utilizada na aula do professor Felipi Bezerra. Disponível em: https://youtu.be/0jZT7yYJ9p8


### Controller

Módulo que realiza o controle dos sistemas representados em **Model**. 
O controlador implementado é um controlador PID Digital, que é regido pela seguinte 
equação de controle:


$$
 Q = \overline{Q} + K_c \left( e(k) + \frac{1}{\tau_i} \sum_{i=1}^{k}e(k)\Delta T + \tau_d \left( \frac{e(k) - e(k-1)}{\Delta T}\right)\right)
$$

### Simulation

Módulo que realiza a simulação temporal do modelo com a ação de controle. 
Esse método de simulação utilização o pacote `scipy.integrate` para resolução de equações diferenciais (função `odeint`).

### Data

### Demo