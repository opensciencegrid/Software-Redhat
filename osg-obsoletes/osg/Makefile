
all: osg-obsoletes.spec

epel%.rpms:
	epel-srpms -b$* % > $@

el%.obs:
	./list-obsoletes.py $* > $@

osg-obsoletes.spec: osg-obsoletes.spec.in el7.obs el8.obs
	sed -e "/EL7 OBSOLETES/r el7.obs" \
            -e "/EL8 OBSOLETES/r el8.obs" < $< > $@

