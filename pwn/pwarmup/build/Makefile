all:
	gcc -Wl,-z,now,-z,norelro main.c -o chall -no-pie -fno-stack-protector -z execstack
	cp ./main.c ../files/
	mv ./chall ../files/
