all: vuln

vuln: vuln.s
	gcc -nostdlib -L/lib/x86_64-linux-musl -lc -fno-plt -no-pie -o $@ $<

vuln_template.s: vuln_template.c
	gcc -fno-plt  -masm=intel -S $<

flag:
	echo -n SECCON{`echo -n "uN1Ntend3d_Endbr64" | sha512sum | cut -c-32`} > $@

clean:
	rm -f vuln
