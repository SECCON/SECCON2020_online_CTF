CFLAGS=-fstack-protector -no-pie -O2
LDFLAGS=-Wl,-z,now,-z,lazy

all:
	gcc $(LDFLAGS) -c main.c -o main.o $(CFLAGS)
	gcc $(LDFLAGS) -c encryptor.c -o encryptor.o $(CFLAGS)
	gcc $(LDFLAGS) main.o encryptor.o -o ../files/encryptor $(CFLAGS) -lssl -lcrypto
	cp encryptor.c ../files/src/
	cp encryptor.h ../files/src/
	cp main.c ../files/src/
	rm *.o
