# Relatório Técnico: Simulação de Ataques em Ambiente MQTT
Atividade ponderada realizada pelos alunos Bruno Moitinho Leão, Israel Nunes Lopes Carvalho e Isabela Amado da Rocha
## Introdução
- *Objetivo do teste:* Simular ataques que impactam a confidencialidade, integridade e disponibilidade em um ambiente MQTT.
- *Ferramentas utilizadas:* Cliente MQTT (MQTTool e MQTTX), broker público MQTT (broker.hivemq.com), Wireshark, scripts Python.

## Configuração do Ambiente
- *Broker MQTT:* broker.hivemq.com
- *Port:* 1883
- *Tópicos:* teste/dos, teste/integridade, teste/confidencialidade
- *Procedimento de conexão:* Conexão utilizando clientes MQTT e scripts Python.

## Ataques Simulados

### Ataque Impactando a Disponibilidade: Denial of Service (DoS)

#### Descrição do Ataque
O ataque DoS visa sobrecarregar o broker MQTT com um grande volume de mensagens ou conexões, fazendo com que ele fique indisponível para os usuários.

#### Ferramentas Necessárias
- Cliente MQTT (ex: MQTTX)
- Broker público MQTT (ex: broker.hivemq.com)
- Script Python para automatizar o envio de mensagens

#### Passo-a-Passo do Ataque
1. *Conexão com o Broker:*
   - Use o cliente MQTT para conectar ao broker broker.hivemq.com na porta 1883.
2. *Escolha do Tópico:*
   - Escolha um tópico para atacar, por exemplo, teste/dos.
3. *Configuração do Script:*
   - Utilize o script Python abaixo para enviar um grande número de mensagens rapidamente.

```python
import paho.mqtt.client as mqtt
import time

broker = "broker.hivemq.com"
port = 1883
topic = "teste/dos"

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

client = mqtt.Client()
client.on_connect = on_connect

client.connect(broker, port, 60)

client.loop_start()

for i in range(10000):  # Envia 10.000 mensagens
    client.publish(topic, "DoS attack message")
    time.sleep(0.01)  # Intervalo de 10 ms entre mensagens

client.loop_stop()
client.disconnect()
```


4. *Execução do Ataque:*
   - Execute o script Python. Ele enviará um grande número de mensagens para o tópico teste/dos rapidamente.
5. *Resultados Esperados:*
   - O broker MQTT deve ficar sobrecarregado, resultando em indisponibilidade ou lentidão na entrega de mensagens para outros usuários.

### Ataque Impactando a Integridade: Manipulação de Mensagens

#### Descrição do Ataque
O ataque de manipulação de mensagens envolve interceptar e modificar mensagens MQTT antes de serem retransmitidas para o broker.

#### Ferramentas Necessárias
- Cliente MQTT (ex: MQTTX)
- Broker público MQTT (ex: broker.hivemq.com)
- Script Python para interceptação e modificação de mensagens

#### Passo-a-Passo do Ataque
1. *Conexão com o Broker:*
   - Use o cliente MQTT para conectar ao broker broker.hivemq.com na porta 1883.
2. *Escolha do Tópico:*
   - Escolha um tópico para interceptar, por exemplo, teste/integridade.
3. *Captura de Pacotes:*
   - Use Wireshark para capturar o tráfego MQTT na rede.
4. *Interceptação e Modificação:*
   - Configure um script Python para interceptar e modificar mensagens.

```python
import paho.mqtt.client as mqtt

broker = "broker.hivemq.com"
port = 1883
topic = "teste/integridade"

def on_message(client, userdata, msg):
    modified_message = msg.payload.decode().replace("original", "tampered")
    client.publish(topic, modified_message)

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(topic)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, port, 60)
client.loop_forever()
```

5. *Execução do Ataque:*
   - Execute o script Python. Ele simulará uma interceptação das mensagens publicadas no tópico teste/integridade, replicará o conteúdo e publicará a mensagem modificada de volta no mesmo tópico.
6. *Resultados Esperados:*
   - As mensagens no tópico teste/integridade serão modificadas, comprometendo a integridade dos dados.

### Ataque Impactando a Confidencialidade: Espionagem

#### Descrição do Ataque
O ataque de espionagem envolve interceptar e ler mensagens MQTT enviadas entre clientes e o broker, violando a confidencialidade das comunicações.

#### Ferramentas Necessárias
- Cliente MQTT (ex: MQTT.fx)
- Broker público MQTT (ex: broker.hivemq.com)
- Ferramenta de captura de pacotes (ex: Wireshark)

#### Passo-a-Passo do Ataque
1. *Conexão com o Broker:*
   - Use o cliente MQTT para conectar ao broker broker.hivemq.com na porta 1883.
2. *Escolha do Tópico:*
   - Escolha um tópico para interceptar, por exemplo, teste/confidencialidade.
   - ![tópico](https://cdn.discordapp.com/attachments/1147673467412545619/1249541075908038727/image.png?ex=6667ad4f&is=66665bcf&hm=ff2132513b36fff027130f1c293fb1043118ec8ed0c99f33420deb78a865ee8f&)
3. *Captura de Pacotes:*
   - Inicie Wireshark e configure para capturar pacotes na interface de rede usada pelo cliente MQTT.
   - Aplique um filtro de captura para o tráfego MQTT: tcp port 1883.
   - ![wireshark](https://cdn.discordapp.com/attachments/1147673467412545619/1249540787209764995/image.png?ex=6667ad0b&is=66665b8b&hm=336ae58bc5cd9dac2dbde506d52e456bf759b23f2204955c2c6ea719727f3a03&)
4. *Análise das Mensagens:*
   - Publique mensagens no tópico teste/confidencialidade usando o cliente MQTT.
   - No Wireshark, localize os pacotes MQTT capturados e examine o conteúdo das mensagens.
   - ![](https://cdn.discordapp.com/attachments/1147673467412545619/1249541002251862098/image.png?ex=6667ad3e&is=66665bbe&hm=d0526161fe6745b99c592148fff641c286fc3125faae9a7833889bd9c67c4a5b&)
5. *Resultados Esperados:*
   - As mensagens enviadas no tópico teste/confidencialidade serão visíveis no Wireshark, demonstrando que a confidencialidade foi comprometida.

## Resultados Obtidos
- *DoS:* Broker ficou sobrecarregado, resultando em indisponibilidade para outros usuários.
- *Manipulação de Mensagens:* Mensagens no tópico foram modificadas, comprometendo a integridade.
- *Espionagem:* Mensagens foram interceptadas e lidas, comprometendo a confidencialidade.

## Conclusões e Recomendações
- *Conclusões:* Os ataques demonstraram vulnerabilidades em termos de disponibilidade, integridade e confidencialidade no ambiente MQTT.
- *Recomendações:* Implementação de TLS/SSL para criptografia, autenticação forte, rate limiting e monitoramento contínuo.

## Anexos
- Scripts utilizados
- Configurações detalhadas de ferramentas
- Capturas de tela ou logs completos
