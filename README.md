Laholátor : Simple app for text generation from given text samples
=====

Laholátor allows you to generate random text based on ngram sample analysis done by NLTK (http://www.nltk.org/).
This particular app generates text based on work by JUDr.PhDr.Mgr. et Mgr.Henryk Lahola, but you can make it work
for any other texts by modifying the "sample" table in db. It's build on Flask (http://flask.pocoo.org/) web framework.

Setup
-----

To install all dependecies just try:

    pip install -r requirements.pip

To setup the app, just edit your settings either in settings/base.py (used both on dev and production), settings/production.py or settings/local_empty.py to suit your needs. If you edit local_empty.py be sure to copy it as local.py in order to get loaded during development.

The WSGI file should work w/out any tuning. Consult your web server docs to make wsgi work with your server. Sample vhost file for Apache would look like this:

    root@kosmik1:/home/starenka# cat /etc/apache2/sites-available/laholator
        <VirtualHost 127.0.0.1:80>
            ServerName laholator
                WSGIDaemonProcess laholator user=starenka group=starenka threads=5
                WSGIScriptAlias / /www/laholator/laholator.wsgi

                <Directory /www/laholator>
                    WSGIProcessGroup laholator
                    WSGIApplicationGroup %{GLOBAL}
                    WSGIScriptReloading On
                    Order deny,allow
                    Allow from all
                </Directory>
        </VirtualHost>

As for nginx and uWSGI & supervisor your config would look like this:

supervisor:
---

    [program:laholator.starenka.net]
    command=/usr/local/bin/uwsgi
      --socket /www/laholator/uwsgi.sock
      --pythonpath /www/laholator
      --touch-reload /www/laholator/app.wsgi
      --chmod-socket 666
      --uid starenka
      --gid starenka
      --processes 1
      --master
      --no-orphans
      --max-requests 5000
      --module laholator
      --callable app
    directory=/www/laholator/
    stdout_logfile=/www/laholator/uwsgi.log
    user=starenka
    autostart=true
    autorestart=true
    redirect_stderr=true
    stopsignal=QUIT

nginx:
---

    server {
            listen       80;
            server_name  laholator.starenka.net;
            root    /www/laholator/;

            access_log  /www/laholator/access.log;
            error_log /www/laholator/error.log;

            location / {
                    uwsgi_pass unix:///www/laholator/uwsgi.sock;
                    include        uwsgi_params;
            }

            location /static {
                    alias /www/laholator/static;
            }
    }


Have fun!

