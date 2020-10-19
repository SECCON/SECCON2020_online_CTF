# Usage
To start pincette server,
```
cd pincette
docker-compose up -d
```

# Files
- README # this file
- musl/ # docker-related files for building musl libc
	- Dockerfile
	- docker-compose.yml
	- nopic.patch
- pincette/ # docker-related files for building pincette server
	- Dockerfile
	- docker-compose.devl.yml
	- docker-compose.prod.yml
	- docker-compose.yml
	- musl/ # debian package of musl libc
		- musl_1.1.21-2nopic1_amd64.deb
	- src/ # source files for pincette server
		- Makefile
		- pintool/
		- server/
- place\_files\_for\_github.sh # script to place FLAG and distribution files

# For developer
To start pincette server in devl environment,
```
cd pincette
docker-compose -f docker-compose.devl.yml up -d
```

To build musl libc with -fno-pic option and copy the debian package to pincette/musl,
```
cd musl
docker-compose run --rm builder
```
