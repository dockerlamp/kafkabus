INFO vagrant uaktualniony do ubu16.04LTS
INFO ustawiono RAM=4096

<=== aplikacja kafkabus ===>
		 
	INFO Aktualna implementacja konsumera i producera (python) produkuje wiadomoœci w
		trybie pub/sub.

	1. uruchom aplikacjê docker-compose

	2. brokery kafki nie s¹ "od razu" gotowe do obs³ugiwania producerów i konsumerów
	   pomimo i¿ kontener jest ju¿ uruchomiony (kolejnoœæ uruchamiania kontenerów jak¹ 
	   okreœla plik docker-compose nie przydaje siê na t¹ okolicznoœæ).
	   
	   Bezpoœrednim nastêpstwem "przypad³oœci" opisanej wy¿ej mo¿e byæ wysypanie siê
	   startuj¹cego producera i konsumera (rzuca wyj¹tkiem jak przyk³adowo poni¿ej).

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
	
	   Kolejno przeskalowane producery ( za pomoc¹ docker-compose scale producer=n) i konsumery uruchomi¹ siê "normalnie" i po³¹cz¹ siê do klastra.
	
	3. Domyœlnie uruchamiany jest jeden broker w klastrze kafki. Po przeskalowaniu kafki (dodanie 
	   brokerów kafki za pomoc¹ docker-compose scale producer=n) producery i consumery ³¹cz¹ siê 
	   tylko do pierwszego brokera (uruchomionego przy starcie docker-compose).
	   
	   Aby producery i konsumery zaczê³y korzystaæ z nowo dodanych brokerów w klastrze kafki nale¿y
	   zmodyfikowaæ istniej¹cy TOPIC "py_topic" w kafce. Instrukcja poni¿ej.:
	   
	   3.a. zaloguj siê do dowolnego, uruchomionego kontenera z brokerem kafki
				docker exec -i 17c7ec2118f4 bash
	   3.b. wejdz do kat. ze skryptami do zarz¹dzania kafk¹
				cd /opt/kafka/bin
	   3.c. podziel istniej¹cy TOPIC "py_topic" na wiêcej partycji (partycje zostan¹ podzielone miêdzy istniej¹ce brokery w kastrze)
				./kafka-topics.sh --alter --zookeeper zookeeper:2181 --topic py_topic --partitions 4
	   3.d. sprawdz czy TOPIC "py_topic" zosta³ podzielony na partycjê miêdzy nowe brokery
				./kafka-topics.sh --zookeeper zookeeper:2181 --describe
				
				przykladowy rezultat:
				Topic:py_topic  PartitionCount:4        ReplicationFactor:1     Configs:
						Topic: py_topic Partition: 0    Leader: 1001    Replicas: 1001  Isr: 1001
						Topic: py_topic Partition: 1    Leader: 1002    Replicas: 1002  Isr: 1002
						Topic: py_topic Partition: 2    Leader: 1001    Replicas: 1001  Isr: 1001
						Topic: py_topic Partition: 3    Leader: 1002    Replicas: 1002  Isr: 1002
		3.e. aktualnie uruchomione producery i konsumery "nie wiedz¹" o nowych partycjach
			 (do oprogramowania po stronie producerów / konsumerów - zale¿ne od scenariusza - do ustalenia).
		     Nowo uruchomione kontenery konsumerów i producerów bêd¹ ju¿ "widzia³y" nowe partycje (w ró¿nych brokerach).
			 
			 Przyk³adowy rezultat produkowania i konsumowania na wiêkszej iloœci brokerów w kafce.:
			 
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


		TODO - automatyczne replikowanie istniej¹cych TOPIC`s (aktualnie TOPIC nie jest replikowany tylko partycjonowany).
			 - testy konsumera i producera w ró¿nych konfiguracjach (queue, pub/sub, groups, replay, etc.)
			 - obs³uga b³êdów w konsumerze i producerze (procedurê z pkt.3 na potrzeby testów mo¿na przenieœæ do producera,
				czy to jest dobry pomys³ - do przedyskutowania...)
			 - test clienta node.js
			 - testy typu zookeeper out of service lub broker crash w klastrze kafki i wp³yw na producery/konsumery
			 - inne ?
