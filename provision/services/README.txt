INFO vagrant uaktualniony do ubu16.04LTS
INFO ustawiono RAM=4096

<=== aplikacja kafkabus ===>
		 
	INFO Aktualna implementacja konsumera i producera (python) produkuje wiadomo�ci w
		trybie pub/sub.

	1. uruchom aplikacj� docker-compose

	2. brokery kafki nie s� "od razu" gotowe do obs�ugiwania producer�w i konsumer�w
	   pomimo i� kontener jest ju� uruchomiony (kolejno�� uruchamiania kontener�w jak� 
	   okre�la plik docker-compose nie przydaje si� na t� okoliczno��).
	   
	   Bezpo�rednim nast�pstwem "przypad�o�ci" opisanej wy�ej mo�e by� wysypanie si�
	   startuj�cego producera i konsumera (rzuca wyj�tkiem jak przyk�adowo poni�ej).

		consumer_1   | consumer settings: topic is py_topic, bootstrap srv is 172.18.0.2:9092
		consumer_1   | Traceback (most recent call last):
		consumer_1   |   File "kafka-consumer.py", line 15, in <module>
		consumer_1   |     consumer = KafkaConsumer(KAFKA_TOPIC_NAME, bootstrap_servers= BOOTSTRAP_SERVERS, value_deserializer = pickle.loads)
		consumer_1   |   File "/usr/local/lib/python3.6/site-packages/kafka/consumer/group.py", line 324, in __init__
		consumer_1   |     self._client = KafkaClient(metrics=self._metrics, **self.config)
		consumer_1   |   File "/usr/local/lib/python3.6/site-packages/kafka/client_async.py", line 221, in __init__
		consumer_1   |     self.config['api_version'] = self.check_version(timeout=check_timeout)
		consumer_1   |   File "/usr/local/lib/python3.6/site-packages/kafka/client_async.py", line 826, in check_version
		consumer_1   |     raise Errors.NoBrokersAvailable()
		consumer_1   | kafka.errors.NoBrokersAvailable: NoBrokersAvailable
	
	   Kolejno przeskalowane producery ( za pomoc� docker-compose scale producer=n) i konsumery uruchomi� si� "normalnie" i po��cz� si� do klastra.
	
	3. Domy�lnie uruchamiany jest jeden broker w klastrze kafki. Po przeskalowaniu kafki (dodanie 
	   broker�w kafki za pomoc� docker-compose scale producer=n) producery i consumery ��cz� si� 
	   tylko do pierwszego brokera (uruchomionego przy starcie docker-compose).
	   
	   Aby producery i konsumery zacz�y korzysta� z nowo dodanych broker�w w klastrze kafki nale�y
	   zmodyfikowa� istniej�cy TOPIC "py_topic" w kafce. Instrukcja poni�ej.:
	   
	   3.a. zaloguj si� do dowolnego, uruchomionego kontenera z brokerem kafki
				docker exec -i 17c7ec2118f4 bash
	   3.b. wejdz do kat. ze skryptami do zarz�dzania kafk�
				cd /opt/kafka/bin
	   3.c. podziel istniej�cy TOPIC "py_topic" na wi�cej partycji (partycje zostan� podzielone mi�dzy istniej�ce brokery w kastrze)
				./kafka-topics.sh --alter --zookeeper zookeeper:2181 --topic py_topic --partitions 4
	   3.d. sprawdz czy TOPIC "py_topic" zosta� podzielony na partycj� mi�dzy nowe brokery
				./kafka-topics.sh --zookeeper zookeeper:2181 --describe
				
				przykladowy rezultat:
				Topic:py_topic  PartitionCount:4        ReplicationFactor:1     Configs:
						Topic: py_topic Partition: 0    Leader: 1001    Replicas: 1001  Isr: 1001
						Topic: py_topic Partition: 1    Leader: 1002    Replicas: 1002  Isr: 1002
						Topic: py_topic Partition: 2    Leader: 1001    Replicas: 1001  Isr: 1001
						Topic: py_topic Partition: 3    Leader: 1002    Replicas: 1002  Isr: 1002
		3.e. aktualnie uruchomione producery i konsumery "nie wiedz�" o nowych partycjach
			 (do oprogramowania po stronie producer�w / konsumer�w - zale�ne od scenariusza - do ustalenia).
		     Nowo uruchomione kontenery konsumer�w i producer�w b�d� ju� "widzia�y" nowe partycje (w r�nych brokerach).
			 
			 Przyk�adowy rezultat produkowania i konsumowania na wi�kszej ilo�ci broker�w w kafce.:
			 
				consumer_1   | recived random message no. 667962 from topic=py_topic, partition=2, key=None
				producer_1   | sent random message no. 695019
				consumer_1   | recived random message no. 695019 from topic=py_topic, partition=3, key=None
				consumer_2   | recived random message no. 695019 from topic=py_topic, partition=3, key=None
				producer_1   | sent random message no. 873717
				consumer_2   | recived random message no. 873717 from topic=py_topic, partition=0, key=None
				consumer_1   | recived random message no. 873717 from topic=py_topic, partition=0, key=None
				producer_2   | Collecting kafka-python
				producer_2   |   Downloading kafka_python-1.3.5-py2.py3-none-any.whl (207kB)
				producer_1   | sent random message no. 993616
				consumer_2   | recived random message no. 993616 from topic=py_topic, partition=3, key=None
				consumer_1   | recived random message no. 993616 from topic=py_topic, partition=3, key=None
				producer_2   | Installing collected packages: kafka-python
				producer_2   | Successfully installed kafka-python-1.3.5
				producer_2   | producer settings: topic is py_topic, bootstrap srv is 172.18.0.2:9092, frequency 1 sec.
				producer_1   | sent random message no. 156486
				consumer_1   | recived random message no. 156486 from topic=py_topic, partition=1, key=None
				consumer_2   | recived random message no. 156486 from topic=py_topic, partition=1, key=None
				producer_2   | sent random message no. 515069
				consumer_2   | recived random message no. 515069 from topic=py_topic, partition=0, key=None
				consumer_1   | recived random message no. 515069 from topic=py_topic, partition=0, key=None
				producer_1   | sent random message no. 502649
				producer_2   | sent random message no. 461426
				consumer_2   | recived random message no. 502649 from topic=py_topic, partition=3, key=None
				consumer_1   | recived random message no. 461426 from topic=py_topic, partition=2, key=None
				consumer_1   | recived random message no. 502649 from topic=py_topic, partition=3, key=None
				consumer_2   | recived random message no. 461426 from topic=py_topic, partition=2, key=None


		TODO - automatyczne replikowanie istniej�cych TOPIC`s (aktualnie TOPIC nie jest replikowany tylko partycjonowany).
			 - testy konsumera i producera w r�nych konfiguracjach (queue, pub/sub, groups, replay, etc.)
			 - obs�uga b��d�w w konsumerze i producerze (procedur� z pkt.3 na potrzeby test�w mo�na przenie�� do producera,
				czy to jest dobry pomys� - do przedyskutowania...)
			 - test clienta node.js
			 - testy typu zookeeper out of service lub broker crash w klastrze kafki i wp�yw na producery/konsumery
			 - inne ?
