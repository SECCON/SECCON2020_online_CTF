#!/bin/sh
TEMPDIR=`mktemp -d`
for dname in `find pincette -type d`
do
	mkdir $TEMPDIR/$dname
done
for fname in `cat distfiles.txt`
do
	ln -sr $fname $TEMPDIR/$fname
done

echo -n SECCON{this_is_dummy_flag} > $TEMPDIR/pincette/src/server/flag
ln -sr pincette/docker-compose.prod.yml $TEMPDIR/pincette/docker-compose.yml

rm -f ../files/pincette.*.tgz
tar cfzh ../files/pincette.tgz --owner=0 --group=0 -C $TEMPDIR/ pincette
mv ../files/pincette.tgz ../files/pincette.`md5sum ../files/pincette.tgz|cut -d' ' -f1`.tgz
rm -fr $TEMPDIR

cp -p pincette/src/server/flag ../FLAG
cp -pf test/test_server.py ../solver/
