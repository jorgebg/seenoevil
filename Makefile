all: bin/seenoevil seenoevil/static/app.js

bin/seenoevil: js/vendor/sjcl.js js/lib.js js/cli.js
	echo "#!/usr/bin/env node" > $@
	cat $^ >> $@
	chmod +x $@

seenoevil/static/app.js: js/vendor/sjcl.js js/lib.js js/web.js
	cat $^ > $@

clean:
	rm bin/seenoevil seenoevil/static/app.js


.PHONY: clean
